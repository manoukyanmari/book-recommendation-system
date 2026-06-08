# run_chatbot.py
import sys
import os

# Force Python to recognize the current directory as a root package source
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.chatbot import router as chatbot_router  # This import will now work perfectly!

# Initialize the core FastAPI application
app = FastAPI(
    title="Company RAG Chatbot API",
    description="Production-ready multi-tenant RAG chatbot service.",
    version="1.0.0"
)

# Add CORS Middleware to allow your Web UI (Frontend) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your chatbot router into the application
app.include_router(chatbot_router)

if __name__ == "__main__":
    print("Starting Chatbot API Server...")
    uvicorn.run("run_chatbot:app", host="0.0.0.0", port=8000, reload=True)
