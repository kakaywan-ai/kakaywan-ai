from __future__ import annotations

import argparse
import os
import sys
import uuid
from pathlib import Path
from typing import Iterable

import chromadb
from dotenv import load_dotenv
from pypdf import PdfReader

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


def ollama_embed(text: str) -> list[float]:
    import json
    from urllib.request import Request, urlopen

    host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    model = os.getenv("EMBED_MODEL", "nomic-embed-text")
    payload = json.dumps({"model": model, "input": text}).encode("utf-8")
    request = Request(
        f"{host}/api/embed",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        result = json.load(response)
    embeddings = result.get("embeddings")
    if embeddings:
        return embeddings[0]
    raise RuntimeError("Ollama returned no embedding")


def ingest_pdf(pdf_path: Path) -> int:
    if not pdf_path.is_file():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}. Place it at data{os.sep}processed.pdf"
        )

    reader = PdfReader(str(pdf_path))
    chunk_size = int(os.getenv("CHUNK_SIZE", "1200"))
    overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
    chunks: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = clean_text(page.extract_text() or "")
        if not page_text:
            continue
        for chunk_index, chunk in enumerate(chunk_text(page_text, chunk_size, overlap)):
            chunks.append(chunk)
            metadatas.append(
                {
                    "document": pdf_path.name,
                    "title": pdf_path.stem,
                    "page": page_number,
                    "section": "",
                    "source_path": str(pdf_path),
                }
            )
            ids.append(str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{pdf_path}:{page_number}:{chunk_index}:{chunk[:100]}")))

    if not chunks:
        raise RuntimeError("The PDF contained no extractable text")

    chroma_dir = Path(os.getenv("CHROMA_DIR", str(ROOT / "chroma_db")))
    if not chroma_dir.is_absolute():
        chroma_dir = ROOT / chroma_dir
    chroma_dir.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(chroma_dir))
    collection = client.get_or_create_collection(
        "kordi_documents",
        metadata={"hnsw:space": "cosine"},
    )
    collection.delete(where={"document": pdf_path.name})

    embeddings = [ollama_embed(chunk) for chunk in chunks]
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest the Kordi PDF into ChromaDB")
    parser.add_argument(
        "pdf",
        nargs="?",
        default=os.getenv("PDF_PATH", str(ROOT / "data" / "processed.pdf")),
        help="PDF path (default: data/processed.pdf)",
    )
    args = parser.parse_args()
    try:
        count = ingest_pdf(Path(args.pdf))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Ingested {count} chunks from {args.pdf}")


if __name__ == "__main__":
    main()
