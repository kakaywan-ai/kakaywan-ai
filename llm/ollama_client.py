"""Thin wrapper around the Ollama Python client (Lab 1.3 patterns).

Handles: connection errors, a missing model (404 -> auto-pull -> retry once),
streaming, and a health check the API can expose.
"""
from __future__ import annotations

from typing import Iterator, Optional

import httpx
import ollama

import config


class OllamaUnavailable(RuntimeError):
    """Ollama server is not reachable."""


def _norm(name: str) -> str:
    return name if ":" in name else f"{name}:latest"


class OllamaClient:
    def __init__(self, model: Optional[str] = None, host: Optional[str] = None, client=None):
        self.model = model or config.OLLAMA_MODEL
        self.host = host or config.OLLAMA_HOST
        self._client = client or ollama.Client(host=self.host, timeout=config.OLLAMA_TIMEOUT)

    # ---- model management -------------------------------------------------
    def installed_models(self) -> list[str]:
        try:
            resp = self._client.list()
        except (ConnectionError, httpx.ConnectError) as e:
            raise OllamaUnavailable(f"Cannot reach Ollama at {self.host}. Is it running?") from e
        return [m.model for m in resp.models]

    def has_model(self) -> bool:
        return _norm(self.model) in {_norm(n) for n in self.installed_models()}

    def ensure_model(self) -> None:
        if not self.has_model():
            self._client.pull(self.model)

    def health(self) -> dict:
        try:
            return {"ollama": True, "model": self.model, "model_ready": self.has_model()}
        except OllamaUnavailable:
            return {"ollama": False, "model": self.model, "model_ready": False}

    # ---- generation -------------------------------------------------------
    def _messages(self, system: str, user: str) -> list[dict]:
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]

    def _options(self, temperature: Optional[float]) -> dict:
        return {
            "temperature": config.LLM_TEMPERATURE if temperature is None else temperature,
            "num_ctx": config.LLM_NUM_CTX,
        }

    def chat(self, system: str, user: str, temperature: Optional[float] = None) -> str:
        kwargs = dict(model=self.model, messages=self._messages(system, user),
                      options=self._options(temperature))
        try:
            try:
                resp = self._client.chat(**kwargs)
            except ollama.ResponseError as e:
                if e.status_code != 404:
                    raise
                self._client.pull(self.model)  # model missing: download, then retry once
                resp = self._client.chat(**kwargs)
        except (ConnectionError, httpx.ConnectError) as e:
            raise OllamaUnavailable(f"Cannot reach Ollama at {self.host}. Is it running?") from e
        return resp["message"]["content"]

    def stream(self, system: str, user: str, temperature: Optional[float] = None) -> Iterator[str]:
        try:
            for chunk in self._client.chat(model=self.model, messages=self._messages(system, user),
                                           options=self._options(temperature), stream=True):
                yield chunk["message"]["content"]
        except (ConnectionError, httpx.ConnectError) as e:
            raise OllamaUnavailable(f"Cannot reach Ollama at {self.host}. Is it running?") from e
