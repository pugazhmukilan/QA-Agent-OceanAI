import streamlit as st
import requests
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

from variables import CHROMA_PATH, COLLECTION_NAME

def createresponse(input,api_key):
    
            
            with st.spinner("Thinking..."):
                context = search_vector_db(input, api_key)
                llm_prompt = f"""
                You are a QA Assistant. Answer based strictly on the context.
                CONTEXT: {context}
                HTML SNIPPET: {st.session_state.html_context[:2000]}
                QUESTION: {input}
                """
                response = generate_with_gemini(llm_prompt, api_key)
                return response
            
           
 



def get_chroma_client():
    """Returns a persistent ChromaDB client."""
    if not os.path.exists(CHROMA_PATH):
        os.makedirs(CHROMA_PATH)
    return chromadb.PersistentClient(path=CHROMA_PATH)

# --- HELPER FUNCTIONS ---

def add_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    # Safety check
    if "logs" not in st.session_state:
        st.session_state.logs = []
    st.session_state.logs.append(f"[{timestamp}] {message}")

def read_file_content(uploaded_file):
    """
    The FIX: Safely reads text from PDF, TXT, MD, JSON.
    """
    try:
        # 1. Handle PDF Files
        if uploaded_file.name.lower().endswith('.pdf'):
            pdf_reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        
        # 2. Handle Text Files (MD, TXT, JSON, HTML)
        else:
            # decode bytes to string
            return uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        add_log(f"Error reading {uploaded_file.name}: {str(e)}")
        return ""

def get_embedding(text, api_key):
    """Fetches embedding from Gemini API."""
    genai.configure(api_key=api_key)
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
            title="QA Document"
        )
        return result['embedding']
    except Exception as e:
        st.error(f"Embedding Error: {e}")
        return []

def build_vector_db(uploaded_docs, html_content, api_key):
    """
    Ingests documents, chunks them, embeds them, and stores in ChromaDB.
    """
    st.session_state.html_context = html_content
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Initialize Chroma Client
    client = get_chroma_client()
    
    # Reset Collection
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass 
    
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    
    total_steps = len(uploaded_docs)
    
    for idx, doc in enumerate(uploaded_docs):
        status_text.text(f"Processing {doc.name}...")
        
        # USE THE SAFE READER FUNCTION HERE
        content = read_file_content(doc)
        
        if not content or not content.strip():
            add_log(f"Skipping empty or unreadable file: {doc.name}")
            continue

        # Simple Chunking
        chunks = [c.strip() for c in content.split('\n\n') if c.strip()]
        
        for i, chunk in enumerate(chunks):
            if len(chunk) < 10: continue # Skip noise
            
            embedding = get_embedding(chunk, api_key)
            if embedding:
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[{"source": doc.name}],
                    ids=[f"{doc.name}_{i}_{int(time.time())}"]
                )
        
        progress_bar.progress((idx + 1) / total_steps)
        add_log(f"Indexed {len(chunks)} chunks from {doc.name}")

    status_text.text("Knowledge Base Built Successfully!")
    st.session_state.kb_built = True
    time.sleep(1)
    status_text.empty()
    progress_bar.empty()

def search_vector_db(query, api_key, top_k=3):
    """Performs Semantic Search using ChromaDB."""
    client = get_chroma_client()
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception:
        return "" 
        
    genai.configure(api_key=api_key)
    try:
        query_embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query"
        )['embedding']
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if not results['documents']:
            return ""

        docs = results['documents'][0]
        metadatas = results['metadatas'][0]
        
        context_str = ""
        for doc, meta in zip(docs, metadatas):
            context_str += f"\n--- Source: {meta['source']} ---\n{doc}\n"
            
        return context_str
        
    except Exception as e:
        st.error(f"Search Error: {e}")
        return ""

def generate_with_gemini(prompt, api_key):
    header = {
        "Content-Type": "application/json",
    }
    body = {
        "apikey": api_key,
        "prompt": prompt,
    }
    response = requests.post("https://qaagent.pugazhmukilan.tech/generate", headers=header, json=body)

    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        st.error(f"Generation Error: {response.status_code} - {response.text}")
        return ""
