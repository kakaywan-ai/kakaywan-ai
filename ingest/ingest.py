"""Chunk one approved UTF-8 text file -> embed -> store in ChromaDB.

Usage:  python -m ingest.ingest [--source data/processed.txt] [--reset]

Only ingest documents listed as approved in data/SOURCES.md.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import config

EMBED_BATCH_SIZE = 32


@dataclass
class Chunk:
    text: str
    document: str
    source_file: str


def split_text(text: str, size: int, overlap: int) -> list[str]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("CHUNK_SIZE must be positive and greater than CHUNK_OVERLAP")

    text = text.strip()
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            boundary = max(
                text.rfind("\n\n", start, end),
                text.rfind("\n", start, end),
                text.rfind(" ", start, end),
            )
            if boundary > start + size // 2:
                end = boundary

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def _title(path: Path, text: str = "") -> str:
    m = re.match(r"\s*#\s+(.+)", text)
    return m.group(1).strip() if m else path.stem.replace("_", " ").replace("-", " ")


def load_chunks(source_path: str | Path, size: int | None = None, overlap: int | None = None) -> list[Chunk]:
    size = config.CHUNK_SIZE if size is None else size
    overlap = config.CHUNK_OVERLAP if overlap is None else overlap
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Data source not found: {source}")
    if not source.is_file() or source.suffix.lower() != ".txt":
        raise ValueError("Ingestion accepts one .txt file; provide data/processed.txt.")

    text = source.read_text(encoding="utf-8-sig")
    title = _title(source, text)
    return [
        Chunk(piece, title, source.name)
        for piece in split_text(text, size, overlap)
    ]


def ingest(source_path: str | Path, embedder, chroma_dir: Optional[str] = None, reset: bool = True) -> int:
    from rag.retriever import get_collection
    chunks = load_chunks(source_path)
    col = get_collection(chroma_dir, reset=reset)
    for start in range(0, len(chunks), EMBED_BATCH_SIZE):
        batch = chunks[start:start + EMBED_BATCH_SIZE]
        embeddings = embedder.encode([chunk.text for chunk in batch])
        if len(embeddings) != len(batch):
            raise RuntimeError("Embedder returned an unexpected number of embeddings")
        ids = [
            hashlib.sha1(f"{chunk.source_file}|{start + offset}|{chunk.text}".encode()).hexdigest()
            for offset, chunk in enumerate(batch)
        ]
        col.upsert(
            ids=ids,
            documents=[chunk.text for chunk in batch],
            embeddings=embeddings,
            metadatas=[{"document": chunk.document} for chunk in batch],
        )
    return len(chunks)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=config.DATA_SOURCE)
    ap.add_argument("--reset", action="store_true", help="rebuild the collection from scratch")
    args = ap.parse_args()
    from rag.embeddings import Embedder
    print("Reminder: ingest only sources marked approved in data/SOURCES.md")
    n = ingest(args.source, Embedder(), reset=args.reset)
    print(f"Indexed {n} chunks from {args.source}" if n else f"No text found in {args.source}")


if __name__ == "__main__":
    main()
