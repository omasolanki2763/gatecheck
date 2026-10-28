# Agentic Document Workflow — GateCheck (eligibility screener)

Om's main portfolio project for AI Engineer / GenAI Developer roles (India).
Priority = **complete the project**; Om walks through and learns every module after it is
done, so he can defend it in interviews. Domain pivoted from Gujarat tenders on 2026-09-27
(`team/decision-log.md` D-010, D-014).

## Product

- **User:** an Indian CS/engineering graduate (e.g. a GATE qualifier like Om) deciding
  "apply or skip" — is it worth paying the fee. One candidate profile vs one notice per run.
- **Input:** one official English, born-digital recruitment / admission PDF (DRDO/RAC,
  BARC OCES/DGFS, IIT M.Tech brochures) + one structured candidate-profile file.
- **Output:** memo — every eligibility criterion with page number + short quote; per
  criterion met / not met / unclear with profile evidence; final APPLY / SKIP /
  NEEDS REVIEW with one-paragraph justification; low-confidence items flagged for a human.
- **Pipeline:** 1. Extract criteria (structured output) → 2. Check vs profile → 3. Draft memo.
- **Version 1 scope (b):** eligibility PDFs only; IIT GATE-cutoff tables are a later stage.

## Differentiator (non-negotiable)

The LLM call is ordinary; the instrumentation and evaluation around it are the point.

- **Observability:** per-run step trace (input, output, model, tokens, latency, retries,
  errors), replayable; token cost per run and per step; timeouts, retry+backoff, max
  steps, cost cap per run — behaviour at each limit defined **and tested**.
- **Evaluation:** labelled ground-truth set (10 → 25 notices × designed profile set); criterion precision/recall,
  per-criterion check accuracy, go/no-go accuracy, cost and latency per run; regression
  suite vs last saved results; error taxonomy built from observed failures with counts.
- **Interfaces:** MCP server with read-only, logged tools `extract_criteria`,
  `check_eligibility`, `draft_memo` (JSON Schema contracts); simple web demo (upload
  notice, pick profile, see memo + trace).
- **Docs:** `DECISIONS.md` (context, options, choice, reasoning — kept current);
  `README.md` at the end with real numbers, architecture diagram, taxonomy, limitations,
  one documented failure + fix.

## Scope

Out of scope — do not build: predicting selection / rank, writing the application,
comparing or ranking multiple candidates, user accounts, automatic portal scraping,
cutoff-table stage (until v1 is done). Ask Om before adding anything out of scope.

## Phase 0 decisions already made (full list: `team/decision-log.md` D-009, D-014)

- Arithmetic in Python, never the LLM (age on a cut-off date, stacked category + PwD
  relaxations, CGPA ↔ % conversion, valid-GATE-year windows); explicit NOT_FOUND →
  NEEDS REVIEW; cross-criterion dependencies (e.g. BARC GATE-only route ⇒ no CBT);
  proof-document checklist per criterion. Addendum / corrigendum handling deferred past Phase 3.
- Data: DRDO/RAC advertisements, BARC OCES/DGFS brochure, IIT M.Tech brochures —
  English, born-digital (no OCR). **Designed synthetic profile set** covering category,
  PwD, age-boundary, final-year, CGPA-vs-% edge cases, plus Om's own profile.
- Two sets: **collection** (unlabelled — crash/cost/latency stats) and **labelled**
  (10 → 25 notices, headline metrics). PDFs not committed; commit a manifest (URL,
  download date, hash).
- Labels: **OpenCode drafts, Om checks every label against the PDF**; provenance per
  label; README says labels were checked by Om reading the PDF. Labeller vendor must
  differ from the pipeline vendor.
- Pipeline LLM: Gemini free tier; fallback local model (Om: 16 GB RAM, NVIDIA 6 GB VRAM).
  API budget ₹0. No fixed deadlines.
- Code: agents write; Om does a full module walkthrough after completion.
  Repo: move out of OneDrive + git init; private until Phase 7.

## Phase 0 open topics (agents research → Om + Claude decide in PLAN.md)

6. PDF text + page-number extraction (born-digital) · 7. locating criteria in long
brochures · 8. structured output + validation · 9. hand-written loop vs LangGraph ·
10. tracing (Langfuse vs own JSONL/SQLite) · 11. storage · 12. candidate-profile +
memo schemas + profile set · 13. web framework + deploy (whichever looks better) ·
14. testing without spending money per run.

