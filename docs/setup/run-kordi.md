# Run Kordi locally (gemma3:4b)

1. Install Ollama, then `ollama pull gemma3:4b` (about 3.4 GB at 4-bit; needs roughly 6 GB free RAM/VRAM).
2. `python -m venv .venv` and activate it, then `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` (model is already `gemma3:4b`).
4. Put APPROVED documents (.pdf, .md, .txt) in `data/processed/` (git-ignored). To try the pipeline first, use the fake text in `data/demo/`.
5. Index them: `python -m ingest.ingest --source data/processed --reset` (demo: `--source data/demo`).
6. Start the app: `uvicorn api.main:app --reload`, then open http://localhost:8000.
7. Check status at http://localhost:8000/api/health (Ollama up, model ready, chunks indexed).
8. Run tests (no Ollama needed): `python -m pytest -q tests`.

Optional Kordi model: `ollama create kordi -f llm/Modelfile`, then set `OLLAMA_MODEL=kordi`.

## Frontend data and threads

The prototype stores conversation history, saved responses, threads, and interface
preferences in the current browser's local storage. This data is not synchronized
to the server and is lost if that browser's site data is cleared. Like/dislike
feedback is also local and is not submitted to an API.

Thread follow-ups use the existing `/api/chat` endpoint. The frontend includes a
short excerpt of the parent response and recent thread replies within the API's
500-character message limit. The backend does not currently store threads or
provide multi-turn thread context, so thread records remain browser-local.

## How a question flows
question -> embed -> ChromaDB top-k -> similarity check (`MIN_SIMILARITY`) -> gemma3:4b with only the passing passages -> answer + sources.
If no passage passes the check, or the model replies `[[NO_ANSWER]]`, the API returns the fallback with `grounded: false` and no sources. `grounded` is set by the backend, never by the model.
