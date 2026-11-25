"""Central settings for Kordi. Values come from environment variables / .env."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")


def _f(name: str, default: float) -> float:
    return float(os.getenv(name, default))


def _i(name: str, default: int) -> int:
    return int(os.getenv(name, default))


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
OLLAMA_TIMEOUT = _f("OLLAMA_TIMEOUT", 180)
LLM_TEMPERATURE = _f("LLM_TEMPERATURE", 0.2)
LLM_NUM_CTX = _i("LLM_NUM_CTX", 4096)

EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
CHROMA_DIR = os.getenv("CHROMA_DIR", str(ROOT / "chroma_db"))
COLLECTION = os.getenv("CHROMA_COLLECTION", "kakaywan")

CHUNK_SIZE = _i("CHUNK_SIZE", 1000)
CHUNK_OVERLAP = _i("CHUNK_OVERLAP", 200)
TOP_K = _i("TOP_K", 3)
# Cosine similarity a chunk must reach to be considered by the model.
MIN_SIMILARITY = _f("MIN_SIMILARITY", 0.25)

MAX_MESSAGE_CHARS = _i("MAX_MESSAGE_CHARS", 500)
DATA_SOURCE = os.getenv("DATA_SOURCE", str(ROOT / "data" / "processed.txt"))
