from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

import chromadb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ingest.txt_ingest import ingest_txt
from rag.pipeline import chat

ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "frontend" / "prototype"


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    txt_path = Path(os.getenv("TXT_PATH", str(ROOT / "data" / "processed.txt")))
    if not txt_path.is_absolute():
        txt_path = ROOT / txt_path
    if txt_path.is_file():
        chroma_dir = Path(os.getenv("CHROMA_DIR", str(ROOT / "chroma_db")))
        if not chroma_dir.is_absolute():
            chroma_dir = ROOT / chroma_dir
        chroma_dir.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(chroma_dir))
        collection = client.get_or_create_collection("kordi_documents")
        if collection.count() == 0:
            try:
                ingest_txt(txt_path)
            except Exception as exc:
                app.state.ingest_error = str(exc)
    yield


app = FastAPI(title="Kordi RAG API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat")
def api_chat(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message must not be empty")
    try:
        return chat(message)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Chat service unavailable: {exc}")


@app.get("/")
def prototype():
    return FileResponse(PROTOTYPE / "index.html")

