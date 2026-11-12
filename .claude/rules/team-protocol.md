---
name: team-protocol
description: How Antigravity, OpenCode and Claude Code work together on this project (roles, dynamic handles, evidence debate, messaging, context management)
topic: orchestration
updated: 2026-11-12
---

# Team protocol

Set by Om. Governs orchestration, roles, peer review, and communication for GateCheck.

## Roles

- **Antigravity** (Gemini 3.8 Flash, Google AI Pro) and **OpenCode** are **equal peers**. Both research,
  both may draft non-critical work, and each reviews the other's work. Reviews follow a logical debate
  of facts between equals. Neither is the boss.
- **Claude Code = PLANNER + REVIEWER OF CRITICAL WORK.** Turns agreed architecture into `PLAN.md` / `DECISIONS.md`,
  reviews all critical deliverables (schemas, eligibility arithmetic, verdict logic, CI config, secrets),
  and resolves pure-judgement deadlocks. Messages to Claude are strictly for critical reviews, handshake/handoff status,
  and escalations.
- **Om = END-RESULT JUDGE.** Evaluates only the finished product; removed from intermediate reviews, approvals,
  and day-to-day gates. Om walks through modules after completion for deep interview defensibility.

## Resuming in a new session (do this first, every time)

Terminal handles **change whenever a terminal or session is restarted**. At the start of every new session:

1. Read this whole file, then `CLAUDE.md`, then the **last ~5 entries** of `team/decision-log.md`
   (not the whole log) to see where work stopped. Check `docs/WORKFLOW.md` for task sequence.
2. Find the live handles dynamically: `orca terminal list --json` → match each terminal's `agentIdentity`
   (`antigravity`, `opencode`, `claude`) and `worktreePath` (`C:/Users/omsol/dev/gatecheck`).
3. Tell your peer you are back with your current handle (send + wake, steps 1-2 below). Include your context percentage.
4. Claude's inbox is `run:run_f4a5b3f23883`. If a send to it fails with an unknown-run error,
   send an escalation to Om in your own terminal output and wait — Claude will create a new run
   and update this file.
5. If this file and your memory disagree, **this file wins**.

## Talking to each other (peer to peer)

Terminal handles are discovered dynamically via `orca terminal list --json` (matching `agentIdentity` and `worktreePath`).

1. **Send:** `orca orchestration send --to <OTHER handle> --type status --subject "<subject>" --body "<text>"`
   (NO `--run` on peer sends — rejected with a Run mismatch; no double quotes inside the body).
   Always report your context percentage in status messages (e.g., `Context: ~15 pct`).
2. **Wake:** The other agent only reads when prompted. Wake it after sending:
   `orca terminal send --terminal <OTHER handle> --text "New peer message: run orca orchestration check --terminal <OTHER handle> --json" --enter`
3. **Wake gotchas:** If `orca terminal send` returns `agent_prompt_blocked`, send `--text` and `--enter` as two separate calls:
   - `orca terminal send --terminal <OTHER handle> --text "New peer message: run orca orchestration check --terminal <OTHER handle> --json"`
   - `orca terminal send --terminal <OTHER handle> --enter`
4. **Git Bash / MSYS note:** When running Orca CLI commands from Git Bash or MSYS, set `MSYS_NO_PATHCONV=1` (or prepend `MSYS_NO_PATHCONV=1`)
   to prevent Git Bash from mangling flag arguments containing slashes or colons (such as `run:run_...` or Windows paths).
5. **Check:** Read your own messages: `orca orchestration check --terminal <YOUR handle> --json`
6. **Communication problem** (send/check errors, peer silent >10 min, stuck in an unresolvable loop): send Claude ONE message with the exact error text:
   `orca orchestration send --to run:run_f4a5b3f23883 --type escalation --subject "Comms issue: <short>" --body "<exact error / what happened>"`
   (The warning "live terminal-only mailbox ... not durable" is normal — ignore it.)

## Review rules — Evidence-based debate of facts

- Every artifact and spec is reviewed by the other peer.
- **Debate of facts between equals:** Every finding, objection, or review point must cite concrete evidence
  (command output, documentation URL + date, CI log, test execution result).
- The other side may counter with evidence. Stronger facts win; the wrong side concedes in writing.
- **No round limit:** Iterate until no doubt is left.
- In the event of a pure-judgement deadlock: Claude Code decides, and both positions are logged in `team/decision-log.md`.
- Facts need a source URL + date; otherwise mark **UNVERIFIED**.

## Context management (50% rule)

- Context percentage must be reported in every status message (e.g., `Context: ~20 pct`).
- If context consumption reaches or exceeds **50%**: commit current changes, push the branch,
  send a `Handoff-context` status message to peer/planner with exact state and next actions, and stop so a fresh session can take over cleanly.

## Git workflow, commits, and CI

- Work is partitioned onto task branches (`task/<name>`). No simultaneous editing of the same files.
- Before committing: ensure `git config --local user.email` is set to `251193805+omasolanki2763@users.noreply.github.com`.
- Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `refactor:`, `chore:`).
- One Conventional Commit per file. No `Co-Authored-By` lines.
- Linear history: Rebase merge only (`gh pr merge --rebase`).
- Pull requests require green CI on both `ubuntu-latest` and `windows-latest` before merge.

## Decision log — the channel to Claude

Every decision or judgement made goes into `team/decision-log.md` as one entry.
Chat stays peer-to-peer in Orca; the log holds only outcomes. Append new entries at the bottom;
never rewrite another entry except its Status / review lines.

```
### D-001 — <short title>
- Status: PROPOSED
- Owner: <agent> · Reviewer: <other agent>
- Decision: <1-3 lines>
- Why: <reasoning, with source URL + date or UNVERIFIED>
- Alternatives rejected: <option — why not>
- Peer review: <1-2 lines: evidence, what changed>
- Claude review: (empty — Claude fills this)
```

Status flow: `PROPOSED` (owner wrote it) → `AGREED` (reviewer accepted via evidence debate) →
Claude sets `CLAUDE-OK` or `CLAUDE-ISSUES: <points>` → on issues, the owner fixes, peer re-reviews,
sets `AGREED` again. Pure-judgement deadlocks → `CLAUDE-DECIDES` with both positions.

Notify Claude **once per batch**, not per entry, when one or more entries reach AGREED:
`orca orchestration send --to run:run_f4a5b3f23883 --type status --subject "Log ready: D-00x..D-00y" --body "AGREED entries ready for review"`
Claude replies by writing into the entry's `Claude review` line and wakes the entry's owner.

## Current task and workflow tracking

Tasks are dispatched by Claude in Orca using the spec format from `CLAUDE.md` and tracked sequentially in `docs/WORKFLOW.md`. Historical task records (T-000 through T-005) are preserved in `team/decision-log.md`.
