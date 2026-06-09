# services/rag_service.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

class RAGChatbotService:
    def __init__(self, company_folder: str):
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.db_path = os.path.join(company_folder, "chroma_db")
        self.embeddings = OpenAIEmbeddings()
        
        self.vector_store = Chroma(
            persist_directory=self.db_path, 
            embedding_function=self.embeddings
        )
        
        self.history_store = {}

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                "You are an intelligent personalized Recommendation Assistant. "
                "Analyze the user's profile data provided in the context and answer their questions or give recommendations based strictly on that information.\n\n"
                "CONTEXT FROM DATABASE:\n{context}"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
        
        self.base_chain = (
            RunnablePassthrough.assign(
                context=lambda inputs: self._get_filtered_context(inputs["question"], inputs["session_id"]),
                question=lambda inputs: inputs["question"]
            )
            | self.prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        self.conversational_chain = RunnableWithMessageHistory(
            self.base_chain,
            get_session_history=self._get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history"
        )

    def get_unique_users(self) -> list:
        """
        Extracts all unique session/user IDs directly from Chroma DB metadata.
        """
        try:
            # Fetch metadata dictionary entries from the active vector collection
            collection_data = self.vector_store._collection.get(include=["metadatas"])
            metadatas = collection_data.get("metadatas", [])
            
            # Extract the ID tracking key. 
            # Note: Change "session_id" if your ingest script labeled this key differently (e.g., "Number", "user_id")
            user_ids = set()
            for meta in metadatas:
                if meta and "session_id" in meta:
                    user_ids.add(str(meta["session_id"]))
                elif meta and "Number" in meta: # Fallback to check your explicit data columns
                    user_ids.add(str(meta["Number"]))
            
            # Return sorted list or a fallback array if database collection returns empty
            return sorted(list(user_ids)) if user_ids else ["No users found"]
        except Exception:
            return ["default_user"]

    def _get_filtered_context(self, question: str, session_id: str) -> str:
        # Match the filtering logic to inspect whatever key you found above
        search_kwargs = {
            "k": 4,
            "filter": {"session_id": session_id} 
        }
        docs = self.vector_store.similarity_search(question, **search_kwargs)
        if not docs:
            # Fallback attempt filtering by the native "Number" string key
            search_kwargs["filter"] = {"Number": session_id}
            docs = self.vector_store.similarity_search(question, **search_kwargs)
            
        if not docs:
            return "No matching profile records found for this user in the database."
        return "\n\n".join(d.page_content for d in docs)

    def _get_session_history(self, session_id: str):
        if session_id not in self.history_store:
            self.history_store[session_id] = InMemoryChatMessageHistory()
        return self.history_store[session_id]

    def ask(self, query: str, session_id: str = "default_user") -> str:
        return self.conversational_chain.invoke(
            {"question": query, "session_id": session_id},
            config={"configurable": {"session_id": session_id}}
        )
