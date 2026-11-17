# Project Kakaywán AI — Team Roles, Tasks, and Two-Week Plan

## Project goal

Build a working, grounded RAG chatbot prototype named **Kordi** for Baguio City eco-literacy and climate action. The system should retrieve from approved official documents, cite the evidence it uses, and fall back when evidence is insufficient.

**Important:** RAG and a system prompt do not guarantee that a model will never hallucinate. The team must implement and evaluate retrieval sufficiency checks, source attribution, fallback behavior, and prompt-injection resistance.

## 1. Team role divisions

### Team Leader — System Architect and Integration Lead

**Primary responsibility:** Keep the whole project technically coherent, integrate the workstreams, and ensure the final system can be demonstrated and defended.

Owns:
- `README.md`
- `TASKS.md`
- `CONTRIBUTING.md`
- `docs/ARCHITECTURE.md`
- `docs/API_CONTRACT.md`
- `eval/` overall evaluation plan and final results coordination
- GitHub Issues, Project board, milestones, review coordination

Main deliverables:
1. Create and maintain the system architecture diagram.
2. Create and maintain the RAG data-flow diagram.
3. Agree on the API request/response contract with Karl and Isaac.
4. Maintain the README, setup guide, `.env.example`, and team workflow.
5. Set up GitHub issues, labels, board, PR review process, and `main` ruleset where available.
6. Coordinate integration between frontend, API, retrieval, and Ollama.
7. Prepare an evaluation set of at least 20 questions: answerable, unanswerable, ambiguous, and adversarial/prompt-injection examples.
8. Coordinate end-to-end tests and record limitations and results.
9. Prepare technical defense notes: explain how a question moves through the system, how citations are produced, and when Kordi refuses or falls back.
10. Ensure all five members understand the complete system, not only their assigned component.

First tasks:
- [ ] Finalize architecture and data-flow diagrams.
- [ ] Agree on the API contract with Karl and Isaac.
- [ ] Complete README and setup instructions.
- [ ] Create the evaluation question set.
- [ ] Verify repository rules and public/private data boundaries.
- [ ] Run integration tests as soon as the first API and retrieval components exist.

### Jerlyn Jyd M. Cortez — Ollama and LLM Lead

**Primary responsibility:** Local language model setup, model selection, Ollama integration, and the team's LLM learning/training experiment.

Owns:
- Ollama setup notes under `docs/`
- `llm/` or the agreed Ollama client module
- `training/` experiment coordination
- Model comparison notes

Main deliverables:
1. Ensure every member can install Ollama and run a local model.
2. Test candidate models such as Gemma 3 and Llama 3 variants, choosing sizes based on available RAM/VRAM.
3. Demonstrate the basic Ollama commands: `ollama pull`, `ollama list`, `ollama run`, and `ollama rm`.
4. Create and explain a Kordi Modelfile using `FROM`, `PARAMETER`, and `SYSTEM`.
5. Implement the Python Ollama client and coordinate its interface with Isaac.
6. Compare models using the same questions and record answer quality, instruction following, latency, and hardware use.
7. Lead the optional LoRA fine-tuning experiment if the core RAG prototype is stable.
8. Document what was actually trained, what data was used, and the evaluation results.

Important distinction:
- Ollama runs and serves local models.
- A Modelfile configures a model; it is not fine-tuning.
- Fine-tuning changes model weights.
- RAG retrieves external knowledge at question time.
- RAG is the factual knowledge mechanism for this project; fine-tuning is an optional experiment for style or answer format.

### Theo U. Acosta — Knowledge Base and Data Lead

**Primary responsibility:** Ensure the chatbot's knowledge base is traceable, clean, current, and based only on approved materials.

Owns:
- `ingest/`
- `data/SOURCES.md`
- `data/README.md`
- Document inventory and metadata
- Data quality notes

Main deliverables:
1. Inventory all documents received or found online.
2. Record title, issuing office, publication/date received, source URL or how received, permission/publication status, and version.
3. Verify the CEPMO online reference document before recording it as an official source.
4. Confirm whether received documents may be used internally and whether they may be redistributed publicly. These are separate permissions.
5. Build PDF/text extraction and cleaning.
6. Use OCR only when the source is scanned and text extraction is insufficient.
7. Preserve page numbers, headings, source title, dates, and other metadata needed for citations.
8. Coordinate chunking requirements and metadata with Isaac.
9. Flag outdated, duplicate, incomplete, or conflicting documents.
10. Ensure no PII, citizen complaint records, or non-approved material enters the public repository, training dataset, or chatbot knowledge base.

Do not upload original CEPMO files to the public repository merely because they were provided to the team.

