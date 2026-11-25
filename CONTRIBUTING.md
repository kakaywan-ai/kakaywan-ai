# Contributing to Project Kakaywán AI

This guide defines how the five team members collaborate without overwriting one another's work. Read it before creating a branch or pushing code.

## 1. Repository visibility and what may be published

The project repository is intended to be **public**.

A public repository may contain:
- Source code written by the team.
- Technical documentation and architecture diagrams.
- Sanitized source inventories and verified public URLs.
- Synthetic test examples and evaluation results that contain no personal data.
- Approved screenshots or design assets.

Do **not** put these in the public repository unless the issuing party has explicitly authorized public redistribution:
- Original CEPMO documents received directly from staff.
- Letters, replies, signed approvals, or private correspondence.
- Internal meeting notes or photos showing staff or visitors without permission.
- Documents marked confidential, internal, restricted, or unclear in status.
- Personal information, citizen complaints, resident records, or personnel records.
- `.env` files, credentials, API keys, model weights, ChromaDB databases, or large generated files.

Keep originals and private evidence in the team's restricted Google Drive. The public repository should contain a sanitized technical record, not a copy of every project artifact. If unsure, do not commit the file; ask the Team Leader and verify permission with the issuing office.

## 2. One-time GitHub setup (Team Leader)

1. Create or use the team's GitHub organization.
2. Create a **public** repository named `kakaywan-ai`.
3. Add all five members with appropriate access. Give developers Write access; keep organization ownership limited to people who need it.
4. Create labels such as `backend`, `data`, `rag`, `frontend`, `ollama`, `training`, `docs`, `testing`, and `bug`.
5. Create a GitHub Project board with: `Backlog`, `Ready`, `In Progress`, `Review`, and `Done`.
6. Create GitHub Issues from `docs/setup/starter-issues.md` and assign an owner.
7. Configure a `main` branch ruleset or branch protection, if the organization's/repository settings permit it:
   - Require a pull request before merging.
   - Require at least one approval from someone other than the author.
   - Require review conversations to be resolved.
   - Block force pushes and branch deletion.
   - Require CI checks after the test workflow exists.
   - Restrict direct pushes to `main`, if that option is available.
8. Verify the ruleset is **active and targeting `main`**. Do not assume it is active just because it was created.

GitHub plan and organization settings can affect which rules are available. If a desired setting is unavailable, keep the team agreement below and have the Team Leader monitor the branch history. Never claim that GitHub is enforcing a rule that has not been verified.

## 3. Team collaboration agreements

- Nobody works directly on `main`.
- Nobody pushes directly to `main`. All changes go through a pull request.
- Each task should have a GitHub Issue, an owner, and a clear acceptance condition.
- Use one branch per task. Avoid multiple people editing the same files without coordination.
- Keep commits small and focused.
- Every pull request needs at least one approval from a teammate other than its author.
- The Team Leader is included as a reviewer for integration-sensitive changes. The Team Leader does not need to be the only reviewer.
- The author must not approve their own pull request.
- Merge only after review, required checks, and conflict resolution.
- The designated merger may be Jerlyn or another person selected by the Team Leader. If Jerlyn's own PR is merged, someone else must review and perform the merge. No one approves their own work.
- Prefer **Squash and merge** to keep the main history readable.
- Delete the feature branch after it has been merged.
- Communicate before changing shared files such as `requirements.txt`, API schemas, configuration, or core entry points.

## 4. One-time setup for every member

Configure Git with your own GitHub identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

Clone the repository:

```bash
git clone https://github.com/<organization>/kakaywan-ai.git
cd kakaywan-ai
```

Create the Python environment:

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

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a dependency installation fails, report the Python version, operating system, full error, and command used. Do not silently change shared dependency versions.

## 5. Daily workflow: branch, commit, push, and pull request

### Step A: Update your local `main`

Do this before starting a new task:

```bash
git switch main
git pull origin main
```

### Step B: Create a task branch

Use the pattern `type/short-description`.

Examples:

```bash
git switch -c feat/text-ingestion
git switch -c feat/ollama-client
git switch -c feat/vector-retrieval
git switch -c feat/chat-api
git switch -c feat/chat-interface
git switch -c docs/ollama-setup
git switch -c test/rag-evaluation
```

Do not use `main` as your working branch.

### Step C: Work and inspect your changes

```bash
git status
git diff
```

Run the relevant tests before committing. Do not commit files you do not understand.

### Step D: Stage only the files you intended to change

Prefer:

```bash
git add path/to/file.py
```

or a specific folder:

```bash
git add rag/
```

Avoid blindly running `git add .` if you have not checked `git status`. This prevents accidentally staging private documents, `.env`, model files, or unrelated changes.

### Step E: Commit with a clear message

Format:

```text
type: short description
```

Examples:

