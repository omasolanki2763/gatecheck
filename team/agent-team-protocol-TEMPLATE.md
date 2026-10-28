---
name: agent-team-protocol
description: Portable protocol for a 3-agent team (Claude Code + Antigravity + OpenCode) coordinated through the Orca CLI — roles, messaging, decision log, review, pause/resume. Copy into any project.
topic: orchestration
version: 1 (drafted by Claude 2026-09-29; reviewed by Antigravity + OpenCode — see bottom)
---

# Agent team protocol — reusable template

Built and battle-tested in the *Agentic Document Workflow* project (Sept 2026). Copy this file
into a new project, fill the `{{PLACEHOLDERS}}`, and the agents will not need to reinvent how to
work together.

`{{PROJECT}}` project name · `{{OWNER}}` the human (decides everything) ·
`{{RUN_ID}}` Claude's Orca inbox (created in setup step 2) ·
`{{HANDLE_*}}` terminal handles (found with `orca terminal list --json`, change on restart).

---

## 1. Roles (default — change per project if needed)

| Who | Role | Why |
|---|---|---|
| **{{OWNER}}** | Decides. Anything the agents cannot agree on goes to them as two written positions. | Human owns the project. |
| **Antigravity** (Gemini) | **Peer**: researches, drafts, reviews OpenCode's work. | A second opinion from a different model family. |
| **OpenCode** | **Peer**: researches, drafts, runs commands and tests to gather evidence, reviews Antigravity's work. | Executes commands and tests directly, so claims get checked rather than argued. |
| **Claude Code** | **Planner + final reviewer**: drafts the plan with the owner; reviews only *agreed* decisions. | Tightest budget (Claude Pro) — so it never does routine chat or coordination loops. |

Peers are **equal** — neither is the boss. They argue with each other directly; Claude only sees
outcomes.

The *Why* column states the structural reason each role exists, not a benchmark of any tool. Re-derive
the split for your own setup; do not inherit speed or quality claims about specific vendors.

## 2. One-time setup in a new project

1. Open the project in Orca with three agent terminals in the same workspace (Claude Code,
   Antigravity CLI `agy`, OpenCode). **Reuse these terminals** — do not spawn new agents with
   `orca orchestration worker-start --agent ...` when they already exist.
2. Claude creates its inbox: `orca orchestration run-create --objective "{{PROJECT}} team" --json`
   → copy `result.run.id` into `{{RUN_ID}}` below.
3. Copy this file to `.claude/rules/team-protocol.md` and fill every placeholder.
4. Create `team/decision-log.md` (UTF-8, **no BOM**) with a one-line header pointing to §6.
5. Pointer files so each agent loads the protocol at session start (pointer only, no copied rules):
   - Claude Code: a line in `CLAUDE.md` → "`.claude/rules/team-protocol.md` is authoritative".
     (`.claude/rules/*.md` is also auto-loaded.)
   - OpenCode: `AGENTS.md` at repo root. **It shadows `CLAUDE.md` for OpenCode** (first match wins,
     no merge), so the pointer must say "read `.claude/rules/team-protocol.md`, then `CLAUDE.md`".
   - Antigravity CLI (`agy`): auto-loads `AGENTS.md` and `GEMINI.md` (and `.agents/rules/*.md`) from
     repo root as directory-based rules (up to 24 KB). A single `AGENTS.md` pointer file at the repo
     root satisfies both OpenCode and Antigravity.
6. Kick off each agent by typing into its terminal (see §4 "wake"): "Read
   .claude/rules/team-protocol.md fully and follow it. Current task: ...".

## 3. Resuming a session (every agent, every time)

1. Read this protocol, then `CLAUDE.md`, then only the **last ~5 entries** of the decision log.
2. Handles change on restart: `orca terminal list --json` → match `agentIdentity`
   (`antigravity`, `opencode`, `claude`) **PLUS** `worktreePath` (critical: multiple terminals often
   exist across different projects in the list). Update the table in §4 if they changed.
3. Tell your peer you are back, with your current handle.
4. Claude additionally: `orca orchestration check --run {{RUN_ID}} --json` first (unacknowledged
   messages replay), then restart its background watcher (§8).
5. If this file and an agent's memory disagree, **this file wins**.

## 4. Messaging (Orca CLI)

| Agent | Handle |
|---|---|
| Antigravity | `{{HANDLE_ANTIGRAVITY}}` |
| OpenCode | `{{HANDLE_OPENCODE}}` |
| Claude Code | inbox `run:{{RUN_ID}}` |

