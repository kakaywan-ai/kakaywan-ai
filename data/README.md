# Data handling

- `SOURCES.md` is the source register. Record provenance, dates, version, and permission status.
- `processed/` may contain only cleaned text that the team is authorized to use and store in this repository.
- Original CEPMO documents and private materials belong in the team's restricted storage, not this public repository.
- `raw/` and `private/` are ignored by Git as an additional safeguard.
- Never add citizen complaint logs, resident records, personnel records, credentials, or personal data.
- Permission to use a document for the project is not automatically permission to redistribute it publicly. Verify both separately.
- Preserve source title, page, section, and date metadata so answers can cite their evidence.

## Local PDF setup

Place the approved PDF at `data/processed.pdf`. Then install Ollama, pull the chat
and embedding models, copy `.env.example` to `.env`, and ingest the PDF:

```powershell
ollama pull gemma3:1b
ollama pull nomic-embed-text
python -m ingest.pdf_ingest
python -m uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000`. The API starts and also ingests the PDF automatically
when the Chroma database is empty. Confirm the source is approved before ingesting it.
