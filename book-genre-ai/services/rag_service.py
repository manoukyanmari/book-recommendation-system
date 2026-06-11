# services/rag_service.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory

# Load environment configuration tokens from root space securely
load_dotenv()

class RAGChatbotService:
    def __init__(self, company_folder: str):
        # Set temperature to 0.0 to prevent hallucinations outside the provided catalogs
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        self.company_folder = company_folder
        self.db_path = os.path.join(company_folder, "chroma_db")
        self.embeddings = OpenAIEmbeddings()
        
        self.vector_store = Chroma(
            persist_directory=self.db_path, 
            embedding_function=self.embeddings
        )
        
        # Setup pure dictionary storage for conversational multi-turn session histories
        self.history_store = {}

        # Synchronized System Prompt aligning strict guardrail string tokens
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                "You are an intelligent personalized Book Recommendation Assistant.\n"
                "Your task is to analyze the user's reading history and match it against the AVAILABLE CATALOG to suggest new books they might enjoy.\n\n"
                "GUARDRAIL RULES:\n"
                "1. If the context states 'GUARDRAIL_TRIGGERED: USER_HAS_NO_DATA', you MUST reply exactly with this safety text: "
                "'I'm sorry, but I couldn't find any book recommendations matching your specific profile in our catalog at the moment.'\n"
                "2. Recommend books ONLY from the 'AVAILABLE CATALOG TO CHOOSE RECOMMENDATIONS FROM' section below. "
                "Never recommend external books or invent items not explicitly listed in that catalog section.\n"
                "3. Do not suggest books that the user has ALREADY read according to their reading history."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
        
        # Clean functional LCEL chain layout processing raw dictionary payloads directly
        self.chain = self.prompt | self.llm | StrOutputParser()

    def get_unique_users(self) -> list:
        try:
            collection_data = self.vector_store._collection.get(include=["metadatas"])
            metadatas = collection_data.get("metadatas", [])
            user_ids = set()
            for meta in metadatas:
                if meta and "session_id" in meta:
                    user_ids.add(str(meta["session_id"]))
            return sorted(list(user_ids)) if user_ids else ["No users found"]
        except Exception:
            return ["default_user"]

    def _compile_runtime_context(self, question: str, session_id: str) -> str:
        """
        Loads the user's reading history from Chroma DB via exact-match lookup, 
        and marries it dynamically to the reference catalog CSV data sheet rows.
        """
        string_session_id = str(session_id).strip()

        try:
            # Direct exact-match metadata lookup bypassing dimension tracking errors
            collection_data = self.vector_store._collection.get(
                where={"session_id": string_session_id},
                include=["documents"]
            )
            documents_list = collection_data.get("documents", [])

            # 🛡️ Guardrail Check: Trigger the exact synchronized fallback code token if empty
            if not documents_list:
                return "GUARDRAIL_TRIGGERED: USER_HAS_NO_DATA"

            user_profile_history = "\n".join(documents_list)

            # 📚 Dynamic Catalog Injection Layer
            catalog_text = "No additional reference catalog items available."
            catalog_csv_path = os.path.join(self.company_folder, "company_u_genres_output.csv")
            
            # Read the companion genre sheet file to pass potential candidate nodes to the model
            if os.path.exists(catalog_csv_path):
                df_cat = pd.read_csv(catalog_csv_path)
                catalog_rows = []
                # Fetch up to 40 candidate books to keep prompt sizes well balanced
                for _, row in df_cat.head(40).iterrows():
                    catalog_rows.append(f"- Book Title: {row['Title']} | Genres: {row['Genres']} | Language: {row['Language']}")
                catalog_text = "\n".join(catalog_rows)

            # Combine the two datasets together into the prompt context payload frame
            complete_context = (
                f"=== USER READING HISTORY PROFILES ===\n{user_profile_history}\n\n"
                f"=== AVAILABLE CATALOG TO CHOOSE RECOMMENDATIONS FROM ===\n{catalog_text}"
            )
            return complete_context

        except Exception as err:
            print(f"Error compiling runtime structural context layouts: {str(err)}")
            return "GUARDRAIL_TRIGGERED: USER_HAS_NO_DATA"

    def _get_session_history(self, session_id: str):
        if session_id not in self.history_store:
            self.history_store[session_id] = InMemoryChatMessageHistory()
        return self.history_store[session_id]

    def ask(self, query: str, session_id: str = "default_user") -> str:
        """
        Manages history variables and context gathering explicitly to bypass 
        parameter key-stripping execution bugs.
        """
        # 1. Compile the synchronized user profile and reference catalog rows
        context_payload = self._compile_runtime_context(question=query, session_id=session_id)
        
        # 2. Extract or initialize chat logs manually for this unique session key
        history_instance = self._get_session_history(session_id)
        historical_messages = history_instance.messages
        
        # 3. Fire payload straight down to the prompt template pipeline execution block
        response = self.chain.invoke({
            "context": context_payload,
            "chat_history": historical_messages,
            "question": query
        })
        
        # 4. Save both text strings back into the log to maintain conversation continuity
        history_instance.add_user_message(query)
        history_instance.add_ai_message(response)
        
        return response
