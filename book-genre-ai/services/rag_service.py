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

# Ensure env variables are loaded whenever this service is imported
load_dotenv()

class RAGChatbotService:
    def __init__(self, company_folder: str):
        # 1. Initialize models (LangChain automatically looks for OPENAI_API_KEY in the environment)
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        
        # 2. Point to the specific company's vector database directory
        db_path = os.path.join(company_folder, "chroma_db")
        self.vector_store = Chroma(
            persist_directory=db_path, 
            embedding_function=OpenAIEmbeddings() # Automatically uses env key
        )
        self.retriever = self.vector_store.as_retriever()
        
        # 3. Create an in-memory dictionary to store session histories
        self.history_store = {}

     # 4. Prompt configuration with strict system instructions (Guardrails)
        # We explicitly instruct the AI to refuse questions outside the book dataset.
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                "You are an expert, friendly Book Recommendation System tailored for this company. "
                "Your task is to help users find books based ONLY on the provided context below.\n\n"
                "CRITICAL RULES:\n"
                "1. If the user asks about a book, genre, or language that is NOT in the context, politely reply that you cannot find it in the company's current catalog.\n"
                "2. Do NOT make up any information or use external knowledge to recommend books not listed here.\n"
                "3. If the user asks general questions completely unrelated to books (e.g., recipes, coding, weather), politely state that you can only assist with book recommendations from the catalog.\n"
                "4. Keep your answers concise, organized, and professional.\n\n"
                "CONTEXT:\n{context}"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

        
        # 5. Context retrieval and chain execution pipeline
        context_chain = self.retriever | (lambda docs: "\n\n".join(d.page_content for d in docs))
        
        self.base_chain = (
            RunnablePassthrough.assign(context=context_chain)

            | self.prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        # 6. Wrap the base chain with message history management
        self.conversational_chain = RunnableWithMessageHistory(
            self.base_chain,
            get_session_history=self._get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history"
        )

    def _get_session_history(self, session_id: str):
        if session_id not in self.history_store:
            self.history_store[session_id] = InMemoryChatMessageHistory()
        return self.history_store[session_id]

    def ask(self, query: str, session_id: str = "default_user") -> str:
        return self.conversational_chain.invoke(
            {"question": query},
            config={"configurable": {"session_id": session_id}}
        )
