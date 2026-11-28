"""Create retrieval embeddings through the configured local Ollama model."""
from __future__ import annotations

import ollama

import config


class Embedder:
    def __init__(
        self,
        model_name: str | None = None,
        client=None,
    ):
        self.model_name = model_name or config.EMBED_MODEL
        self._client = client or ollama.Client(
            host=config.OLLAMA_HOST,
            timeout=config.OLLAMA_TIMEOUT,
        )

    def encode(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        result = self._client.embed(model=self.model_name, input=texts)
        if len(result.embeddings) != len(texts):
            raise RuntimeError("Ollama returned an unexpected number of embeddings")
        return result.embeddings
