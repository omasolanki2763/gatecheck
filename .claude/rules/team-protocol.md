---
name: team-protocol
description: How Antigravity, OpenCode and Claude Code work together on this project (roles, peer review, messaging, current task)
topic: orchestration
updated: 2026-09-27
---

# Team protocol

Set by Om on 2026-09-27. Overrides the role lines in CLAUDE.md "Orchestration" where they differ.

## Roles

- **Antigravity** (Gemini, Google AI Pro) and **OpenCode** are **equal peers**. Both research,
  both may draft, and each reviews the other's work. Neither is the boss.
- **Claude Code = PLANNER + FINAL REVIEWER.** Turns agreed work into `PLAN.md` / `DECISIONS.md`,
  runs the interview with Om, and reviews every AGREED decision in `team/decision-log.md`.
  Claude's budget is the tightest (Claude Pro): do **not** message Claude for discussion or status.
  Claude reads only the decision log entries you mark AGREED (see "Decision log" below).
- **Om** decides. Anything the two of you cannot agree on goes to Om as two written positions.

## Resuming in a new session (do this first, every time)

Terminal handles in the table below are from 2026-09-27 and **change whenever a terminal is
restarted**. At the start of every new session:

1. Read this whole file, then `CLAUDE.md`, then the **last ~5 entries** of `team/decision-log.md`
   (not the whole log) to see where work stopped. The "Current task" section below is the task.
2. Find the live handles: `orca terminal list --json` → match each terminal's `agentIdentity`
   (`antigravity`, `opencode`, `claude`). Use those handles instead of the table below.
3. Tell your peer you are back with your current handle (send + wake, steps 1-2 below).
4. Claude's inbox is `run:run_f4a5b3f23883`. If a send to it fails with an unknown-run error,
   send an escalation to Om in your own terminal output and wait — Claude will create a new run
   and update this file.
5. If this file and your memory disagree, **this file wins**.

## Talking to each other (peer to peer)

| Agent | Terminal handle |
|---|---|
| Antigravity | `term_8a30dbb2-2c3b-47db-bdc0-096bcfb5033f` (2026-10-28) |
| OpenCode | `term_e6c5e0f1-6f5c-41bd-bee4-3283b7ed6f79` (2026-10-28) |
| Claude Code (planner) | inbox `run:run_f4a5b3f23883` · terminal `term_d7522647-5f87-4abb-8c57-3487390bc916` (2026-10-28) |

1. Send: `orca orchestration send --to <OTHER handle> --type status --subject "<subject>" --body "<text>"`
   (NO `--run` on peer sends — rejected with a Run mismatch; no double quotes inside the body).
   Match handles on `agentIdentity` PLUS `worktreePath`. Handoff notes use
   `### Handoff — <agent> (<date>)`, not a D-number. Full lessons: `team/agent-team-protocol-TEMPLATE.md` §10.
2. Wake the other agent, because it only reads when prompted:
   `orca terminal send --terminal <OTHER handle> --text "New peer message: run orca orchestration check --terminal <OTHER handle> --json" --enter`
3. Read your own messages: `orca orchestration check --terminal <YOUR handle> --json`
4. **Communication problem** (send/check errors, peer silent >10 min, you two stuck in a loop, or
   you disagree about the protocol itself): send Claude ONE message with the exact error text:
   `orca orchestration send --to run:run_f4a5b3f23883 --type escalation --subject "Comms issue: <short>" --body "<exact error / what happened>"`
   Claude will fix it. (The warning "live terminal-only mailbox ... not durable" is normal — ignore it.)

## Review rules (keep overhead low)

- Every artifact is reviewed by the other peer. Reply per point: **ACCEPT** (say what changes) or
  **DEFEND** (concrete reason). Agreeing just to be agreeable is a failure of your job.
- **One message per round**, all points batched, under ~200 words.
- **Max 3 rounds per item.** Still unresolved → write both positions under "Open disagreements" for Om.
- Facts need a source URL + date; otherwise mark **UNVERIFIED**.
- Only **one agent edits a file at a time** (folder is in OneDrive, not git). The editor passes the
  turn explicitly in a message ("TEAM.md is yours").
- Phase 0: no code, no files other than those named in the current task.

## Decision log — the only channel to Claude

Every decision or judgement either of you makes goes into `team/decision-log.md` as one entry.
Chat stays peer-to-peer in Orca; the log holds only outcomes. Append new entries at the bottom;
never rewrite another entry except its Status / review lines.

