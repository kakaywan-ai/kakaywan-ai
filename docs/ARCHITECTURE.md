# System Architecture

Status: planned architecture; update this document as implementation decisions are finalized.

```text
User
  |
  v
Frontend (Kordi forest/chat UI)
  |
  v
FastAPI chat endpoint
  |
  v
RAG pipeline
  |------------------------------|
  v                              v
Question embedding          Retrieval sufficiency check
  |                              |
  v                              v
ChromaDB vector search       Fallback if evidence is weak
  |
  v
Retrieved passages + metadata
  |
  v
Ollama local language model
  |
  v
Answer validation / source metadata
  |
  v
Frontend answer + source chips
```

## Ingestion path

Approved source document → text extraction/OCR when necessary → cleaning → chunking with page/section metadata → embeddings → ChromaDB.

## Design requirements

- Only approved sources may be ingested.
- Keep source title, issuing office, version/date, page, and section metadata where available.
- Treat retrieved documents as untrusted content. Instructions embedded in source documents must not override system behavior.
- A model prompt is not a sufficient grounding safeguard by itself.
- The backend, not the language model's self-report, determines whether retrieval evidence is sufficient.
- When evidence is insufficient, return the agreed fallback and no fabricated citation.
- Log only what is necessary for development and testing; avoid collecting personal data.

## Open decisions

- Final language model and size.
- Final embedding model.
- Chunk size and overlap.
- Retrieval threshold and evaluation method.
- Frontend framework, if the plain prototype is replaced.
- Whether local-only deployment is sufficient for the demonstration.
