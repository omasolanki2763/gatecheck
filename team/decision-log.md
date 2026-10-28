# Team decision log

Channel to Claude Code (planner + final reviewer). Peer chat happens in Orca; this file holds
outcomes only. Append at the bottom. Never rewrite another entry except its Status / review
lines. One agent edits this file at a time (OneDrive, not git).

Format per `team-protocol.md`. Status: PROPOSED → AGREED → CLAUDE-OK | CLAUDE-ISSUES | OM-DECIDES.
All sources checked 2026-09-27 unless a different date is given.

---

### D-001 — Capability table: what each agent is actually good at
- Status: AGREED
- Owner: OpenCode · Reviewer: Antigravity
- Decision: Build the capability table from measured evidence, not self-report. Three rows:
  Antigravity = Gemini 3.8 Flash (Medium) on Google AI Pro; OpenCode = `opencode/big-pickle`
  (model UNIDENTIFIED, see below); Claude Code = Claude Opus 5 / Sonnet 5 on Claude Pro $20.
- Why:

  **Antigravity — Gemini 3.8 Flash.** GA 2026-09-02. 1,048,576 in / 65,536 out tokens. Accepts
  Text, Image, Video, Audio **and PDF** natively — the only one of the three with declared
  image+PDF input. <https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash>
  Google names Gemini 3.8 Flash as the default model for the Antigravity agent and Antigravity
  SDK, which independently confirms Antigravity's own model string.
  <https://ai.google.dev/gemini-api/docs/latest-model> (2026-09-23). Antigravity self-reports
  "Gemini 3.8 Flash (Medium) under Google AI Pro" — consistent.
  Benchmarks that matter to us (Google model card, 2026-09-02,
  <https://deepmind.google/models/model-cards/gemini-3-8-flash/>): GDP.PDF Expert PDF
  comprehension 35.0%; Terminal-bench 2.1 agentic terminal coding 89.4%; HLE-Verified 54.9%;
  Terminal-bench 4.0 general agentic 19.1%.
  Independent (Artificial Analysis, <https://artificialanalysis.ai/models/releases/gemini-3-8-flash>):
  Intelligence Index 59, rank 17/196; Agentic Index 50.0 (up from 45.1 on 3.7 Flash); Coding Index
  76.3 (flat, +0.2 = noise); output 299 tok/s, rank 3/196; time-to-first-token 13.2 s (1.2 s
  *worse* than 3.7 Flash). LMArena text 1494 ±9, rank 8, preliminary.
  **Caveat we must not hide:** 3.8 Flash is a post-training update on 3.7 Flash, not a new
  pretraining run; knowledge cutoff stays March 2026. And Google's own card reports safety
  performance **across non-English languages regressed** vs 3.7 Flash (multilingual safety
  +5.4pp, lower-is-better). That is the only non-English signal Google publishes, and it is the
  one that matters most for a Gujarati-heavy corpus. Not proof of weaker Gujarati OCR, but it is
  the opposite of reassurance.

  **OpenCode — `big-pickle`. The real model cannot be identified, and that is the finding.**
  OpenCode Zen lists exactly one curated model, `big-pickle`, at an OpenAI-compatible endpoint
  (<https://opencode.ai/docs/zen/>). models.dev lists it as provider-specific, 200,000 context,
  32,000 output, $0.00/$0.00, reasoning + tool calls + structured output declared, and **no image,
  audio or video modality** (<https://models.dev/providers/opencode>). Third parties describe it as
  a deliberate *stealth* model with *rotating* backends
  (<https://github.com/agent0ai/agent-zero/issues/1302>; r/opencodeCLI). So: **UNVERIFIED which
  vendor model is behind it, by design, and it can change without notice.** Consequences we accept:
  (a) any capability claim about "OpenCode" is a claim about *today's* routing, not a model;
  (b) nothing in the README may name a model for the agent's own output; (c) nothing in the
  product may depend on big-pickle's identity. Antigravity's "community consensus points to
  DeepSeek-Coder / Qwen-2.5-Coder / GLM" is **UNVERIFIED** — no source, and it contradicts the
  rotating-backends framing, so treat it as folklore.
  Antigravity's "zero multimodal vision for Gujarati scans" is **partly confirmed**: no image
  modality is declared, so it cannot be relied on to read a scanned page. Declared-absent is not
  the same as proven-absent, so we log it as "no declared image input".

  **Claude Code — Claude Opus 5 / Sonnet 5 on Pro $20.** Strongest raw scores of the three where
  reasoning and planning matter: GDP.PDF Expert 37.0% (best of the three), Terminal-bench 4.0
  51.8% (vs Gemini 3.8 Flash's 19.1% — a very large gap on general agentic work), HLE-Verified
  54.4%, LMArena Fable 5 1507 / Opus 4.6 High 1505 / Opus 4.7 High 1502 (all above Gemini 3.8
  Flash's 1494). Source: Google model card table + codersera/usingclaude, 2026-09.
  Budget is the binding constraint, not capability. Pro has **three** limits, not one: a rolling
  5-hour session window, a weekly cap, and a *separate* weekly Opus cap
  (<https://support.claude.com/en/articles/9797557-usage-limit-best-practices>,
  <https://claude.com/pricing>). Anthropic's own illustration is ~45 messages per 5 hours on a
  light model with short chats. Claude Code 5-hour limits were permanently doubled 2026-05-06;
  from 2026-09-14 weekly limits settle at a permanent +25% over the pre-July baseline.
  Third-party estimate (<https://continuumcode.ai/guides/claude-pro-usage-limit/>, 2026-08):
  Sonnet small tasks ~2-3 h/day, large repo exploration ~1 h, Opus often under 1 h with the Opus
  cap arriving first, and **"agent teams in plan mode" roughly one seventh of that** — treat as
  UNVERIFIED but directionally clear. Antigravity's "~45 msgs dropping to 10-20 at 100k+ context"
  is plausible and consistent but is **UNVERIFIED** (no Anthropic source states it).

  Net capability read for this project: Claude is the best planner/reviewer; Gemini 3.8 Flash is
  the only agent that can *see* a scanned Gujarati page and is near-frontier on agentic coding;
  big-pickle is a free, fast, tool-heavy worker that is blind to images and unstable underneath.
- Alternatives rejected:
  - Benchmarking the three head-to-head on our own tender PDFs — rejected for now: costs money,
    needs a labelled set we do not have yet, and Phase 0 forbids code. Revisit in Phase 5.
  - Relying on vendor launch benchmarks alone — rejected; every launch number here is
    self-reported and the independent runs already disagree (Terminal-bench 2.1: Google 89.4%,
    Artificial Analysis 87.6%, vals.ai 81.27% — a 8-point spread between runs both treat as
    independent).
- Peer review: 1 round. Antigravity: ACCEPT — "concur with UNVERIFIED flags; capability evidence
  is solid and fair." Antigravity's own Claude research matched ours on every number except the
  unsourced ~10-20 messages at 100k+ context, which stays UNVERIFIED. No change to the decision.
- Claude review: (empty — Claude fills this)

---

### D-002 — Work split: Phase 0 topics 5-14 and Phases 1-7
- Status: AGREED
- Owner: OpenCode · Reviewer: Antigravity
- Decision: Split by measured strength, not by seniority. Every topic has one owner and one
  reviewer, and neither role is permanent across phases.

  **Phase 0 topics (CLAUDE.md):**

  | # | Topic | Owner | Reviewer |
  |---|---|---|---|
  | 5 | LLM choice | Antigravity | **OpenCode** (primary; it lives on the quota) |
  | 6 | PDF parsing / OCR | OpenCode (harness + measured evidence) | Antigravity (Gujarati/scanned quality) |
  | 7 | chunking / locating criteria | OpenCode | Antigravity |
  | 8 | structured output + validation | Antigravity | OpenCode |
  | 9 | hand-written loop vs LangGraph | Antigravity | OpenCode |
  | 10 | tracing (Langfuse vs own JSONL/SQLite) | OpenCode | Antigravity |
  | 11 | storage | OpenCode | Antigravity |
  | 12 | company-profile + memo schemas | Antigravity | OpenCode |
  | 13 | web framework + deploy (gated on 6) | Antigravity | OpenCode (key exposure, upload cap, visible trace) |
  | 14 | testing without spending money per run | OpenCode | Antigravity |

  Topic 5 review sits with OpenCode because Antigravity runs on the leading candidate; a model
  reviewing its own vendor is the exact conflict CLAUDE.md already avoids for the labeller. This
  supersedes my kickoff listing of 5 as review-only.

  **Phases 1-7:** P1 ingestion OpenCode implements / Antigravity reviews · P2 extraction
  Antigravity drafts prompt + schema / OpenCode reviews · P3 checking + memo OpenCode implements
  the Python arithmetic / Antigravity reviews + drafts the memo prompt · P4 observability OpenCode
  (traces, cost, timeouts, retries, limits, tests) / Antigravity reviews · P5 evaluation OpenCode
  builds the runner / Antigravity judges output quality · P6 MCP Antigravity / OpenCode reviews
  key handling and logging · P7 web demo Antigravity / OpenCode reviews. **Claude Code owns
  PLAN.md, DECISIONS.md, the Om interview output, and final review of AGREED entries — nothing
  else**, because its budget is the scarcest of the three.

  Already locked in kickoff, re-opened only with evidence: topic 6 split; topic 13 gated on
  topic 6's OCR choice; Om code walkthrough = full coverage, teach-then-retest. Antigravity has
  not yet reviewed the walkthrough rule.
- Why: D-001. The split follows the two facts that actually constrain us — only Gemini can read
  a scanned page, and only Claude is rationed enough that it must not do routine work.
- Alternatives rejected:
  - Splitting by topic number (first half / second half) — rejected, it ignores the capability
    evidence that is the entire point of D-001.
  - Giving Claude the implementation work — rejected: Opus drains Pro fastest and hits its own
    weekly cap first; every hour Claude spends coding is an hour not spent reviewing.
- Peer review: 1 round. Antigravity: ACCEPT — "work split matches measured strengths and our
  TEAM.md matrix." Round 2 found `TEAM.md` disagreeing with this entry on two rows (topic 5 owner,
  Phase 3 roles); both were raised in **D-008**, both accepted by Antigravity, and `TEAM.md` now
  matches this entry. Final state: 2 rounds, 0 items unresolved.
- Claude review: (empty — Claude fills this)

---

### D-003 — Add Sarvam Vision 2.1 to the topic 6 OCR candidate set
- Status: AGREED
- Owner: OpenCode · Reviewer: Antigravity
- Decision: Topic 6 must benchmark at least Sarvam Vision 2.1 alongside Gemini's own PDF input
  path, Tesseract with `guj` traineddata, and one commercial OCR API. Do not assume Gemini wins
  because Antigravity runs on it.
- Why: On Sarvam's Indic OCR bench (6,909 samples, 22 Indian languages + English; vendor-run, so
  treat the absolute numbers with care — <https://www.sarvam.ai/blogs/sarvam-vision-2-1>,
  2026-09-24) the **Gujarati** column reads: Sarvam Vision 2.1 **88.87**, Gemini 3.6 Flash 83.68,
  Bodhan Indic-OCR 83.26, **Claude Opus 5 70.92**, GPT 6 Astra 70.71, Gemma 4 70.68, Mistral
  OCR4 68.19, Surya OCR 2 65.80, Google Cloud Vision 64.40, Chandra-OCR2 59.14, Infinity-Parser2
  Pro 48.09, Azure Vision 4.0 11.79, AWS Textract 10.01. Overall: Sarvam 87.39, Bodhan 84.94,
  Gemini 3.6 Flash 79.35, Opus 5 68.81.
  Three things follow. (1) Claude Opus 5 — the strongest reasoner of our three agents — is
  **worse than Gemini on Gujarati OCR**. This vindicates the existing rule that the pipeline LLM
  must not be Claude, and it means Antigravity is not a conflicted judge of Gujarati quality: it
  is judging on the strongest mainstream option. (2) The two candidates that beat Gemini are
  India-focused (Sarvam, Bodhan), which is exactly the pattern you would expect and exactly why
  a general-purpose model should not be assumed sufficient. (3) **This bench scores Gemini 3.6
  Flash, not 3.8 Flash** — extrapolating 3.6 → 3.8 is an inference, UNVERIFIED.
  A second, independent signal points the same way but disagrees on absolutes: IndicVisionBench
  (ICLR 2026, <https://arxiv.org/html/2511.04727>) reports leading-model Gujarati ANLS of only
  24.09, versus Sarvam's 88.87. Different corpora (Wikisource scans, printed + handwritten) and
  different metrics, so the two numbers are **not comparable**; the usable fact is the ordering,
  not the value. Tesseract is viable for Gujarati only via the `guj` traineddata pack
  (<https://docs.cloud.google.com/vision/docs/languages> lists Gujarati `gu`; Cloud Vision's
  Gujarati row is 64.40 on the Sarvam bench, so a classical OCR floor exists to beat).
- Alternatives rejected:
  - Gemini-only OCR, because it is already available — rejected: it is the most
    conflict-of-interest-shaped choice available and the bench says India-focused models beat it.
  - Deciding topic 6's answer now — rejected; the numbers are vendor-run and from a different
    model version. We benchmark on our own pages before choosing.
- Peer review: 1 round. Antigravity: ACCEPT, and answered the conflict-of-interest objection
  directly — no objection provided evaluation is **blinded** (transcripts presented as Candidate
  A/B/C/D with no model names, scored against PDF ground truth) and the Commander decides the
  final selection. Blinding is now a condition of this entry: a judge who cannot tell which
  candidate is which cannot quietly favour their own vendor.
- Claude review: (empty — Claude fills this)

---

### D-004 — Planning: decided by Om, not reopened
- Status: DECIDED-BY-OM (supersedes the proposal below; recorded for audit only)
- Owner: OpenCode · Reviewer: Antigravity
- Decision: **Om and Claude draft `PLAN.md` together. Antigravity and OpenCode then review it
  peer to peer, fix it, and log every change. Claude gives the final gate** (`CLAUDE-OK` or
  `CLAUDE-ISSUES`). See "Plan workflow" in `.claude/rules/team-protocol.md`, 2026-09-27.
  Antigravity and I proposed Antigravity run the interview instead; **Om overruled us and we do
  not re-open it.** The proposal is kept below only so the reasoning is not silently lost.
- Why (superseded proposal, kept for audit): we argued Claude Pro is the wrong tier for a long
  interactive interview, because its binding constraints are a rolling 5-hour session, a weekly
  cap and a separate weekly Opus cap, and a third-party estimate puts "agent teams in plan mode"
  at roughly one seventh of a single session's headroom
  (<https://continuumcode.ai/guides/claude-pro-usage-limit/>, 2026-08, UNVERIFIED but
  directionally unambiguous). That reasoning did not win, and it is not a criticism of Om's call:
  the interview determines what gets built, so Om owning it directly is defensible on its own
  terms, and Claude-as-planner is the role the protocol already gave it.
- Residual risk we flag for Claude, not as a condition of approval: the interview plus `PLAN.md`
  drafting will consume a large share of Pro's weekly allowance, and the weekly allowance dropped
  to a permanent +25% over the pre-July baseline on 2026-09-14
  (<https://support.claude.com/en/articles/9797557-usage-limit-best-practices>). Two practical
  asks, both compatible with Om's decision: chunk the interview across sittings so a weekly-cap
  hit does not lose it, and keep Claude's later load to the AGREED entries only — which is what
  D-002 already commits us to.
- Alternatives rejected: Antigravity running the interview (rejected by Om); splitting the
  interview across peers (rejected — incoherent plan, doubled context-switching for Om).
- Peer review: 1 round. Antigravity proposed the same thing independently; Om overruled both of
  us. Accepted.
- Claude review: (empty — Claude fills this)

---

### D-005 — OM-DECIDES: how Om owns code the agents write
- Status: OM-DECIDES
- Owner: OpenCode · Reviewer: Antigravity
- Decision: Undecided by design. It is Om's call and it is the single decision that most affects
  whether this portfolio is defensible in an interview. Escalated with both positions and the
  arithmetic.
- Why: CLAUDE.md sets the bar — Om must defend *every* line, not just the architecture. Two
  coherent answers exist and they are not compatible.
  - **Position A — agents write, Om audits per module (~20 min each).** For each file Om answers
    three fixed questions: what breaks if I delete this line; why this library over the
    alternative recorded in `DECISIONS.md`; what the test actually proves. A line he cannot answer
    gets a plain-language note from the owning agent in `DECISIONS.md`, then he re-answers; only a
    *second* failure changes the code. Arithmetic: Phase 1-4 is an estimated 12-18 small
    single-purpose modules x 20 min = 4-6 h against roughly 6 h/week of his time (45 min x 4
    weekdays + 3 h Saturday), so roughly one week. Module count is an **estimate, UNVERIFIED**
    until `PLAN.md` exists. Cheapest, and it front-loads his learning.
  - **Position B — Om writes first, agents write tests and scaffolding.** Maximum defensibility,
    maximum Om time. At 12-18 modules this likely does not fit Phase 1-4 dates at all.
  - Shared ground both positions accept: full coverage, no module skipped (a skipped module is an
    undefendable module); the owning agent adds a short *why* comment on any line that is not
  self-evident; nothing merges with an unanswered question.
- Alternatives rejected: "he picks which modules to review" — rejected, it silently creates
  undefendable modules, which is the exact failure CLAUDE.md is trying to prevent.
- Peer review: 1 round. Antigravity: ACCEPT — "all trade-offs accurately framed." The gap noted
  in round 1 is now closed: Antigravity has reviewed and does not object to the teach-then-retest
  rule. Both positions stand as written for Om.
- Claude review: (empty — Claude fills this)

---

### D-006 — OM-DECIDES: git repository and the OneDrive move
- Status: OM-DECIDES
- Owner: OpenCode · Reviewer: Antigravity
- Decision: Undecided. Two sub-questions: (a) initialise git here, and (b) whether the repo moves
  out of OneDrive. Both must be settled before the first parallel dispatch, because the team
  protocol's one-editor-at-a-time rule is a *mitigation*, not a fix.
- Why: The folder is not a git repository, so there are no worktrees, no branches, and no
  `git diff main...task/T-XXX` for a reviewer to read — which means the review loop the whole
  protocol depends on cannot run as written. Meanwhile the folder sits inside OneDrive, and
  parallel agents writing there risk sync locks and partial writes. The measured symptom already
  exists: third-party work reports 10-20 usable Claude messages per 5 hours against an
  illustrative 45 (UNVERIFIED).
  - **Position A — `git init` here, dispatch strictly serially.** Fastest, keeps OneDrive backup.
    Cost: no parallelism at all, and two agents still touching OneDrive at different times can
    still collide.
  - **Position B — move the repo to a local path (e.g. `C:\dev\agentic-doc-workflow`), `git init`,
    work normally.** Enables real parallel worktrees and the branch-per-task rule. Cost: Om loses
    OneDrive sync/mobile access, and must move or re-sync by hand.
  - **Position C — `git init` here, serial dispatch until Phase 1 is proven, then revisit the
    move.** Cheapest decision now, with an explicit revisit point.
- Alternatives rejected: staying in OneDrive with parallel worktrees — rejected: two file-lock
  risks stacked (OneDrive *and* git worktrees) is how you lose a day silently.
- Peer review: 1 round. Antigravity: ACCEPT — "all trade-offs accurately framed." No change. Note
  that this blocks nothing in T-000; it must be settled before the first Phase 1 dispatch.
- Claude review: (empty — Claude fills this)

---

### D-007 — OM-DECIDES: who drafts the ground-truth labels
- Status: OM-DECIDES
- Owner: OpenCode · Reviewer: Antigravity
- Decision: Undecided, and the different-vendor rule makes the obvious answers illegal or worse.
- Why: CLAUDE.md already requires the pipeline LLM to be a different vendor from the labeller
  (Claude), to avoid shared blind spots, and that Om checks every label against the PDF while
  recording minutes spent. D-001 shows the vendor question is sharper than it looked.
  - **Position A — Antigravity drafts the labels, Om checks each one.** Keeps the labeller and
    the pipeline on the same vendor, which *violates* the stated rule if the pipeline is Gemini.
    Rejected on the rule, not on quality.
  - **Position B — big-pickle (OpenCode) drafts, Om checks.** Satisfies different-vendor from
    Claude, and costs nothing. But the labeller would then be an unidentifiable rotating model
    (D-001), so labels would be unreproducible: a re-run could give different labels, and Om
    could not point to a model card in an interview. That is a bad property for a portfolio.
  - **Position C — Antigravity drafts, and the pipeline uses a non-Gemini vendor.** Preserves
    different-vendor separation *and* reproducibility (a named model card), at the cost of giving
    up the free Gemini tier that CLAUDE.md currently recommends for the pipeline. This is the
    position we prefer, and it is a direct trade of money for defensibility, so it is Om's call.
  - Note the interaction with D-003: Sarvam Vision 2.1 scores 88.87 on Gujarati against Gemini's
    83.68. If Sarvam wins topic 6, it changes what "the pipeline vendor" even means, so settle
    topic 6 before settling this.
- Alternatives rejected: Claude drafts (Om already reversed this once, and it breaks the
  different-vendor rule outright).
- Peer review: 1 round. Antigravity: ACCEPT — "all trade-offs accurately framed." No change.
- Claude review: (empty — Claude fills this)

---

### D-008 — TEAM.md review round 1: six factual corrections applied, two rows disputed
- Status: AGREED
- Owner: OpenCode · Reviewer: Antigravity
- Decision: Reviewing Antigravity's `TEAM.md` (file turn received in the D-001..D-007 acceptance
  message). I corrected six factual errors in place and logged two rows I would not silently
  overwrite. The corrections are mechanical fixes backed by a source; the two disputed rows are
  genuine differences of opinion and stay open.
- Why — corrections applied (each would have cost credibility in an interview):
  1. **"Claude Opus 5.5" did not exist.** The draft named the engine twice as Opus 5.5. The
     Anthropic lineup is Opus 5 / Sonnet 5 / Haiku 4.5 / Fable 5; models.dev lists `claude-opus-5`.
     Corrected to Opus 5. A fabricated model name in a portfolio artifact is the single most
     damaging kind of error here — it is trivially checkable.
  2. **Claude context was given as 200k.** On Claude Code with Pro/Max/Team/Enterprise, Opus 5 and
     Sonnet 5 support 1M, though Pro must enable usage credits for the 1M window on Opus models
     (<https://support.claude.com/en/articles/8325614-context-window>, checked 2026-09-27).
     Corrected, with the real caveat that *quota* drains faster with a longer window — the window
     was never Claude's binding constraint.
  3. **The `big-pickle` backend was stated as fact.** "Community consensus: DeepSeek-Coder /
     Qwen-2.5-Coder / GLM" appeared unqualified in the capability table despite having no source,
     and it contradicts the same table's own "stealth model" description: a *rotating* backend
     cannot have a fixed three-model list. Replaced with "unknown by design" plus the honest
     implication — capability may change under us, which is a portfolio risk worth stating.
  4. **"Elite" and "Elite & Fast" on OpenCode's row.** Removed. The draft ranked an unidentifiable
     rotating model as elite in the same table where it admits the model is unknown. Unevidenced
     superlatives are the easiest thing for an interviewer to knock down, and D-001 already says we
     cannot rank. Replaced with the specific, defensible strengths: fast at *executing* pytest,
     timing chaos limits, hashing fixtures, mechanical code.
  5. **Antigravity's rate limits were misattributed.** "RPM 15-60, TPM 1M-4M" are Gemini *API* tiers,
     which apply to API keys, not the Antigravity app. The real constraint is the Google AI Pro
     agent quota ($19.99/mo, refreshes every 5h up to a weekly limit, shared across Gemini
     models). Corrected to the constraint that actually bites.
  6. **The Gujarati evidence was missing entirely.** The capability table rated Antigravity
     "moderate to high" and Claude "moderate" with no numbers, despite D-003 resting on the single
     most decision-relevant OCR measurement in this whole task. Replaced with the actual bench
     numbers and the two facts that follow from them: Gemini beats Claude on Gujarati (83.68 vs
     70.92), and an India-focused model (Sarvam 88.87) beats Gemini. The second is why Claude can
     never be the pipeline model.
- Why — rows I did **not** overwrite (logged, not decided):
  1. **Topic 5 owner.** `TEAM.md` gives Claude Code; D-002 gives Antigravity. OpenCode's position:
     Antigravity researches (direct quota knowledge, near-zero cost), Claude decides in its planner
     role, OpenCode reviews with dated pricing. This keeps vendor separation and keeps Claude's
     scarce budget out of research. If Claude owns it outright instead, D-002 must be amended so
     the log and `TEAM.md` agree — an artefact contradicting an AGREED entry is worse than either
     version on its own.
  2. **Phase 3 roles.** `TEAM.md` gives Antigravity the phase with OpenCode reviewing
     "deterministic arithmetic"; D-002 gives OpenCode the arithmetic. OpenCode's position: CLAUDE.md
     already decided arithmetic happens in Python rather than the LLM, so split the phase on that
     line — Antigravity owns the judging logic and memo prompt, OpenCode owns the deterministic
     arithmetic module, each reviewing the other. This matches CLAUDE.md and D-002 simultaneously.
- Alternatives rejected:
  - Accepting `TEAM.md` as drafted — rejected: it contained one non-existent model name and one
    unsourced fixed-backend list, both trivially falsifiable.
  - Rewriting all of `TEAM.md` — rejected: Antigravity drafted it, and the protocol says we
    alternate. Corrected only what evidence forced, and left its structure and its rows intact.
  - Silently editing the two disputed rows to match D-002 — rejected: that is how a log stops being
    the source of truth. Both readings are recorded in both files.
- Peer review: 1 round. Antigravity: **ACCEPT all six corrections** ("evidence is rock-solid") and
  **ACCEPT both disputed rows**, then edited `TEAM.md` itself rather than leaving them logged as
  open: topic 5 owner is now Antigravity-research / OpenCode-review / Claude+Om-decide, and Phase 3
  is now split OpenCode-arithmetic / Antigravity-eval-and-memo with mutual review. Section 6 of
  `TEAM.md` records the resolution. OpenCode verified the edits landed before flipping this to
  AGREED. Total: 2 rounds, 0 items unresolved.
- Claude review: (empty — Claude fills this)

### D-009 — Om's answers (recorded by Claude, 2026-09-27)
- Status: DECIDED-BY-OM
- Owner: Om (via Claude) · Reviewer: —
- Decision:
  - D-005 code ownership: agents write the code; Om does the full walkthrough (every module, 3 questions/file, teach-then-retest) AFTER the project is complete. Priority is completing the project.
  - D-006 git: move the project out of OneDrive + git init. Repo stays PRIVATE until Phase 7.
  - D-007 labels: OpenCode drafts, Om checks (valid only if OpenCode's model is not the pipeline vendor).
  - Pipeline LLM: Gemini free tier; if its quota runs out, a local model (Om's laptop: 16 GB RAM, NVIDIA 6 GB VRAM). API budget: ₹0.
  - Topics 9 (loop vs LangGraph), 10 (tracing), 13 (web UI — whichever looks better): decide after agent research.
  - Non-English text: read it, flag low confidence; Om cannot read Gujarati, so both agents must independently reach the same reading.
  - No fixed deadlines. Om's time is variable.
  - **DOMAIN PIVOT under consideration (T-001):** Om finds tenders uninteresting and hard to remember. Claude's review of D-001..D-003 and D-008 is DEFERRED until the domain is chosen, since D-002/D-003 may change.
- Claude review: n/a

### D-010 — Domain: GateCheck (PSU recruitment + IIT M.Tech admission eligibility screener)
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: Replace the Gujarat-tender domain with admission/recruitment eligibility screening for
  Indian CS graduates. Input = one official English notification or brochure PDF + one candidate
  profile. Output = per-criterion met / not met / unclear with page cite and short quote, plus a
  final APPLY / SKIP / NEEDS REVIEW memo. Pipeline shape is unchanged: extract criteria (structured
  output) → check against profile (deterministic arithmetic in Python, never the LLM) → draft memo.
- Why, requirement 1 (public, legal, downloadable now, 25+ labels). Verified 2026-09-27. The
  corpus is *enumerable*, not scraped-and-hoped:
  - DRDO/RAC numbered advertisement series — one source, English, born-digital: `advt_136`
    (270 vacancies, valid GATE 2017/2018/2019), `advt_137` (167 vacancies, 2020), `advt_140_v2`
    and `advt_140_v3` (630 vacancies, 2022), `advt_152` (Apr 2025, Scientist D/E/F,
    experience-weighted), `advt_156_v2` (152 vacancies, May 2025) plus `advt_156_addendum.pdf`,
    and `advt_157` (published 2026-06-04). DRDO runs a paginated vacancy archive.
    <https://rac.gov.in/download/archive/advt_136.pdf> ·
    <https://drdo.gov.in/drdo/en/offerings/vacancies/archive>
  - BARC / IGCAR OCES-DGFS-2026 brochure (Dec 2025), live cycle: applications 2025-12-22 to
    2026-01-21, exam 2026-03-14/15, interviews 2026-05-12 to 2026-06-12.
    <https://www.barc.gov.in/careers/barc_ts_OCES_DGFS_brochure.pdf>
  - IIT M.Tech brochures: IIT Bombay `MTECH_BROUCHURE2025-26.pdf`, IIT Kharagpur
    `JMP_Brochure_2025_26.pdf` (60+ pages, per-school eligibility), and roughly one per IIT
    across the ~20 IITs running GATE-based PG admissions. IISc COAP 2025 acts as a hub.
    <https://www.iitb.ac.in/newacadhome/MTECH_BROUCHURE2025-26.pdf> ·
    <https://gateoffice.iitkgp.ac.in/jmp/d/docs/JMP_Brochure_2025_26.pdf>
  DRDO/RAC alone plausibly yields 20–40 documents; adding the IITs and BARC clears 50. Antigravity's
  "50+" is optimistic; the required 25+ is safe. All are **born-digital, not scans** — text
  extraction returns clean section numbering and intact tables, so no OCR subsystem is needed at all.
- Why, requirement 2 (ground truth checkable without domain expertise). This is *stronger* than
  "Om can read it": the ground truth is externally verifiable against third-party facts Om already
  holds — GATE scorecard, date of birth, category certificate, CGPA. Verified eligibility surface,
  quoted:
  - IIT Bombay A.5.1, a four-way disjunction with a category branch: GN/EWS/OBC(NC) needs "a
    minimum of 60% marks in aggregate, OR a First Class as specified by the University, OR a
    minimum Cumulative Grade Point Average (CGPA) / CPI of 6.0 on the scale of 0-10, OR an
    equivalent to 6.0 on other corresponding proportional requirements"; SC/ST/PwD needs 55% or
    CGPA 5.5. Per-discipline additions sit in Table A.5.3.
  - IIT Bombay: CGPA ≥ 8.00 (0–10) IIT degree-holders are "exempted from requirement of GATE
    qualification"; A.5.1 is mandatory across all application categories (a)–(e).
  - BARC OCES/DGFS-2026, age as on 2026-08-01: max 26 general / 29 OBC-NCL / 31 SC-ST / 31
    Dep.1984 / 31 DOM-Kashmir, with "extent of disability 40% or more … considered for age
    relaxation" **stacking on top of** the category relaxation; minimum age 18 on the same date.
  - BARC: GATE cutoffs "will be finalized only after the conclusion of the online examination" —
    the document declares its own rule unresolvable at read time. A first-class NEEDS REVIEW case
    that is a property of the source, not a model failure.
  - BARC: applicants who opt for GATE-score-only screening "will NOT be eligible for online exam
    (CBT)" — a cross-criterion dependency that independent per-criterion checking gets wrong.
  - BARC: degree requirements complete by 2026-07-31, but final-year-awaiting-results candidates
    may apply and submit marksheets by 2026-12-31. Two conditions, two different dates.
  - Valid-GATE year windows differ per notification: RAC 136 → 2017/2018/2019; RAC 156 →
    2023/2024/2025; BARC 2026 → 2024/2025/2026. The profile check must be year-aware.
  None of this requires procurement experience or Gujarati.
- Why, requirement 4 (real user, real decision, ₹0). Not rhetorical: Om holds GATE 2026
  scores and faces OCES/DGFS-2026 and DRDO RAC personally. The decision is
  pay-the-fee-or-skip. Gemini free tier covers it, and D-009's "pipeline must not be big-pickle"
  constraint still holds because the pipeline is Gemini.
- The published cutoff matrices are a second, stronger ground-truth source. IITs publish
  machine-readable per-discipline, per-category, PwD-vs-non-PwD GATE cutoff tables — IIT Bombay
  `Minimum_Qual_Cutoff_GATE2025.pdf`, IIT BHU `mtech_admission_through_coap25_gate_cuttoff_scores.pdf`,
  IIT Madras `M.Tech.2025_Cutoff.pdf`, IIT ISM Round 10, IIT Roorkee normalized marks, IISc COAP.
  For the IIT-M.Tech path, "can I actually get in" is therefore a lookup, not an opinion. Two
  document families result: eligibility prose and tables (the LLM extraction target) and numeric
  cutoff matrices (mechanical check). That is a stronger eval story than one family, because prose
  extraction and table extraction get measured separately.
- What this candidate costs, stated plainly rather than buried:
  1. **It is structurally the same three-step pipeline as the tender project.** "Just a re-skin"
     is a fair interviewer objection. The answer cannot be the pitch; it has to be label
     provenance plus the relaxation-arithmetic eval plus the two-family extraction. Nothing else
     rescues this candidate if that answer is unconvincing.
  2. Link rot on ageing PSU sites is real. The brief's manifest approach (URL, download date,
     hash) is the mitigation and is already decided.
  3. Revisions and addenda exist as separate documents (`advt_140_v2`, `advt_140_v3`,
     `advt_156_addendum.pdf`), so amendment handling is a *native* corpus property. CLAUDE.md
     deferred corrigendum handling past Phase 3 — keep that deferral, but record that this corpus
     supplies amendment pairs for free instead of requiring them to be manufactured.
  4. Part of the final decision reduces to a lookup against published cutoffs, which makes that
     part easy. The eligibility-rule half stays genuinely hard, which is why the balance still
     holds — but the memo must not be allowed to collapse into a lookup.
- Peer review: 1 round. Antigravity raised GateCheck as its own candidate; OpenCode independently
  arrived at the same family and supplied the corpus enumeration, the quoted eligibility surface,
  and the two-family framing. Antigravity reviewed the ranking and accepted it (see D-013). Peers recommend Option (a) for the scope question (retain both eligibility and cutoff-matrix families for separate prose/table eval and mechanical ground truth), with Option (b) (eligibility brochures only in Phase 1) flagged for Om if build effort needs staging.
- Claude review: CLAUDE-OK (2026-09-27) — no major flaw; sources concrete, costs stated honestly.
  Carry two conditions into PLAN.md: (1) **Profile set is missing.** Om's own profile is ONE
  profile; eval needs a designed set of synthetic candidate profiles (category, PwD, age-boundary,
  final-year, CGPA-vs-% edge cases) so labels are not all one person's outcomes — owner of topic 12
  must specify it. (2) Section "requirement 2" overstates: the label is "does profile P meet
  criterion C of document D", checked by Om reading the PDF; Om's scorecard only verifies his own
  profile's facts. Word it that way in README. Scope (a) vs (b): Om decides.

### D-011 — Domain: DepRisk (dependency breaking-change evaluator) — ranked 2, not selected
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: Keep on the shortlist as the runner-up. Input = upstream release changelog or migration
  guide plus the consumer codebase. Output = affected call sites, breakage risk, go/no-go on the
  version bump. Evaluation by running the test suite before and after.
- Why it is genuinely strong: it has the **best mechanical ground truth of any candidate we
  considered** — does the suite still pass is boolean, needs zero domain expertise, and has zero
  labelling ambiguity. Requirements 1 and 2 are the cleanest in the whole set, and GitHub release
  notes give unlimited, permanently available data.
- Why it lost, and the reasons are structural, not cosmetic:
  1. **It is not really a document workflow.** The changelog is a document, but the actual work is
     AST analysis, and the LLM contributes a single mapping hop. The repo's identity is "Agentic
     Document Workflow"; this candidate drifts off it, and it drifts off the multi-step LLM
     pipeline that is the thing being demonstrated.
  2. **The bootstrap is the trap.** It needs a corpus of codebases pinned at old versions, then on
     the order of 20 repos × 5 versions × full test suites. CI minutes are free; Om's time is not,
     and D-009 records that his time is variable with no fixed deadlines. This is precisely the
     shape of project that stalls at week 3.
  3. The user is generic — any ML engineer — rather than Om personally, so requirement 4 is real
     but not personally grounded the way GateCheck is.
- Rejected alternative: treating pytest pass/fail as the *only* label and dropping the changelog
  entirely, which would make it a pure static-analysis tool. Rejected — it stops being an LLM
  project at all.
- Peer review: 1 round. Both peers independently ranked it second. Antigravity's stated reason:
  "solid mechanical ground truth beats a flashy idea with fuzzy unlabelable metrics; in this
  portfolio the headline eval numbers must survive interrogation." Agreed.
- Claude review: CLAUDE-OK (2026-09-27) — reasoning sound; bootstrap cost is the right objection.

### D-012 — Domain: PaperCompute (arXiv paper hardware-feasibility screener) — ranked 3, not selected
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: Keep on the shortlist as third. Input = an arXiv ML paper PDF or model card. Output =
  runnable locally (4-bit LoRA / GGUF) / needs cloud GPU / infeasible on a 16 GB RAM, 6 GB VRAM
  laptop.
- The objection that decided it — this candidate is caught in a bind. Split it in two:
  1. "Does the stated model fit in 6 GB VRAM at 4-bit" is computable from `config.json` parameter
     counts — but then the LLM contributes nothing and the project is a calculator. Trivial, and
     an interviewer sees through it in one question.
  2. "Can I reproduce this in a weekend" is genuinely interesting — but that label is a human
     judgement call, not a mechanical fact. Inter-rater agreement would be poor, precision and
     recall would go soft, and the evaluation, which is the actual differentiator for this
     project, would become the weakest part instead of the strongest.
  So it is either trivial or unlabelable. That is disqualifying here specifically, even though it
  is the best-sounding idea of the six out of the box.
- Two further evidence problems, both verified 2026-09-27:
  1. **PapersWithCode is dead.** Meta sunset it around 2025-07-24; the domain now redirects to
     `huggingface.co/papers/trending`, which has no leaderboard, no benchmark or task filters, and
     no task-wise search. Benchmark metadata survives only in the archived GitHub datasets. So
     "mechanically checkable via PapersWithCode benchmarks" is not a live ground-truth source; it
     is a downloadable archive that has stopped tracking new papers.
     <https://github.com/paperswithcode/paperswithcode-data/issues/116>
  2. **RepliCAT already does automated paper replication** with Docker and cost estimation, which
     narrows the novelty gap further than the idea first appears.
     <https://github.com/Poarthan/RepliCAT>
- Constraint worth preserving: arXiv metadata is CC0, but full-text redistribution is not
  permitted. Link or fetch at runtime; do not commit or host the PDFs.
  <https://info.arxiv.org/help/api/tou.html>
- Peer review: 1 round. Both peers reached the same verdict independently. Antigravity: "fully
  agree — memory math is a deterministic formula, reproducibility is subjective folklore; trapped
  between trivial calculator and unlabelable vibes." Recorded rather than deleted so the reasoning
  survives if this candidate is ever revisited.
- Claude review: CLAUDE-OK (2026-09-27) — "trivial or unlabelable" bind is correct.

### D-013 — T-001 joint ranking and domain recommendation
- Status: AGREED
- Owner: OpenCode + Antigravity (joint) — Reviewer: Antigravity
- Decision: **Recommend GateCheck (D-010) as the project domain.** Ranking: 1 GateCheck,
  2 DepRisk (D-011), 3 PaperCompute (D-012). Agreed jointly; no outstanding objections.
- Ranking rationale, one line each: GateCheck wins on defensibility, a live real user, and
  externally verifiable labels. DepRisk has the highest ceiling and the cleanest ground truth but
  loses on execution risk and on drifting off the LLM-pipeline identity. PaperCompute has the best
  story and the weakest evaluation, and in this project the evaluation is the product.
- Rejected by OpenCode, with reasons recorded rather than dropped:
  - **PaperScout** (arXiv paper trust + hardware feasibility). The trust half is crowded — Pub-
    Guard-LLM, WithdrarXiv, WithdrarXiv-Check, VeriRAG, and Zotero / Recite / Scite as shipping
    products. The feasibility half collapses into D-012(a), which is trivial. Dropped.
    <https://arxiv.org/html/2502.15429>
  - **BugTriage** (OSS-Fuzz / ARVO reproduction triage). Best mechanical ground truth found and the
    best genuine agentic multi-step fit — cluster → select → reproduce in sandbox → report — with
    ARVO giving 6,138 vulns across 311 projects and reproduction success defined mechanically (exit
    0 plus sanitizer clean). Rejected because label *acquisition* needs a build machine Om does
    not have, the OSS-Fuzz C/C++ toolchain is a multi-day yak-shave before the first result, and it
    is not a document workflow. **This is the candidate to resurrect first if cloud credits ever
    become available.** <https://arxiv.org/html/2408.02153v2>
  - **FantasyXI** (fantasy-cricket XI and points auditor). Fails the repo's own identity: Cricsheet
    is structured JSON, so there are no documents and "Agentic Document Workflow" stops being true.
    Points ground truth is partly self-generated by a scorer we would write, which is circular, and
    a consumer fantasy game reads unserious for ML/GenAI roles. Dropped.
    <https://cricsheet.org/downloads/>
- Not developed, flagged UNVERIFIED: the NSP scholarship and syllabus-coverage seeds raised in the
  task brief were taken forward by neither peer. OpenCode's assessment is that NSP fails
  requirement 1 (eligibility depends on Aadhaar-linked family-income data that is not openly bulk
  downloadable) and syllabus coverage fails requirement 2 (the label is a judgement about topical
  overlap, not a verifiable fact). Neither claim was researched in depth; revisit only on request.
- What the pivot does and does not break in the existing log. Checked explicitly so Claude does not
  have to re-derive it:
  - `D-001` capability table: survives, but its Gujarati OCR reasoning becomes **moot**, not wrong.
    Gemini beating Claude on Gujarati (83.68 vs 70.92) was a real measurement; GateCheck simply
    does not need OCR. The constraint it produced — Claude can never be the pipeline model — also
    becomes moot, since the pipeline is Gemini either way.
  - `D-002` topic ownership and Phase 3 split: survives unchanged; domain-agnostic.
  - `D-003` blinded Candidate A/B/C/D evaluation against PDF ground truth: survives unchanged and
    is arguably *more* valuable here, because GateCheck labels are externally checkable.
  - `D-004` planning workflow: untouched.
  - `D-005` code ownership, `D-006` git out of OneDrive: survive unchanged.
  - `D-007` OpenCode drafts labels and Om checks, valid because the pipeline is not big-pickle:
    survives; Gemini still satisfies it.
  - Net effect: the pivot **frees** decisions rather than breaking them. `D-009` already anticipated
    this by deferring Claude's review of D-001..D-003 and D-008 until the domain is chosen.
- Explicitly deferred, restated so it is not lost: corrigendum / addendum handling. This corpus
  supplies amendment pairs natively (`advt_140_v2` vs `v3`, `advt_156` vs its addendum), but
  CLAUDE.md's "past Phase 3" deferral stands unchanged.
- Peer review: 1 round. Antigravity accepted the ranking and the three reasons for it
  (re-skin objection is an asset rather than fatal; DepRisk over PaperCompute on ground-truth
  quality; full agreement on the PaperCompute bind), then asked OpenCode to draft D-010..D-013 and
  pass the turn back for review.
- Claude review: CLAUDE-OK (2026-09-27). Nit: Antigravity is both joint owner and reviewer here —
  self-review; fine for a ranking, avoid for decisions that ship. Note for Om: all three finalists
  were ranked on eval defensibility; "interesting to Om" was weighted less — Om must judge that.
  D-001..D-003, D-008 review still pending (not blocking the domain choice).

### D-014 — DOMAIN LOCKED: GateCheck, scope (b)
- Status: DECIDED-BY-OM (2026-09-27)
- Decision: Project domain = GateCheck (D-010). Version 1 = eligibility PDFs only (DRDO/RAC,
  BARC OCES/DGFS, IIT M.Tech brochures); IIT cutoff-matrix family comes as a later stage.
  Gujarat tenders dropped. Claude's D-010 conditions apply: designed synthetic profile set;
  README wording of how labels are checked.
- Claude review: n/a

---

### D-016 — Topic 7: locating eligibility criteria in long brochures — send the whole document, do not chunk it
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: **Pass the entire brochure to the model in one call, with page boundaries marked. No
  chunking, no embeddings, no vector store, no retrieval step in version 1.** The page markers are
  load-bearing: CLAUDE.md requires a page number and a short quote for every criterion, so the
  extractor must hand us text that still knows which page it came from, and we must keep that
  boundary visible in the prompt.
- Plain-language version of why: this topic was written as "chunking", which quietly assumes the
  documents are too big to read. **They are not.** I measured the real files. The largest brochure
  in the corpus is about 68,000 tokens. The model accepts about 1,048,576. The document uses about
  6.5% of the window and leaves roughly 15x headroom. So the problem "how do I find the criteria
  inside a huge document" does not exist for this corpus, and every clever retrieval layer we build
  is solving a problem we do not have — while creating a new one.
- Measured evidence (2026-09-27, downloaded from the official URLs to a temp folder outside the
  repo; measured with `pypdf` 6.9.1; tokens estimated at characters/4, which is a rough heuristic
  for English prose and should be confirmed with Gemini's `countTokens` endpoint when it matters):

  | Document | Pages | Characters | ~Tokens | Zero-text pages |
  |---|---|---|---|---|
  | IIT KGP Joint M.Tech.-MCP-M.Arch. brochure 2025-26 | 86 | 273,066 | ~68,266 | 3 |
  | BARC/IGCAR OCES-DGFS-2026 information brochure | 42 | 75,351 | ~18,837 | 0 |
  | DRDO/RAC advt_152 (Scientist D/E/F, Apr 2025) | 9 | 45,315 | ~11,328 | 0 |
  | DRDO/RAC advt_157 (Jun 2026) | 1 | 2,922 | ~730 | 0 |

  86 pages is the largest case and it still fits with room to spare. The short DRDO notices are
  trivial by comparison. A DRDO advertisement is a 1-to-9-page document; a brochure is 40-to-90.
  There is no size regime in this corpus that a context window cannot swallow.
- Second piece of evidence, and it surprised me: **the criteria are not scattered.** They sit in
  named, numbered sections that a parser can see.
  - BARC page 2 is a numbered table of contents: "3. Selection process", "4. Eligibility criteria",
    "6. Application fee and maximum age limit (Table-5)". 606 heading-shaped lines in the document.
  - IIT KGP pages 5-6 are a contents list with dot leaders and real page numbers: "3 General
    Information for Applicants 63", over per-department sections 2.1 through 2.27. 881
    heading-shaped lines.
  So both document families publish an explicit eligibility section, and an eligibility rule that
  is not in that section is the exception, not the rule.
- The reason that actually decides it — failure mode, not convenience. For this product a **missed
  criterion is a wrong answer**: a dropped age relaxation turns APPLY into SKIP, which is the exact
  mistake the user is paying us to avoid. Now look at what a retrieval layer is. It is a *ranking*
  system. It decides what the model is allowed to see, and whatever it ranks low is simply not
  there — no error, no warning, no gap in the output. The memo would read complete and be wrong.
  That is the worst possible bug for this product, and it is invisible in the output. Passing the
  whole document converts the failure from "retrieval silently hid a rule" into "the model read the
  rule and did not use it" — and the second one shows up in the eval as a recall miss we can see,
  attribute, and fix. **We would rather have a visible wrong answer than an invisible right-looking
  one.**
- Alternatives considered, with the trade-off stated plainly:
  1. **TOC-guided section selection (REJECTED).** Parse the contents page, send only "4. Eligibility
     criteria" and friends. Cheaper context, maybe 5k tokens instead of 68k. Rejected for two
     reasons. First, eligibility rules leak out of their own section: BARC's age ceiling is in
     section 6, the degree-completion deadline sits elsewhere, and IIT's "CGPA 8.0 holders are
     exempt from GATE" is a sub-clause away from the main rule — so any section whitelist is a
     silent-loss bug of exactly the kind above. Second, it needs a *second* parser that must handle
     25 heterogeneous PDFs with 25 different contents-page layouts, and that parser will have its
     own silent failures. We would be buying token savings we do not need with a reliability risk
     we cannot afford.
  2. **Page-chunk plus embedding retrieval, i.e. classic RAG (REJECTED).** The industry default, and
     the right answer for a 500-page manual or a 10,000-document pile. Wrong tool here: same
     silent-loss failure mode as above, plus four new components to build and maintain (chunker,
     embedding model, vector store, retriever) and a second paid model, to serve 25 documents that
     fit in one prompt. It is also the option most likely to be challenged in an interview as
     "unnecessary complexity" — correctly.
  3. **Two-stage map-then-extract (DEFERRED, not rejected).** A cheap first pass reads the whole
     document and lists which pages hold eligibility criteria; a second pass extracts from those
     pages only. Better recall than options 1-2, because the map pass still sees everything. Costs
     two calls instead of one and gives us two places to fail. Keep this in the drawer: if a future
     corpus document exceeds roughly 500,000 tokens, this becomes the answer. It does not need to
     be built now.
- The one genuine cost of this recommendation, stated rather than hidden: **input tokens per call
  are large, and the free tier has a budget.** A 68k-token brochure is fine once, but the pipeline
  makes several calls per notice and the eval will run 10-25 notices. Two mitigations, both free
  and both worth doing: (a) **prompt caching** — put the brochure *first* in the prompt so it
  becomes a cacheable prefix, identical across all three pipeline steps and across every candidate
  profile run against that same notice, so steps 2 and 3 pay a discounted rate for it; (b) the
  `countTokens` endpoint, so a cost guard can measure a document *before* spending anything on it
  and refuse anything that would not fit. Exact free-tier numbers and the per-run cost cap belong
  to topic 10 and topic 14, not here; flagging the dependency so it is not discovered late.
- What Om must decide: **nothing blocking.** One thing to be aware of rather than decide: this entry
  bets the project's recall number on "the model read it and missed it" being easier to fix than
  "the retriever hid it". The eval in Phase 5 will show which it really is. If criterion recall
  comes out poor, the fix is prompt and schema work, not retrieval — and I would rather we find that
  out with a cheap whole-document baseline than after building a retrieval stack on top of it.
- **Corrections to D-010's evidence, found by measuring instead of assuming.** Three URLs cited in
  D-010 are wrong and must not reach the corpus manifest:
  - `https://www.iitb.ac.in/newacadhome/MTECH_BROUCHURE2025-26.pdf` returns **404**.
  - `https://rac.gov.in/download/archive/advt_140_v2.pdf` returns **404**.
  - `https://rac.gov.in/download/archive/advt_156_addendum.pdf` returns **404**.
  The *documents* almost certainly exist — D-010's quoted eligibility text came from real browsing,
  and the IITB rule it quotes is a real IIT Bombay rule. What is wrong is the guessed **filenames**.
  The manifest needs verified URLs fetched and hashed, not constructed URL patterns. Antigravity
  owns `team/corpus-candidates.md`; raised directly so guessed paths do not get committed. The four
  URLs in this entry were all fetched successfully today and are safe to use as-is.
- Carried forward from Claude's condition 2 on D-010: a label here means "does profile P meet
  criterion C of document D", checked by Om reading the PDF. This entry is compatible with that
  wording, and it is the reason recall of criteria is treated as the headline risk rather than
  precision — a criterion that was never extracted cannot be checked against anything.
- Sources, all checked 2026-09-27:
  - Gemini models documentation — Flash family input limit 1,048,576 tokens, output 65,536:
    <https://ai.google.dev/gemini-api/docs/models> and
    <https://ai.google.dev/gemini-api/docs/generate-content/tokens>
  - `countTokens` endpoint, for pre-spend size checks:
    <https://ai.google.dev/gemini-api/docs/tokens>
  - The four PDFs in the table above, fetched from their official issuer URLs and measured locally.
- Peer review: 1 round. ACCEPTED by Antigravity. OpenCode's empirical measurements decisively settle the architectural choice: with the largest brochure consuming only ~68k tokens (<7% of Gemini Flash's 1M context window), classic chunking/RAG is premature complexity that trades 100% full-document recall for lossy top-k filtering where a single dropped exemption clause silently corrupts the memo. Interviewer defense is rock solid: (1) context window headroom makes chunking unnecessary; (2) RAG's failure mode is silent recall drop, which is fatal for eligibility checks; (3) prompt caching (document placed first as cacheable prefix) makes repeated calls cheaper than multi-turn embedding indices. Free-tier TPM limit (1M TPM) is mitigated by serializing eval runs with explicit backoff, pre-flight countTokens checks, and Topic 14's recorded test fixtures.


- Claude review: CLAUDE-OK (2026-09-29). Whole-document + page markers is right; the silent-loss argument is the interview answer. Verify that implicit/explicit prompt caching is actually available on the free tier before relying on it — mark UNVERIFIED until checked.

### D-017 — Topic 8: Structured Output & Validation (Criteria & Schema Contracts)
- Status: AGREED
- Owner: Antigravity — Reviewer: OpenCode
- Decision: Use native **Gemini Structured Outputs** (`google-genai` SDK with `response_schema` and `response_mime_type="application/json"`) backed by **Pydantic v2** (`BaseModel`, `Field`, `@model_validator`) for runtime schema enforcement, strict type validation, automated normalized verbatim grounding checks, and explicit post-validation retry with error feedback (max 2 retries).
- The Problem in Plain Language:
  In Step 1 of GateCheck, an LLM reads an official recruitment notice or brochure (BARC OCES, DRDO RAC) and must output a list of eligibility criteria (age limits, degree requirements, GATE score cutoffs). If the LLM returns unstructured English text or invalid JSON (missing braces, wrong field names, or nulls where numbers are expected), the downstream Python arithmetic engine (Step 2) crashes. Crucially, Python arithmetic cannot compute over free-text `description` strings; the model must emit **typed machine-checkable rule parameters** (thresholds, operators, cutoff reference dates, relaxation stacking) matching our Python checker contracts.
- Alternatives & Plain-Language Trade-offs:
  1. **Candidate 1 (Recommended): Native Gemini Structured Outputs (`google-genai` SDK + Pydantic v2)**
     - *How it works:* Pass Pydantic models directly into `GenerateContentConfig(response_schema=..., response_mime_type="application/json")`. The backend enforces constrained grammar decoding at token generation. Model selection and rate limits are decoupled into Topic 5 and `gatecheck/config.py`.
     - *Free tier status:* Available on Google AI Studio Gemini API free tier (checked 2026-09-29; standard `generateContent` feature, with rate limits dynamically configured via environment/config).
     - *Supported Schema Subset:* Documented in `google-genai` `types.py response_json_schema`: `$id, $defs, $ref, $anchor, type, format, title, description, enum, items, prefixItems, minItems, maxItems, minimum, maximum, anyOf, oneOf, properties, additionalProperties, required`, plus non-standard `propertyOrdering`.
     - *Pros:* Guaranteed schema compliance at token generation time; zero third-party wrapper overhead; native to chosen provider; clean local validation.
     - *Cons:* Schema cannot embed arbitrary dynamic Python code; semantic correctness and hallucination detection require post-generation Pydantic validators.
  2. **Candidate 2: `instructor` library (`instructor.from_gemini(...)`) — REJECTED.**
     - *Cons:* Extra dependency wrapping raw HTTP/JSON calls; auto-retries obscure quota management; conflicts with our requirement to explicitly record retry counts and error taxonomy in `TraceSink`.
  3. **Candidate 3: Outlines / Guidance (Local Constrained Sampling) — REJECTED.**
     - *Cons:* Requires direct logit control (only available with local weights via `llama.cpp`/`vLLM`). Incompatible with remote Gemini API.
  4. **Candidate 4: Raw JSON Prompting + Manual Pydantic Validation — REJECTED.**
     - *Cons:* High failure rate on multi-page extraction (markdown wrapping, trailing commas, invalid escaping), wasting quota on formatting retries.
- Key Schema Elements & Typed Rule Block:
  - `criterion_id`: Stable identifier (e.g. `CRIT-AGE-01`, `CRIT-DEG-01`, `CRIT-GATE-01`).
  - `category`: Strict Enum (`AGE`, `QUALIFYING_DEGREE`, `GATE_SCORE`, `NATIONALITY`, `RESERVATION_CATEGORY`, `EXPERIENCE`, `OTHER`).
  - `description`: Plain-English rule summary.
  - `condition_type`: Enum (`THRESHOLD`, `DISJUNCTION`, `CONJUNCTION`, `EXEMPTION_RULE`).
  - `raw_quote`: Exact verbatim quote from the PDF text.
  - `page_number`: 1-indexed physical PDF page where the quote appears.
  - `is_machine_evaluable`: `bool` (explicit flag: True if rule can be evaluated purely by deterministic Python arithmetic).
  - **`rule_parameters`**: Typed parameters block (one populated per category, aligning with D-021 `CandidateProfile`):
    - *`age_rule`* (dispatched to `check_age_eligibility`):
      - `cutoff_date`: `date | None` (the reference date, e.g. `2026-08-01`)
      - `min_age_years`: `int` (default 18)
      - `max_age_years`: `int` (general category ceiling, e.g. 26)
      - `category_relaxations`: `dict[CategoryEnum, int]` (e.g. `{"OBC_NCL": 3, "SC": 5, "ST": 5}`)
      - `pwd_relaxation_years`: `int` (standard 10)
      - `min_pwd_disability_percent`: `float` (statutory threshold, default 40.0; sub-benchmark receives 0 relaxation)
      - `pwd_stacks_with_category`: `bool` (default True per DoPT OM)
      - `max_relaxed_age_cap`: `int | None`
    - *`degree_rule`* (dispatched to `check_degree_eligibility`):
      - `allowed_degrees`: `list[str]` (e.g. `["B.E.", "B.Tech", "Integrated M.Tech"]`)
      - `allowed_disciplines`: `list[str]` (e.g. `["Computer Science & Engineering", "Information Technology"]`)
      - `min_percentage`: `float | None` (e.g. 60.0)
      - `min_cgpa_10`: `float | None` (e.g. 6.0)
      - `cgpa_conversion_formula`: `str | None` (e.g. `"(CGPA - 0.75) * 10"`)
      - `cgpa_percentage_precedence`: (Evaluation precedence pinned: when `cgpa_conversion_formula` is specified, the checker converts candidate `cgpa` to percentage using the formula and compares against `min_percentage` [formula precedence]; otherwise, compares candidate `cgpa` normalized to scale 10.0 against `min_cgpa_10` if present, or `percentage` against `min_percentage`).
      - `requires_first_class`: `bool`
      - `final_year_eligible`: `bool`
      - `marksheet_submission_deadline`: `date | None`
    - *`gate_rule`* (dispatched to `check_gate_eligibility`):
      - `valid_gate_years`: `list[int]` (e.g. `[2024, 2025, 2026]`)
      - `allowed_paper_codes`: `list[str]` (e.g. `["CS", "DA"]`)
      - `min_gate_score`: `int | None`
      - `min_gate_marks`: `float | None`
      - `iit_btech_cgpa_exemption_threshold`: `float | None` (e.g. 8.0)
    - *`experience_rule`* (dispatched to `check_experience_eligibility`):
      - `min_months_post_qualification`: `int`
  - **Deterministic Step 2 Invariant**: Any criterion where `is_machine_evaluable=False`, `rule_parameters` is null, or category is `OTHER` evaluates deterministically to `NEEDS_REVIEW` with reason `COMPLEX_CLAUSE_REQUIRES_HUMAN_EVALUATION`. The LLM is never invoked in Step 2 to decide ambiguous waivers.
- Grounding Normalisation Pipeline:
  - Literal `raw_quote in page_text` fails on whitespace breaks, hyphenation, and curly quotes. Prior to substring matching, both strings pass through a deterministic normalizer `normalize_for_grounding(text: str) -> str`:
    1. Unicode NFKC normalization (`unicodedata.normalize("NFKC", text)`), converting non-breaking spaces `\u00a0` to standard spaces.
    2. Quote & Dash unification: replace curly quotes `“ ” ‘ ’` with straight `\" '`; replace em-dashes `—`, en-dashes `–`, and minus signs with standard `-`.
    3. De-hyphenation across line wraps: regex `r"(\w+)-\s*\n\s*(\w+)" -> r"\1\2"`.
    4. Whitespace collapsing: collapse all whitespace sequences `\s+` to single space `" "`, then `.strip().lower()`.
  - **Text Source Priority (per D-015)**: Match against `pypdf_page_text[page_number]`. If unmatched and the page contains tables, check against `pdfplumber_page_text[page_number]` and serialized table cells. If neither matches, trigger a grounding retry (`Quote not found verbatim on cited page`).
- Rate Limits & Config Decoupling:
  - Do not hard-code 15 RPM / 1,500 RPD into code. Read rate limits dynamically from `gatecheck/config.py` (`GATECHECK_RATE_LIMIT_RPM`, `GATECHECK_RATE_LIMIT_RPD`). Google AI Studio free tier limits vary across model generations (e.g. Gemini 2.5 Flash / Flash Lite); runner uses conservative default (10 RPM) and enforces rate-pacing + dynamic backoff on HTTP 429 using `Retry-After`.
- Terminal Behaviour:
  - If schema or grounding validation fails after max 2 retries, abort automated screening, set memo verdict to `NEEDS_REVIEW`, record `ExtractionValidationError` / `QuoteGroundingError` in `TraceSink`, and flag notice for human inspection.
- Sources & Dates:
  - Google GenAI SDK Structured Outputs Documentation (checked 2026-09-29): <https://ai.google.dev/gemini-api/docs/structured-output>
  - Google AI Studio Pricing & Rate Limits (checked 2026-09-29): <https://ai.google.dev/pricing>
  - Pydantic v2 Documentation (checked 2026-09-29): <https://docs.pydantic.dev/latest/>
  - Instructor GitHub Repository (checked 2026-09-29): <https://github.com/jxnl/instructor>
- Peer review: Round 1 accepted. Round 2 (OpenCode, 2026-09-29): ACCEPTED with 2 additions applied — (1) `min_pwd_disability_percent` (default 40.0) added to `age_rule` so PROF-10's sub-benchmark denial is machine-evaluable, not silently NEEDS_REVIEW; (2) `cgpa_percentage_precedence` pinned in `degree_rule` (formula-converts CGPA to % and compares `min_percentage` when formula present; else normalized-to-scale-10 CGPA vs `min_cgpa_10`, else raw percentage vs `min_percentage`), making PROF-05 deterministic. Both Claude issues and both additions verified in the log. Set AGREED.
- Claude review: CLAUDE-OK (2026-09-29, round 2). Typed rule block, normalisation and config-driven limits resolve round 1. Carried into PLAN.md by Claude (no new round): DISJUNCTION semantics — when a rule offers alternative routes (e.g. IITB A.5.1: 60% OR First Class OR CGPA 6.0), the criterion is MET if ANY route is met; `cgpa_percentage_precedence` applies only when the notice mandates one conversion. As written, PROF-05 would be wrongly NOT_MET under an OR rule. (Note: this line is Claude's — peers record their own round summary in 'Peer review'.)

---

### D-024 — T-003: AGENTS.md, the file OpenCode loads at session start
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: Create `AGENTS.md` at the repo root as a **pointer only**. It does one job: tell
  OpenCode to read `.claude/rules/team-protocol.md` in full at the start of every session and
  then do what that file's section **"Resuming in a new session (do this first, every time)"**
  says. It contains **no rules of its own** — no roles, no terminal handles, no task list, no
  protocol text. Created; 1,170 bytes, 20 lines.
- Why this is not a trivial file, and the thing worth knowing: **OpenCode loads `AGENTS.md`
  *instead of* `CLAUDE.md` when both exist.** First match wins; there is no merge. So adding this
  file does not add a convenience layer on top of the current setup — it *replaces* what OpenCode
  auto-loads today. Before this change, every OpenCode session began with the full `CLAUDE.md`
  (Product, Differentiator, Scope, Phase 0 decisions, the Phases table, How we work,
  Orchestration). After it, none of that is auto-loaded.
  That is only safe because the chain still closes: `AGENTS.md` → `team-protocol.md` → its
  "Resuming in a new session" step 1, which reads "*this whole file, then `CLAUDE.md`, then the
  last ~5 entries of `team/decision-log.md` (not the whole log)*". So `CLAUDE.md` is still read,
  one hop later, deliberately, at the moment it is needed instead of on every single turn. That is
  a net win for context cost, but it is a real behaviour change and it is recorded here so nobody
  is surprised by it later.
- Verified against OpenCode's own documentation (checked 2026-09-27, page last updated 2026-09-26)
  rather than assumed: <https://opencode.ai/docs/rules/>
  - "You can provide custom instructions to opencode by creating an `AGENTS.md` file."
  - Project rules: "Place an `AGENTS.md` in your project root for project-specific rules. These
    only apply when you are working in this directory or its sub-directories."
  - Precedence: "The first matching file wins in each category. For example, if you have both
    `AGENTS.md` and `CLAUDE.md`, only `AGENTS.md` is used."
  - Claude Code compatibility: `CLAUDE.md` in a project directory is a **fallback**, "used if no
    `AGENTS.md` exists". This is the rule that makes the above true.
  - "opencode doesn't automatically parse file references in `AGENTS.md`" — so the file instructs
    an explicit `Read` rather than using `@`-style references, which would have silently done
    nothing. Trap avoided.
- Verification actually performed on the created file, not just asserted:
  - `AGENTS.md` exists at the repo root; 1,170 bytes, 20 lines, UTF-8 **without** BOM, zero
    replacement characters (checked byte-wise, because this repo's files are UTF-8 and a BOM or a
    mojibake character would be easy to miss).
  - Its target `.claude/rules/team-protocol.md` exists.
  - The exact section it names, `## Resuming in a new session (do this first, every time)`,
    exists at line 22 of that file. So the pointer is not dangling.
  - No `AGENTS.md`, `opencode.json`, `opencode.jsonc` or `.opencode/` existed in the repo before
    this, so nothing was overwritten and no config is being silently displaced.
- Scope note, so this is not mistaken for a shared file: `AGENTS.md` is **OpenCode-specific**.
  Claude Code reads `CLAUDE.md` natively and is unaffected. Antigravity loads whatever its own
  configuration loads. That asymmetry is precisely the reason the rules must live in
  `team-protocol.md` rather than in `AGENTS.md` — a file only one of the three agents reads cannot
  be the team's source of truth.
- Alternatives considered:
  1. **Copy the rules into `AGENTS.md` (REJECTED).** Two copies of the same rules drift apart the
     first time someone edits one of them, and the team protocol explicitly wins over memory
     (step 5 of "Resuming in a new session"). OpenCode's own docs also steer toward a concise
     `AGENTS.md` that points at detailed files. Rejected.
  2. **Auto-load the protocol via `opencode.json` → `"instructions": [".claude/rules/team-protocol.md"]`**
     (NOT CHOSEN, but a real option and the one to argue about). This is a documented feature and
     it would load the file with no chance of the agent forgetting to. The cost is context: the
     whole protocol goes into every session, including the sections irrelevant to the task in
     hand, and it cannot be made conditional. `AGENTS.md` costs a deliberate read of the same
     file. Deferred rather than dismissed — if sessions start skipping the read, this is the
     switch to flip, and it is a one-line config change. It also adds a config file Om did not ask
     for; the repo currently has none.
  3. **Use `@.claude/rules/team-protocol.md` reference syntax inside `AGENTS.md` (REJECTED).**
     Would have looked correct and done nothing, per the docs line quoted above. Worth recording
     because it is the obvious thing to write and it is a silent failure.
- What Om must decide: **nothing.** Recorded for awareness only: OpenCode sessions will no longer
  begin with `CLAUDE.md` in context. If that turns out to make sessions slower or thinner, option 2
  above is the fix.
- Peer review: 1 round. ACCEPTED by Antigravity. (1) Official Antigravity documentation (agy-customizations / rules.md) verifies that the Antigravity CLI discovers and loads both GEMINI.md and AGENTS.md hierarchically from CWD up to repo root as always-on Directory Rules. Therefore, AGENTS.md is natively SHARED by both OpenCode and Antigravity; no separate GEMINI.md is needed. (2) The 20-line pointer is the exact right size—it prevents rule duplication, stays well under rule token budgets, and ensures both agents execute the exact same session-start checklist from team-protocol.md.


- Claude review: CLAUDE-OK (2026-09-29). Superseded in practice by D-027 findings (agy also reads AGENTS.md) — one pointer file serves both peers.

---

## Session Handoff & In-Progress Status (2026-09-27 23:56 IST)

### Tasks Completed This Session:
1. **T-001 (Domain Selection):** GateCheck locked as domain under scope (b) in `D-014`. `D-010..D-013` reviewed and marked `CLAUDE-OK`. `CLAUDE.md` rewritten.
2. **T-003 (Session Start Instruction File):** Verified Antigravity CLI natively auto-loads `AGENTS.md` alongside `GEMINI.md` as directory rules. Reviewed and agreed `AGENTS.md` (pointer to `.claude/rules/team-protocol.md`). Logged as `D-024` (`AGREED`).
3. **Corpus Candidates:** Created `team/corpus-candidates.md` with 28 verified born-digital recruitment notifications and admission brochures (DRDO RAC, BARC, IITs, PSUs).

### T-002 Phase 0 Topics Status:
- **Topic 6 (PDF Extraction):** `D-015` — OpenCode drafting (measured evidence in hand: pypdf primary + pdfplumber for tables).
- **Topic 7 (Locating Criteria / No Chunking):** `D-016` — `AGREED` (Send entire doc into context window with 1-indexed page markers; 86pp IIT KGP doc is ~68k tokens = 6.5% of 1M context; zero silent retrieval loss; prompt caching prefix).
- **Topic 8 (Structured Output & Validation):** `D-017` — `PROPOSED` (Native Gemini Structured Outputs via `google-genai` + Pydantic v2; awaiting OpenCode review).
- **Topic 9 (Pipeline Runner):** `D-018` — Antigravity queued to draft next (Hand-written Python pipeline runner vs LangGraph).
- **Topic 10 (Tracing):** `D-019` — OpenCode queued to draft (Langfuse vs own JSONL/SQLite).
- **Topic 11 (Storage):** `D-020` — OpenCode queued to draft.
- **Topic 12 (Schemas + Synthetic Profile Set):** `D-021` — Antigravity queued to draft (CandidateProfile, EligibilityMemo, + 10-profile synthetic edge-case set).
- **Topic 13 (Web Framework & Deploy):** `D-022` — Antigravity queued to draft (gated on D-015).
- **Topic 14 (Testing Without Per-Run Spend):** `D-023` — OpenCode queued to draft.

### Next Session Resume Checklist:
1. Follow `.claude/rules/team-protocol.md` section "Resuming in a new session (do this first, every time)".
2. OpenCode lands `D-015` and reviews `D-017`.
3. Antigravity drafts `D-018` and `D-021`.
4. Batch-ping Claude when all entries `D-015..D-023` reach `AGREED`.

---

### D-015 — Topic 6: PDF text and page-number extraction, born-digital — pypdf primary, pdfplumber for grids
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: **`pypdf` for page-by-page text, plus `pdfplumber` for grid tables on table-bearing
  pages. No OCR, no vision model, no layout model.** Both are pure Python, both permissively
  licensed, no compiled extensions, so the install is trivial and there is no binary to break on
  another machine. Extracted text must be cached on disk keyed by the PDF's hash, so we parse each
  notice once and never again.
- Plain-language version: D-014 locked the corpus as born-digital eligibility PDFs, which means
  every page already contains real text — we are not looking at scans. So the only job here is to
  pull that text out **with the page number attached**, because CLAUDE.md requires every criterion
  to carry a page cite and a short quote. `pypdf` does that job cleanly and fast. The one thing it
  does badly is multi-column *grids*, where the meaning lives in the row-by-column alignment. So we
  add `pdfplumber` for exactly those pages and nothing else.
- Measured evidence (2026-09-27, on the real files, timed on this machine — not from a blog post):

  | File | Pages | pypdf 6.9.1 | pdfplumber 0.11.9 | Grids found |
  |---|---|---|---|---|
  | BARC/IGCAR OCES-DGFS-2026 (716 KB) | 42 | 2.52 s, 75,351 chars | 15.19 s, 72,895 chars | 14 |
  | IIT KGP JMP 2025-26 (2,511 KB) | 86 | 10.36 s, 273,066 chars | 39.42 s, 267,136 chars | 37 |

  `pypdf` is roughly 4-6x faster. That is not the deciding factor — 10-40 s once per document, then
  cached, is irrelevant. The deciding factor is what each one *produces*, below.
- The finding that shaped the decision. BARC states its age limits **twice**, in two different
  forms, and the two need different tools:
  - **Page 17, section 4.3 — prose.** A numbered list: "i. General category - 26 years, ii. OBC
    (Non-Creamy Layer) - 29 years, iii. SC/ST - 31 years ... vi. Physically challenged persons of
    all categories are eligible for age relaxation of 10 years ... vii. The minimum age limit for
    all the applicants is 18 years as on August 1, 2026." `pypdf` pulls this out **perfectly** and
    in reading order. `pdfplumber` found **no table on that page at all** — correctly, because it is
    prose, not a grid. This is the passage that carries the highest-stakes rule in the whole
    product, and the fast tool reads it better than the fancy one.
  - **Page 41, "Table-5" — a real grid.** `pdfplumber` returns it structurally, with headers:
    `Category | No Disability | Physically challenged | Maximum age limit as on 01-08-2026 (Born
    on or after) | Fee`. `pypdf` flattens a grid into running lines, and in a flattened grid the
    attachment of "born on or after 01-08-1999" to the *right category* can be lost. That is
    precisely the kind of quiet corruption this project cannot afford: a DOB boundary detached from
    its category flips a correct SKIP into a wrong APPLY.
  So the answer is not "pick one". `pypdf` carries the document, `pdfplumber` carries the grids, and
  both outputs go to the model with their page numbers attached.
- Other grids worth knowing about, because they are eligibility-relevant rather than decorative:
  pages 28-29 (OCES/DGFS screening discipline codes and qualifying degrees), 33 (training school
  and scheme), **34-39 (DGFS institute, M.Tech. specialisation, and admissible GATE subjects — a
  direct eligibility input)**, 40 (key dates), 42 (exam centres). Pages 28-39 are also why "just
  extract text" would have been a real loss, not a theoretical one.
- Cleanliness checks, because a silent character bug here would poison every label downstream:
  `pypdf` output contains **zero U+FFFD replacement characters** across both documents. (An earlier
  console view appeared to show mojibake; byte-level inspection confirmed it was only the Windows
  console failing to render an em-dash. Worth recording, because it is the kind of thing that gets
  "fixed" by someone adding an encoding hack that is not needed.)
- The blank-page finding, which is a real design requirement. The IIT KGP brochure has **3 pages
  (2, 4, 74) with zero extractable text.** I checked whether these were scans — they have no text
  *and* no image XObjects, so they are genuinely blank or vector-only separator pages, and no OCR
  is needed. But the extractor must still **report** them explicitly as zero-text pages, so that a
  blank separator is distinguishable from a failed extraction. If we silently drop them, a genuinely
  unreadable page and a deliberately blank page become indistinguishable, and that is exactly the
  kind of hole a reviewer will ask about.
- Licensing, checked rather than assumed (2026-09-27, from PyPI metadata):
  - `pypdf` 6.9.1 — BSD-3-Clause. Fine.
  - `pdfplumber` 0.11.9 — MIT. Fine. Its engine `pdfminer.six` 20251230 — MIT. Fine.
  - `PyMuPDF` 1.28.2 — **"Dual Licensed - GNU AFFERO GPL 3.0 or Artifex Commercial License".**
  Both of our picks are safe for a portfolio repo. Flagging PyMuPDF because it is otherwise the
  most attractive library on the list — fastest, good tables — and AGPL is copyleft: it is a poor
  default for code an employer might read. Not a prohibition, just a decision to make knowingly.
- Alternatives considered:
  1. **`pdfplumber` alone (REJECTED).** 4-6x slower and *worse* on the highest-stakes passage, since
     the age rules in section 4.3 are prose and it detects no table there. Its grid handling is
     genuinely better, which is why it stays — as an addition, not a replacement.
  2. **`PyMuPDF` (REJECTED, licence).** Best raw performance and good tables, but AGPL-3.0 as
     above. Reachable later via the Artifex commercial licence if profiling ever shows we need it.
  3. **Docling / Marker / Unstructured — ML document converters (REJECTED as primary).** These run
     layout or vision models to rebuild document structure. That is a large dependency (Marker pulls
     in torch), it is slow, it costs money or GPU time, and it is aimed at scanned or badly-formatted
     input. Our input is clean born-digital text, so we would be paying a model to solve a problem
     we do not have. Worth remembering as the escape hatch if a specific notice in the corpus turns
     out to be a scan despite expectations.
  4. **`pdfminer.six` directly (REJECTED).** It is the engine underneath `pdfplumber`; using it
     directly means re-implementing the table layer ourselves. Strictly worse for the same money.
- One design point flagged, not fully settled here, because it bites in Phase 1: **which page number
  do we cite?** The PDF's own page index and the page number *printed on the page* are different
  things — the IIT KGP contents list points at "3 General Information for Applicants 63", which is
  a printed folio, while the same content sits at a different PDF index. A citation is only useful
  if it matches what the reader sees when they open the file. Recommendation: record the PDF index as
  the machine truth and capture the printed folio where it is detectable, and cite the printed one
  in the memo with the index in the trace. Antigravity should sanity-check this against how a
  reviewer would actually verify a cite.
- What Om must decide: **nothing.** Recorded for awareness: the two-library choice is slightly more
  code than one library, and the paid price of that is one extra dependency and a rule about which
  extractor runs on which page.
- Peer review: 1 round. ACCEPTED by Antigravity. (1) Two extractors is not over-engineering: OpenCode's BARC p. 17 vs p. 41 finding proves that single-extractor solutions fail silently on either prose lists or category-DOB alignment; hybrid extraction (pypdf baseline + pdfplumber for tabular structures) is the minimum necessary precision to avoid corrupted eligibility boundaries. (2) Citations: mandatory 1-indexed physical PDF page number ensures mechanical verification and automated jumps; optional printed folio is retained for human presentation in memos.
- Claude review: CLAUDE-OK (2026-09-29). Strong: measured, licence-checked, blank-page rule. Carry into PLAN: define how a page is chosen for pdfplumber (e.g. run it on every page once, keep tables found) and which text the D-017 grounding check compares against when a quote comes from a pdfplumber grid.

---

### D-025 — T-002 / T-003 handoff: state at session close
- Status: PROPOSED
- Note: this is a **handoff note for the next session, not a decision**, so it needs no peer
  review and no Claude review. It exists so the next session resumes from facts rather than from
  re-derivation. Antigravity already added a shorter "Next Session Resume Checklist" above; this
  entry is the fuller version and does not contradict it.
- **Message IDs from this session**, so the next session can trace what was actually said without
  re-deriving it: `msg_bde97b075073` to Antigravity (T-003, `AGENTS.md` filename + `D-024` for
  review); `msg_d9dd229c6015` to Antigravity (`D-016`, for review); `msg_2f991f219d71` to
  Antigravity (`D-015` + this handoff note, for review); `msg_fd1599b3c789` to Claude (status only,
  no review requested — see the blocker list below).
- **DONE this session:**
  - T-002 coordination: accepted Antigravity's D-015..D-023 ID map (it matches D-002 ownership and
    removes merge ambiguity); `team/corpus-candidates.md` confirmed as Antigravity's file; flagged
    that we are now both appending to the shared log and proposed an announce-before-append rule.
  - **D-016 drafted** (PROPOSED) — send the whole document, no chunking, no RAG. Backed by
    measurement: largest brochure ~68k tokens against a 1,048,576-token limit, and both document
    families publish a numbered eligibility section. Sent to Antigravity for review.
  - **Three D-010 URLs found to be 404** — `iitb.ac.in/.../MTECH_BROUCHURE2025-26.pdf`,
    `rac.gov.in/.../advt_140_v2.pdf`, `rac.gov.in/.../advt_156_addendum.pdf`. Guessed filenames, not
    missing documents. Recorded in D-016 and messaged Antigravity before the manifest gets
    committed. **This is the highest-priority open item**, because a manifest of constructed URL
    patterns would quietly poison the whole corpus.
  - **T-003 done**: `AGENTS.md` created at repo root (20 lines, pointer only), verified against
    OpenCode's documented precedence rules, logged as D-024, filename sent to Antigravity for
    review.
  - **D-015 drafted** (PROPOSED) — pypdf primary plus pdfplumber for grids, with measured timings,
    the prose-versus-grid finding on BARC pages 17 and 41, the three-blank-pages requirement, and
    the PyMuPDF AGPL finding.
- **NOT DONE — mine, next session:**
  - Get `D-015` and `D-016` reviewed and marked `AGREED`. **`D-015` gates Antigravity's `D-022`**,
    so it is the blocking item for the whole topic-13 track.
  - **Review Antigravity's `D-017`** (topic 8, structured output and validation). It is drafted and
    waiting on me; I have not attacked it yet. It overlaps my D-015 and D-016 on schema and
    validation, so it is worth reading properly rather than skimming.
  - **Review `D-024`**, and answer Antigravity's open question: does Antigravity need its own
    pointer file? I did not create one because I do not know what Antigravity auto-loads.
  - Draft `D-019` (topic 10, tracing: Langfuse vs own JSONL/SQLite), `D-020` (topic 11, storage),
    `D-023` (topic 14, testing without per-run LLM spend). Not started. Direction already scoped:
    tracing must serve replayability plus per-step token and cost reporting plus a *visible* trace
    in the web demo, which is the constraint that decides Langfuse-versus-our-own; storage looks
    like SQLite plus a local file store for PDFs outside git, with no database server because
    user accounts are out of scope; testing should separate free deterministic tests from
    deliberately-run paid eval runs, and Gemini prompt caching is the lever that makes whole-document
    prompts affordable. None of that is researched yet — treat it as a starting hypothesis, not a
    finding.
- **NOT DONE — Antigravity's:** draft `D-018` (topic 9) and `D-021` (topic 12, including Claude's
  required synthetic profile set), draft `D-022` once `D-015` lands, and build
  `team/corpus-candidates.md` with **verified** URLs, issuer, year, page count, and hash. Do not
  download the PDFs into git.
- **Still owed to Claude:** the **batch review ping** once `D-015..D-023` are all `AGREED`, with
  `D-024` riding along. **That ping is still NOT sent and must not be sent yet**, because Claude
  reads only `AGREED` entries and nothing new has reached `AGREED`.
  A *status* message to Claude was sent this session (`msg_fd1599b3c789`, subject "T-002 status, no
  review requested yet - 3 corpus URLs are 404, blocking for the manifest") and deliberately asked
  for **no** review. Do not mistake it for the batch ping, and do not re-send it; it exists to
  warn Claude about the 404s and the PyMuPDF licence while that is still cheap to act on. Claude's
  inbox is `run:run_f4a5b3f23883` (a durable run mailbox, unlike the terminal-only peer mailbox),
  so it does not need re-pinging and survives the session ending.
- **BLOCKERS, gathered in one place so the next session does not have to infer them:**
  1. **Antigravity's `D-022` (topic 13) is gated on `D-015` reaching `AGREED`.** `D-015` is
     `PROPOSED` and waiting on Antigravity. This is the only hard dependency, and it blocks one
     topic, not the whole track.
  2. **`team/corpus-candidates.md` is blocked on verified URLs.** Antigravity owns it. Three
     `D-010` paths are 404 (constructed filename patterns, not missing documents) and must be
     re-found by search rather than by guessing another filename. Only four URLs are
     fetch-verified so far: BARC OCES-DGFS-2026, IIT KGP JMP 2025-26, DRDO `advt_152`,
     DRDO `advt_157`. A manifest padded to 25 rows with unverified patterns would look
     authoritative and be quietly wrong, so a short verified list beats a long speculative one.
  3. **`D-024` is `PROPOSED` and needs Antigravity's review.** Antigravity has now confirmed in
     `D-026` that its CLI also auto-loads `AGENTS.md` and that `D-024` "works seamlessly" with it.
     That **answers the open question in `D-024`**: Antigravity does **not** need its own pointer
     file. Treat that sub-question as closed; only the review of the entry itself is still open.
  4. **Nothing is blocked on Om.** No open question on `D-015` or `D-016` requires him. If the next
     session finds itself waiting on him, that is a scheduling fact, not a technical blocker, and
     it should not be logged as one.
- **Carry these forward, they are easy to get wrong:**
  - `AGENTS.md` now **shadows** `CLAUDE.md` for OpenCode (first match wins, no merge). Next session
    must follow the `AGENTS.md` pointer: read `.claude/rules/team-protocol.md` in full, then its
    "Resuming in a new session" section, which is what pulls in `CLAUDE.md` and the log tail.
  - Terminal handles from the protocol table are stale whenever a terminal restarts. Re-derive them
    with `orca terminal list --json` and match on `agentIdentity` **plus** `worktreePath` before
    messaging anyone — `agentIdentity` alone is ambiguous, because there are multiple `claude` and
    `opencode` terminals across other projects in the list. **This already bit us:** Antigravity's
    handle changed mid-session from `term_83c74f8f-…` (dead, send failed with *no live pane or
    durable Run/Dispatch mailbox*) to `term_5898bff5-22d5-4900-a8e8-c51e72dd69b1`. Confirmed live as
    of the 2026-09-28 session close. OpenCode's own handle in this worktree is
    `term_a23bc3f2-b17f-457a-bd9f-ce6e0c3f8e93`. Verify again next session; do not trust any of
    these, including this sentence.
  - **Two agents edited `D-025` in the same window.** Antigravity was observed updating the handoff
    entry concurrently with these edits. So the next session must **re-read `D-025` in full before
    editing it**, merge rather than overwrite, and expect its `DONE`/`NEXT` lists to have moved.
    Do not assume the version described here is still the current one on disk.
  - The measurement scripts and downloaded PDFs used for D-015 and D-016 live in a temp folder and
    will **not** survive. Every number is transcribed into the entries themselves, so nothing is
    lost — but re-measuring means re-downloading, and DRDO's site is slow and intermittently times
    out, so use a long timeout and retry rather than marking a document dead.
  - This log is UTF-8 without a BOM. Append with an explicit-UTF-8 editor. Do not use PowerShell
    `Add-Content`, which can corrupt the non-ASCII characters, and note that the Windows console
    renders em-dashes as `?` even when the file is clean — check with a byte-level U+FFFD count
    before "fixing" anything.
- Peer review: n/a — handoff note.
- Claude review: n/a — handoff note.


---

### D-026 — Antigravity Session Handoff & State at Pause (2026-09-28)
- Status: PROPOSED
- Note: Handoff note for session resumption; no peer review or Claude review required.
- **DONE this session:**
  - Resumed session cleanly per .claude/rules/team-protocol.md checklist: verified handles via orca terminal list --json and checked inbox.
  - Successfully contacted Claude's run inbox (
un:run_f4a5b3f23883) via Orca CLI (orca orchestration send).
  - Notified peer OpenCode (	erm_a23bc3f2-b17f-457a-bd9f-ce6e0c3f8e93) with active terminal handle.
  - Observed Claude Code paused on an interactive permission prompt in its terminal (	erm_92ac9396), and noted OpenCode API socket reconnection retry status.
  - Confirmed D-024 (T-003 AGENTS.md pointer file) works seamlessly with Antigravity CLI, which auto-loads AGENTS.md as well.
- **NEXT session (Antigravity):**
  - Peer review OpenCode's D-015 (PDF extraction: pypdf + pdfplumber) and D-016 (whole document context / no chunking) to reach AGREED.
  - Draft D-018 (Topic 9: hand-written loop vs LangGraph).
  - Draft D-021 (Topic 12: candidate profile + memo schemas + synthetic profile set).
  - Draft D-022 (Topic 13: web framework & deploy) once D-015 reaches AGREED.
  - Build verified manifest 	eam/corpus-candidates.md (excluding 404 URL patterns).
- **BLOCKERS / OPEN ITEMS:**
  - No blockers on Om.
  - D-022 is gated on D-015 reaching AGREED.
  - Batch ping to Claude for D-015..D-024 deferred until all entries reach AGREED.
- Peer review: n/a — handoff note.
- Claude review: n/a — handoff note.

---
### D-027 — Portable Agent Team Protocol Template (T-004)
- Status: AGREED
- Owner: Antigravity (initial edit pass), OpenCode (final fixes) · Reviewer: each other, 3 rounds
- Decision: `team/agent-team-protocol-TEMPLATE.md` is revised and accepted as the portable 3-agent
  coordination protocol. It stays generic and short, with every Orca command verified against the live
  CLI. Settled this round: peer-to-peer sends omit `--run` (a mismatched `--run` is rejected with a Run
  mismatch error); `--to run:{{RUN_ID}}` is used only for Claude; `{{ANTIGRAVITY_AUTOLOAD}}` = `agy`
  auto-loads `AGENTS.md` and `GEMINI.md` from the repo root, so one `AGENTS.md` pointer serves both
  OpenCode and Antigravity while Claude Code reads `CLAUDE.md`; handles are matched on
  `agentIdentity` **PLUS** `worktreePath`; all 9 send types are documented with `handoff` reserved for the
  pause ritual; bare-handle peer mail is flagged non-durable; shared-log discipline is announce-ID-then-
  append with explicit UTF-8 and no BOM; handoff notes stop consuming `D-xxx` numbers.
- Why: the template failed on the two errors that actually cost time, not on the happy path. Three
  PowerShell quoting/encoding failures came from long bodies and non-ASCII on one line, and a peer wake
  could not be confirmed. Three template claims were unverified or wrong: `--wait-submit` is accepted by
  old hosts that still answer `provider: unsupported`, so it cannot be relied on to prove delivery;
  `--types` filters only the `--wait` wake condition and never the returned delivery, and acking a batch
  acks every message in it, so unprocessed mail is lost; and the §1 role table carried unsourced vendor
  speed claims that the template's own §5 evidence rule forbids. Verified against `orca ... --help` and
  live sends on 2026-09-29, including a throwaway `run-create` that confirmed the `result.run.id` path.
- Alternatives rejected:
  - **Re-title the 2026-09-28 handoff to free `D-026` for T-004** (Antigravity's round-2 proposal) —
    rejected. The log is append-only, and `D-025` already cites `D-026` as the source for the Antigravity
    autoload finding, so re-titling would silently falsify that cross-reference and destroy the
    provenance for the placeholder this very entry ships. A number gap costs nothing; rewriting a landed
    entry costs the log its trustworthiness. T-004 is therefore `D-027`.
  - Keep `--run {{RUN_ID}}` on the peer-send example, as the template and this project's protocol both
    did — rejected. It presumes the sender is bound to that run; it worked for OpenCode and failed for
    Antigravity, so it encodes one team's accident as a rule.
  - Keep the role table's per-vendor speed adjectives — rejected as unsourced claims about specific
    tools, in a document whose §5 requires a source URL for facts.
- Peer review: 3 rounds. R1 (OpenCode, 11 points) + R1 (Antigravity, 6 points). R2: split on the peer
  `--run` rule — OpenCode split the finding from the prescription, Antigravity's simpler "omit `--run`"
  default was accepted with the failure mode retained; OpenCode conceded its own `--wait-submit` point
  against interest with live evidence, and Antigravity accepted. R3: one DEFEND on the `D-026`
  collision, resolved when Antigravity conceded and left `D-026` untouched. Antigravity then held the
  edit turn; OpenCode applied the final 5 fixes and re-verified encoding (no BOM, 0 U+FFFD).
- Claude review: CLAUDE-OK (2026-09-29). Template FINAL. Nit fixed by Claude: §8 watcher timeout
  (Claude's shell tool caps at 10 min, so ≤ 590000 ms, not 900000). Claude also synced this
  project's `.claude/rules/team-protocol.md` to the template's fixes (peer send without `--run`,
  handoff-note format, worktreePath matching). Good call keeping D-026 untouched.

---

### D-018 — Topic 9: Pipeline Orchestration — Hand-Written Python Loop vs LangGraph
- Status: AGREED
- Owner: Antigravity — Reviewer: OpenCode
- Decision: **Build a hand-written Python pipeline loop (`gatecheck/pipeline/runner.py`) using explicit dataclass/Pydantic state, deterministic step transitions, and lightweight step wrapper functions. Reject LangGraph, CrewAI, and LangChain.**
- Plain-language version:
  GateCheck's pipeline is a straight line with 3 steps: `extract_criteria` → `check_eligibility` → `draft_memo`. There are no dynamic multi-agent conversations, no cyclic graph paths, and no autonomous agent branching. What *does* matter is measuring every single token, timing each step, managing free-tier rate limits (15 RPM / 1,500 RPD) with exponential backoff on HTTP 429 (`RESOURCE_EXHAUSTED`), logging full replayable traces, and having test cases that explicitly trigger timeouts and retries. Wrapping 3 linear function calls in LangGraph adds a large transitive dependency footprint, hides control flow inside framework internals, and couples tracing to third-party cloud platforms—all to solve a graph orchestration problem this product does not have.
- Why hand-written wins on this project's core differentiator:
  1. **Auditability & Traceability:** CLAUDE.md non-negotiable requirement is per-run step tracing (inputs, outputs, model name, tokens, latency, retry counts, errors) saved to disk. In a hand-written loop, a lightweight context manager (`@trace_step`) records exact timings, token counts from the Gemini API response, and exceptions into a clean JSONL/SQLite structure with zero framework magic.
  2. **Strict Deterministic Arithmetic Boundary:** Step 2 is 100% deterministic Python arithmetic and rule evaluation, never the LLM (age boundary on cut-off dates, category relaxation stacking, CGPA-to-% conversion, GATE validity window). If a criterion contains ambiguous language that cannot be evaluated against profile fields by deterministic code, Step 2 flags it as `UNCLEAR` / `NEEDS_REVIEW` with an explicit reason—the LLM is never invoked in Step 2 to decide waivers, preventing non-deterministic eligibility flips.
  3. **Interview Defensibility for Om:** Om must walk through and defend every line of code in Indian GenAI Engineer interviews. An interviewer will respect a clean, well-tested, modular Python state machine with custom exponential backoff on HTTP 429 (`RESOURCE_EXHAUSTED`), quota guards (`QuotaExhaustedError`), and step timeouts (`StepTimeoutError`). Wrapping a 3-node linear sequence in LangGraph looks like unnecessary framework adoption.
  4. **Data Privacy & Zero Cloud Lock-in:** LangSmith tracing requires streaming candidate profile data and recruitment notices to a third-party cloud SaaS, with a limited 14-day retention window on its free tier. Hand-written tracing logs locally to JSONL/SQLite, keeping candidate data private and self-contained at ₹0.
  5. **Lightweight & Fast:** Zero framework lock-in, zero dependency breakage across library releases, and instantaneous startup for local CLI runs and unit tests.
- Alternatives considered and plain-language trade-offs:
  1. **LangGraph (REJECTED).** The industry standard for complex multi-agent graphs with cycles.
     - *Pros:* Built-in state persistence (`MemorySaver`, `SqliteSaver`), visual graph diagrams, time-travel debugging.
     - *Cons:* Large transitive dependency footprint (`langgraph`, `langchain-core`); opinionated state reducers that obscure simple variable passing; default tracing couples to LangSmith cloud SaaS; premature complexity for a 3-node linear DAG.
  2. **LlamaIndex Workflows (REJECTED).**
     - *Pros:* Event-driven async step architecture with typed events.
     - *Cons:* Same issue as LangGraph: introduces a heavy framework layer between our code and the Google GenAI SDK; designed around vector indices and RAG ecosystems, which GateCheck does not use (per D-016).
  3. **Temporal / Prefect (REJECTED).**
     - *Pros:* Industrial durable execution engine; resumes state across process crashes.
     - *Cons:* Requires a dedicated daemon/server process and external database infrastructure; massive operational overhead for a local CLI/web demo.
- Proposed Architecture for `runner.py`:
  - `PipelineState`: Pydantic model holding `notice_pdf_path`, `candidate_profile`, `criteria_list`, `evaluations`, `memo`, and `RunTrace`.
  - `run_pipeline(pdf_path, profile, config) -> PipelineResult`:
    1. Pre-flight check: rate limiter pacing (prevent exceeding 15 RPM).
    2. Step 1: `extract_criteria(pdf_text)` (LLM call with max 2 retries on Pydantic/grounding failure; exponential backoff on HTTP 429).
    3. Step 2: `check_eligibility(criteria, profile)` (100% deterministic Python arithmetic; ambiguous clauses marked `UNCLEAR` / `NEEDS_REVIEW`).
    4. Step 3: `draft_memo(criteria, evaluations, profile)` (LLM call formatting evidence and plain-English justification).
    5. Flush `RunTrace` to local SQLite/JSONL storage.
- What Om must decide:
  - Nothing blocking; pure engineering choice.
- Sources & Dates:
  - LangGraph Documentation (checked 2026-09-29): <https://langchain-ai.github.io/langgraph/>
  - LangSmith Pricing & Limits (checked 2026-09-29): <https://www.langchain.com/pricing>
  - Google Gemini API Rate Limits & Errors (checked 2026-09-29): <https://ai.google.dev/gemini-api/docs/rate-limits>
- Peer review: 1 round. Core ACCEPTED by OpenCode with 4 fixes applied: (1) replaced cost-cap model with free-tier quota model (rate limiter, exponential backoff on HTTP 429 `RESOURCE_EXHAUSTED`, `QuotaExhaustedError`); (2) enforced 100% deterministic rule arithmetic in Step 2 with zero LLM waiver evaluation (ambiguities become `NEEDS_REVIEW`); (3) replaced weak budget objection against LangSmith with data privacy and 14-day cloud retention limits; (4) disentangled framework alternatives into separate evaluations and dated all sources (2026-09-29).
- Claude review: CLAUDE-OK (2026-09-29). Hand-written loop is right for a 3-step line. Depends on the D-017 typed-rule fix for Step 2 to be implementable. Rate-limit numbers: same caveat as D-017 (config, re-verify).

---

### D-021 — Topic 12: Schemas (CandidateProfile, EligibilityMemo) and Synthetic Edge-Case Set
- Status: AGREED
- Owner: Antigravity — Reviewer: OpenCode
- Decision: **Define formal Pydantic v2 schemas for `CandidateProfile` and `EligibilityMemo`, establish a 10-profile synthetic test set covering statutory Indian recruitment/admission boundary conditions, and define per-notice dynamic boundary variants (exact cut-off date, +1 day overage, -1 day underage, GATE validity window). Expected ground-truth labels always derive from Om inspecting the PDF, never from profile text.**
- Plain-language version:
  GateCheck evaluates whether a specific student profile qualifies for a specific job/admission notice. To make the evaluation mathematically rigorous (and not just "vibes"), we need strict schema definitions for inputs and outputs, and a designed set of benchmark profiles that stress-test every edge case in Indian government recruitment rules. If the pipeline cannot correctly flag an age cutoff down to the day, or miscalculates 10-year PwD relaxation on top of 5-year SC relaxation, the screener fails its primary job.
- Schema Alignment with D-017 Typed Rules:
  Field names, data types, and enums in `CandidateProfile` match 1:1 with `D-017 RuleParameters`:
  1. **`CategoryEnum`**: `GENERAL`, `OBC_NCL`, `SC`, `ST`, `EWS` (exact identical strings in both schemas).
  2. **`Qualification`**:
     - `degree_title`: `str` (matched against `DegreeRuleParameters.allowed_degrees`)
     - `discipline`: `str` (matched against `DegreeRuleParameters.allowed_disciplines`)
     - `percentage`: `float | None` (matched against `DegreeRuleParameters.min_percentage`)
     - `cgpa`: `float | None` (matched against `DegreeRuleParameters.min_cgpa_10`)
     - `cgpa_scale`: `float` (default 10.0)
     - `university_conversion_formula`: `str | None` (e.g. `"(CGPA - 0.75) * 10"`)
     - `is_first_class`: `bool | None` (matched against `requires_first_class`)
     - `is_appearing`: `bool` (matched against `final_year_eligible`)
     - `expected_completion_date`: `date | None` (matched against `marksheet_submission_deadline`)
  3. **`GateRecord`**:
     - `year`: `int` (matched against `GateRuleParameters.valid_gate_years`)
     - `paper_code`: `str` (e.g. `CS`, `DA`; matched against `GateRuleParameters.allowed_paper_codes`)
     - `score`: `int` (matched against `GateRuleParameters.min_gate_score`)
     - `marks`: `float` (matched against `GateRuleParameters.min_gate_marks`)
     - `all_india_rank`: `int | None`
     - `is_qualified`: `bool`
  4. **`CandidateProfile`**:
     - `candidate_id`: Stable identifier (e.g., `PROF-01-BASELINE-OM`).
     - `full_name`: `str`
     - `dob`: `date` (evaluated against `AgeRuleParameters.cutoff_date` and relaxation logic)
     - `category`: `CategoryEnum`
     - `is_pwd`: `bool`
     - `pwd_disability_percent`: `float` (statutory 40.0% threshold benchmark)
     - `pwd_category`: `PwdCategoryEnum` (`LOCOMOTOR`, `VISUAL`, `HEARING`, `OTHER`)
     - `is_iit_graduate`: `bool` (evaluated against `iit_btech_cgpa_exemption_threshold`)
     - `qualifications`: `list[Qualification]`
     - `gate_records`: `list[GateRecord]`
     - `experience_months`: `int` (post-qualification experience, matched against `ExperienceRuleParameters`)
- Synthetic Profile Set Design (10 Profiles):
  1. `PROF-01-BASELINE-OM`: Category: `GENERAL`, B.Tech CSE: `[PLACEHOLDER]`, DOB: `[PLACEHOLDER]`, GATE 2026 CS ~380 / DA ~414: `[PLACEHOLDER — pending Om confirmation per CLAUDE.md]`. Never invent owner data; fields marked PLACEHOLDER until Om provides them.
  2. `PROF-02-AGE-BOUNDARY-EXACT`: Born on exact notice cut-off boundary date `T - A years`. (Expected: `MET` via inclusive `<=`).
  3. `PROF-03-RELAXATION-STACKING`: SC (5-yr relaxation) + PwD (10-yr relaxation) = 15 yrs total. Tests additive relaxation stacking per DoPT OM.
  4. `PROF-04-FINAL-YEAR-APPEARING`: B.Tech final semester appearing (graduation July 2026; marksheet deadline Dec 2026). Tests provisional eligibility.
  5. `PROF-05-CGPA-PERCENT-CONFLICT`: CGPA 6.4/10 from university where formula is `(CGPA - 0.75) * 10 = 56.5%` (fails 60%), but raw 10x is 64%. Tests formula precedence.
  6. `PROF-06-BRANCH-EQUIVALENCE`: B.Tech in "Information Technology" applying to post specifying "Computer Science & Engineering". Tests branch mapping equivalence.
  7. `PROF-07-EXPIRED-GATE-YEAR`: GATE attempt from `Y_min - 1` applying to notice requiring `[Y_min..Y_max]`. Tests 3-year validity window expiration.
  8. `PROF-08-IIT-BTECH-EXEMPTION`: IIT B.Tech with CGPA 8.2 without GATE score applying to IIT M.Tech brochure. Tests GATE waiver rule.
  9. `PROF-09-OBC-NCL-DATE-INVALID`: OBC candidate whose NCL certificate was issued prior to April 1 of the financial year. Tests document validity date requirements.
  10. `PROF-10-SUB-BENCHMARK-PWD`: PwD candidate with 35% disability (< 40% statutory benchmark). Tests that PwD reservation/relaxation is denied if disability < 40%.
- Notice-Relative Boundary Variant Pairing:
  - Exact age boundaries and GATE validity windows are notice-relative: cut-off dates differ across notices (e.g. BARC 2026-08-01 vs DRDO 2025-03-24).
  - Test framework pairs notices using a dynamic generator `generate_boundary_profiles(notice_metadata: NoticeMetadata) -> list[CandidateProfile]`:
    - `PROF-AGE-EXACT`: `dob = notice.age_cutoff_date - max_age_years` (Expected: `MET`).
    - `PROF-AGE-OVER`: `dob = (notice.age_cutoff_date - max_age_years) - 1 day` (Expected: `NOT_MET`).
    - `PROF-AGE-UNDER`: `dob = (notice.age_cutoff_date - max_age_years) + 1 day` (Expected: `MET`).
    - `PROF-GATE-EXPIRED`: `gate_year = min(notice.valid_gate_years) - 1` (Expected: `NOT_MET`).
    - `PROF-GATE-VALID`: `gate_year = max(notice.valid_gate_years)` (Expected: `MET`).
  - **Ground Truth Invariant**: Expected labels are never inferred from profile descriptions; they are drafted by OpenCode reading the PDF and verified by Om reading the PDF (per D-007 and CLAUDE.md).
- Sources & Dates:
  - DoPT Information Document on Grant of Relaxation of Upper Age Limit for Persons with Disabilities (serving `application/pdf` 254 KB, checked 2026-09-29): <https://documents.doptcirculars.nic.in/D2/D02est/Information%20document%20on%20grant%20of%20relaxation%20of%20upper%20age%20limitMystc.pdf> with official portal cross-reference <https://doptcirculars.nic.in/Default.aspx?URL=9kxp2fN1VRBHARCH>
  - GATE 2026 Official FAQs, IIT Guwahati (Scorecard validity for three years, checked 2026-09-29): <https://gate2026.iitg.ac.in/faqs.html>
- Peer review: Round 1 accepted. Round 2 (OpenCode, 2026-09-29): ACCEPTED — PLACEHOLDER discipline for PROF-01 Om fields is right and preserves the CLAUDE.md GATE 2026 fact without inventing data; two-tier profile pairing (fixed generic set + per-notice `generate_boundary_profiles` exact/+1/-1/GATE-window variants) makes the edge set notice-relative and durable; ground-truth invariant (labels from Om reading the PDF, never from profile text) holds. Schema parity with D-017 `rule_parameters` confirmed, including the two Round-2 additions (`min_pwd_disability_percent`, `cgpa_percentage_precedence`). Set AGREED.
- Claude review: CLAUDE-OK (2026-09-29, round 2). PLACEHOLDER discipline + per-notice boundary generator resolve round 1. Carried into PLAN.md: PROF-05's expected outcome depends on whether the notice's degree rule is a disjunction (see D-017 review); generator expectations are Step-2 unit-test oracles, while eval labels stay Om-checked from the PDF. Om supplies PROF-01 facts during planning.

---

### D-022 — Topic 13: Web Demo Framework & Deployment Architecture
- Status: AGREED
- Owner: Antigravity — Reviewer: OpenCode
- Decision: **Build the web demo using Streamlit (`gatecheck/ui/app.py`) for the local interface and deploy to Streamlit Community Cloud (or Hugging Face Spaces) at ₹0 cost. Reject FastAPI+React, Next.js, and Gradio.**
- Plain-language version:
  The web demo has one clear purpose: let Om (and prospective interviewers) upload or pick a notice PDF, select a synthetic candidate profile (from D-021), click "Run Screener", and inspect:
  1. The final eligibility memo (verdict, justification, criteria breakdown).
  2. The full step-by-step trace (tokens per step, latency, model used, cost in ₹0, intermediate JSON schemas).
  3. Side-by-side text/PDF view showing the exact cited pages.
  Streamlit delivers this in ~200 lines of pure Python with zero frontend build tooling (no Node.js, npm, Webpack, or Tailwind). It offers native expanders (`st.expander`) for trace inspection, JSON visualizers (`st.json`), and easy deployment on Streamlit Community Cloud tied directly to the GitHub repo.
- Plain-language trade-offs and alternatives considered:
  1. **Streamlit (Recommended):**
     - *Pros:* 100% Python, rapid iteration; built-in widgets for file uploading, side-by-side columns (`st.columns`), JSON inspection, tabs, and metrics cards; free one-click deployment via Streamlit Community Cloud; zero frontend maintenance overhead.
     - *Cons:* Stateful reruns require careful use of `st.session_state`; not intended for high-concurrency multi-user production apps (which is explicitly out of scope per CLAUDE.md).
  2. **Gradio (REJECTED):**
     - *Pros:* Native support on Hugging Face Spaces; rapid form prototyping.
     - *Cons:* Layout customization is rigid; collapsible trace logs and multi-tab structured memos look less polished than Streamlit's native dashboard layout primitives.
  3. **FastAPI + React / Next.js (REJECTED):**
     - *Pros:* Fully decoupled production frontend/backend architecture.
     - *Cons:* Massive overhead for a single-user demo: requires setting up Node/React, writing custom CSS, managing API CORS/routes, and hosting two separate services (or building Docker containers). Violates the priority to finish Phase 0-7 cleanly without yak-shaving.
  4. **FastAPI + Jinja2 / HTMX (REJECTED as primary):**
     - *Pros:* Pure Python backend with lightweight server-rendered HTML.
     - *Cons:* Still requires writing HTML templates and CSS styling; Streamlit provides a richer, more polished dashboard appearance out of the box in less development time.
- Demo Interface Layout & Execution Plan:
  - **Left Sidebar:** Upload custom PDF or select from corpus (e.g. BARC OCES 2026, DRDO 157, IIT KGP); select candidate profile (from the 10 synthetic profiles in D-021); API settings (model selection: Gemini Flash free tier).
  - **Main Area (Tabs):**
    - *Tab 1 — Eligibility Memo:* Headline Verdict badge (APPLY in green / SKIP in red / NEEDS_REVIEW in yellow), executive summary justification, criteria breakdown table (status, page cite, quote, candidate evidence), document checklist.
    - *Tab 2 — Execution Trace & Observability (The Differentiator):* Total tokens, latency, cost estimate (₹0), per-step breakdown table (step name, duration, input tokens, output tokens, retry count), raw JSON trace download button. Rendered natively from the SQLite/JSONL `TraceSink` (D-019).
    - *Tab 3 — Side-by-Side PDF & Extracted Grounding:* Two-column layout (`st.columns([1, 1])`). Left column displays extracted criteria cards with highlighted quotes. Right column renders the exact PDF page cited using `st.components.v1.html` embedding a local PDF viewer iframe (`<iframe src="/pdf_file#page=N">`) or PDF.js canvas. The page position is kept in sync with the selected criterion via `st.session_state["selected_page"]`.
    - *Tab 4 — Extracted Criteria & Schema Contract:* Raw validated JSON output from Step 1 (`CriteriaCollection`).
  - **Quota Caching Discipline:**
    - Because Streamlit executes top-to-bottom on every widget click, `PipelineRunner.run_pipeline` is decorated with `@st.cache_data` keyed on `(pdf_hash, profile_id)`. Pipeline results and the `TraceSink` run record are cached in `st.session_state` so interacting with tabs, filters, or criterion dropdowns does NOT re-trigger LLM calls or consume free-tier API quotas.
- What Om must decide:
  - Nothing blocking; pure engineering choice.
- Sources & Dates:
  - Streamlit API Reference (checked 2026-09-29): <https://docs.streamlit.io/develop/api-reference>
  - Streamlit Community Cloud Deployment Guide (checked 2026-09-29): <https://docs.streamlit.io/deploy/streamlit-community-cloud>
  - Streamlit Caching Documentation (`st.cache_data` / `st.cache_resource`, checked 2026-09-29): <https://docs.streamlit.io/develop/concepts/architecture/caching>
- Peer review: 1 round. ACCEPTED by OpenCode with 2 specifications applied: (1) Defined exact PDF side-by-side viewer mechanism via st.components.v1.html iframe/#page=N synchronized with st.session_state; (2) Added st.cache_data / st.session_state caching discipline to prevent accidental LLM re-invocation on UI widget reruns.
- Claude review: CLAUDE-OK (2026-09-29). Streamlit fine. Two notes for PLAN: (a) a public demo spends Om's free-tier quota on every visitor click — ship a demo mode that serves recorded runs (D-023 fixtures) by default and gates live runs; (b) iframe `#page=N` PDF embedding is browser-dependent in Streamlit — check the current native PDF component before building PDF.js by hand.

---
### D-019 — Topic 10: Tracing and Observability — Langfuse vs Own JSONL/SQLite
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: Build tracing as **our own append-only JSONL writer plus a SQLite index**, behind a single
  `TraceSink` interface. Reject Langfuse as a Phase 1 dependency; keep it reachable later as an
  alternative `TraceSink` implementation without touching any call site.
- The problem in plain language:
  A run of GateCheck makes several paid-quota LLM calls, can retry, and can hit free-tier rate limits.
  When something goes wrong we must be able to answer, after the fact: which model was called, what was
  sent, how many tokens it used, how long it took, how many retries happened, and exactly which error
  class occurred. If we cannot show that, we cannot debug a wrong eligibility answer, and we cannot
  show an interviewer that the system is real rather than a demo. This is the observability
  differentiator named in CLAUDE.md.
- Alternatives and plain-language trade-offs:
  1. **Own JSONL + SQLite via the standard library — RECOMMENDED.**
     - *How it works:* every step writes one JSON object per line to a run-scoped `.jsonl` file
       (append-only, crash-safe, human-readable with no tooling), and inserts a row into a SQLite table
       for querying. `sqlite3` and `json` ship with Python, so this adds zero dependencies.
     - *Pros:* nothing to install and nothing to keep running; the file is readable with `notepad` or
       `grep`, which matters when Om has to show a trace in an interview; total cost is roughly
       150 lines that Om can explain line by line; works fully offline; no third party ever sees notice
       text or candidate data; retry counts and quota events are recorded exactly as we define them.
     - *Cons:* no pretty trace UI, so inspecting a run means querying SQLite; we must write the
       aggregation queries ourselves; no built-in prompt-versioning or scoring UI.
  2. **Langfuse, self-hosted — REJECTED for Phase 1.**
     - *How it works:* an open-source LLM observability platform. We would run it locally via Docker
       Compose and point a Python SDK at it.
     - *Pros:* a genuinely good trace UI, which is the most impressive thing we could show a
       interviewer; handles prompts, scores and evaluations as first-class concepts; actively
       maintained, currently at v4.
     - *Cons, and this is the decisive one:* per Langfuse's own self-hosting documentation, a
       self-hosted instance runs **six components** — the `langfuse` web container, the `langfuse`
       worker, PostgreSQL for transactional data, ClickHouse for trace/observation data, Redis or
       Valkey for cache and queueing, and S3 or equivalent blob storage for raw events. That is six
       moving parts to stand up, upgrade, seed and keep healthy, purely so a human can look at traces
       for a pipeline that has three steps. Some features additionally require a paid license key.
     - *Plain-language cost of that:* the first time the Docker stack fails, the debugging session goes
       to ClickHouse or to a stale Redis queue rather than to GateCheck. For a portfolio project whose
       main asset is a clean, defensible repository, that is a bad trade.
  3. **Langfuse Cloud free tier — REJECTED.**
     - *Pros:* zero infrastructure, fastest possible start, keeps the nice UI.
     - *Cons:* sends real admission notices and real candidate profiles to a third-party service; free
       tiers carry retention limits, so a trace we need for a bug report may already be gone; a demo
       that silently stops working when a free quota is hit is a bad demo; and it makes the repo
       non-reproducible for an interviewer who does not want to sign up.
  4. **Do nothing / print to stdout — REJECTED.**
     - *Pros:* zero work.
     - *Cons:* interleaved stdout from three pipeline steps is not a durable record, cannot be queried
       after the fact, and cannot answer the retry and quota questions above.
- The design decision that makes this reversible:
  Define one interface, `TraceSink`, with methods roughly `start_run`, `record_step`, `record_retry`,
  `record_quota_event`, `finish_run`. The pipeline only ever calls `TraceSink`; it never writes files or
  opens a database directly. The SQLite/JSONL implementation is the first one. If we later want the
  Langfuse UI, we write a second implementation of the same interface and change one line at startup.
  The cost of this abstraction is about 20 lines. That is cheap insurance against being wrong, and it
  is the honest way to reject a tool without closing the door.
- What the trace must record (this is the checklist other topics depend on):
  - `run_id`, `step_name`, `started_at`, `ended_at`, `latency_ms`
  - `model` actually used, not the one we intended to use
  - `input_hash` and `output_hash` (so runs are comparable without storing candidate PII twice)
  - `prompt_tokens`, `completion_tokens`, `total_tokens` read from the API response
  - `retry_count` and the validation error text that triggered each retry
  - `quota_events`: every HTTP 429 with its `Retry-After`, so rate limiting is visible rather than inferred
  - `error_class` using a fixed taxonomy, so failures are groupable rather than free-text
- Cross-references: this entry supplies the recording surface that D-017 fix 4 (post-validation retry
  counts) and D-018 fix 1 (quota exhaustion instead of a cost-cap error model) both depend on. If this
  entry is rejected or changed, those two fixes must be revisited.
- What Om must decide:
  - Nothing blocking. One judgement call worth naming: whether Om wants to show a trace UI in interviews
    badly enough to accept the six-component Docker stack later. We recommend deferring that until the
    pipeline is correct, because a trace of a wrong answer is not a compelling demo.
- Sources and dates:
  - Langfuse self-hosting documentation, page last updated 2026-09-09, fetched and verified 2026-09-29:
    <https://langfuse.com/self-hosting>. Supports the six-component architecture claim: the documented
    stack is web container, worker, PostgreSQL, ClickHouse, Redis/Valkey, and S3/blob storage.
  - Langfuse v4 release announcement, 2026-08-17, referenced from the self-hosting page, fetched 2026-09-29:
    <https://langfuse.com/changelog/2026-08-17-langfuse-v4>. Supports the current-major-version claim.
  - Python standard library `sqlite3` and `json` modules: part of the standard library, no external
    source required. UNVERIFIED against a specific Python version pin; should be pinned when we choose
    the interpreter version.
- Peer review: 1 round. ACCEPTED by Antigravity. Own append-only JSONL + SQLite index behind a clean TraceSink interface is the exact right choice. Defensibility points accepted and reinforced: (1) Dual durability guarantee: JSONL is the crash-resilient append-only truth; SQLite is the query index that can be rebuilt from JSONL at any time; (2) Trace UI solved at zero overhead: D-022 Streamlit demo (Tab 2) directly queries SQLite / parses the JSONL trace, rendering visual step breakdown, token metrics, and retry logs without needing Langfuse's 6-container Docker footprint; (3) Failure taxonomy explicitly unifies QuotaExhaustedError (D-018), ExtractionValidationError (D-017), StepTimeoutError, and QuoteGroundingError.
- Claude review: CLAUDE-OK (2026-09-29). TraceSink interface + JSONL truth / SQLite index is clean and reversible. Good.

---
### D-020 — Topic 11: Storage — SQLite for Structured State, JSONL for Raw Traces, PDFs On-Demand
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: **Use one SQLite database file as the single store for all structured pipeline artifacts
  (traces, eligibility memos, evaluation labels, the candidate-profile set), keep the raw trace stream
  in append-only JSONL (see D-019), and never store notice PDFs in the repository — cache them on
  demand in a gitignored folder keyed by URL hash.**
- The problem in plain language:
  GateCheck produces data that must survive the demo: for every notice and candidate we want the
  trace, the memo, the labelled verdict, and the profile that was used. We also need to re-run the
  evaluation later to check precision and recall. If each piece sits in a different bespoke file
  format in different folders, there is no single way to ask a question like "which profiles did the
  pipeline mark APPLY that Om labelled SKIP?". A single storage decision now avoids inventing one
  piecemeal during Phase 2-4.
- Alternatives and plain-language trade-offs:
  1. **Single SQLite database (gatecheck.db) — RECOMMENDED.**
     - *How it works:* `sqlite3` ships inside Python (stdlib), so no dependency is added. One file
       holds several tables: `traces`, `memos`, `profiles`, `labels`. SQL gives us joins and filters
       for the precision/recall evaluation for free.
     - *Pros:* zero setup, zero running service, one file to back up or delete; the query language is
       standard and interview-legible; it overlaps naturally with D-019, where SQLite is already the
       trace index.
     - *Cons:* a single file needs a tiny bit of discipline (use one connection per write, or
       `WAL` mode) to avoid lock errors; not a network database, so no concurrent multi-process
       writes — an acceptable constraint for a single-user pipeline.
  2. **Plain JSON/JSONL files for everything — REJECTED.**
     - *Pros:* simplest possible, human-readable, no schema to design.
     - *Cons:* every cross-cutting question (which memos reference notice Z, compare verdicts vs
       labels) becomes a manual grep-and-join in Om's head. That is precisely the query the eval
       phase needs; doing it by hand is error-prone and slow. JSONL stays for the raw trace (D-019)
       because it is append-only and typed per event, but it is not a good relational store.
  3. **PostgreSQL — REJECTED.**
     - *Pros:* industry-standard, robust concurrency.
     - *Cons:* requires installing and babysitting a server, costs memory, adds nothing for a
       single-user local pipeline. Same over-engineering reasoning as the Langfuse six-container
       stack in D-019. It can be swapped in later behind the same SQL abstraction if ever needed.
  4. **Parquet / Arrow — REJECTED.**
     - *Pros:* fast columnar analytics for huge datasets.
     - *Cons:* adds dependencies, needs read/write tooling to inspect, and our dataset is tens of rows
       per notice, not billions. Premature optimization.
- How the pieces fit together (this is the part Om should be able to explain):
  - *Input PDFs:* not stored in git at all. The corpus manifest (team/corpus-candidates.md) keeps the
    verified URL list; the pipeline downloads a notice to a gitignored `data/pdfs/<url_hash>.pdf`
    cache on first use and reuses it. This keeps the repo small and the corpus reviewable as text
    links while still giving us local PDFs to parse.
  - *Raw trace stream:* append-only JSONL per run (D-019), the crash-safe record of exactly what
    happened.
  - *Structured query state:* SQLite, written at the end of each step from the same objects the
    JSONL holds — the DB is an index and query layer over the trace, not a second source of truth.
  - *Candidate profiles and labels:* the 10-profile set from D-021 lives as a committed JSON file
    (it is test input, needs to be in git); Om's labels are added to SQLite so eval queries can join
    them with memos.
- Cross-references: D-019 already chose SQLite as the trace index; this entry extends that choice to
  the rest of the structured state so there is exactly one database and one rationale. D-021 supplies
  the schema of the profile set stored here. D-023's eval queries read from this database.
- What Om must decide:
  - Nothing blocking. One preference worth stating: whether to gitignore both the SQLite file and the
    PDF cache (recommended) so the repo never contains generated data, or commit a seed database so
    an interviewer can browse a pre-populated run. We recommend gitignore, because a clean repo with
    the corpus manifest plus the 10-profile JSON demonstrates the design better than a squashed binary.
- Sources and dates:
  - Python stdlib `sqlite3` module: part of the standard library, no external dependency. UNVERIFIED
    against a specific Python version pin; pin the interpreter during Phase 1.
  - No other external claim is made; storage design is internal architecture.
- Peer review: 1 round. ACCEPTED by Antigravity. Architecture is clean, minimal, and fully interview-defensible. Two operational specifications added: (1) Mandate WAL mode (`PRAGMA journal_mode=WAL;`) and a busy timeout (`5000` ms) in the SQLite connection factory so concurrent reads from the Streamlit UI (D-022) never lock writes from pipeline execution; (2) Gitignore `gatecheck.db` and provide a clean schema initialization DDL script (`migrations/001_initial.sql` or Python function) so fresh repository clones bootstrap instantly.
- Claude review: CLAUDE-OK (2026-09-29). Agree: gitignore DB + PDF cache, commit profiles JSON + DDL. WAL + busy timeout accepted.

---
### D-023 — Topic 14: Testing Without Per-Run Spend — Replay Fixtures, not Live Calls
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: **Split the test suite into two deliberate modes. REGRESSION (replay fixtures): recorded
  request/response pairs answer instead of the network — offline, deterministic, free, runs on every
  commit. EVAL (live): a deliberate, quota-budgeted run over the labelled corpus is the ONLY source of
  the headline precision/recall/token numbers; it records itself as it runs, and the recording becomes
  the next round of regression fixtures. Unit tests cover the deterministic Step-2 scoring boundary and
  verdict logic offline; a single opt-in smoke test makes one live free-tier call.**
- The problem in plain language:
  The project has three things that are expensive to test naively: (1) structured-output calls to the
  model, (2) the arithmetic that turns extracted criteria into an eligibility verdict, and (3) the
  trace/eval pipeline that records all of it. If every test run calls the free-tier API, tests are
  slow, they depend on the network, they are rate-limited, and they hide what testers usually need —
  does my change break the deterministic logic or the output shape. Om never gets a test suite he can
  run 50 tracks a day for free; and the ₹0 budget is a hard constraint.
- Alternatives and plain-language trade-offs:
  1. **Replay-fixture testing — RECOMMENDED.**
     - *How it works:* Record one real run per scenario once, save the exact request/response pairs
       (input prompt, response JSON, token counts) as committed JSON fixture files, then during tests
       an injected fake transport answers from those fixtures instead of the network. The pipeline
       code is unchanged; only the transport is swapped. This is the standard recording
       (VCR-like) idiom.
     - *Pros:* runs offline, instantly, forever-free, deterministic — the exact three properties a
       regression suite needs; a model-API change is visible as a fixture-label change rather than a
       mystery test failure; fixtures double as readable documentation of what the model returns.
- *Cons:* fixtures freeze the model generation's behaviour at the time they were recorded (so a
        genuinely improved model is not reflected until fixtures are re-recorded — a deliberate,
        documented step); writing the fake transport takes a little code (~30 lines) once.
  2. **Live-API testing per run — REJECTED.**
     - *Pros:* always tests the real model.
     - *Cons:* slow (seconds each), network-dependent, rate-limit-flaky, and paid-quota-consuming
       (the free tier is a hard cap, not a toy). Exactly what the differentiator must not be.
  3. **Mock everything by hand, no fixtures — REJECTED.**
     - *Pros:* zero recording step.
     - *Cons:* hand-written mocks quickly drift from real responses (wrong fields, wrong shapes), so
       tests pass against a fantasy API; fixtures capture real responses, mocks capture imagination.
  4. **Dependency-inject a fully synthetic LLM — REJECTED.**
     - *Pros:* full control of 100% of outputs.
     - *Cons:* synthetic outputs cannot exercise boundary behaviour the real schema enforces (e.g.
       grounding failures, partial JSON, long justification text); fixtures at least come from the
       real system under test.
- What the layers actually are (so the suite is fast AND meaningful):
  1. *Unit (fastest, zero I/O):* pure functions for verdict math, boundary arithmetic, schema
     validation, quote-grounding checks. No model at all.
  2. *Regression (replay):* pipeline steps against recorded fixtures — a full run reproduces memos
     byte-for-byte, so regressions are caught as diffs. Runs on every commit; offline, free.
  3. *Eval run (LIVE, deliberate, quota-budgeted):* the ONLY producer of the headline precision/recall/
     token numbers, run over the labelled corpus against the real API. Every call is recorded while it
     happens (TraceSink, D-019), so the run itself becomes the next round of regression fixtures —
     one recording serves both analyses, and the live numbers are never estimated from cached data.
  4. *Smoke (opt-in `--live`):* ONE real call to confirm auth+tier are working, run manually before
     a demo, never in CI.
- Quota arithmetic for one full live eval (does it fit the free tier, and in how many days?):
  - *Step 1 (extraction):* ONE call per notice, profile-independent -> 25 calls for the current
    25-notice eval corpus. The extraction result is cached (SQLite, per D-020), so re-runs and
    multi-profile passes never re-pay it.
  - *Step 2 (verdict):* deterministic Python, ZERO LLM calls.
  - *Step 3 (memo):* ONE call per notice x profile -> 25 x N_profiles calls.
  - *Total calls per full eval = 25 + 25 x N.* With the 10-profile set from D-021: 25 + 250 = 275
    calls. With a quick 3-profile pass: 25 + 75 = 100 calls.
  - *Token estimate:* a born-digital notice's text is ~1-2k input tokens; the extraction prompt adds
    ~1-2k; a Step-3 call (profile + criteria + memo prompt) runs ~2-3k. So a full eval is roughly
    25 x ~4k + 250 x ~3k ~ 850k input tokens. Free-tier TPM (typically >10^6/min) does NOT bind here;
    **RPD is the binding constraint**.
  - *How many days:* days = ceil(275 / RPD_read_from_config). At RPD=1500 (older published figure)
    -> 1 day; at RPD~250 (a 2026 community-measured free-tier value) -> 2 days; near the reported
    20/day floor it would take ~2 weeks. Because per-project RPD is read live (per D-017's
    `gatecheck/config.py`) and RPD counts reset daily (midnight Pacific), the eval runner computes
    days = ceil(calls/RPD_cfg) and warns before starting. Numbers here are orders of magnitude,
    refined after the first recorded run.
- What Om must decide:
  - Nothing blocking. Useful for Om to know: after a model update (e.g. a new
    Gemini version) we intentionally re-record fixtures, check diffs, and commit them, so the test
    suite tracks the real system instead of pretending the model never changes.
- Sources and dates:
  - I instrumented nothing yet; the ReplayFixture idiom is the VCR pattern for HTTP-testing. The
    reference implementation and honest example: pytest documentation describing fixtures and
    tmp_path (checked 2026-09-29): <https://docs.pytest.org/en/stable/getting-started.html>; the
    VCR-inspired pattern for replaying HTTP interactions is implemented by the `pytest-recording`
    plugin (checked 2026-09-29): <https://github.com/kiwicom/pytest-recording> and its pytest
    docs <https://pytest-recording.readthedocs.io>. Both UNVERIFIED as exact versions;
    pin when pytest is added in Phase 1.
  - The layer split and opt-in live smoke test are internal design, no external claim.
- Peer review: Round 1 ACCEPTED. Round 2 ACCEPTED by Antigravity (2026-09-29): all Claude review issues cleanly resolved — live eval vs replay regression split is crisp, quota arithmetic (275 calls / ~850k tokens) proves free-tier feasibility, and all nits fixed.
- Claude review: CLAUDE-OK (2026-09-29, round 2). Live-eval vs replay-regression split is right; RPD as the binding limit is right. Corrections carried into PLAN.md: Step 1 sends the whole notice (D-016) — brochures are ~19k-68k tokens, not ~4k, so Step-1 input is ~0.5-0.7M tokens per full eval; per-notice boundary variants (D-021, ~5 per notice) add ~125 Step-3 calls (~400 total). Plan must include a mitigation if RPD is at the low end (cache Step-1 per notice; consider deterministic memo template with LLM only for the justification paragraph).
- Owner fix (OpenCode, 2026-09-29): rewrote Decision/Problem to split REGRESSION (replay) from EVAL (live, deliberate, quota-budgeted); rewrote Layer 3 as the live eval run (headline numbers only from live runs; every call recorded via TraceSink so the run becomes the next regression fixtures); added quota arithmetic (calls = 25 + 25xN, tokens ~850k for N=10, days = ceil(275/RPD_cfg), TPM non-binding, RPD binding, read live per D-017); fixed nits: Step-2 scoring boundary, dropped the Topic-6 precision/recall claim (eval now explicitly the labelled-corpus precision/recall), corrected pytest-recording to <https://github.com/kiwicom/pytest-recording>, replaced 'December-era' with 'the model generation's behaviour at recording time'.

---

### D-028 — Balanced Corpus Manifest: 50/50 Multi-Page Brochure and Recruitment Notice Mix
- Status: AGREED
- Owner: Antigravity — Reviewer: OpenCode
- Decision: **Rebalance `team/corpus-candidates.md` from a DRDO-heavy set (93% DRDO) to a balanced 50/50 mix: 14 multi-page academic brochures & major PSU-via-GATE recruitment notifications (IIT Madras 110p, IIT Kharagpur 86p, BARC 42p, IIT BHU 33p, IIT Roorkee 32p, IIT ISM Dhanbad 18p, IOCL 13p, NIT Warangal 11p, PowerGrid 9p, NPCIL 4p, IISc 4p) + 16 diverse DRDO RAC recruitment notices (1-20 pages, covering Scientist 'B', Senior Scientist, lateral appointments, revised corrigenda). Total: 30 live, born-digital documents, 100% fetch-verified on 2026-09-29.**
- Why: DRDO notices are short (1-8 pages) and follow a standardized template. The hardest extraction challenges (complex disjunctions / OR-rules across multiple qualifying degrees, inter-departmental eligibility matrices, qualifying GATE score percentiles, and IIT B.Tech CGPA waivers) live in long academic brochures and PSU recruitment packages. An evaluation corpus skewed 93% towards DRDO risks artificially inflating precision/recall numbers. Balancing the corpus 50/50 between brochures (up to 110 pages) and notices ensures the evaluation rigorously stress-tests the multi-step pipeline across genuine real-world document diversity without metric inflation.
- Alternatives rejected:
  1. *Keeping the 28 DRDO + 2 brochures set* — rejected: 93% DRDO homogeneity distorts benchmark validity.
  2. *100% brochures* — rejected: ignores the high volume of concise PSU/defence recruitment notices that form an essential part of an applicant's screening workflow.
- What Om must decide: Nothing blocking. Om will sample from this balanced pool to label ground truth.
- Sources and dates: All 30 URLs live-tested with HTTP 200 OK, `application/pdf`, `%PDF` magic bytes, and measured with `pypdf` on 2026-09-29. Manifest committed in `team/corpus-candidates.md`.
- Peer review: (OpenCode, 2026-09-29) ACCEPTED — rebalance directly answers the 93% DRDO-skew risk; hardest extraction challenges (multi-degree OR-rules, inter-departmental matrices, GATE percentiles, CGPA waivers) are indeed brochure-side, and the split keeps the concise-notice class represented. Spot-verified 15/30 URLs independently: BARC, IITKGP, POWERGRID x2, IOCL x2, NPCIL, IITM, IITBHU, IITR, IITISM, NITW, IISc x2, DRDO 145/152/156 — all `application/pdf` with `%PDF` magic bytes as claimed. Manifest columns (issuer/year/pages/verify date) complete. Set AGREED.
- Claude review: CLAUDE-OK (2026-09-29). Balance fixed (14 brochures/PSU + 16 DRDO). Claude spot-checked 4 non-DRDO URLs: all %PDF. Nit: `IISc MTech_MDes_seat_matrix.pdf` is a seat table, not eligibility text (close to the deferred cutoff-table family, scope b) — keep it in the collection set only, or swap it for an IISc eligibility brochure in the labelled set.

---

### D-029 — Formal Schema Contracts: Criterion, CandidateProfile, EligibilityMemo, and RunTrace (T-005)
- Status: AGREED
- Owner: Antigravity — Reviewer: OpenCode
- Decision: **Define and publish comprehensive, field-by-field Pydantic v2 schema contracts in `docs/schemas.md` for all GateCheck data entities: `Criterion` (with typed `AgeRuleParameters`, `DegreeRuleParameters`, `GateRuleParameters`, `ExperienceRuleParameters`), `CandidateProfile` (with `Qualification`, `GateRecord`, `is_indian_citizen`), `EligibilityMemo` (with `final_verdict` [`APPLY`, `SKIP`, `NEEDS_REVIEW`], 3-tier aggregation hierarchy, and `EXEMPTION_RULE` resolution), `RunTrace`, and `ProvenanceRecord` (with `was_modified_by_om`, `original_draft_value`). Explicitly formalize DISJUNCTION semantics (alternative qualifying degree routes evaluate via logical OR; mandatory conversion formulas apply only when no independent CGPA cutoff option exists).**
- Why: GateCheck's multi-step architecture strictly separates stochastic extraction (Step 1) from deterministic Python scoring (Step 2) and synthesis (Step 3). Without formal, typed parameter contracts (`rule_parameters`), Step 2 arithmetic cannot execute deterministically. Documenting the complete schema contracts in `docs/schemas.md` ensures consistent validation, accurate quote grounding, unambiguous evaluation logic, and uniform observability recording in `TraceSink`.
- Alternatives rejected:
  1. *Loose dictionary interfaces without typed sub-models* — rejected: causes silent runtime key/type errors and prevents static type verification.
  2. *Free-text criteria without typed parameter structs* — rejected: Python arithmetic cannot compute over arbitrary English sentences.
  3. *Enforcing conversion formulas globally over independent CGPA thresholds* — rejected: violates official brochure semantics (e.g. IIT Bombay A.5.1) where alternative qualifying routes are disjunctive (MET if any route qualifies).
- What Om must decide: Nothing blocking. Om will provide personal baseline facts for `PROF-01-BASELINE-OM` during planning.
- Sources and dates: Pydantic v2 Documentation (<https://docs.pydantic.dev/latest/>, 2026-09-29), D-017, D-019, D-021, and Claude's T-002 review notes. Document landed at `docs/schemas.md`.
- Peer review: Round 1 ACCEPTED with 3 fixes. Round 2 (OpenCode, 2026-10-02): ACCEPTED — verified `final_verdict` (`APPLY`, `SKIP`, `NEEDS_REVIEW`) added to `EligibilityMemo` with explicit 3-tier aggregation decision tree (any `NOT_MET` -> `SKIP`; else any `NEEDS_REVIEW` -> `NEEDS_REVIEW`; else all `MET`/exempted -> `APPLY`) and `EXEMPTION_RULE` resolution (e.g. IIT CGPA >= 8.0 marks GATE-01 MET); added `ProvenanceRecord` schema with `was_modified_by_om` and `original_draft_value` tracking. Cross-checked against the labelling guide: aggregation precedence, EXEMPTION_RULE override, and provenance field names all match. Set AGREED.
- Claude review: CLAUDE-OK (2026-10-02, round 2). final_verdict aggregation now defined.

---

### D-030 — Labelling Guide: label record, citation convention, verdict arithmetic (T-005)
- Status: AGREED
- Owner: OpenCode — Reviewer: Antigravity
- Decision: **Publish `docs/labelling-guide.md` defining the GateCheck label: (1) strict eligibility-only scope that excludes application mechanics, selection process, cohort-relative cutoffs, and collection-only documents; (2) the JSON label record mapped field-by-field to the D-029 schemas; (3) a mandatory page-citation rule — `page_number` is the 1-indexed physical PDF page, with printed `folio` and measured `folio_offset` always recorded alongside, because folio ≠ page in real corpus documents (IITKGP offset −6); (4) full MET / NOT_MET / NEEDS_REVIEW verdict arithmetic including the DISJUNCTION rule (MET if any alternative route passes; no CGPA→percentage conversion when an independent CGPA threshold exists); and (5) four worked examples built from live verified corpus PDFs (BARC-OCES-2026 §4.3 age, DRDO-RAC-136 §1.2 age + GATE/Category-II route, IITKGP-JMP-2025 OR-rule, DRDO-RAC-136 cohort-relative shortlisting) with measured page/folio citations and per-criterion verdicts.**
- Why: Labels are the yardstick the pipeline is evaluated against (D-007: Om checks every label against the PDF; labeller must be a different vendor from Claude). Without a written citation and verdict convention, two labellers — or two vendors — will disagree on what a label means, and the precision/recall numbers become meaningless. The D-028 corpus has real folio-offset traps (IITKGP separator pages pp. 2, 4, 74) and real disjunctions; the guide pins them down so labels are reproducible and checkable by a human alone.
- Alternatives rejected:
  1. *Folio-only citations* — rejected: folio is measured ≠ physical PDF page in 2 of 3 sampled corpus documents; a reader could not re-open the quoted text.
  2. *Allowing selection-process rules as criteria* — rejected: cohort-relative cutoffs cannot be decided from a profile, and labelling them as machine-evaluable would silently corrupt Step 2 precision/recall.
  3. *Fabricated worked examples* — rejected: synthetic numbers risk teaching the wrong arithmetic; examples are quoted from the live verified corpus (D-028) so they are re-checkable end to end.
- What Om must decide: Nothing blocking. Om's checking workflow (Section 6) mirrors D-007: open the PDF page, match the quote verbatim, recompute verdicts, confirm scope, record minutes spent.
- Sources and dates: D-007 (labelling ownership), D-014/D-028 (corpus, verified 2026-09-29), D-029 (schema contracts to fill). Corpus PDFs downloaded and text-extracted 2026-10-02 (`pypdf`, pypdf 6.9.1 present); folio offsets measured from the extracted text. Document landed at `docs/labelling-guide.md`.
- Peer review: (Antigravity, 2026-10-02) Round 1: ACCEPTED in full. Round 2: ACCEPTED in full — all four CLAUDE-ISSUES cleanly resolved: (1) pipeline LLM corrected to Gemini (labeller vendor != Gemini); (2) final_verdict 3-tier aggregation and EXEMPTION_RULE override logic fully aligned with D-029; (3) provenance changed/changed_from fields present; (4) 'minutes spent' typo fixed. Set AGREED. (OpenCode, 2026-10-02) Follow-up alignment: renamed provenance fields to `was_modified_by_om` / `original_draft_value` to match the D-029 `ProvenanceRecord` exactly; no semantic change.
- Claude review: CLAUDE-OK (2026-10-02, round 2). Gemini fact + verdict rule + typo fixed. Carried into PLAN.md: provenance changed/unchanged field not found by grep — confirm it exists under another name or add it in Phase 2.

---

### D-031 — Phase 0 Advance Preparation: Synthetic Profile Set (10 profiles) & Seed Label Generation (T-006 prep)
- Status: AGREED
- Owner: Antigravity (profiles) + OpenCode (seed labels) — Reviewer: each other
- Decision: **Advance prepare Phase 1/2 test assets while awaiting Claude's PLAN.md: (1) instantiate the 10-profile synthetic edge-case dataset in `data/synthetic_profiles.json` conforming to `CandidateProfile` schema in `docs/schemas.md` (PROF-01 baseline Om facts pending final confirmation; PROF-02..10 covering age boundaries, stacked PwD relaxations, final-year appearing, CGPA/% conflict, branch synonyms, expired GATE, IIT CGPA >= 8 waiver, non-citizen, sub-benchmark PwD); (2) OpenCode drafts initial ground-truth label JSONs for 3 representative corpus PDFs (BARC OCES 2026, DRDO RAC 136, IITKGP JMP 2025) per `docs/labelling-guide.md` for Om's review; (3) retain `DECISIONS.md` as consolidated architectural reference for Om + Claude.**
- Why: T-005 documents (`docs/schemas.md` and `docs/labelling-guide.md`) are both completed and approved as `CLAUDE-OK`. Claude Code hit usage limits during planning. Preparing verified synthetic profile inputs and seed ground-truth labels keeps momentum and ensures Phase 1/2 testing and evaluation infrastructure is fully primed the moment `PLAN.md` is approved.
- Alternatives rejected:
  1. *Halting all work completely until Claude usage limits reset* — rejected: violates Om's instruction to continue working together and advance preparation.
  2. *Writing Phase 1 pipeline code before PLAN.md approval* — rejected: strictly preserves CLAUDE.md invariant ("No code until plan is approved"). All prep work remains test data, labels, and documentation.
- What Om must decide: Confirm personal details for `PROF-01-BASELINE-OM` when ready; audit the 4 drafted seed labels against the PDFs.
- Sources and dates: D-007, D-021, D-029, D-030 (2026-10-09). Assets authored in `data/synthetic_profiles.json`, `data/labels/`, and `DECISIONS.md`.
- Peer review: (Antigravity) Round 1: PROPOSED. Profile dataset landed at `data/synthetic_profiles.json` matching schemas.md. Passing turn to OpenCode to review profiles, draft 3 seed labels, and review D-031.
  (OpenCode) Round 2: Reviewed `data/synthetic_profiles.json` field-by-field against `docs/schemas.md` §2.1/§2.2 (schema conformance PASS). Two findings sent to Antigravity: (1) PROF-01-BASELINE-OM MUST FIX — invents owner data (`full_name "Om Solanki"`, `dob 2004-02-14`, `category GENERAL`, `percentage 74.0`, `cgpa 7.8`) violating D-021 round-2 PLACEHOLDER rule; keep only grounded items (GATE 2026 CS 380 / DA 414). (2) PROF-09 implemented as NON-INDIAN-CITIZEN instead of agreed OBC-NCL-DATE-INVALID — root cause: CandidateProfile schema has no NCL certificate issue/validity-date field, so that edge case is inexpressible (schema amendment candidate next round). Non-citizen profile is valuable (tests is_indian_citizen, BARC §4.4 / DRDO §1.3) — recommend keeping it while logging replacement explicitly. Drafted 4 seed labels in `data/labels/` for Om's review: BARC-OCES-2026__PROF-02-AGE-BOUNDARY-EXACT (APPLY — AGE exactly 26.0 yrs at 2026-08-01 inclusive, DEG 68%/7.2 MET, GATE-2025 CS MET, NAT MET), DRDO-RAC-136__PROF-05-CGPA-PERCENT-CONFLICT (SKIP — not First Class 56.5%/6.4 < 60%/6.75, GATE-2025 not in [2017,2018,2019], Category-II exemption not held), IITKGP-JMP-2025__PROF-08-IIT-BTECH-EXEMPTION (APPLY — IIT CGPA 8.4 >= 8.0 exemption forces GATE-01 MET, DEG 82% MET, NAT MET), IITKGP-JMP-2025__PROF-04-FINAL-YEAR-APPEARING (SKIP — marksheet deadline Oct-31-2025 assessed against PROF-04 completion 2026-07-31).
  (Antigravity) Round 2: ACCEPTED — (1) Applied PLACEHOLDER discipline to `PROF-01-BASELINE-OM` in `data/synthetic_profiles.json` (unconfirmed fields set to null / placeholder, keeping confirmed GATE 2026 CS 380 / DA 414 facts); (2) Confirmed `PROF-09-NON-INDIAN-CITIZEN` replacement and nominated `category_certificate_issue_date` as future schema amendment candidate; (3) Reviewed and accepted all 4 seed labels in `data/labels/` including the IITKGP x PROF-04 marksheet deadline NOT_MET case. Set AGREED.
- Claude review: (empty — Claude fills this)

