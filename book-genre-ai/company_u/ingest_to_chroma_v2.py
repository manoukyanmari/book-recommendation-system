# company_u/ingest_to_chroma_v2.py
#
# Improved RAG ingestion for Company U.
#
# Key design decisions:
#
#  user_profiles collection (OpenAI text-embedding-3-small, 1536-dim)
#    - Two docs per user: detailed reading history + aggregated taste summary
#    - Used for exact metadata lookup by session_id (embedding dim doesn't matter here)
#    - Genre/language info annotated on every book so the LLM has rich context
#
#  catalog_books collection (TasteEmbeddingFunction, 8-dim)
#    - One doc per book from company_u_genres_output.csv
#    - Embedded using the pre-trained taste neural network vectors from
#      book_taste_profiles.csv (dimensions: Complexity, Tone, Cultural_Fit,
#      Narrative_Density, Language_Match, Topic_Specificity, Engagement_Appeal,
#      Detail_Level)
#    - Enables collaborative-filtering-style retrieval: find catalog books
#      whose taste profile is closest to the user's mean taste vector
#
# Run once to (re)build chroma_db.  Safe to re-run — wipes and rebuilds both collections.

import os
import re
from collections import Counter

import chromadb
import pandas as pd
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# ── Paths ──────────────────────────────────────────────────────────────────────
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir    = os.path.abspath(os.path.join(current_dir, "..", ".."))
load_dotenv(dotenv_path=os.path.join(root_dir, ".env"))

USERS_CSV        = os.path.join(current_dir, "company_u.csv")
CATALOG_CSV      = os.path.join(current_dir, "company_u_genres_output.csv")
TASTE_CSV        = os.path.join(current_dir, "book_taste_profiles.csv")
CHROMA_PATH      = os.path.join(current_dir, "chroma_db")

# Keep in sync with rag_service_v2.py
COLLECTION_USERS   = "user_profiles"
COLLECTION_CATALOG = "catalog_books"

# Taste dimension column names (must match book_taste_profiles.csv header order)
TASTE_DIMS = [
    "Complexity", "Tone", "Cultural_Fit", "Narrative_Density",
    "Language_Match", "Topic_Specificity", "Engagement_Appeal", "Detail_Level",
]
TASTE_DIM = len(TASTE_DIMS)  # 8


# ── Helpers ────────────────────────────────────────────────────────────────────

def normalize_title(raw: str) -> str:
    """Lowercase, strip ALL punctuation, collapse whitespace."""
    t = str(raw).lower().strip()
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def extract_title_from_library_entry(raw: str) -> str:
    """Strip author/editor suffix that follows ' / ' in raw library strings."""
    return re.split(r"\s+/\s+", raw.strip())[0].strip()


def parse_user_books(raw_books_string: str) -> list:
    """Split comma-period-separated user book string into individual entries."""
    entries = re.split(r"\.,\s*", str(raw_books_string))
    return [e.strip() for e in entries if e.strip()]


def build_genre_lookup(catalog_df: pd.DataFrame) -> dict:
    """Return {normalized_title: {"Genres": str, "Language": str}}"""
    lookup = {}
    for _, row in catalog_df.iterrows():
        key = normalize_title(str(row["Title"]))
        lookup[key] = {
            "Genres":   str(row.get("Genres",   "Unknown")),
            "Language": str(row.get("Language", "Unknown")),
        }
    return lookup


def build_taste_lookup(taste_df: pd.DataFrame) -> dict:
    """
    Return {normalized_title: [8-dim float vector]}.
    Used to compute user mean taste vectors and as catalog embeddings.
    """
    lookup = {}
    for _, row in taste_df.iterrows():
        key = normalize_title(str(row["Title"]))
        vec = [float(row[d]) for d in TASTE_DIMS]
        lookup[key] = vec
    return lookup


# ── Custom embedding function for catalog ─────────────────────────────────────

