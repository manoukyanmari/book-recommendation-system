# ui_chatbot.py
import os
import sys
import streamlit as strlt
from dotenv import load_dotenv

# 1. Get exact path blueprints for system environments
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(base_dir, "book-genre-ai")

# 2. Append the target path to sys.path so python imports work correctly
if project_dir not in sys.path:
    sys.path.append(project_dir)

# 3. Load secret tokens safely from the root folder's .env file
load_dotenv(os.path.join(base_dir, ".env"))

# Import your core LangChain business service layer
from services.rag_service import RAGChatbotService

# 4. Initialize layout headers and browser tab titles
strlt.set_page_config(page_title="Company RAG Chatbot", page_icon="📚", layout="centered")
strlt.title("📚 Multi-Tenant Book Recommendation Assistant")
strlt.write("Interact with your indexed catalog databases in real-time.")

# 5. Dropdown Selector UI block to toggle company configurations
company_selection = strlt.selectbox(
    "Select the active Company Catalog Workspace:",
    options=["company_a", "company_n", "company_u"],
    index=0
)

# 6. Build isolated history dictionaries to enforce total memory isolation
session_tracking_key = f"chat_history_{company_selection}"

if "current_company" not in strlt.session_state:
    strlt.session_state.current_company = company_selection

# If workspace flips, flush old states instantly to prevent layout artifacts
if strlt.session_state.current_company != company_selection:
    strlt.session_state.current_company = company_selection
    if session_tracking_key in strlt.session_state:
        del strlt.session_state[session_tracking_key]
    strlt.rerun()

if session_tracking_key not in strlt.session_state:
    strlt.session_state[session_tracking_key] = []

# 7. Use streamlit resource caching mechanisms to prevent recreating instances during state updates
@strlt.cache_resource
def get_cached_rag_service(folder_name: str, full_project_path: str):
    # Pass the full path context (e.g., "book-genre-ai/company_a") so LangChain locates the databases
    dynamic_company_folder_path = os.path.join(full_project_path, folder_name)
    return RAGChatbotService(company_folder=dynamic_company_folder_path)

try:
    # Bootstrap backend components using cached resource lookups
    rag_backend = get_cached_rag_service(company_selection, project_dir)
except Exception as init_err:
    strlt.error(f"Failed to bootstrap LangChain Service: {init_err}")
    strlt.stop()

# 8. Loop and render active text payloads down the interface frame
for message_node in strlt.session_state[session_tracking_key]:
    with strlt.chat_message(message_node["role"]):
        strlt.markdown(message_node["content"])

# 9. Watch input bars and append logs dynamically upon hit submissions
if user_prompt_string := strlt.chat_input("Ask a recommendation (e.g., Recommend a fantasy book in English)..."):
    
    with strlt.chat_message("user"):
        strlt.markdown(user_prompt_string)
    strlt.session_state[session_tracking_key].append({"role": "user", "content": user_prompt_string})
    
    with strlt.chat_message("assistant"):
        with strlt.spinner("Searching the company catalogs and compiling suggestions..."):
            try:
                # Trigger the underlying LangChain execution logic using isolated workspace keys
                ai_generated_output = rag_backend.ask(
                    query=user_prompt_string, 
                    session_id=f"streamlit_session_{company_selection}"
                )
                strlt.markdown(ai_generated_output)
                strlt.session_state[session_tracking_key].append({"role": "assistant", "content": ai_generated_output})
            except Exception as service_err:
                strlt.error(f"An unexpected error occurred: {str(service_err)}")
