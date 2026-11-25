"""Show WHY Kordi answers or falls back. Run from the repo root:

  python -m eval.debug_retrieval                      # all questions in eval/questions.txt
  python -m eval.debug_retrieval "your question"      # one question
  python -m eval.debug_retrieval --answer             # also call gemma3:4b for passing questions

Per question: best similarity scores, the matching document/section, and PASS/FALLBACK
against MIN_SIMILARITY. If a question you EXPECT to be answerable shows FALLBACK with a
low score, the documents don't cover it (add sources) or MIN_SIMILARITY is too high.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import config
from rag.embeddings import Embedder
from rag.retriever import Retriever, get_collection


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?")
    ap.add_argument("--answer", action="store_true", help="also generate an answer with Ollama")
    ap.add_argument("--min", type=float, default=config.MIN_SIMILARITY, help="similarity threshold to test")
    args = ap.parse_args()

    qs = [args.question] if args.question else [
        q.strip() for q in Path(__file__).with_name("questions.txt").read_text(encoding="utf-8").splitlines() if q.strip()]
    retriever = Retriever(get_collection(), Embedder())
    print(f"Chunks indexed: {retriever.count()} | threshold: {args.min} | top_k: {retriever.top_k}\n")
    if retriever.count() == 0:
        print("Index is empty. Run: python -m ingest.ingest --source data/processed --reset")
        return

    pipeline = None
    if args.answer:
        from llm.ollama_client import OllamaClient
        from rag.pipeline import KordiPipeline
        from rag.safety import SafetyGuard
        llm = OllamaClient()
        pipeline = KordiPipeline(retriever, llm, args.min, guard=SafetyGuard(llm))

    passed = 0
    for q in qs:
        hits = retriever.retrieve(q)
        best = hits[0].score if hits else 0.0
        ok = best >= args.min
        passed += ok
        print(f"[{'PASS' if ok else 'FALLBACK'}] {q}")
        for h in hits[:3]:
            where = h.document + (f" p.{h.page}" if h.page else "") + (f" / {h.section}" if h.section else "")
            print(f"    {h.score:.2f}  {where}")
        if pipeline and ok:
            r = pipeline.ask(q)
            print(f"    -> {'GROUNDED' if r.grounded else 'MODEL SAID NO ANSWER'}: {r.answer[:200]!r}")
        print()
    print(f"{passed}/{len(qs)} questions reach the threshold.")


if __name__ == "__main__":
    main()