class TasteEmbeddingFunction:
    """
    LangChain-compatible embedding function that returns pre-computed 8-dim
    taste network vectors for catalog books.

    embed_documents: parse 'Book: <title>' from doc text, look up taste vector.
    embed_query:     returns a zero vector — catalog is always queried via
                     similarity_search_by_vector() with a pre-computed user
                     mean taste vector, so this method is never called in prod.
    """

    def __init__(self, taste_lookup: dict):
        self._lookup = taste_lookup
        self._zero   = [0.0] * TASTE_DIM

    def embed_documents(self, texts: list) -> list:
        results = []
        for text in texts:
            title = self._extract_title(text)
            # Try both full title and subtitle-stripped variant
            vec = (
                self._lookup.get(normalize_title(title))
                or self._lookup.get(normalize_title(re.split(r"\s+:\s+", title)[0]))
                or self._zero[:]
            )
            results.append(vec)
        return results

    def embed_query(self, text: str) -> list:
        # Not used — see docstring above
        return self._zero[:]

    def _extract_title(self, text: str) -> str:
        for line in text.splitlines():
            if line.startswith("Book: "):
                return line[6:].strip()
        return text[:120]


# ── Document builders ──────────────────────────────────────────────────────────

def build_user_documents(users_df: pd.DataFrame, genre_lookup: dict) -> list:
    """
    Per-user: one 'history' doc (annotated book list) + one 'taste' doc
    (genre percentage summary).  Used in the user_profiles collection.
    """
    docs = []

    for _, row in users_df.iterrows():
        user_id   = str(row["id"]).strip()
        raw_books = str(row["books"])

        raw_titles = parse_user_books(raw_books)
        if not raw_titles:
            continue

        enriched_books = []
        genre_counter  = Counter()
        lang_counter   = Counter()

        for raw_t in raw_titles:
            display_title = extract_title_from_library_entry(raw_t)
            norm_key      = normalize_title(display_title)
            meta          = genre_lookup.get(norm_key, {})
            genres        = meta.get("Genres",   "Unknown")
            language      = meta.get("Language", "Unknown")

            enriched_books.append(
                f"  • {display_title} | Genres: {genres} | Language: {language}"
            )
            for g in [g.strip() for g in genres.split(",") if g.strip() != "Unknown"]:
                genre_counter[g] += 1
            if language != "Unknown":
                lang_counter[language] += 1

        total_g = sum(genre_counter.values()) or 1
        total_l = sum(lang_counter.values()) or 1

        # Doc 1 — detailed annotated history
        docs.append(Document(
            page_content=(
                f"User ID: {user_id}\n"
                f"Books read ({len(enriched_books)} titles):\n"
                + "\n".join(enriched_books)
            ),
            metadata={
                "session_id": user_id,
                "doc_type":   "history",
                "source":     "company_u_catalog",
                "book_count": len(enriched_books),
            }
        ))

        # Doc 2 — taste profile summary
        genre_lines = [
            f"  {g}: {c} book(s) ({100*c//total_g}%)"
            for g, c in genre_counter.most_common(10)
        ]
        lang_lines = [
            f"  {lang}: {c} book(s) ({100*c//total_l}%)"
            for lang, c in lang_counter.most_common(5)
        ]
        docs.append(Document(
            page_content=(
                f"User ID: {user_id}\n"
                f"Reading Taste Profile ({len(enriched_books)} books total):\n"
                f"Top genres:\n" + ("\n".join(genre_lines) or "  Unknown") + "\n"
                f"Languages read:\n" + ("\n".join(lang_lines) or "  Unknown")
            ),
            metadata={
                "session_id": user_id,
                "doc_type":   "taste",
                "source":     "company_u_catalog",
                "top_genre":  genre_counter.most_common(1)[0][0] if genre_counter else "Unknown",
            }
        ))

    return docs


