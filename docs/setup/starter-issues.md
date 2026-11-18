# Starter GitHub Issues

Create one issue per task, add an owner, label, and acceptance criteria. Do not assign all tasks to one person.

## Team Leader
1. Configure public repository, team access, `main` ruleset, labels, and Project board.
2. Create architecture and RAG data-flow diagrams.
3. Agree API contract with Karl and Isaac.
4. Prepare 20–30 evaluation questions and final evaluation report.
5. Coordinate end-to-end integration and technical defense notes.

## Theo — Knowledge Base and Data
6. Verify CEPMO online reference and record source provenance/permission.
7. Complete `data/SOURCES.md`.
8. Implement document text extraction and metadata preservation.
9. Implement cleaning and chunking preparation.
10. Review source freshness, duplicates, and conflicts.

## Isaac — RAG and Guardrails
11. Set up Sentence Transformers embeddings and ChromaDB.
12. Implement retrieval with top-k passages and source metadata.
13. Implement retrieval sufficiency checks and fallback.
14. Test answerability, ambiguity, source accuracy, and prompt injection.
15. Optional only after core RAG is stable: create Kordi mascot with three expressions.

## Jerlyn — Ollama and LLM
16. Install Ollama and document model setup.
17. Create and explain Kordi Modelfile.
18. Implement Python Ollama client.
19. Compare candidate models on the same evaluation questions.
20. Run optional LoRA experiment if core RAG is stable.

## Karl — Frontend and API
21. Build FastAPI chat endpoint using the agreed contract.
22. Connect the existing forest prototype to the API.
23. Display sources and implement loading/error/fallback states.
24. Test responsive UI and API failure handling.

## Shared learning
25. All five members complete the Ollama command, Modelfile, Python client, RAG-flow, and model-training explanation exercises.
