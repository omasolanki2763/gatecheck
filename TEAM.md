# Multi-Agent Team Capability & Ownership Matrix (TEAM.md)

This document establishes the capability profiles, verified constraints, and concrete ownership split across the three agents for the **GateCheck (eligibility screener)** project, as defined under [.claude/rules/team-protocol.md](file:///.claude/rules/team-protocol.md).

---

## 1. Agent Capability Matrix

| Job / Dimension | Antigravity (Gemini 3.8 Flash) | OpenCode (opencode/big-pickle) | Claude Code (Opus 5 / Pro) |
|---|---|---|---|
| **Underlying Engine & Platform** | Gemini 3.8 Flash (Medium), Google DeepMind. Confirmed twice: self-reported, and Google's own docs name 3.8 Flash the default Antigravity model. Quota: Google AI Pro ($19.99/mo). | **Unknown by design.** OpenCode Zen lists one curated model, `big-pickle`; third parties describe it as a deliberate *stealth* model with *rotating* backends. Quota: Zen free tier, $0. | Claude Opus 5 (lineup also Sonnet 5, Haiku 4.5, Fable 5), Anthropic. Quota: Claude Pro ($20/mo). |
| **Context Window** | 1,048,576 in / 65,536 out. Reads complete recruitment notices, academic brochures, and lengthy transcripts without truncation. | 200k in / 32k out. Strong local context for multi-file scripts and test runs. | 1M in Claude Code on Pro/Max/Team/Enterprise, but Pro must enable usage credits for the 1M window on Opus models. Longer context drains quota faster — that, not the window, is the limit. |
| **Web Research** | Fast research, synthesis, and architectural comparison. | Search-backed research via context7, Firecrawl, Tavily, websearch, GitHub issues. Excellent at version-sensitive library docs. | Deep analytical synthesis, but high token cost makes it inefficient for raw browsing. |
| **Reading Long PDFs & Complex Layouts** | **High.** Native multimodal input natively parses layout, tables, multi-column recruitment notices and brochures, and administrative formats. | **Low.** Text extraction only (via pypdf/pdfplumber); cannot natively inspect visual layout or non-text elements. | High text comprehension; visual inspection possible if converted to images, but consumes high quota. |
| **Python Coding & Refactoring** | Strong at architecture, schema contracts, type annotations, and Pydantic models. | Fast at mechanical work: shell scripts, pytest fixtures, benchmark loops, regex extractors. Not ranked against the others — see the big-pickle row. | High code correctness, concise implementations, minimal refactor churn. |
| **Writing Tests & Harnesses** | Strong at property-based test design and edge-case contracts. | Fast at *executing* pytest, timing chaos limits, hashing fixtures, and measuring. | Excellent at specifying acceptance tests and verification assertions. |
| **Adversarial Code & Spec Review** | **Primary Reviewer.** Attacks design assumptions, schema loose ends, and failure modes. | Strong at checking mechanical errors, missing dependencies, and syntax/runtime failures. | **Final Reviewer.** Verifies interview-defensibility, system invariants, and merge safety. |
| **Quota & Cost Constraints** | Google AI Pro $19.99/mo; agent quota refreshes every 5 hours up to a weekly limit, shared across Gemini models. Low marginal cost. (Gemini *API* RPM/TPM tiers do not apply — that is for API keys, not the Antigravity app.) | Free tier on OpenCode Zen; fast turnaround, zero API dollar spend. Capability may change under us if the backend rotates. | **Scarcest Resource.** Three limits, not one: rolling 5h session, weekly cap, and a separate weekly Opus cap. Anthropic's own illustration is ~45 messages per 5h on a light model with short chats. Must be protected from chat churn. |

*Sources (checked 2026-09-27 & verified current):* Gemini 3.8 Flash model card <https://deepmind.google/models/model-cards/gemini-3-8-flash/> · Gemini API model + pricing docs <https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash> · Antigravity-as-default-model confirmation <https://ai.google.dev/gemini-api/docs/latest-model> · Artificial Analysis <https://artificialanalysis.ai/models/releases/gemini-3-8-flash> · OpenCode Zen <https://opencode.ai/docs/zen/> · models.dev OpenCode provider <https://models.dev/providers/opencode> · Claude pricing <https://claude.com/pricing> · Claude usage limits <https://support.claude.com/en/articles/9797557-usage-limit-best-practices> · Antigravity plans <https://antigravity.google/docs/plans/> · *UNVERIFIED:* big-pickle backend identity; Antigravity exact agent-quota numbers; Claude "~10-20 messages at 100k+ context".

---

## 2. Phase 0 Topic Split (Topics 5–14)

Per protocol, each open topic has one assigned Owner and one Primary Reviewer:

| Topic | Description | Owner | Primary Reviewer | Final Reviewer | Status / Agreement |
|---|---|---|---|---|---|
| **Topic 5** | LLM Choice (Pipeline Model) | **Antigravity** | **OpenCode** (hard pricing & rate-limit citations) | **Claude Code** | Aligned with D-002: Antigravity researches options; OpenCode reviews with dated citations; Claude decides. |
| **Topic 6** | PDF Text & Page-Number Extraction (born-digital) | **OpenCode** (Harness & benchmarks) | **Antigravity** (Semantic quality & text fidelity) | **Claude Code** | Locked in D-016. OpenCode benchmarks extraction speed and page-offset accuracy; Antigravity verifies text fidelity. |
| **Topic 7** | Chunking & Locating Criteria | **OpenCode** | **Antigravity** | **Claude Code** | OpenCode benchmarks text retrieval; Antigravity checks boundary preservation. |
| **Topic 8** | Structured Output & Validation | **Antigravity** | **OpenCode** | **Claude Code** | Antigravity designs Pydantic / Instructor contracts; OpenCode verifies validation runtime. |
| **Topic 9** | Hand-written Loop vs LangGraph | **Antigravity** | **OpenCode** | **Claude Code** | Antigravity evaluates state transitions and debuggability; OpenCode evaluates testability. |
| **Topic 10** | Tracing (Langfuse vs JSONL/SQLite) | **OpenCode** | **Antigravity** | **Claude Code** | OpenCode evaluates storage footprint and offline replay; Antigravity reviews schema. |
| **Topic 11** | Storage (local files / DB) | **OpenCode** | **Antigravity** | **Claude Code** | OpenCode designs lightweight storage layer; Antigravity checks concurrency and serialization. |
| **Topic 12** | Candidate Profile & Memo Schemas | **Antigravity** | **OpenCode** | **Claude Code** | Antigravity drafts core data contracts (`docs/schemas.md`); OpenCode tests edge-case deserialization. |
| **Topic 13** | Web Framework & Deployment | **Antigravity** | **OpenCode** | **Claude Code** | Streamlit auto-deployed to Streamlit Community Cloud from `main`. Interface decoupled via API/MCP client. |
| **Topic 14** | Testing Without Per-Run Spend | **OpenCode** | **Antigravity** | **Claude Code** | OpenCode implements mock fixtures, VCR/playback recording, and deterministic ground-truth tests. |

---

## 3. Team Roles and Workflow

- **Antigravity & OpenCode = Equal Peers:** Both research, both may draft non-critical work, and each reviews the other's work. Reviews follow a logical debate of facts backed by concrete evidence (command output, URL, CI log, test); stronger facts win, and neither agent is subordinate to the other.
- **Claude Code = Planner + Reviewer of Critical Work:** Plans phases and tasks (`PLAN.md` / `DECISIONS.md`), reviews all critical deliverables (schemas, eligibility arithmetic, verdict logic, CI config, secrets), and resolves pure-judgement deadlocks.
- **Om = End-Result Evaluator:** Judges only the finished product; removed from day-to-day reviews, approvals, and intermediate gates. Om conducts full module walkthroughs after completion to ensure deep interview defensibility.

---

## 4. Implementation Phases (Phases 1–7) Role Division

| Phase | Milestone Deliverable | Primary Worker (Draft/Code) | Peer Reviewer | Final Reviewer / Gate |
|---|---|---|---|---|
| **Phase 1** | Ingestion & PDF Parsing Pipeline | OpenCode (Harness & pipelines) | Antigravity (Text fidelity & page mapping) | Claude Code (Test validation & merge) |
| **Phase 2** | Criteria Extraction | Antigravity (Prompt & extraction logic) | OpenCode (Batch harness & token costs) | Claude Code (Review on 3 labelled notices) |
| **Phase 3** | Checking & Memo Drafting | **Split:** OpenCode (Python arithmetic) · Antigravity (Eval logic & memo prompt) | Mutual peer review | Claude Code (End-to-end memo review & arithmetic validation) |
| **Phase 4** | Observability & Limits | OpenCode (Tracing, cost caps, timeouts) | Antigravity (Trace schema & failure taxonomy) | Claude Code (Chaos test verification) |
| **Phase 5** | Evaluation Suite | OpenCode (Eval runner & regression suite) | Antigravity (Taxonomy categorization) | Claude Code (Headline metric review) |
| **Phase 6** | MCP Server | Antigravity (Server tools & JSON schemas) | OpenCode (Client integration & latency tests) | Claude Code (MCP client verification) |
| **Phase 7** | Web Demo & Docs | Antigravity (Web UI & packaging) | OpenCode (Security & cold-start review) | Claude Code (Final sign-off; Om evaluates end product) |

---

## 5. Governance & Review Principles

1. **Evidence-Based Debate of Facts:**
   - Every finding or objection in code and spec reviews must cite concrete evidence (command output, documentation URL + date, CI log, test execution).
   - The other peer may counter with evidence; stronger facts win, and the wrong side concedes in writing. There is no artificial round limit; peers iterate until no doubt remains.
   - In the event of a pure-judgement deadlock, Claude Code decides and records both positions in `team/decision-log.md`.
2. **Git Branches, Pull Requests, and Strict CI:**
   - Work is partitioned onto task branches (`task/<name>`). No simultaneous editing of the same files.
   - Every task is merged into `main` via linear rebase merge (`gh pr merge --rebase`) only after peer review PASS and green CI on both `ubuntu-latest` and `windows-latest`.
3. **Labelling Authority & Provenance:**
   - Ground-truth labels are drafted by OpenCode, audited via evidence debate with Antigravity, and checked against verbatim PDF page quotes (verified automatically in CI).
   - Provenance is explicitly tracked per label (`drafted_by`, `was_modified_by_om`, `original_draft_value`, `minutes_spent`).
