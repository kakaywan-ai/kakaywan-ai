# Run Kordi locally (gemma3:4b)

1. Install Ollama, then `ollama pull gemma3:4b` (about 3.4 GB at 4-bit; needs roughly 6 GB free RAM/VRAM).
2. `python -m venv .venv` and activate it, then `pip install -r requirements.txt`.
3. Pull the embedding model: `ollama pull nomic-embed-text`.
4. Put the approved, cleaned text in `data/processed.txt` (git-ignored). The Lab Guide is reference material, not a chatbot data source.
5. Index the source: `python -m ingest.ingest --source data/processed.txt --reset`.
6. Start the local frontend and RAG server: `python -m api.main`, then open http://127.0.0.1:8000.
7. Check status at http://127.0.0.1:8000/api/health (Ollama status and chunks indexed).
8. Run tests: `python -m pytest -q tests`.

Optional Kordi model: `ollama create kordi -f llm/Modelfile`, then set
`$env:OLLAMA_MODEL = "kordi"` in PowerShell before starting the server.

## Frontend data and threads

The prototype stores conversation history, saved responses, threads, and interface
preferences in the current browser's local storage. This data is not synchronized
to the server and is lost if that browser's site data is cleared. Like/dislike
feedback is also local and is not submitted to an API.

Thread follow-ups use the local `/api/chat` endpoint. The frontend includes a
short excerpt of the parent response and recent thread replies within the API's
500-character message limit. The backend does not currently store threads or
provide multi-turn thread context, so thread records remain browser-local.

## How a question flows
question -> embed -> ChromaDB top-k -> similarity check (`MIN_SIMILARITY`) -> gemma3:4b with only the passing passages -> answer + sources.
If no passage passes the check, or the model replies `[[NO_ANSWER]]`, the API returns the fallback with `grounded: false` and no sources. `grounded` is set by the backend, never by the model.
