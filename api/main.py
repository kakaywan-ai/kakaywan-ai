"""Local standard-library HTTP server for the frontend and RAG pipeline."""
from __future__ import annotations

import argparse
import json
from functools import lru_cache
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

import config
from llm.ollama_client import OllamaClient, OllamaUnavailable
from rag.embeddings import Embedder
from rag.pipeline import KordiPipeline
from rag.retriever import Retriever, get_collection
from rag.safety import SafetyClassifierError, SafetyGuard

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend" / "prototype"
ASSETS = ROOT / "frontend" / "assets"
MAX_BODY_BYTES = 64 * 1024


@lru_cache
def get_llm() -> OllamaClient:
    return OllamaClient()


@lru_cache
def get_retriever() -> Retriever:
    return Retriever(get_collection(), Embedder())


@lru_cache
def get_pipeline() -> KordiPipeline:
    llm = get_llm()
    return KordiPipeline(get_retriever(), llm, guard=SafetyGuard(llm))


class KordiRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def translate_path(self, path: str) -> str:
        parsed_path = urlsplit(path).path
        if parsed_path.startswith("/assets/"):
            directory = self.directory
            self.directory = str(ASSETS)
            try:
                return super().translate_path(parsed_path[len("/assets"):])
            finally:
                self.directory = directory
        return super().translate_path(path)

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/api/health":
            info = get_llm().health()
            info["chunks_indexed"] = get_retriever().count()
            self._send_json(200, info)
        elif path.startswith("/api/"):
            self._send_json(404, {"detail": "Not found"})
        else:
            super().do_GET()

    def do_POST(self) -> None:
        if urlsplit(self.path).path != "/api/chat":
            self._send_json(404, {"detail": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"detail": "Invalid Content-Length"})
            return
        if content_length <= 0:
            self._send_json(400, {"detail": "Request body is required"})
            return
        if content_length > MAX_BODY_BYTES:
            self._send_json(413, {"detail": "Request body is too large"})
            return

        try:
            payload = json.loads(self.rfile.read(content_length))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(400, {"detail": "Request body must be valid JSON"})
            return
        if not isinstance(payload, dict):
            self._send_json(422, {"detail": "Request body must be a JSON object"})
            return

        message = payload.get("message")
        if not isinstance(message, str) or not message.strip():
            self._send_json(422, {"detail": "message must not be empty"})
            return
        message = message.strip()
        if len(message) > config.MAX_MESSAGE_CHARS:
            self._send_json(422, {"detail": "message is too long"})
            return

        mode = payload.get("mode")
        if mode is not None and not isinstance(mode, str):
            self._send_json(422, {"detail": "mode must be a string"})
            return

        try:
            result = get_pipeline().ask(message, mode)
        except OllamaUnavailable as error:
            self._send_json(503, {"detail": str(error)})
            return
        except SafetyClassifierError:
            self._send_json(503, {"detail": "Safety check failed; please try again."})
            return

        self._send_json(200, {
            "answer": result.answer,
            "sources": result.sources,
            "grounded": result.grounded,
        })


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Kordi's local RAG chat server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), KordiRequestHandler)
    print(f"Kordi is available at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Kordi.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
