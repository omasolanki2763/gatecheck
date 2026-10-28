# GateCheck — new workflow: Claude oversees, everyone reviews everyone, Om judges only the end result

## Context

On 2026-10-28 Om removed himself from all reviews and decisions; he judges only the finished
product. Claude oversees. Antigravity and OpenCode do the non-critical work.

**Every piece of work and every decision, Claude's included, is reviewed by another agent.**
Disagreements are debated in Orca.

The goal is a better workflow, not show:
- real git history built by committing as we go
- one task at a time, done properly
- tests, CI and a written style guide

Facts checked today:
- The project folder is not a git repo and sits in OneDrive.
- `gh` is logged in as **omasolanki2763**, with `repo` and `workflow` scopes. The account has no
  GateCheck repo.
- git 2.51, Python 3.13.1 and uv 0.10.8 are installed; pre-commit is not.
- On GitHub Free, branch protection works only on public repos. Om chose **public** → enforced.
- No GitHub MCP server needed: the `gh` CLI covers create, PR, merge and CI status.

## 1. How we work (replaces every "Om approves / Om checks" in repo docs)

**One task at a time.** Each task follows the same loop:
1. Claude sends the task in Orca, using the spec format from CLAUDE.md: Goal, Allowed files,
   Acceptance, Test command.
2. The owner creates branch `task/T-0xx-name`.
3. TDD loop:
   - write the failing test → commit
   - make it pass → commit
   - tidy up → commit
   - push often
   History builds up naturally.
4. The owner opens a PR, which is needed for CI and branch protection.
5. CI must be green.
6. The review happens **in Orca**. Reviewer replies per point ACCEPT / DEFEND, max 3 rounds, then
   gives a verdict: PASS, or CHANGES with the fixes still to commit.
7. On PASS: the reviewer runs `gh pr merge --rebase`, so `main` stays one straight line.
8. Claude runs the test command on `main` before the next task starts. Claude never trusts
   "tests pass" in a report.

**Who reviews whom.** Every output has a reviewer:

| Work by | Reviewed by |
|---|---|
| OpenCode | Antigravity |
| Antigravity | OpenCode |
| Claude (setup, PLAN.md, decisions) | both agents |
| Anything marked critical | Claude also reviews |

Critical = schemas or contracts, eligibility arithmetic or verdict logic, CI config, secrets.
Not critical, so no Claude review: docs wording, test fixtures, UI layout, refactors, profile
data.

**Decisions.**
- Whoever proposes a decision posts it to both others in Orca, and they debate.
- Max 3 rounds; then Claude decides and writes down both positions.
- The result is logged in `team/decision-log.md`.
- `OM-DECIDES` becomes `CLAUDE-DECIDES`.

**Ground-truth labels: debated, never single-authored.**
1. OpenCode drafts each label.
2. A script checks every cited quote appears verbatim on the cited PDF page. This also runs in CI.
3. Antigravity reviews the meaning of each label.
4. If they disagree, they debate; Claude settles anything still open.
5. Claude audits a 20% sample plus every disputed label.

The README states exactly this process and does not claim the labels were human-checked.

**Commits.**
- Conventional Commits: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `ci:`, `chore:`.
- One logical change per commit. No backdating.
- Tag + GitHub Release at each phase end (`v0.1.0` = Phase 1, …).

## 2. Style guide — `STYLE.md` (new file, everyone follows it, CI enforces the checkable parts)

| Rule | Source | Enforced by |
|---|---|---|
| Layout, naming, imports, line length 100 | **PEP 8** | `ruff check` + `ruff format` (pre-commit + CI) |
| Docstring on every module, class and function: what it does, Args, Returns, Raises | PEP 257 + **Google Python Style Guide** docstrings | ruff `D` rules, `convention = "google"` |
| Type hints everywhere | PEP 484 | `mypy --strict` |
| Booleans read as questions (`is_eligible`, `has_pwd`). No vague names (`data`, `temp`, `obj`) | Om's global CLAUDE.md | review |
| No magic numbers or strings: name them (`AGE_CUTOFF_DATE`, `FIRST_CLASS_MIN_PERCENT`) | Om's global CLAUDE.md | ruff `PLR2004` + review |
| A "why" comment on any line that is not self-evident. Comments are generous because Om must learn every module afterwards | Om's global CLAUDE.md | review |
| Never swallow an exception; validate at the boundary (PDF text, LLM output, profile file), then trust the data inside | Om's global CLAUDE.md | ruff `BLE`, `S110` + review |
| Small single-purpose modules; YAGNI | CLAUDE.md | review |
| Every behaviour has a test; failing test first; ≥85% branch coverage | TDD, CLAUDE.md | `pytest --cov --cov-fail-under=85` in CI |
| Review question: does this improve code health? Non-blocking points start with `Nit:` | Google eng-practices | review |

