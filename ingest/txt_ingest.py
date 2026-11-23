from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Iterable
from urllib.request import Request, urlopen

import chromadb
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def clean_text(text: str) -> str:
    lines = (line.strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)


def chunk_text(text: str, chunk_size: int, overlap: int) -> Iterable[str]:
    if chunk_size <= overlap:
        raise ValueError("CHUNK_SIZE must be greater than CHUNK_OVERLAP")

    step = chunk_size - overlap
    for start in range(0, len(text), step):
        chunk = text[start : start + chunk_size].strip()
        if len(chunk) >= 40:
            yield chunk
        if start + chunk_size >= len(text):
            break


def ollama_embed(texts: list[str]) -> list[list[float]]:
    host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    model = os.getenv("EMBED_MODEL", "nomic-embed-text")
    payload = json.dumps({"model": model, "input": texts}).encode("utf-8")
    request = Request(
        f"{host}/api/embed",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        result = json.load(response)
    embeddings = result.get("embeddings")
    if embeddings and len(embeddings) == len(texts):
        return embeddings
    raise RuntimeError("Ollama returned an unexpected embedding response")


def ingest_txt(txt_path: Path) -> int:
    if not txt_path.is_file():
        raise FileNotFoundError(
            f"Text file not found: {txt_path}. Place it at data{os.sep}processed.txt"
        )

    text = clean_text(txt_path.read_text(encoding="utf-8"))
    if not text:
        raise RuntimeError("The text file is empty")

    chunk_size = int(os.getenv("CHUNK_SIZE", "1200"))
    overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
    chunks = list(chunk_text(text, chunk_size, overlap))
    if not chunks:
        raise RuntimeError("The text file contained no usable chunks")

    metadatas = [
        {
            "document": txt_path.name,
            "title": txt_path.stem,
            "page": None,
            "section": "",
            "source_path": str(txt_path),
        }
        for _ in chunks
    ]
    ids = [
        str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{txt_path}:{chunk_index}:{chunk[:100]}",
            )
        )
        for chunk_index, chunk in enumerate(chunks)
    ]

    chroma_dir = Path(os.getenv("CHROMA_DIR", str(ROOT / "chroma_db")))
    if not chroma_dir.is_absolute():
        chroma_dir = ROOT / chroma_dir
    chroma_dir.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(chroma_dir))
    collection = client.get_or_create_collection(
        "kordi_documents",
        metadata={"hnsw:space": "cosine"},
    )
    collection.delete(where={"document": txt_path.name})

    batch_size = max(1, int(os.getenv("EMBED_BATCH_SIZE", "32")))
    embeddings: list[list[float]] = []
    for start in range(0, len(chunks), batch_size):
        embeddings.extend(ollama_embed(chunks[start : start + batch_size]))

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a text file into ChromaDB")
    parser.add_argument(
        "text",
        nargs="?",
        default=os.getenv("TXT_PATH", str(ROOT / "data" / "processed.txt")),
        help="Text file path (default: data/processed.txt)",
    )
    args = parser.parse_args()
    try:
        count = ingest_txt(Path(args.text))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Ingested {count} chunks from {args.text}")


if __name__ == "__main__":
    main()
