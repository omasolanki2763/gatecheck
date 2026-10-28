# Multi-Agent Team Capability & Ownership Matrix (TEAM.md)

This document establishes the capability profiles, verified constraints, and concrete ownership split across the three agents for the **Tender Go/No-Go Checker** project, as defined under [.claude/rules/team-protocol.md](file:///.claude/rules/team-protocol.md).

---

## 1. Agent Capability Matrix

| Job / Dimension | Antigravity (Gemini 3.8 Flash) | OpenCode (opencode/big-pickle) | Claude Code (Opus 5 / Pro) |
|---|---|---|---|
| **Underlying Engine & Platform** | Gemini 3.8 Flash (Medium), Google DeepMind. Confirmed twice: self-reported, and Google's own docs name 3.8 Flash the default Antigravity model. Quota: Google AI Pro ($19.99/mo). | **Unknown by design.** OpenCode Zen lists one curated model, `big-pickle`; third parties describe it as a deliberate *stealth* model with *rotating* backends. Quota: Zen free tier, $0. | Claude Opus 5 (lineup also Sonnet 5, Haiku 4.5, Fable 5), Anthropic. Quota: Claude Pro ($20/mo). |
| **Context Window** | 1,048,576 in / 65,536 out. Reads complete tender documents and lengthy transcripts without truncation. | 200k in / 32k out. Strong local context for multi-file scripts and test runs. | 1M in Claude Code on Pro/Max/Team/Enterprise, but Pro must enable usage credits for the 1M window on Opus models. Longer context drains quota faster — that, not the window, is the limit. |
| **Web Research** | Fast research, synthesis, and architectural comparison. | Search-backed research via context7, Firecrawl, Tavily, websearch, GitHub issues. Excellent at version-sensitive library docs. | Deep analytical synthesis, but high token cost makes it inefficient for raw browsing. |
| **Reading Long PDFs & Complex Layouts** | **High.** Native multimodal input natively parses layout, tables, multi-column tenders, and stamps. | **Low.** Text extraction only (via pypdf/pdfplumber); cannot natively inspect visual layout or non-text elements. | High text comprehension; visual inspection possible if converted to images, but consumes high quota. |
| **OCR / Scanned Gujarati Text** | **Best of the three, but not the best available.** On Sarvam's Indic OCR bench (6,909 samples; vendor-run, and it scores Gemini 3.6 not 3.8) Gujarati accuracy is Gemini 3.6 Flash **83.68**, Claude Opus 5 **70.92**. India-focused Sarvam Vision 2.1 beats both at **88.87**. Pending our own blinded test. See D-003. | **None.** No declared image modality, so it cannot be relied on to read a scanned page. Relies on external OCR (Tesseract `guj`, Surya, Sarvam). | Weakest of the three here: 70.92 on the same Gujarati bench, below Gemini, and costly for batch OCR. This is the concrete reason the pipeline LLM must not be Claude. |
| **Python Coding & Refactoring** | Strong at architecture, schema contracts, type annotations, and Pydantic models. | Fast at mechanical work: shell scripts, pytest fixtures, benchmark loops, regex extractors. Not ranked against the others — see the big-pickle row. | High code correctness, concise implementations, minimal refactor churn. |
| **Writing Tests & Harnesses** | Strong at property-based test design and edge-case contracts. | Fast at *executing* pytest, timing chaos limits, hashing fixtures, and measuring. | Excellent at specifying acceptance tests and verification assertions. |
| **Adversarial Code & Spec Review** | **Primary Reviewer.** Attacks design assumptions, schema loose ends, and failure modes. | Strong at checking mechanical errors, missing dependencies, and syntax/runtime failures. | **Final Reviewer.** Verifies interview-defensibility, system invariants, and merge safety. |
| **Quota & Cost Constraints** | Google AI Pro $19.99/mo; agent quota refreshes every 5 hours up to a weekly limit, shared across Gemini models. Low marginal cost. (Gemini *API* RPM/TPM tiers do not apply — that is for API keys, not the Antigravity app.) | Free tier on OpenCode Zen; fast turnaround, zero API dollar spend. Capability may change under us if the backend rotates. | **Scarcest Resource.** Three limits, not one: rolling 5h session, weekly cap, and a separate weekly Opus cap. Anthropic's own illustration is ~45 messages per 5h on a light model with short chats. Must be protected from chat churn. |

*Sources (all checked 2026-09-27):* Gemini 3.8 Flash model card <https://deepmind.google/models/model-cards/gemini-3-8-flash/> · Gemini API model + pricing docs <https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash> · Antigravity-as-default-model confirmation <https://ai.google.dev/gemini-api/docs/latest-model> · Artificial Analysis <https://artificialanalysis.ai/models/releases/gemini-3-8-flash> · OpenCode Zen <https://opencode.ai/docs/zen/> · models.dev OpenCode provider <https://models.dev/providers/opencode> · Claude pricing <https://claude.com/pricing> · Claude usage limits <https://support.claude.com/en/articles/9797557-usage-limit-best-practices> · Antigravity plans <https://antigravity.google/docs/plans/> · **Sarvam Indic OCR bench (vendor-run) <https://www.sarvam.ai/blogs/sarvam-vision-2-1>** · IndicVisionBench, ICLR 2026 <https://arxiv.org/html/2511.04727> · *UNVERIFIED:* big-pickle backend identity; Antigravity exact agent-quota numbers; Claude "~10-20 messages at 100k+ context".

---

## 2. Phase 0 Topic Split (Topics 5–14)

Per protocol, each open topic has one assigned Owner and one Primary Reviewer:

| Topic | Description | Owner | Primary Reviewer | Final Reviewer | Status / Agreement |
|---|---|---|---|---|---|
| **Topic 5** | LLM Choice (Pipeline Model) | **Antigravity** | **OpenCode** (hard pricing & rate-limit citations) | **Claude Code / Om** | Aligned with D-002: Antigravity researches options; OpenCode reviews with dated citations; Claude/Om decides. |
| **Topic 6** | PDF Parsing / OCR (scanned Gujarati) | **OpenCode** (Harness & benchmarks) | **Antigravity** (Judges semantic quality & Gujarati OCR) | **Claude Code** | Locked in kickoff. OpenCode runs speed/accuracy tests; Antigravity verifies text fidelity. |
| **Topic 7** | Chunking & Locating Criteria | **OpenCode** | **Antigravity** | **Claude Code** | OpenCode benchmarks text retrieval; Antigravity checks boundary preservation. |
| **Topic 8** | Structured Output & Validation | **Antigravity** | **OpenCode** | **Claude Code** | Antigravity designs Pydantic / Instructor contracts; OpenCode verifies validation runtime. |
| **Topic 9** | Hand-written Loop vs LangGraph | **Antigravity** | **OpenCode** | **Claude Code** | Antigravity evaluates state transitions and debuggability; OpenCode evaluates testability. |
| **Topic 10** | Tracing (Langfuse vs JSONL/SQLite) | **OpenCode** | **Antigravity** | **Claude Code** | OpenCode evaluates storage footprint and offline replay; Antigravity reviews schema. |
| **Topic 11** | Storage (local files / DB) | **OpenCode** | **Antigravity** | **Claude Code** | OpenCode designs lightweight storage layer; Antigravity checks concurrency and serialization. |
| **Topic 12** | Company Profile & Memo Schemas | **Antigravity** | **OpenCode** | **Claude Code** | Antigravity drafts core data contracts; OpenCode tests edge-case deserialization. |
| **Topic 13** | Web Framework & Deployment | **Antigravity** | **OpenCode** | **Claude Code** | Gated on Topic 6 (OCR engine dependencies). Interface decoupled via API/MCP client. |
| **Topic 14** | Testing Without Per-Run Spend | **OpenCode** | **Antigravity** | **Claude Code** | OpenCode implements mock fixtures, VCR/playback recording, and deterministic ground-truth tests. |

---

## 3. Plan Workflow (Decided by Om, 2026-09-27)

1. **Om + Claude Code** conduct the Phase 0 planning interview and draft `PLAN.md`.
2. **Antigravity + OpenCode** review the draft peer-to-peer: find issues, debate trade-offs, refine the document, and record each change as an entry in `team/decision-log.md`.
3. **Claude Code** performs final verification of the agreed changes via the decision log (`CLAUDE-OK` or `CLAUDE-ISSUES`).

---

## 4. Implementation Phases (Phases 1–7) Role Division

| Phase | Milestone Deliverable | Primary Worker (Draft/Code) | Peer Reviewer | Final Reviewer / Gate |
|---|---|---|---|---|
| **Phase 1** | Ingestion & OCR pipeline | OpenCode (Harness & pipelines) | Antigravity (OCR quality & schema) | Claude Code (Test validation & merge) |
| **Phase 2** | Criteria Extraction | Antigravity (Prompt & extraction logic) | OpenCode (Batch harness & token costs) | Claude Code (Review on 3 labelled tenders) |
| **Phase 3** | Checking & Memo Drafting | **Split:** OpenCode (Python arithmetic) · Antigravity (Eval logic & memo prompt) | Mutual peer review | Claude Code (End-to-end memo review) |
| **Phase 4** | Observability & Limits | OpenCode (Tracing, cost caps, timeouts) | Antigravity (Trace schema & failure taxonomy) | Claude Code (Chaos test verification) |
| **Phase 5** | Evaluation Suite | OpenCode (Eval runner & regression suite) | Antigravity (Taxonomy categorization) | Claude Code (Headline metric review) |
| **Phase 6** | MCP Server | Antigravity (Server tools & JSON schemas) | OpenCode (Client integration & latency tests) | Claude Code (MCP client verification) |
| **Phase 7** | Web Demo & Docs | Antigravity (Web UI & packaging) | OpenCode (Security & cold-start review) | Claude Code + Om (Live demo sign-off) |

---

## 5. Decision Gates for Om (OM-DECIDES)

1. **Code Ownership & Interview Defensibility:**
   - Proposal: 100% module coverage with a structured 3-question viva per file (*What breaks if deleted? Why this dependency? What does the test prove?*). Authoring agent teaches Om any unclear lines before merge.
2. **Repository & OneDrive Relocation:**
   - Blocker: The project root is currently uninitialized Git sitting inside a syncing OneDrive directory. Before parallel dispatches commence in Phase 1, the workspace must be initialized as a Git repo and moved outside OneDrive (or operated in strict serial mode).
3. **Labelling Authority & Vendor Independence:**
   - Brief rule: Pipeline LLM and labelling LLM must be from different vendors. If Claude drafts labels and Om verifies every label, does Gemini serve as the pipeline model, and who generates the golden ground-truth dataset?
   - Three positions are argued in **D-007**; none is closed. Note the interaction with D-003: if Sarvam wins topic 6, it changes what "the pipeline vendor" even means, so settle topic 6 first.

---

## 6. Peer Review Resolution (Round 1 — Resolved)

Both points raised by OpenCode in round 1 review have been fully accepted and resolved in `TEAM.md`:

1. **Topic 5 Owner:** Aligned with D-002. Antigravity leads research on candidate models (Gemini vs alternatives), OpenCode reviews with hard pricing and rate-limit documentation, and Claude/Om makes the decision.
2. **Phase 3 Split:** Aligned with D-002 and CLAUDE.md. OpenCode implements the deterministic Python arithmetic module; Antigravity implements the evaluation logic and memo drafting prompt; each peer reviews the other.
