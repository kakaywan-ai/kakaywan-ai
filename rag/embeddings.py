"""Sentence-Transformers embedder (lazy-loaded so tests can swap in a fake)."""
from __future__ import annotations

import config


class Embedder:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or config.EMBED_MODEL
        self._model = None

    def encode(self, texts: list[str]) -> list[list[float]]:
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model.encode(texts, normalize_embeddings=True).tolist()