```bash
git commit -m "feat: add processed text ingestion"
git commit -m "feat: implement ChromaDB retrieval"
git commit -m "fix: handle empty retrieval results"
git commit -m "docs: explain Ollama setup"
git commit -m "test: add unanswerable RAG questions"
```

Use `feat`, `fix`, `docs`, `test`, `refactor`, or `chore`. Keep each commit focused on one logical change.

### Step F: Push your branch to GitHub

For the first push of a branch:

```bash
git push -u origin feat/text-ingestion
```

Replace the branch name with your actual branch. For later pushes to the same branch:

```bash
git push
```

**Pushing a feature branch is expected. Pushing directly to `main` is not.**

### Step G: Open a pull request

1. Open the repository on GitHub.
2. Select **Compare & pull request** for your pushed branch, or go to **Pull requests → New pull request**.
3. Set the base branch to `main` and compare branch to your feature branch.
4. Use a clear title, for example `feat: add processed text ingestion`.
5. Link the issue using `Closes #<issue-number>`.
6. Complete the pull request template.
7. Request a reviewer who did not author the change.
8. Wait for feedback. Do not merge your own PR.
9. If changes are requested, edit the same branch, commit, and push again. The pull request updates automatically.
10. After approval and passing checks, the authorized merger merges it and deletes the branch.

## 6. Keep your branch updated

Before continuing work or opening a PR, bring in the latest `main`:

```bash
git switch main
git pull origin main
git switch feat/text-ingestion
git merge main
```

If there are conflicts:
1. Open each conflicted file.
2. Decide the correct combined content with the file owner if needed.
3. Remove Git conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
4. Test the result.
5. Stage and commit the resolution:

```bash
git add path/to/resolved-file
git commit -m "fix: resolve merge conflict"
git push
```

If you are unsure, stop and ask for help. Do not force-push and do not delete another member's work.

## 7. Pull request checklist

Before requesting review, confirm:

- [ ] The PR has a linked issue.
- [ ] The branch is based on the latest `main`.
- [ ] Only relevant files are included.
- [ ] No `.env`, credentials, API keys, private correspondence, non-public source files, PII, model weights, or generated databases are included.
- [ ] Code runs or the limitation is explained.
- [ ] Relevant tests were run and results are stated.
- [ ] Documentation or setup instructions were updated where needed.
- [ ] API/schema/config changes were coordinated with affected owners.
- [ ] Screenshots are included for meaningful UI changes, where useful.

## 8. File ownership and coordination

See `TASKS.md` for the full responsibility matrix. The default ownership is:

| Area | Primary owner | Coordinate with |
|---|---|---|
| Architecture, README, project integration | Team Leader | Everyone |
| `ingest/`, source register, data documentation | Theo | Isaac |
| Ollama client, model setup, prompt behavior | Jerlyn | Isaac, Team Leader |
| `rag/`, embeddings, retrieval, guardrails | Isaac | Theo, Jerlyn |
| `api/`, frontend, UI integration | Karl | Isaac, Team Leader |
| Shared dependencies and API contract | Team Leader coordinates | Relevant owners |

Only the primary owner should make substantial changes to their area unless the owners agree otherwise. Anyone may report bugs or suggest improvements.

## 9. Secrets, data, and generated files

Never commit:
- `.env` or any real credentials.
- API keys, passwords, tokens, private URLs, or personal access tokens.
- Original CEPMO documents unless public redistribution is explicitly approved.
- Citizen complaint logs, resident records, personnel information, or other personal data.
- Local ChromaDB folders, caches, model weights, or large generated artifacts.
- Photos or screenshots without appropriate permission.

The `.gitignore` helps prevent accidental commits, but it is not a security boundary. Always inspect `git status` and the PR file list.

If a secret is accidentally pushed, deleting it in a later commit is not enough. Notify the Team Leader immediately, revoke or rotate the exposed credential, and follow GitHub's sensitive-data removal process if necessary.

## 10. Useful commands

| Purpose | Command |
|---|---|
| Current branch and changes | `git status` |
| Review unstaged changes | `git diff` |
| See recent commits | `git log --oneline -10` |
| Change branch | `git switch <branch>` |
| Update main | `git switch main` then `git pull origin main` |
| Discard unstaged changes to a file | `git restore <file>` |
| Unstage a file | `git restore --staged <file>` |
| Temporarily save uncommitted changes | `git stash` |
| Restore stashed changes | `git stash pop` |
| See remote branches | `git branch -r` |

Be careful: `git restore` discards local changes to the specified file. Check `git diff` first.

## 11. Team communication and definition of done

Daily check-in (brief):
- What did I finish?
- What am I working on next?
- What is blocking me?
- Do I need another member to review or coordinate?

A task is **Done** only when:
- The implementation or document is complete.
- It has been tested or checked.
- A teammate has reviewed it.
- The PR has been merged into `main`.
- Required documentation is updated.
- No private or unauthorized data has been introduced.
