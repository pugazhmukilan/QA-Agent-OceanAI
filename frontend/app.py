import streamlit as st
import google.generativeai as genai
from langchain_core.messages import AIMessage, HumanMessage
import chromadb
import json
import time
import shutil
import os
import pypdf 
from datetime import datetime
import io
from init_app import init_session_state
from utils import (
    get_chroma_client,
    add_log,
    read_file_content,
    get_embedding,
    build_vector_db,
    search_vector_db,
    generate_with_gemini,
    createresponse
)
from variables import COLLECTION_NAME


st.set_page_config(
    page_title="Autonomous QA Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


init_session_state()


with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Get from aistudio.google.com")
    
    st.divider()
    st.subheader("📂 Data Ingestion")
    
    uploaded_html = st.file_uploader("Upload checkout.html", type=["html"])
    # Added 'pdf' to allowed types
    uploaded_docs = st.file_uploader("Upload Specs/Docs", type=["md", "txt", "json", "pdf"], accept_multiple_files=True)
    
    if st.button("Build Knowledge Base", type="primary"):
        if not api_key:
            st.error("API Key is required!")
        elif not uploaded_html and not uploaded_docs:
            st.warning("Please upload files first.")
        else:
            html_text = ""
            if uploaded_html:
                # Read HTML safely
                html_text = read_file_content(uploaded_html)
            
            docs_list = uploaded_docs if uploaded_docs else []
            
            with st.spinner("Building Knowledge Base..."):
                build_vector_db(docs_list, html_text, api_key)
            st.success("Ready!")

    st.divider()
    st.subheader("System Logs")
    log_container = st.container(height=200)
    with log_container:
        if not st.session_state.logs:
            st.caption("No logs yet.")
        else:
            for log in st.session_state.logs:
                st.text(log)


st.title("🤖 Autonomous QA Agent")
st.caption("Powered by Gemini 2.5 • ChromaDB Vector Store • Selenium Generation")

# Define Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Knowledge Base", "💬 QA Chat", "📝 Test Planner", "💻 Script Gen"])


with tab1:
    if st.session_state.kb_built:
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✅ HTML Context Loaded ({len(st.session_state.html_context)} chars)")
            st.code(st.session_state.html_context[:500] + "...", language="html")
        with col2:
            # Get stats from Chroma
            client = get_chroma_client()
            try:
                coll = client.get_collection(COLLECTION_NAME)
                count = coll.count()
                st.info(f"✅ ChromaDB Status: Active")
                st.metric("Stored Document Chunks", count)
                
                if count > 0:
                    peek = coll.peek(limit=1)
                    with st.expander("View Stored Data Structure"):
                        st.json(peek)
            except:
                st.warning("ChromaDB collection not found yet.")
    else:
        st.info("👈 Please upload files and click 'Build Knowledge Base' in the sidebar to start.")


with tab2:
    st.subheader("Chat with your Documentation")
    if input := st.chat_input("Ask about the specs (e.g., 'What is the discount logic?')"):
        response = createresponse(input,api_key)
        st.session_state.chat_history.append([HumanMessage(content=input), AIMessage(content=response)])
        
    for humanmsg,aimsg in st.session_state.chat_history[::-1]:
        with st.chat_message("user"):
            st.write(humanmsg.content)
        with st.chat_message("assistant"):
            st.write(aimsg.content)
        st.divider()
                
    

# --- TAB 3: TEST PLANNER ---
with tab3:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Test Case Generator")
    with col2:
        mode = st.selectbox("Generation Mode", ["Standard Functional", "Edge Cases & Security"])
    
    if st.button("Generate Test Cases", type="primary"):
        if not st.session_state.kb_built:
            st.error("Knowledge Base not ready.")
        else:
            with st.spinner("Analyzing specs and creating test plan..."):
                context = search_vector_db("business rules validation logic positive negative scenarios", api_key, top_k=5)
                
                prompt_instruction = "Focus on SECURITY (XSS, Injection), BOUNDARY values." if "Edge" in mode else "Focus on standard HAPPY PATHS."

                final_prompt = f"""
                Act as a QA Lead. Generate 3-5 diverse test cases.
                {prompt_instruction}
                DOCS CONTEXT: {context}
                HTML TARGET: {st.session_state.html_context}
                OUTPUT JSON ARRAY ONLY: [{{ "id": "TC-01", "feature": "...", "scenario": "...", "expected_result": "...", "grounding": "..." }}]
                """
                
                response = generate_with_gemini(final_prompt, api_key)
                
                try:
                    clean_json = response.replace("```json", "").replace("```", "").strip()
                    st.session_state.test_cases = json.loads(clean_json)
                    add_log(f"Generated {len(st.session_state.test_cases)} test cases.")
                except Exception as e:
                    st.error(f"Failed to parse AI response: {response}")
                    add_log(f"JSON Parse Error: {e}")

    if st.session_state.test_cases:
        st.write("### Generated Test Plan")
        for tc in st.session_state.test_cases:
            with st.expander(f"**{tc.get('id')}**: {tc.get('feature')} - {tc.get('scenario')}"):
                st.markdown(f"**Expected Result:** {tc.get('expected_result')}")
                st.markdown(f"**Source Grounding:** _{tc.get('grounding')}_")
                if st.button("Select for Automation", key=tc.get('id')):
                    st.session_state.selected_test_case = tc
                    st.session_state.generated_script = ""
                    st.session_state.script_explanation = ""
                    st.success(f"Selected {tc.get('id')}! Go to 'Script Gen' tab.")

# --- TAB 4: SCRIPT GENERATOR ---
with tab4:
    st.subheader("Selenium Script Generator")
    
    tc = st.session_state.selected_test_case
    
    if not tc:
        st.info("👈 Please select a test case from the 'Test Planner' tab first.")
    else:
        with st.container():
            st.markdown("#### Selected Scenario")
            st.info(tc.get("scenario"))

            st.markdown("#### Expected Result")
            st.success(tc.get("expected_result"))

        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("Generate Python Script", type="primary"):
                with st.spinner("Writing Selenium code..."):
                    context = search_vector_db(f"{tc['feature']} {tc['scenario']} rules", api_key, top_k=2)
                    
                    prompt = f"""
                    Act as a selenium (Python) expert
                    Use appropriate selectors (IDs, names, CSS selectors) based on the actual HTML
                    Write a Python Selenium script using webdriver.Chrome().
                    TEST CASE: {tc}
                    HTML SOURCE (Use these IDs): {st.session_state.html_context}
                    RULES: {context}
                    REQUIREMENTS: Explicit Waits, Assume 'checkout.html' local, Comments. Return ONLY code.
                    Produce high-quality, fully executable code

                    """
                    
                    script = generate_with_gemini(prompt, api_key)
                    st.session_state.generated_script = script.replace("```python", "").replace("```", "").strip()
        
        with col2:
            if st.session_state.generated_script and st.button("Explain Code"):
                with st.spinner("Analyzing code..."):
                    explanation = generate_with_gemini(f"Explain this selenium code simply:\n{st.session_state.generated_script}", api_key)
                    st.session_state.script_explanation = explanation

        if st.session_state.generated_script:
            st.code(st.session_state.generated_script, language="python")
            
        if st.session_state.script_explanation:
            with st.chat_message("assistant"):
                st.markdown("**Code Explanation:**")
                st.write(st.session_state.script_explanation)