- **Send to peer:** `orca orchestration send --to <handle> --type status --subject "<s>" --body "<b>"`
  *(Do NOT specify `--run` on peer-to-peer sends; Orca will reject it with a Run mismatch error if the recipient terminal belongs to another run).*
- **Send to Claude:** `orca orchestration send --to run:{{RUN_ID}} --type status --subject "<s>" --body "<b>"`
  *(Note: `{{RUN_ID}}` already starts with `run_`, so `run:{{RUN_ID}}` produces `run:run_...` — this doubled "run" is intentional in Orca syntax).*
- **Wake peer:** `orca terminal send --terminal <RECIPIENT_HANDLE> --text "New message: run orca orchestration check --terminal <RECIPIENT_HANDLE> --json" --enter`
  *(Always use the recipient's handle so they check their own inbox. Optional flags: `--interrupt`; and `--wait-submit <seconds>`, which asks the provider to confirm the input was submitted. **Do not rely on `--wait-submit`.** Older hosts accept the flag and still answer `provider: unsupported / delivery observation: unsupported`, so "not confirmed" means *unknown*, not *failed*. Check the recipient's inbox rather than resending, or you will double-post.)*
- **Read own inbox:** `orca orchestration check --terminal <YOUR_HANDLE> --json`
- **Inbox reads are batched, never filtered:** `--types` is only the *wake* condition for `--wait`; a
  returned delivery is always the whole FIFO batch. A bound run **replays the same delivery until it is
  acknowledged**, so read every message in the batch *before* you `--ack <delivery_id>` — acking a batch
  acks all of it, and an unprocessed message is then gone.
- **Valid message types:** `status`, `dispatch`, `worker_done`, `merge_ready`, `escalation`, `handoff`, `decision_gate`, `question`, `heartbeat`. (Use `handoff` for the §9 pause ritual).
- **Non-durable peer mail warning:** Mail sent to a bare terminal handle (`legacy_handle`) is live-terminal only and is **lost** if that terminal exits or restarts. Anything that must survive across session restarts belongs in a run inbox (`run:<id>`).

**Who messages whom**
- Peer ↔ peer: free, as needed, **one message per review round, all points batched, < ~200 words**.
- Peer → Claude: strictly limited to (a) one **batch** "Log ready: D-0xx..D-0yy" ping when entries reach AGREED, or (b) an `escalation` with exact error text when comms break. Every message wakes Claude and incurs a full context re-read. **Never send status reports or interim findings to Claude**; put findings in the decision log.
- Claude → peer: only after a review ("D-0xx CLAUDE-ISSUES, see log") or a new task.

## 5. Review rules

- Every artifact is reviewed by the other peer. Reply per point **ACCEPT** (what changes) or
  **DEFEND** (concrete reason). Agreeing just to be agreeable is a failure of the reviewer's job.
- **Max 3 rounds per item**; still unresolved → status `OM-DECIDES` with both positions.
- Facts need a source URL + date, else mark **UNVERIFIED**. Never write a guessed URL; fetch-verify every URL and record the verification date.
- One agent edits a given file at a time; pass the turn explicitly ("file X is yours"). The decision log
  is the shared exception — both peers append, under the announce-then-append discipline in §6.

## 6. Decision log — the only channel to Claude

Chat stays in Orca; the log holds **outcomes only**, so Claude reads a few lines instead of the
whole conversation. Append at the bottom; never rewrite another entry except Status/review lines.

```
### D-001 — <short title>
- Status: PROPOSED
- Owner: <agent> · Reviewer: <other agent>
- Decision: <1-3 lines>
- Why: <reasoning, source URL + date or UNVERIFIED>
- Alternatives rejected: <option — why not>
- Peer review: <rounds, what changed>
- Claude review: (empty — Claude fills this)
```

Status flow: `PROPOSED` → `AGREED` (peer accepted) → Claude sets `CLAUDE-OK` or
`CLAUDE-ISSUES: <points>` → owner fixes, peer re-reviews, `AGREED` again.
Other statuses: `OM-DECIDES`, `DECIDED-BY-OM`.

**Shared log discipline:**
- Re-read the tail of `team/decision-log.md` immediately before appending, and announce the ID you are claiming in peer chat to prevent concurrent write collisions.
- **Handoff notes must NOT consume `D-xxx` decision numbers.** Use `### Handoff — <agent> (<date>)` format instead. This prevents ID collisions and numbering gaps when both peers pause concurrently.

## 7. Planning and task format

