import streamlit as st       
def init_session_state():
    """Initialize all session state variables safely."""
    defaults = {
        "html_context": "",
        "logs": [],
        "chat_history": [],
        "test_cases": [],
        "selected_test_case": None,
        "generated_script": "",
        "script_explanation": "",
        "kb_built": False,
        "vector_db": [] 
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