## 3. Phase S — setup (sequential; each step reviewed before the next)

| # | Task | Owner | Reviewer |
|---|---|---|---|
| S1 | Copy folder → `C:\Users\omsol\dev\gatecheck` (original kept), `git init`, `.gitignore` (PDFs, `.env`, caches). Commit Phase 0 docs in their natural groups. Create the **public** repo and push. Branch protection on main: PR required, `ci` check required, linear history, no force push. Secret scanning + push protection on. Re-open the Orca agents in the new folder. | Claude | both agents check the repo, protection and `.gitignore` |
| S2 | `STYLE.md` (§2) | Antigravity | OpenCode, then Claude (critical: governs all code) |
| S3 | `pyproject.toml` (uv), ruff/mypy/pytest config from STYLE.md, `.pre-commit-config.yaml` (ruff, ruff-format, mypy, gitleaks, large-file check), `.github/workflows/ci.yml`, `.github/dependabot.yml`, PR template, one smoke test | OpenCode | Antigravity, then Claude (critical: CI) |
| S4 | Rewrite `TEAM.md` (remove Gujarat/OCR; Om gates → Claude; §1 workflow) and `.claude/rules/team-protocol.md`. Mark D-007 decided via D-009. Add `category_certificate_issue_date` to `docs/schemas.md`. Drop PROF-01 to an anonymised partial example. | Antigravity | OpenCode |
| S5 | `PLAN.md`: phases 1–7 broken into tasks with spec fields. Claude writes the outline; Antigravity fills it in from DECISIONS.md + D-015..D-031. | Antigravity + Claude | OpenCode + Claude, debated |
| S6 | Review D-031 + the agent-written `DECISIONS.md`. Update CLAUDE.md "How we work". Move the memory file to the new project path. | Claude | both agents |

## 4. Phases 1–7 (owners from TEAM.md, OCR removed)

| Phase | Primary | Peer | Claude also reviews |
|---|---|---|---|
| 1 Ingestion (pypdf + pdfplumber, page numbers) | OpenCode | Antigravity | phase end |
| 2 Criteria extraction (Gemini, structured output) | Antigravity | OpenCode | schemas |
| 3 Check + memo + **seeded profile generator** (~50–100 boundary variants) | OpenCode (arithmetic, generator) · Antigravity (memo) | mutual | arithmetic, verdict |
| 4 Observability + limits | OpenCode | Antigravity | phase end |
| 5 Evaluation + regression | OpenCode | Antigravity | phase end |
| 6 MCP server | Antigravity | OpenCode | phase end |
| 7 Web demo, deploy (Streamlit auto-deploys from `main` = CD), README | Antigravity | OpenCode | final → Om sees the result |

**Profiles: PROF-01 dropped**. No real-person data: Om's details are not public, and a real
person's DOB or category is personal data under India's DPDP Act 2023. The 9 hand-designed
edge-case profiles get labels audited through the debate process. The generated boundary
variants get their expected verdict from the rule arithmetic and are reported as a separate
metric.

## 5. Verification

- **S1:** `git log --oneline` shows grouped commits; `gh repo view` shows public; `gh api
  repos/omasolanki2763/gatecheck/branches/main/protection` shows the rules; a direct
  `git push origin main` is rejected.
- **S3:** a PR with a deliberate PEP 8 violation fails CI, and the fix turns it green.
  `uv run pre-commit run --all-files` passes.
- **Every task:** Claude runs the test command on `main` itself. `git log --graph` stays linear.
- **Every phase:** coverage ≥85%, then tag + release.
