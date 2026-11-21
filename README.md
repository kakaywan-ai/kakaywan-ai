# Project Kakaywán AI

**A Grounded RAG Chatbot for Baguio City Eco-Literacy and Climate Action**

Project Kakaywán AI is a University of Baguio School of Information Technology project. Its assistant, **Kordi**, is intended to help users find information about Baguio City's environment, waste management, parks, trees, watersheds, and climate action.

Kordi uses Retrieval-Augmented Generation (RAG): the system retrieves relevant passages from an approved collection of official documents and supplies those passages to a language model when answering. The goal is to make answers traceable to sources, not to claim that an AI model can never hallucinate.

## Project status

**Starter stage.** The forest-style frontend prototype is included. The live backend, document ingestion, retrieval pipeline, source validation, and end-to-end integration still need to be implemented and tested.

Do not describe the current prototype as a functioning RAG chatbot until the retrieval backend is connected and evaluated.

## Core goals

- Build a curated knowledge base from documents that the team is authorized to use.
- Retrieve relevant passages for each user question.
- Show source information, including document title and page or section where available.
- Return a clear fallback when the retrieved evidence is missing, weak, or insufficient.
- Keep the system privacy-conscious and exclude citizen complaint logs and personal records.
- Make the interface accessible to both residents and visitors.

**Important limitation:** prompts and RAG do not guarantee hallucination-free output. The team must implement retrieval sufficiency checks, source attribution, fallback behavior, testing, and human review.

## Planned technology

| Layer | Planned tools |
|---|---|
| Backend/API | Python, FastAPI, Uvicorn |
| Local model serving | Ollama |
| Candidate language models | Gemma 3 and Llama 3 variants, selected after hardware and quality tests |
| Embeddings | Sentence Transformers |
| Vector store | ChromaDB |
| Document extraction | PyMuPDF or pypdf; OCR only when needed |
| Frontend | Existing HTML/CSS/JavaScript prototype initially; framework decision to be confirmed by the team |
| Testing | pytest and API tests |

The team must record the exact versions that are tested together. Do not assume every package version is compatible.

## Repository map

```text
kakaywan-ai/
├── api/                 FastAPI routes and request/response handling
├── data/
│   ├── SOURCES.md       Register of approved sources
│   └── processed/       Permitted, cleaned text for development
├── docs/                Public technical documentation
├── eval/                Test questions, metrics, and results
├── frontend/
│   └── prototype/       Initial clickable forest UI
├── ingest/              Document loading, cleaning, and chunking
├── rag/                 Embeddings, retrieval, grounding, and guardrails
├── training/            Approved experiments and training notes
├── .github/             Issue and pull-request templates
├── CONTRIBUTING.md      Git workflow and collaboration rules
└── TASKS.md             Roles, deliverables, and project schedule
```

## Quick start

1. Install Git and a supported Python version agreed by the team.
2. Install Ollama from [ollama.com](https://ollama.com).
3. Clone the repository:

```bash
git clone https://github.com/<organization>/kakaywan-ai.git
cd kakaywan-ai
```

4. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

5. Install the current dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env` and adjust local settings. Never commit `.env`.

7. Check available model and hardware capacity before downloading a model. For a lightweight initial test:

```bash
ollama pull gemma3:1b
ollama run gemma3:1b
```

Model availability and hardware requirements can change. The team should compare candidate models on the actual development machines before choosing the final model.

## Team and role ownership

| Member | Role |
|---|---|
| Colleen Jose | System Architect and Integration Lead |
| Jerlyn Jyd M. Cortez | Ollama and LLM Lead |
| Theo U. Acosta | RAG Pipeline and Guardrails Lead | 
| Isaac A. Bagsangi | Knowledge Base and Data Lead |
| Karl Angelo B. Marteja | Frontend and API Lead |

See [`TASKS.md`](TASKS.md) for detailed responsibilities, handoffs, learning requirements, and the two-week plan. See [`CONTRIBUTING.md`](CONTRIBUTING.md) before making changes.

## Data, privacy, and public-repository rules

This repository is public. **Public code does not mean every project document is approved for public release.**

- Commit only code and technical documentation that the team is authorized to publish.
- Keep original CEPMO files, correspondence, signed approvals, internal meeting notes, and any non-public materials in the team's restricted storage.
- Do not commit citizen complaint logs, resident records, personal data, credentials, API keys, `.env` files, model weights, or local vector database files.
- Record source provenance and permission status in `data/SOURCES.md`.
- Do not redistribute official documents unless their publication or redistribution permission is clear.
- If permission is uncertain, do not upload the file. Ask the team leader and verify with the issuing office.

The project is designed to minimize personal-data use. This README is not a legal determination or a certification of compliance with RA 10173; the team must follow applicable institutional guidance and confirm its actual data-handling practices.

## API contract (initial proposal)

The frontend and backend should agree on one contract before integration. The following is a proposed starting point, not a claim that the endpoint already exists.

`POST /api/chat`

Request:

```json
{
  "message": "What does the city say about watershed protection?"
}
```

Response when sufficient evidence is retrieved:

```json
{
  "answer": "Answer grounded in the retrieved official passages.",
  "sources": [
    {
      "document": "Document title",
      "page": 5,
      "section": "Relevant section"
    }
  ],
  "grounded": true
}
```

Response when evidence is insufficient:

```json
{
  "answer": "Information not available in the current approved records.",
  "sources": [],
  "grounded": false
}
```

The final schema may be adjusted by the Team Leader, Isaac, and Karl together. Do not set `grounded: true` merely because the language model says it used sources; it must reflect the backend's evidence checks.

## Evaluation expectations

Test at least these categories:

- Answerable questions with clear supporting passages.
- Unanswerable questions outside the approved documents.
- Ambiguous questions that need clarification.
- Adversarial or prompt-injection questions.
- Questions where multiple sources conflict or have different dates.

Measure retrieval quality, source correctness, answer faithfulness, fallback behavior, response time, and usability. Keep test data free of personal information.

## License and attribution

No open-source license has been selected yet. Until the team agrees on a license and checks third-party assets and dependencies, do not add a license file or imply that the repository is available for unrestricted reuse.
