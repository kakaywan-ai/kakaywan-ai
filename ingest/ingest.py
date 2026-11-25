"""Load approved text -> chunk with section metadata -> embed -> ChromaDB.

Usage:  python -m ingest.ingest [--source data/processed.txt] [--reset]

Only ingest documents listed as approved in data/SOURCES.md.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

import config


@dataclass
class Chunk:
    text: str
    document: str
    page: int  # 0 = unknown (txt/md)
    section: str
    source_file: str


def split_text(text: str, size: int, overlap: int) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    units: list[str] = []
    for p in paras:
        if len(p) <= size:
            units.append(p)
        else:
            step = max(size - overlap, 1)
            units.extend(p[i:i + size] for i in range(0, len(p), step))
    chunks, cur = [], ""
    for u in units:
        if cur and len(cur) + len(u) + 2 > size:
            chunks.append(cur)
            cur = (cur[-overlap:] + "\n\n" + u) if overlap else u
        else:
            cur = f"{cur}\n\n{u}" if cur else u
    if cur:
        chunks.append(cur)
    return chunks


def _title(path: Path, text: str = "") -> str:
    m = re.match(r"\s*#\s+(.+)", text)
    return m.group(1).strip() if m else path.stem.replace("_", " ").replace("-", " ")


def _markdown_sections(text: str) -> Iterator[tuple[str, str]]:
    heading, buf = "", []
    for line in text.splitlines():
        m = re.match(r"(#{1,6})\s+(.*)", line)
        if m:
            if "".join(buf).strip():
                yield heading, "\n".join(buf)
            heading, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    if "".join(buf).strip():
        yield heading, "\n".join(buf)


def load_chunks(source_path: str | Path, size: int | None = None, overlap: int | None = None) -> list[Chunk]:
    size, overlap = size or config.CHUNK_SIZE, config.CHUNK_OVERLAP if overlap is None else overlap
    chunks: list[Chunk] = []
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Data source not found: {source}")
    if source.is_file() and source.suffix.lower() not in {".md", ".txt"}:
        raise ValueError("Only .txt and .md text sources can be ingested; PDF files are not supported.")
    paths = [source] if source.is_file() else sorted(source.rglob("*"))
    for path in paths:
        suffix = path.suffix.lower()
        if suffix in {".md", ".txt"}:
            text = path.read_text(encoding="utf-8-sig")
            title = _title(path, text)
            sections = _markdown_sections(text) if suffix == ".md" else [("", text)]
            for heading, body in sections:
                for piece in split_text(body, size, overlap):
                    chunks.append(Chunk(piece, title, 0, heading, path.name))
    return chunks


def ingest(source_dir: str | Path, embedder, chroma_dir: Optional[str] = None, reset: bool = True) -> int:
    from rag.retriever import get_collection
    chunks = load_chunks(source_dir)
    col = get_collection(chroma_dir, reset=reset)
    if not chunks:
        return 0
    ids = [hashlib.sha1(f"{c.source_file}|{c.page}|{c.section}|{c.text}".encode()).hexdigest() for c in chunks]
    col.upsert(
        ids=ids,
        documents=[c.text for c in chunks],
        embeddings=embedder.encode([c.text for c in chunks]),
        metadatas=[{"document": c.document, "page": c.page, "section": c.section,
                    "source_file": c.source_file} for c in chunks],
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
    print(f"Indexed {n} chunks from {args.source}" if n else f"No .md or .txt files found in {args.source}")


if __name__ == "__main__":
    main()