### Isaac A. Bagsangi — RAG Pipeline and Guardrails Lead

**Primary responsibility:** Build the retrieval system that finds relevant evidence and controls when Kordi may answer.

Owns:
- `rag/`
- Embedding and vector-store implementation
- Retrieval tests
- Grounding and fallback logic
- Coordination of RAG integration with Jerlyn and Theo

Main deliverables:
1. Learn and explain embeddings and semantic search.
2. Implement the embedding workflow using Sentence Transformers.
3. Set up ChromaDB and define the stored chunk metadata.
4. Implement top-k retrieval and return source metadata with each chunk.
5. Work with Theo to validate chunk size, overlap, page metadata, and source quality.
6. Work with Jerlyn to pass retrieved context to Ollama.
7. Implement a retrieval sufficiency/relevance check. Do not let the model answer confidently when retrieved passages are irrelevant or insufficient.
8. Implement the fallback response for unsupported questions.
9. Ensure source references shown to the user correspond to the passages actually retrieved.
10. Test ambiguous, unanswerable, conflicting-source, and prompt-injection questions.

**Optional UI enhancement — Kordi mascot (only after core RAG work is on track):**
- Design Kordi, the project mascot, for the frontend.
- Create at least three consistent expressions:
  1. Happy / Welcoming
  2. Thinking / Searching
  3. Unsure / Concerned
- Provide transparent PNG or WebP assets with consistent proportions and dimensions.
- Coordinate with Karl on asset size, placement, and how the UI changes expression.
- This is optional and must not delay ingestion, retrieval, guardrails, or the working chatbot.

### Karl Angelo B. Marteja — Frontend and API Lead

**Primary responsibility:** Turn the prototype into a usable interface and connect it to the backend.

Owns:
- `frontend/`
- `api/`
- Frontend/API integration tests
- UI states and source display

Main deliverables:
1. Preserve and improve the existing forest-style prototype.
2. Implement the chat interface and message history for the prototype.
3. Build the API route with the agreed request/response contract, coordinating with Isaac and the Team Leader.
4. Connect the frontend to the real API rather than sample keyword-matched answers.
5. Display answer sources clearly, including document title and page/section when available.
6. Add loading, empty, error, and fallback states.
7. Keep the UI responsive and usable.
8. Implement tourist/local suggested-question modes if time permits.
9. Coordinate with Isaac if the optional Kordi mascot is created.
10. Test the interface against successful, unsupported, and failed API responses.

## 2. Shared ownership boundaries and handoffs

| Component / decision | Primary owner | Required coordination |
|---|---|---|
| Architecture and overall integration | Team Leader | All members |
| `README.md`, `TASKS.md`, `CONTRIBUTING.md` | Team Leader | All members |
| `data/SOURCES.md`, source inventory | Theo | Team Leader, Isaac |
| `ingest/` | Theo | Isaac |
| Ollama client and model setup | Jerlyn | Isaac, Team Leader |
| Prompt/model behavior | Jerlyn | Isaac |
| `rag/`, embeddings, ChromaDB retrieval | Isaac | Theo, Jerlyn |
| Grounding, fallback, retrieval tests | Isaac | Team Leader, Jerlyn |
| `api/` | Karl | Isaac, Team Leader |
| `frontend/` | Karl | Team Leader; Isaac for mascot |
| `requirements.txt` | Team Leader coordinates | All owners before dependency changes |
| API contract | Team Leader coordinates | Karl and Isaac |

Do not make a breaking change to a shared interface without telling the affected owners first.

## 3. Everyone must learn Ollama and model training

The professor expects all five members to understand Ollama and model training. Do not leave this knowledge with Jerlyn alone.

Every member must complete these shared exercises:
1. Install Ollama and verify it runs.
2. Pull and run at least one model that their computer can handle.
3. Practice `ollama pull`, `ollama list`, `ollama run`, and `ollama rm`.
4. Understand a Modelfile with `FROM`, `PARAMETER`, and `SYSTEM`.
5. Run the Kordi Modelfile and explain what it changes.
6. Install the Python Ollama package and run a basic `ollama.chat()` example.
7. Explain the RAG flow: document extraction → chunking → embeddings → ChromaDB → retrieval → context to Ollama → answer and sources.
8. Explain the difference between running a model, configuring it, fine-tuning it, and using RAG.
9. Participate in model evaluation and explain the results.

Suggested mini-workshops:
- Jerlyn: Ollama, model selection, Modelfile, Python client.
- Theo: source preparation, PDF extraction, metadata, chunking.
- Isaac: embeddings, vector databases, retrieval, guardrails.
- Karl: API integration, frontend request/response handling.
- Team Leader: architecture, evaluation, integration, and defense.