```
### D-001 — <short title>
- Status: PROPOSED
- Owner: <agent> · Reviewer: <other agent>
- Decision: <1-3 lines>
- Why: <reasoning, with source URL + date or UNVERIFIED>
- Alternatives rejected: <option — why not>
- Peer review: <1-2 lines: rounds, what changed>
- Claude review: (empty — Claude fills this)
```

Status flow: `PROPOSED` (owner wrote it) → `AGREED` (reviewer accepted, peer rounds done) →
Claude sets `CLAUDE-OK` or `CLAUDE-ISSUES: <points>` → on issues, the owner fixes, peer re-reviews,
sets `AGREED` again. Unresolved after 3 peer rounds → `OM-DECIDES` with both positions.

Notify Claude **once per batch**, not per entry, when one or more entries reach AGREED:
`orca orchestration send --to run:run_f4a5b3f23883 --type status --subject "Log ready: D-00x..D-00y" --body "AGREED entries ready for review"`
Claude replies by writing into the entry's `Claude review` line and wakes the entry's owner.

## Plan workflow (decided by Om, 2026-09-27)

1. **Om + Claude** discuss and draft the plan (`PLAN.md`).
2. **Antigravity + OpenCode** review it back and forth: find issues, argue them peer to peer, fix
   them, and log every change as a decision-log entry (what changed in the plan, why).
3. **Claude** reviews the modified plan via the AGREED entries. No major flaw → `CLAUDE-OK`
   and the modified plan is implemented. Major flaw → `CLAUDE-ISSUES`, back to step 2.

## Previous task (T-004): make our way of working reusable — DONE (D-027, CLAUDE-OK). Resume T-002 below.

Om wants to reuse how we three communicate in other projects, so new teams do not reinvent it.
Claude drafted `team/agent-team-protocol-TEMPLATE.md` (a generic, placeholder-based version of
this file). Your job: make it correct and complete from YOUR side of the experience.

1. Both read it fully. Each checks, independently: every command/flag against the live Orca CLI
   (`orca skills get orchestration`, `--help`) — mark anything wrong; the setup steps (could a
   fresh team follow them with zero history?); missing lessons from your side (D-024/D-025
   findings, encoding, handoff, context limits, anything that broke).
2. **Antigravity must verify and fill `{{ANTIGRAVITY_AUTOLOAD}}`** — which file the `agy` CLI
   auto-loads at session start (and whether it reads AGENTS.md).
3. Batch your points, argue peer to peer (max 3 rounds), then ONE agent edits the template at a
   time. Keep it generic — no GateCheck specifics. Keep it short; cut anything a new team
   would not need.
4. Fill the "Review record" at the bottom; log one entry D-026 (what you changed, why).
   Mark AGREED and batch-ping Claude. Then resume T-002.

## Current task (T-005): draft the two remaining Phase 0 documents (Claude + Om do PLAN.md in parallel)

CLAUDE.md: Phase 0 ends with PLAN.md, DECISIONS.md, **schemas** and a **labelling guide**.
Claude writes PLAN.md/DECISIONS.md with Om. You two draft the other two — documents, NOT code:

1. **`docs/schemas.md`** — owner Antigravity, reviewer OpenCode. Field-by-field contracts for
   Criterion (+ typed `rule_parameters`), CandidateProfile, EligibilityMemo, RunTrace record, from
   D-017/D-019/D-021. MUST include Claude's carried fix: **DISJUNCTION semantics** — a rule with
   alternative routes (e.g. 60% OR First Class OR CGPA 6.0) is MET if ANY route is met;
   conversion precedence applies only when the notice mandates one formula. Plain-language note
   per field (Om reads it).
2. **`docs/labelling-guide.md`** — owner OpenCode (it drafts labels per D-007), reviewer
   Antigravity. How to label one notice × profile: what counts as a criterion, how to cite page
   (PDF index + printed folio), MET / NOT_MET / NEEDS_REVIEW rules with 3 worked examples from real
   corpus PDFs, provenance fields (drafted by / checked by Om / changed?), and a minutes-spent field.
   Write it so Om can check a label without asking anyone.

Peer review as usual, max 3 rounds; log one entry per document (D-029, D-030); one batch ping.

## Previous task (T-002): research open Phase 0 topics for GateCheck — DONE (D-015..D-024, D-028 CLAUDE-OK)

