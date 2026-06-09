# ui_chatbot.py
import os
import sys
import streamlit as strlt
from dotenv import load_dotenv

# Set up project path environments
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(base_dir, "book-genre-ai")

if project_dir not in sys.path:
    sys.path.append(project_dir)

load_dotenv(os.path.join(base_dir, ".env"))

from services.rag_service import RAGChatbotService

strlt.set_page_config(page_title="Company RAG Chatbot", page_icon="📚", layout="centered")
strlt.title("📚 Multi-Tenant Book Recommendation Assistant")
strlt.write("Interact with your indexed catalog databases in real-time.")

# 1. Sidebar - Select Company Workspace First
with strlt.sidebar:
    strlt.header("Workspace Controls")
    company_selection = strlt.selectbox(
        "Select Company Catalog:",
        options=["company_a", "company_n", "company_u"],
        index=0
    )

# Cache resource generation to prevent continuous reloading pipelines
@strlt.cache_resource
def get_cached_rag_service(folder_name: str, full_project_path: str):
    dynamic_company_folder_path = os.path.join(full_project_path, folder_name)
    return RAGChatbotService(company_folder=dynamic_company_folder_path)

try:
    rag_backend = get_cached_rag_service(company_selection, project_dir)
except Exception as init_err:
    strlt.error(f"Failed to bootstrap LangChain Service: {init_err}")
    strlt.stop()

# 2. Sidebar - Dynamically Pull and Display User IDs from Chroma DB
available_users = rag_backend.get_unique_users()

with strlt.sidebar:
    strlt.write("---")
    strlt.header("User Selection")
    # Dropdown populated natively by scanning the vector database
    current_user_id = strlt.selectbox(
        "Select Active User Profile:",
        options=available_users
    )

# 3. Create isolated history session tracking tokens
session_tracking_key = f"chat_history_{company_selection}_{current_user_id}"

if "current_state_token" not in strlt.session_state:
    strlt.session_state.current_state_token = session_tracking_key

# Wipe layouts immediately if workspace flips or user toggles
if strlt.session_state.current_state_token != session_tracking_key:
    strlt.session_state.current_state_token = session_tracking_key
    if session_tracking_key in strlt.session_state:
        del strlt.session_state[session_tracking_key]
    strlt.rerun()

if session_tracking_key not in strlt.session_state:
    strlt.session_state[session_tracking_key] = []

# Render active message nodes down the screen frame
for message_node in strlt.session_state[session_tracking_key]:
    with strlt.chat_message(message_node["role"]):
        strlt.markdown(message_node["content"])

# Watch chat bar inputs
if user_prompt_string := strlt.chat_input("Ask a recommendation (e.g., What books are similar to my profile?)..."):
    
    with strlt.chat_message("user"):
        strlt.markdown(user_prompt_string)
    strlt.session_state[session_tracking_key].append({"role": "user", "content": user_prompt_string})
    
    with strlt.chat_message("assistant"):
        with strlt.spinner("Retrieving user vector profiles and compiling rules..."):
            try:
                # Trigger the underlying RAG system utilizing targeted user session IDs
                ai_generated_output = rag_backend.ask(
                    query=user_prompt_string, 
                    session_id=current_user_id
                )
                strlt.markdown(ai_generated_output)
                strlt.session_state[session_tracking_key].append({"role": "assistant", "content": ai_generated_output})
            except Exception as service_err:
                strlt.error(f"An unexpected error occurred: {str(service_err)}")
