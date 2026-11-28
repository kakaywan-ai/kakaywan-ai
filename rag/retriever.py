"""ChromaDB storage + top-k retrieval returning source metadata with every chunk."""
from __future__ import annotations

from dataclasses import dataclass

import chromadb

import config


@dataclass
class Hit:
    text: str
    document: str
    score: float  # cosine similarity, higher = more similar


def get_collection(chroma_dir: str | None = None, reset: bool = False):
    client = chromadb.PersistentClient(path=chroma_dir or config.CHROMA_DIR)
    if reset:
        try:
            client.delete_collection(config.COLLECTION)
        except Exception:
            pass
    return client.get_or_create_collection(config.COLLECTION, metadata={"hnsw:space": "cosine"})


class Retriever:
    def __init__(self, collection, embedder, top_k: int | None = None):
        self.collection = collection
        self.embedder = embedder
        self.top_k = top_k or config.TOP_K

    def count(self) -> int:
        return self.collection.count()

    def retrieve(self, question: str) -> list[Hit]:
        if self.count() == 0:
            return []
        res = self.collection.query(
            query_embeddings=self.embedder.encode([question]),
            n_results=min(self.top_k, self.count()),
        )
        hits = []
        for text, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            hits.append(Hit(
                text=text,
                document=meta["document"],
                score=1.0 - dist,
            ))
        return sorted(hits, key=lambda h: h.score, reverse=True)