Domain locked: **GateCheck, scope (b)** — see D-014 and the updated CLAUDE.md (Product,
decisions, open topics 6-14). Tenders, OCR and Gujarati are gone.

For each open topic 6-14, the owner from D-002 researches and writes ONE decision-log entry
(D-015 onward): recommendation, 2-3 alternatives with plain-language trade-offs, sources +
dates, and what Om must decide (if anything). Reviewer from D-002 attacks it; max 3 rounds.
Explain every trade-off so a fresh graduate understands it — Om reads these.
Topic 12 must include the synthetic **profile set** design (edge cases in CLAUDE.md).
Also: find and list 25+ candidate notice PDFs with URLs in a manifest draft
`team/corpus-candidates.md` (URL, issuer, year, pages if known) — do NOT download into git.
No code. Batch-ping Claude when entries are AGREED (one ping for many entries).

## Previous task (T-001): find a better project domain — DONE, locked in D-014

Om finds government tenders uninteresting and hard to remember. Find a domain a 22-year-old CS
grad (job hunting for ML/GenAI Engineer roles in India, GATE aspirant) finds genuinely interesting.
Om: "push this project to the limit, as real-world as possible"; completing it is the main goal.

**Hard requirements (reject any idea that fails one):**
1. Data readily available now: public, downloadable, legal to use, enough for 25+ labelled examples.
2. Verifiable ground truth: Om (English, no domain expertise) can check labels, or they are
   mechanically checkable.
3. Keeps the differentiator from CLAUDE.md: multi-step LLM pipeline with structured output,
   per-step tracing + cost/limits, labelled eval with precision/recall + regression suite,
   MCP server, web demo. The document shape may change.
4. A real user with a real decision; fits Om's ₹0 budget (Gemini free tier / local model).

**Seed ideas from Claude (beat them if you can):** eligibility checker for PSU-via-GATE
recruitment notices / M.Tech-PhD admission brochures / NSP scholarships (student profile →
eligible / not / needs review with page cites); syllabus-coverage checker (syllabus vs notes or
papers → gap report). Brainstorm widely beyond these — careers, learning, tech, games, sports,
open-source, research papers, anything.

**Method:** each of you brainstorms and web-researches independently first (no copying), then
swap lists and attack each other's ideas against the 4 requirements. Keep the top 3.

**Output:** one decision-log entry per finalist (D-010..D-012): idea, user, data sources with URLs
+ how many documents exist, ground-truth plan, what the pipeline steps become, why it is
interesting, risks. Plus D-013: your joint ranking with reasons. Mark AGREED, then the one batch
ping to Claude. Om picks the domain; do not start other work until then.

## Previous task (T-000) — done, Claude review deferred until the domain is chosen: who is best at what, and the work split

1. **Deep web research** (split it: Antigravity researches OpenCode's model + Claude; OpenCode
   researches Gemini 3.8 Flash + Claude — each checks the *other's* strengths, not its own).
   First identify the real model behind OpenCode's `opencode/big-pickle`. Compare on this project's
   jobs: web research, reading long PDFs, OCR / scanned Gujarati, Python coding, writing tests,
   code review, planning. Use public benchmarks, model cards, docs, and plan quotas (Google AI Pro,
   OpenCode Zen free tier, Claude Pro $20 — Claude is the scarcest).
2. **Agree the split** of Phase 0 topics 5–14 (CLAUDE.md) and of Phases 1–7 roles. Planning is
   already decided by Om — see "Plan workflow" above; do not re-open it.
   Already agreed in kickoff (re-open only with evidence): topic 6 = OpenCode builds the benchmark
   harness + evidence, Antigravity judges Gujarati/scanned quality; topic 13 gated on topic 6's OCR
   choice; Om code walkthrough = full coverage, teach-then-retest (Antigravity has not reviewed this yet).
3. **Output:** `TEAM.md` at the repo root (capability table with sources + ownership table:
   owner + reviewer per topic/phase), plus decision-log entries: D-001 capabilities, D-002 work
   split, and one `OM-DECIDES` entry each for code ownership, git / OneDrive move, and who drafts
   labels given the different-vendor rule. Antigravity drafts `TEAM.md` first; OpenCode reviews;
   then alternate. Create the `team/` folder and `team/decision-log.md` if missing.
4. **Done signal:** entries marked AGREED + the one batch message to Claude (see Decision log).
