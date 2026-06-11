# company_u/ingest_to_chroma.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Calculate absolute directory path environments
current_file_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.abspath(os.path.join(current_file_directory, "..", ".."))
env_path = os.path.join(root_directory, ".env")

# Force-load your environment keys safely
load_dotenv(dotenv_path=env_path)

def run_ingestion():
    csv_file_path = os.path.join(current_file_directory, "company_u.csv")
    vector_db_path = os.path.join(current_file_directory, "chroma_db")
    
    # 1. Read input configurations
    df_users = pd.read_csv(csv_file_path) # Contains columns: 'id', 'books'
    
    # 2. Convert user reading columns into clean document string layouts
    documents = []
    for _, row in df_users.iterrows():
        raw_user_id = str(row['id']).strip() # Extracts "User002", "User003", etc.
        user_books = str(row['books']).strip()
        
        # We append all text patterns together into the context payload layout
        combined_text = (
            f"User Profile Account Number: {raw_user_id}\n"
            f"Reading History Records and Borrowed Books: {user_books}"
        )
        
        doc = Document(
            page_content=combined_text, 
            metadata={
                "session_id": raw_user_id, # Maps exactly to your web app selectbox keys
                "source": "company_u_catalog"
            }
        )
        documents.append(doc)
        
    # 3. Perform text chunking using a text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    # 4. Generate standard OpenAI vector embeddings to guarantee search compliance
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError(f"CRITICAL: OPENAI_API_KEY could not be read from: {env_path}")

    Chroma.from_documents(
        documents=chunks, 
        embedding=OpenAIEmbeddings(), 
        persist_directory=vector_db_path
    )
    print(f"Success! Chroma DB generated with {len(documents)} matching user text tokens.")

if __name__ == "__main__":
    run_ingestion()