def build_catalog_documents(catalog_df: pd.DataFrame) -> list:
    """One document per catalog book.  Embedded via TasteEmbeddingFunction."""
    docs = []
    for _, row in catalog_df.iterrows():
        title    = str(row["Title"])
        genres   = str(row.get("Genres",   "Unknown"))
        language = str(row.get("Language", "Unknown"))
        raw_num  = row.get("Number", 0)
        number   = int(float(raw_num)) if pd.notna(raw_num) else 0

        docs.append(Document(
            page_content=(
                f"Book: {title}\n"
                f"Genres: {genres}\n"
                f"Language: {language}\n"
                f"Checkout frequency: {number}"
            ),
            metadata={
                "title":     title,
                "genres":    genres,
                "language":  language,
                "frequency": number,
                "source":    "company_u_genres_output",
            }
        ))
    return docs


# ── Main ingestion ─────────────────────────────────────────────────────────────

def run_ingestion(verbose: bool = True) -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(f"OPENAI_API_KEY not found — checked .env at {root_dir}")

    # Load data
    users_df   = pd.read_csv(USERS_CSV)
    catalog_df = pd.read_csv(CATALOG_CSV)
    taste_df   = pd.read_csv(TASTE_CSV)

    if verbose:
        print(f"Loaded: {len(users_df)} users | {len(catalog_df)} catalog books | "
              f"{len(taste_df)} taste profiles")

    genre_lookup = build_genre_lookup(catalog_df)
    taste_lookup = build_taste_lookup(taste_df)

    taste_coverage = sum(1 for t in catalog_df["Title"].dropna()
                         if normalize_title(str(t)) in taste_lookup)
    if verbose:
        print(f"Taste vector coverage: {taste_coverage}/{len(catalog_df)} catalog books "
              f"({100*taste_coverage//len(catalog_df)}%)")

    # Drop both collections so we rebuild cleanly from scratch
    raw_client = chromadb.PersistentClient(path=CHROMA_PATH)
    for col_name in (COLLECTION_USERS, COLLECTION_CATALOG):
        try:
            raw_client.delete_collection(col_name)
            if verbose:
                print(f"Dropped old '{col_name}' collection.")
        except Exception:
            pass  # doesn't exist yet — fine

    # ── Collection 1: User profiles (OpenAI text embeddings) ──────────────────
    if verbose:
        print(f"\nBuilding user profile documents...")

    user_docs = build_user_documents(users_df, genre_lookup)

    if verbose:
        print(f"  {len(user_docs)} docs ({len(user_docs)//2} history + "
              f"{len(user_docs)//2} taste profiles) for {len(users_df)} users")
        print(f"  Embedding with text-embedding-3-small → '{COLLECTION_USERS}'...")

    Chroma.from_documents(
        documents=user_docs,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_USERS,
    )
    if verbose:
        print(f"  ✓ user_profiles ready.")

    # ── Collection 2: Catalog books (taste network embeddings) ────────────────
    if verbose:
        print(f"\nBuilding catalog documents with 8-dim taste network embeddings...")

    catalog_docs  = build_catalog_documents(catalog_df)
    taste_emb_fn  = TasteEmbeddingFunction(taste_lookup)

    if verbose:
        print(f"  {len(catalog_docs)} catalog docs → '{COLLECTION_CATALOG}'...")

    Chroma.from_documents(
        documents=catalog_docs,
        embedding=taste_emb_fn,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_CATALOG,
    )
    if verbose:
        print(f"  ✓ catalog_books ready (dimensions: {TASTE_DIM}).")
        print(f"\nDone. Chroma DB at {CHROMA_PATH}")
        print(f"  '{COLLECTION_USERS}':   {len(user_docs)} docs  (1536-dim OpenAI)")
        print(f"  '{COLLECTION_CATALOG}': {len(catalog_docs)} docs  ({TASTE_DIM}-dim taste network)")


if __name__ == "__main__":
    run_ingestion()
