# routers/chatbot.py
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_service_v2 import RAGChatbotService

# Create the FastAPI router instance
router = APIRouter()

# Define the incoming request structure with session tracking for chat history
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"  # Optional session ID with a fallback value

# Endpoint that dynamically handles chat requests per company using path parameters
@router.post("/api/{company_name}/chat")
async def company_chat_endpoint(company_name: str, request: ChatRequest):
    # Verify if the specified company directory exists on the file system
    if not os.path.exists(company_name):
        raise HTTPException(status_code=404, detail="Company project not found")
        
    try:
        # Initialize the RAG service dynamically for the requested company folder
        rag_service = RAGChatbotService(company_folder=company_name)
        
        # Invoke the LangChain pipeline by passing the user query and session ID
        response = rag_service.ask(request.message, session_id=request.session_id)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))