Phase 0 ends with `PLAN.md`, initial `DECISIONS.md`, schemas and a labelling guide —
then stop for Om's approval. **No code until the plan is approved.**

## Phases and target dates

| Phase | Goal | Done when |
|---|---|---|
| 0 | Interview, `PLAN.md`, `DECISIONS.md`, schemas, labelling guide | Om approves; no code |
| 1 | Repo skeleton, config, PDF ingestion incl. scanned pages | Tests pass on sample PDFs; text + page numbers correct |
| 2 | Criteria extraction to validated structured output | Works on 3 labelled tenders; Om reviews |
| 3 | Checking + memo drafting | End-to-end memo for 3 tenders, evidence cites pages |
| 4 | Observability: traces, cost, timeouts, retries, limits | Every limit has a test that triggers it |
| 5 | Evaluation: metrics, regression runner, history, taxonomy | Full labelled-set run with results table |
| 6 | MCP server with the three tools | Works from an MCP client; calls logged |
| 7 | Web demo, deploy, README, diagram | Live link; README has real numbers |

No fixed dates (Om, 2026-09-27) — move as fast as quality allows. Om's time is variable.

## How we work

- Phase-gated: at each phase end, run the tests, show real output, stop for approval.
- For every module, explain in plain language what it does, why, and the alternatives,
  and record it in `DECISIONS.md`.
- One commit per file. Never commit secrets (`.env` + `.gitignore`).
- Ask before adding any dependency. Give an API cost estimate before any full
  labelled-set run.
- Type hints everywhere, `pytest`, small single-purpose modules.
- If a fix fails, don't stack patches — step back and propose a cleaner design.
- Lasting topic-specific rules go in `.claude/rules/*.md` with YAML frontmatter.

## Orchestration (Orca multi-agent team)

Source of truth for every command/flag: `orca skills get orchestration`. Never invent
flags from memory; on failure, re-read the guide before retrying.

**Roles changed 2026-09-27 — `.claude/rules/team-protocol.md` is authoritative.**
- **Antigravity + OpenCode = equal PEERS:** both research/draft, each reviews the other,
  talk peer-to-peer. Split of work lives in `TEAM.md`.
- **Claude Code = PLANNER + FINAL REVIEWER:** `PLAN.md` / `DECISIONS.md` + Om interview;
  reviews AGREED entries in `team/decision-log.md`. Tightest budget — no coordination loops.

Rules:
- Task spec starts with a ROLE line and contains: Goal | Allowed files | Forbidden files |
  Acceptance criteria | Test command | Branch: `task/T-XXX`. ≤5 files, ~1 hour of work.
- Never run two workers on tasks that touch the same file. Workers ask through the
  orchestration `ask` flow, never guess.
- Never trust "tests pass" in a report; the commander runs the test command itself.
- Merge only after REVIEW = PASS and a green commander test run.
- Irreversible actions (deleting files, schema/data migrations, force-push, major
  dependency upgrades) → decision gate, ask Om.
- Release finished workers. After every step print: Task | Agent | Status | Branch | Notes.
- Worktrees need a git repo — this folder is not one yet (and sits inside OneDrive, which
  risks file locks with parallel worktrees). Resolve before the first dispatch.
- Open decision (not yet settled by Om): agents writing most of the code conflicts with
  Om defending every line. Settle how Om owns the code before the first WORKER dispatch.

Templates:
- SCOUT: "ROLE: SCOUT. Research only; do NOT edit files. Goal: <topic>. worker_done body:
  relevant files + line refs, patterns to follow, pitfalls, open questions. Mark anything
  unconfirmed as UNVERIFIED."
- WORKER: "ROLE: WORKER. Implement exactly this spec; no extra refactors or renames.
  Branch task/T-XXX, one commit per file. <Goal/Allowed/Forbidden/Criteria/Test>.
  worker_done body: files changed, pasted test output, doubts."
- REVIEWER: "ROLE: REVIEWER. Do NOT edit code. Review `git diff main...task/T-XXX`
  against the spec of T-XXX. worker_done body starts with PASS or CHANGES, then
  numbered issues."
