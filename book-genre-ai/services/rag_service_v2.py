# services/rag_service_v2.py
#
# Improved RAG service for Company U.
#
# Retrieval architecture:
#   1. User lookup    — exact metadata query (session_id) on user_profiles
#   2. Catalog search — similarity_search_by_vector() using the user's MEAN
#      TASTE VECTOR computed from the pre-trained 8-dim taste network embeddings
#      (book_taste_profiles.csv).  This is collaborative-filtering style:
#      "find catalog books that taste like the books this user has read."
#   3. Already-read filter — normalized title dedup so we never re-recommend.
#
# Requires chroma_db built by ingest_to_chroma_v2.py.

import os
import re

import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

COLLECTION_USERS   = "user_profiles"
COLLECTION_CATALOG = "catalog_books"
CATALOG_TOP_K      = 25

TASTE_DIMS = [
    "Complexity", "Tone", "Cultural_Fit", "Narrative_Density",
    "Language_Match", "Topic_Specificity", "Engagement_Appeal", "Detail_Level",
]
TASTE_DIM = len(TASTE_DIMS)  # 8


# ── Catalog embedding stub (matches the one used in ingest_to_chroma_v2.py) ───
# The catalog collection was built with 8-dim taste vectors.
# We never call embed_* at query time — we pass pre-computed vectors directly —
# but Chroma still requires an embedding_function at init.
class _TasteEmbeddingStub:
    def embed_documents(self, texts):
        return [[0.0] * TASTE_DIM for _ in texts]
    def embed_query(self, text):
        return [0.0] * TASTE_DIM


