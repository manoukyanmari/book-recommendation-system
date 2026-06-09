# company_n/ingest_to_chroma.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Calculate absolute directory path points dynamically based on this file's position
current_file_directory = os.path.dirname(os.path.abspath(__file__))

# Navigate up one level from 'n' to find the '.env' file in 'book-genre-ai'
# Or up two levels if your .env file is in the main 'book-recommendation' folder
root_directory = os.path.abspath(os.path.join(current_file_directory, "..", ".."))
env_path = os.path.join(root_directory, ".env")

# Force-load the environment keys from the verified absolute path location
load_dotenv(dotenv_path=env_path)

def run_ingestion():
    csv_file_path = os.path.join(current_file_directory, "company_n_genres_output.csv")
    vector_db_path = os.path.join(current_file_directory, "chroma_db")
    
    # 1. Read the input CSV file safely
    df = pd.read_csv(csv_file_path)
    
    # 2. Convert raw tabular rows into documents
    documents = []
    for _, row in df.iterrows():
        combined_text = (
            f"User Number: {row['Number']}\n"
            f"Genres: {row['Genres']}\n"
            f"Language: {row['Language']}"
        )
        
        doc = Document(
            page_content=combined_text, 
            metadata={
                "session_id": str(row['Number']),
                "genres": str(row['Genres']),
                "language": str(row['Language'])
            }
        )
        documents.append(doc)
        
    # 3. Perform text chunking using a text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    
    # 4. Generate embeddings and save the vectors
    # Ensure the environment variable is picked up correctly
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError(f"CRITICAL: OPENAI_API_KEY could not be read from: {env_path}. Double-check that this file exists and contains your key.")

    Chroma.from_documents(
        documents=chunks, 
        embedding=OpenAIEmbeddings(), 
        persist_directory=vector_db_path
    )
    print(f"Chroma DB successfully created at: {vector_db_path}")

if __name__ == "__main__":
    run_ingestion()
