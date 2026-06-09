# company_a/ingest_to_chroma.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables from the root folder's .env file
load_dotenv()

def run_ingestion():
    # 1. Read the input CSV file containing book data
    df = pd.read_csv("company_n/company_n_genres_output.csv")
    
    # 2. Convert raw tabular rows into combined structured text documents
    documents = []
    for _, row in df.iterrows():
        combined_text = (
            f"Book Title: {row['Title']}\n"
            f"Genres: {row['Genres']}\n"
            f"Language: {row['Language']}"
        )
        
        doc = Document(
            page_content=combined_text, 
            metadata={
                "title": str(row['Title']),
                "genres": str(row['Genres']),
                "language": str(row['Language'])
            }
        )
        documents.append(doc)
        
    # 3. Perform text chunking using a text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    
    # 4. Generate embeddings and save the vectors (API key is automatically pulled from environment)
    Chroma.from_documents(
        documents=chunks, 
        embedding=OpenAIEmbeddings(), # No need to pass api_key parameter anymore!
        persist_directory="company_n/chroma_db"
    )
    print("Chroma DB successfully created at company_n/chroma_db directory.")

if __name__ == "__main__":
    run_ingestion()