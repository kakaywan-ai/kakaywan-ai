# Data handling

- `SOURCES.md` is the source register. Record provenance, dates, version, and permission status.
- `processed.txt` is the local, cleaned UTF-8 text file used for ingestion. Keep it out of Git.
- Original CEPMO documents and private materials belong in the team's restricted storage, not this public repository.
- `raw/` and `private/` are ignored by Git as an additional safeguard.
- Never add citizen complaint logs, resident records, personnel records, credentials, or personal data.
- Permission to use a document for the project is not automatically permission to redistribute it publicly. Verify both separately.
- The loader reads one `.txt` file only; it does not ingest Markdown, PDFs, or directories. The Ollama Lab Guide is reference material, not Kordi's data source.

## Local text setup

Place the approved, cleaned data at `data/processed.txt`, install Ollama, pull
the chat and embedding models, and build the local ChromaDB index:

```powershell
ollama pull gemma3:4b
ollama pull nomic-embed-text
python -m ingest.ingest --source data/processed.txt --reset
python -m api.main
```

Open `http://127.0.0.1:8000`. Ingestion is a separate step; starting the server
does not create or populate the index. The `.txt` source is chunked and embedded
in batches before the chunks are saved to ChromaDB.