## 4. Two-week implementation plan

### Days 1–2: Foundations
- Team Leader: confirm public repository, ruleset, issues, project board, architecture, and API contract.
- Jerlyn: install Ollama, test a small model, demonstrate the commands and Modelfile.
- Theo: inventory available documents, verify source links and permission status.
- Isaac: study embeddings/ChromaDB and produce a minimal retrieval design.
- Karl: preserve the prototype, decide the frontend approach with the team, and define the API integration point.
- Everyone: clone the repo, create a virtual environment, run the starter setup, and complete an Ollama smoke test.

### Days 3–5: First working RAG prototype
- Theo: extraction, cleaning, chunking, metadata, and approved sample corpus.
- Isaac: embeddings, ChromaDB, retrieval, and retrieval tests.
- Jerlyn: Ollama Python client and model comparison baseline.
- Karl: FastAPI endpoint and frontend API connection using a placeholder response first.
- Team Leader: integrate early, test the end-to-end flow, and document blockers.
- Target: one question can travel from frontend to API to retrieval to Ollama and return an answer with source metadata by Day 5.

### Days 6–7: Grounding and interface integration
- Isaac: relevance/sufficiency checks, fallback, source attribution, adversarial tests.
- Jerlyn: tune inference parameters and coordinate prompt behavior.
- Theo: verify document/page metadata and identify conflicts or outdated sources.
- Karl: connect real responses, show sources, implement loading/error/fallback UI.
- Team Leader: run end-to-end tests and review failures with owners.

### Days 8–9: Evaluation and improvement
- All members: run the shared question set and record failures.
- Jerlyn: compare candidate language models; perform LoRA experiment only if core work is stable.
- Isaac: compare retrieval settings and embedding models.
- Theo: verify answer evidence against source documents and maintain source register.
- Karl: usability and responsive-interface testing.
- Team Leader: consolidate metrics, limitations, risk register, and defense notes.

### Day 10: Freeze and demonstrate
- Stop adding nonessential features.
- Fix high-priority bugs.
- Run the final evaluation set.
- Verify every displayed citation.
- Record the demo and prepare the report/presentation.
- Clearly disclose limitations and what is not yet implemented.

## 5. Evaluation question set

The Team Leader coordinates at least 20 questions, preferably 30:

| Category | Minimum | What it tests |
|---|---:|---|
| Answerable | 5 | Can the system retrieve correct evidence and answer accurately? |
| Unanswerable | 5 | Does Kordi refuse to invent unsupported facts? |
| Ambiguous | 5 | Does Kordi ask for clarification or qualify its answer? |
| Adversarial / prompt injection | 5 | Does Kordi ignore instructions embedded in user input or retrieved content that conflict with system rules? |

For each test, record:
- Question and category.
- Expected evidence or expected fallback.
- Retrieved document/chunk and relevance.
- Whether the answer is supported.
- Whether the citation is correct.
- Whether fallback behavior is correct.
- Notes and proposed fix.

Do not treat a model's self-reported confidence or a `grounded` field generated by the model as proof of grounding. Grounding status must be determined by backend checks and evaluation.

## 6. Suggested first GitHub issues

Create one issue per task and assign an owner:
1. Set up repository rules, labels, project board, and team access — Team Leader.
2. Finalize architecture and RAG data-flow diagrams — Team Leader.
3. Agree API request/response contract — Team Leader, Karl, Isaac.
4. Verify CEPMO online reference and document permission status — Theo.
5. Complete source register — Theo.
6. Implement PDF/text loader with metadata — Theo.
7. Implement chunking and metadata preservation — Theo, Isaac.
8. Set up ChromaDB and embeddings — Isaac.
9. Implement top-k retrieval with source metadata — Isaac.
10. Implement relevance check and unsupported-question fallback — Isaac.
11. Install Ollama and document setup — Jerlyn.
12. Implement Python Ollama client — Jerlyn.
13. Compare candidate models on fixed questions — Jerlyn, all members.
14. Build FastAPI chat endpoint — Karl.
15. Connect frontend to API — Karl.
16. Display source citations and fallback states — Karl, Isaac.
17. Create evaluation dataset — Team Leader, all members.
18. Test prompt injection and data-handling risks — Isaac, Theo, Team Leader.
19. Optional: create Kordi mascot with three expressions — Isaac, only if core RAG milestones are on track.

## 7. Definition of done

A task is done only when:
- The work matches the issue's acceptance criteria.
- It runs or has been checked in the intended environment.
- Relevant tests were run and recorded.
- A teammate reviewed the pull request.
- The pull request was merged into `main`.
- Required documentation was updated.
- No secrets, personal data, or unauthorized documents were added.