class RAGChatbotServiceV2:

    def __init__(self, company_folder: str):
        self.llm            = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        self.company_folder = company_folder
        self.db_path        = os.path.join(company_folder, "chroma_db")
        self.history_store  = {}

        # User profiles — embedded with OpenAI text-embedding-3-small
        self.user_store = Chroma(
            persist_directory=self.db_path,
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
            collection_name=COLLECTION_USERS,
        )

        # Catalog books — embedded with 8-dim taste network vectors
        self.catalog_store = Chroma(
            persist_directory=self.db_path,
            embedding_function=_TasteEmbeddingStub(),
            collection_name=COLLECTION_CATALOG,
        )

        # Taste lookup: normalized_title -> 8-dim vector (for mean taste query)
        self.taste_lookup = self._load_taste_lookup()

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an intelligent personalized Book Recommendation Assistant.\n"
                "Analyze the user's reading history and taste profile, then recommend "
                "books ONLY from the AVAILABLE CATALOG section.\n\n"
                "RULES:\n"
                "1. If context says 'GUARDRAIL_TRIGGERED: USER_HAS_NO_DATA', reply exactly: "
                "'I'm sorry, but I couldn't find any book recommendations matching your "
                "specific profile in our catalog at the moment.'\n"
                "2. Only recommend books listed in the AVAILABLE CATALOG. Never invent titles.\n"
                "3. Never recommend books the user has already read.\n"
                "4. When justifying each recommendation, reference the user's genre preferences "
                "and taste dimensions (Complexity, Tone, etc.) shown in their profile.\n\n"
                "Context:\n{context}"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

    # ── Public API ─────────────────────────────────────────────────────────────

    def get_unique_users(self) -> list:
        try:
            data = self.user_store._collection.get(include=["metadatas"])
            ids  = {
                str(m["session_id"])
                for m in data.get("metadatas", [])
                if m and "session_id" in m
            }
            return sorted(ids) or ["No users found"]
        except Exception:
            return ["default_user"]

    def ask(self, query: str, session_id: str = "default_user") -> str:
        context  = self._compile_context(query, session_id)
        history  = self._get_session_history(session_id)
        response = self.chain.invoke({
            "context":      context,
            "chat_history": history.messages,
            "question":     query,
        })
        history.add_user_message(query)
        history.add_ai_message(response)
        return response

    # ── Context compilation ────────────────────────────────────────────────────

    def _compile_context(self, question: str, session_id: str) -> str:
        sid = str(session_id).strip()

        user_docs = self._fetch_user_documents(sid)
        if not user_docs:
            return "GUARDRAIL_TRIGGERED: USER_HAS_NO_DATA"

        history_doc = next((d for d in user_docs if d["doc_type"] == "history"), None)
        taste_doc   = next((d for d in user_docs if d["doc_type"] == "taste"),   None)

        if not history_doc and not taste_doc:
            return "GUARDRAIL_TRIGGERED: USER_HAS_NO_DATA"

        user_section = ""
        if history_doc:
            user_section += f"=== USER READING HISTORY ===\n{history_doc['content']}\n\n"
        if taste_doc:
            user_section += f"=== USER TASTE PROFILE ===\n{taste_doc['content']}\n\n"

        already_read    = self._extract_read_titles(history_doc["content"] if history_doc else "")
        user_taste_vec  = self._compute_user_taste_vector(history_doc["content"] if history_doc else "")
        catalog_section = self._retrieve_catalog(user_taste_vec, already_read, question)

        return user_section + catalog_section

    def _fetch_user_documents(self, session_id: str) -> list:
        try:
            result = self.user_store._collection.get(
                where={"session_id": session_id},
                include=["documents", "metadatas"],
            )
            docs = []
            for content, meta in zip(
                result.get("documents", []),
                result.get("metadatas",  []),
            ):
                if content and meta:
                    docs.append({"content": content, "doc_type": meta.get("doc_type", "")})
            return docs
        except Exception as e:
            print(f"[RAGServiceV2] Error fetching user docs for {session_id}: {e}")
            return []

    # ── Taste vector helpers ───────────────────────────────────────────────────

    def _load_taste_lookup(self) -> dict:
        """Load book_taste_profiles.csv into {normalized_title: [8-dim vector]}."""
        taste_csv = os.path.join(self.company_folder, "book_taste_profiles.csv")
        if not os.path.exists(taste_csv):
            print("[RAGServiceV2] Warning: book_taste_profiles.csv not found — "
                  "falling back to text-based catalog retrieval.")
            return {}
        try:
            df = pd.read_csv(taste_csv)
            lookup = {}
            for _, row in df.iterrows():
                key = self._normalize(str(row["Title"]))
                vec = [float(row[d]) for d in TASTE_DIMS if d in df.columns]
                if len(vec) == TASTE_DIM:
                    lookup[key] = vec
            print(f"[RAGServiceV2] Loaded taste vectors for {len(lookup)} books.")
            return lookup
        except Exception as e:
            print(f"[RAGServiceV2] Error loading taste profiles: {e}")
            return {}

    def _compute_user_taste_vector(self, history_text: str) -> list | None:
        """
        Average the taste vectors of all books the user has read.
        Returns None if no taste vectors can be matched (triggers text fallback).
        """
        if not self.taste_lookup:
            return None

        vecs = []
        for line in history_text.splitlines():
            if "•" not in line or "|" not in line:
                continue
            raw_title = line.split("•", 1)[1].split("|")[0].strip()
            vec = (
                self.taste_lookup.get(self._normalize(raw_title))
                or self.taste_lookup.get(self._normalize(re.split(r"\s+:\s+", raw_title)[0]))
            )
            if vec:
                vecs.append(vec)

        if not vecs:
            return None

        # Element-wise mean (pure Python — no numpy needed at runtime)
        mean_vec = [sum(v[i] for v in vecs) / len(vecs) for i in range(TASTE_DIM)]
        return mean_vec

    # ── Catalog retrieval ──────────────────────────────────────────────────────

    def _retrieve_catalog(
        self,
        user_taste_vec: list | None,
        already_read: set,
        fallback_query: str,
        k: int = CATALOG_TOP_K,
    ) -> str:
        """
        Primary path: similarity_search_by_vector with user's 8-dim mean taste vector.
        Fallback:     similarity_search with the user's question text (text embeddings).
        """
        try:
            fetch_k = k + len(already_read) + 10

            if user_taste_vec is not None:
                results = self.catalog_store.similarity_search_by_vector(
                    user_taste_vec, k=fetch_k
                )
                method = "taste-network similarity"
            else:
                results = self.catalog_store.similarity_search(
                    fallback_query, k=fetch_k
                )
                method = "text similarity (no taste vectors matched)"

            catalog_lines = []
            seen = set()

            for doc in results:
                meta       = doc.metadata
                title      = str(meta.get("title", "")).strip()
                title_norm = self._normalize_for_dedup(title)

                if title_norm in already_read or title_norm in seen:
                    continue
                seen.add(title_norm)

                genres   = meta.get("genres",   "Unknown")
                language = meta.get("language", "Unknown")
                freq     = meta.get("frequency", 0)
                catalog_lines.append(
                    f"  - {title} | Genres: {genres} | Language: {language} "
                    f"| Checkouts: {freq}"
                )
                if len(catalog_lines) >= k:
                    break

            if not catalog_lines:
                return "=== AVAILABLE CATALOG ===\nNo matching unread catalog books found.\n"

            return (
                f"=== AVAILABLE CATALOG "
                f"(top {len(catalog_lines)} books matched via {method}) ===\n"
                + "\n".join(catalog_lines) + "\n"
            )

        except Exception as e:
            print(f"[RAGServiceV2] Catalog retrieval error: {e}")
            return "=== AVAILABLE CATALOG ===\nCatalog temporarily unavailable.\n"

    # ── Normalization helpers ──────────────────────────────────────────────────

    @staticmethod
    def _normalize(t: str) -> str:
        """Same normalization as ingest_to_chroma_v2.py — used for taste lookup."""
        t = str(t).lower().strip()
        t = re.sub(r"[^\w\s]", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    @staticmethod
    def _normalize_for_dedup(title: str) -> str:
        """Strip subtitle, remove punctuation — for already-read dedup."""
        t = re.split(r"\s+:\s+", title)[0]
        t = t.lower().strip()
        t = re.sub(r"[^\w\s]", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def _extract_read_titles(self, history_text: str) -> set:
        read = set()
        for line in history_text.splitlines():
            if "•" in line and "|" in line:
                raw_title = line.split("•", 1)[1].split("|")[0].strip()
                read.add(self._normalize_for_dedup(raw_title))
        return read

    # ── Session history ────────────────────────────────────────────────────────

    def _get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id] = InMemoryChatMessageHistory()
        return self.history_store[session_id]


# Backward-compatible alias — existing code that imported RAGChatbotService keeps working
RAGChatbotService = RAGChatbotServiceV2