- **Plan:** owner + Claude draft `PLAN.md` → peers review and fix it via the log → Claude's final
  gate: no major flaw ⇒ `CLAUDE-OK` ⇒ implement.
- **Task section** (in the project's protocol copy, "Current task (T-00x)"): goal, hard
  requirements, method, output (which log entries / files), done signal. Keep finished tasks
  below as "Previous task" for history.

## 8. Claude's side (cost rules)

- Background watcher, restarted when it ends (Claude Code's shell tool caps one command at 10 min,
  so keep `--timeout-ms` ≤ 590000; the ending is a checkpoint, not a failure):
  `orca orchestration check --run {{RUN_ID}} --wait --types "status,question,escalation" --timeout-ms 590000 --json`
- On a ping: read **only** the named entries (grep headings, then read with offset/limit), write
  the `Claude review` line, acknowledge via `orca orchestration check --run {{RUN_ID}} --ack <delivery_id> ...`, and wake the owner if issues.
- Never run multi-round critique itself — that is the peers' job.

## 9. Pause / resume ritual

- **Pause:** owner tells Claude "pause"; Claude sends each peer: "finish current step, write a
  handoff note (done / next / blockers) using `### Handoff — <agent> (<date>)`, tell your peer via type `handoff`, stop." Wait ~1 min before closing.
- **Resume:** owner types "resume" in each terminal; everyone follows §3.

## 10. Pitfalls we hit (so you don't)

- **Windows PowerShell 5.1 argument quoting:** PowerShell strips or mangles `"` inside native CLI arguments. For long or structured messages, write the text to a file and read it (`$b = Get-Content -Raw msg.txt; orca orchestration send ... --body $b`), **but the file-read trick does NOT make `"` safe — the body text itself must contain no double quotes** (Orca splits the argument at the `"` and dies with `Unknown command`). `--body-file` does not exist and `pwsh` is not installed on this host; keep `"` out of the text or use Python.
- **PowerShell strips quotes in `--payload` JSON:** prefer `--task-id`, `--dispatch-id`, etc. over raw JSON payloads.
- **Peer send `--run` mismatch error:** Passing `--run <run_id>` on peer-to-peer sends fails with `<handle> belongs to Run X, not explicitly requested Run Y`. Omit `--run` on peer terminal sends.
- **Terminal handle collisions across workspaces:** Always match `agentIdentity` PLUS `worktreePath` in `orca terminal list --json`; matching identity alone will pick terminals from other projects.
- **Claude communication drift:** Agents drift into sending "urgent" status updates to Claude. Urgency is not an exception. Claude Pro budget is scarce. Findings go into the decision log; Claude receives only batch "Log ready" pings or blocking escalations.
- **Decision log append races:** Two agents appending simultaneously will collide. Announce the ID in peer chat before writing, and re-read the file tail.
- **Handoff ID collisions:** Decouple handoff notes from `D-xxx` numbers to avoid colliding when pausing together.
- **Non-ASCII encoding (UTF-8 no BOM):** Non-ASCII characters (₹, —, →) inside PowerShell commands can corrupt parsing. Append to files with an explicit UTF-8 editor, never PowerShell `Add-Content`.
- **Guessed document URLs 404:** Never write a guessed URL into a manifest or doc. Fetch-verify every URL and record the verification date.
- **`worker-start` timeouts vs terminal reuse:** `worker-start` against existing interactive terminals can time out at `agent_readiness`. Reuse active terminals via `orca terminal send`.
- **Antigravity must be signed in** before any task (`agent_prompt_blocked` otherwise).
- **Context size management:** Compact agent context (e.g. `/compact` in OpenCode) between tasks, not mid-step.
- **OneDrive file locks:** OneDrive sync delays cause file access locks during concurrent operations; prefer a local git repository outside OneDrive.

---
## Review record (peers fill in)
- Antigravity review: ACCEPTED with fixes applied (2026-09-29; filled `{{ANTIGRAVITY_AUTOLOAD}}`, fixed peer `--run` bug, added `worktreePath` matching, documented Claude status discipline, decoupled handoffs from D-xxx IDs, added PowerShell file-read workaround and missing CLI flags).
- OpenCode review: ACCEPTED with fixes applied (2026-09-29; verified every Orca command and flag against
  the live CLI rather than the docs alone; removed unsourced vendor speed claims from the §1 role table;
  corrected `--wait-submit`, which this host accepts but answers `provider: unsupported`; documented that
  `--types` does not filter a returned delivery and that acking a batch acks every message in it; logged
  the `D-026` collision as a one-round DEFEND → `D-027`).
