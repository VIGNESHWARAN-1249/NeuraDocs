
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_DIR = BASE_DIR / "documents"
UPLOADS_DIR = DOCUMENTS_DIR / "uploads"
CHROMA_DIR = BASE_DIR / "chroma_db"

DOCUMENTS_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "gemini-2.5-flash"

COLLECTION_NAME = "document_collection"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
TOP_K = 4
