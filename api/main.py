
"""FastAPI app. Run from the repo root: uvicorn api.main:app --reload"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

import config
from llm.ollama_client import OllamaClient, OllamaUnavailable
from rag.embeddings import Embedder
from rag.pipeline import KordiPipeline
from rag.retriever import Retriever, get_collection

app = FastAPI(title="Kordi API", version="0.5")


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=config.MAX_MESSAGE_CHARS)
    mode: Optional[str] = Field(
        None,
        description="Optional: 'local' or 'tourist'"
    )

    @field_validator("message")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("message must not be empty")
        return v


class Source(BaseModel):
    document: str
    page: Optional[int] = None
    section: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    grounded: bool


@lru_cache
def get_llm() -> OllamaClient:
    return OllamaClient()


@lru_cache
def get_retriever() -> Retriever:
    return Retriever(get_collection(), Embedder())


def get_pipeline() -> KordiPipeline:
    return KordiPipeline(get_retriever(), get_llm())


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest, pipeline: KordiPipeline = Depends(get_pipeline)):
    try:
        result = pipeline.ask(req.message, req.mode)
    except OllamaUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))

    return ChatResponse(
        answer=result.answer,
        sources=result.sources,
        grounded=result.grounded
    )


@app.get("/api/health")
def health():
    info = get_llm().health()
    info["chunks_indexed"] = get_retriever().count()
    return info


# Serve the frontend prototype after registering API routes.
_frontend = Path(__file__).resolve().parent.parent / "frontend" / "prototype"
_assets = Path(__file__).resolve().parent.parent / "frontend" / "assets"

if _frontend.is_dir():
    if _assets.is_dir():
        app.mount(
            "/assets",
            StaticFiles(directory=_assets),
            name="frontend-assets"
        )
    app.mount(
        "/",
        StaticFiles(directory=_frontend, html=True),
        name="frontend"
    )
