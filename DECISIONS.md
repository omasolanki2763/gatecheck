# GateCheck — Architecture & Design Decisions (`DECISIONS.md`)

This document records the architectural, technical, and operational decisions agreed upon for **GateCheck**, an automated eligibility screener for Indian PSU recruitment and IIT postgraduate admissions notices.

---

## Decision Summary Table

| ID | Title / Topic | Decision Summary | Status |
|---|---|---|---|
| **D-001** | Agent Capabilities & Roles | Antigravity (Gemini AI Pro) & OpenCode (Big Pickle) are equal peers; Claude Code is planner & reviewer. | AGREED |
| **D-002** | Topic & Phase Ownership | Research topics and phases split evenly between Antigravity and OpenCode; peer-reviewed before merge. | AGREED |
| **D-003** | Blinded Evaluation | Systematic evaluation against PDF ground-truth labels; precision, recall, and cost metrics tracked. | AGREED |
| **D-007** | Labelling Ownership & Vendor Separation | OpenCode drafts ground-truth labels; Om verifies every label against the source PDF. Labeller vendor $\ne$ pipeline LLM (Gemini). | AGREED |
| **D-009** | Budget & API Quotas | Strict ₹0 budget; Google AI Studio Gemini API free tier with rate pacing; local fallback option. | AGREED |
| **D-010** | Domain Selection | Pivoted from Gujarat tenders to GateCheck: Indian PSU-via-GATE & IIT M.Tech admission eligibility screener. | AGREED |
| **D-014** | Domain Scope Lock | Locked Scope (b): Official eligibility PDFs only (DRDO RAC, BARC OCES, IIT brochures). Cutoff tables deferred. | DECIDED-BY-OM |
| **D-015** | PDF Text & Grid Extraction | `pypdf` for fast physical page extraction + `pdfplumber` for table cell grids. Zero OCR overhead. | AGREED |
| **D-016** | Criterion Discovery in Brochures | Whole document passed directly in-context with 1-indexed page boundaries. No vector DBs or RAG chunking. | AGREED |
| **D-017** | Structured Output & Validation | Gemini Native Structured Outputs (`google-genai`) + Pydantic v2 schemas + NFKC quote grounding normalizer. | AGREED |
| **D-018** | Pipeline Orchestration | Hand-written 3-step Python runner loop (`runner.py`). No LangGraph/LangChain dependencies. | AGREED |
| **D-019** | Observability & Tracing | Append-only JSONL event stream + local SQLite index behind a clean `TraceSink` interface. | AGREED |
| **D-020** | Storage & Cache Strategy | Single `gatecheck.db` (SQLite with WAL mode) for structured state; on-demand PDF disk cache (gitignored). | AGREED |
| **D-021** | Profiles & Edge-Case Benchmark | 10 designed synthetic candidate profiles + dynamic notice-relative boundary variants generator. | AGREED |
| **D-022** | Web Demo & UI | Streamlit dashboard (`gatecheck/ui/app.py`) with memo tabs, trace visualizer, and side-by-side PDF grounding. | AGREED |
| **D-023** | Testing Without Spend | Two test modes: offline deterministic replay-fixtures (regression) vs deliberate live quota-budgeted runs (eval). | AGREED |
| **D-024** | Session Autoload Pointer | `AGENTS.md` at root acts as a concise pointer to `.claude/rules/team-protocol.md`. | AGREED |
| **D-027** | Multi-Agent Team Protocol | Portable orchestration protocol in `team/agent-team-protocol-TEMPLATE.md`. | AGREED |
| **D-028** | Corpus Manifest Balance | Balanced 50/50 mix: 14 multi-page academic brochures & major PSUs + 16 DRDO RAC notices (30 live verified PDFs). | AGREED |
| **D-029** | Formal Schema Contracts | Complete Pydantic v2 schemas in `docs/schemas.md` with 3-tier verdict aggregation (`SKIP` > `NEEDS_REVIEW` > `APPLY`). | AGREED |
| **D-030** | Labelling Guide & Convention | Ground-truth standard in `docs/labelling-guide.md`: physical page + folio offset citations, 4 worked examples. | AGREED |

---

## Detailed Decision Records

### 1. Domain & Scope (D-010, D-014)
- **Context:** Previous domain (Gujarat tenders) was hard to verify without procurement knowledge and required complex Gujarati OCR.
- **Decision:** Pivot to **GateCheck** (Scope b: Eligibility screening from official English PDF notices). Input is one recruitment/admission notice PDF + one candidate profile. Output is a structured memo with per-criterion citations, quotes, and an overall `APPLY`, `SKIP`, or `NEEDS_REVIEW` verdict.
- **Rationale:** Public, permanent born-digital PDFs; verifiable ground truth anchored to candidate attributes (DOB, category, GATE scorecard, CGPA); real decision personal to Om.

### 2. PDF Extraction & Locating Strategy (D-015, D-016)
- **Context:** Official brochures range from 1 page to 110 pages (IIT Madras, IIT Kharagpur, BARC).
- **Decision:**
  - Extract text page-by-page using `pypdf` (1-indexed physical page numbers) with `pdfplumber` for complex tabular grids.
  - Pass the entire document into Gemini Flash's 1M token context window with clear page boundary markers (`--- PAGE N ---`).
  - **No RAG, no embeddings, no chunking.**
- **Rationale:** The largest brochure in the corpus consumes ~68k tokens (<7% of context window). Traditional RAG introduces silent retrieval loss where a dropped relaxation or waiver clause produces a false negative. Whole-document in-context processing guarantees 100% clause recall.

### 3. Structured Outputs & Deterministic Boundary (D-017, D-018)
- **Context:** Stochastic LLMs often hallucinate arithmetic or format text unpredictably.
- **Decision:**
  - Step 1 (Extraction) uses native Gemini Structured Outputs enforced via Pydantic v2 schemas (`Criterion` with typed `rule_parameters`).
  - Step 2 (Verification) executes **100% deterministic Python arithmetic** (age calculation at reference date, relaxation stacking, CGPA/percentage comparisons, GATE validity windows).
  - Step 3 (Synthesis) formats the plain-English explanation citing exact page quotes.
  - Ambiguous clauses or non-machine-evaluable criteria deterministically evaluate to `NEEDS_REVIEW`. The LLM is never permitted to guess statutory waivers in Step 2.

### 4. Observability, Storage & Quotas (D-019, D-020, D-023)
- **Context:** Need rigorous observability at ₹0 cost without complex third-party SaaS dependencies.
- **Decision:**
  - Standard library `TraceSink` interface recording per-step token counts, latencies, retries, and errors into append-only JSONL files and indexed into a local `gatecheck.db` SQLite database (WAL mode enabled).
  - Reject Langfuse 6-container Docker stack to keep repository lightweight and self-contained.
  - Test suite split into fast, offline replay-fixture tests (run on every commit) and deliberate, quota-budgeted live eval runs. Rate limits dynamically read from config (`GATECHECK_RATE_LIMIT_RPM`, `GATECHECK_RATE_LIMIT_RPD`).

### 5. Final Verdict Aggregation & Exemption Semantics (D-029, D-030)
- **Context:** Memos must aggregate multiple criteria (age, degree, GATE, citizenship) into a single actionable recommendation.
- **Decision:** Strict 3-tier deterministic aggregation hierarchy:
  1. Any criterion `NOT_MET` $\implies$ **`SKIP`** (hard disqualification).
  2. Else any criterion `NEEDS_REVIEW` $\implies$ **`NEEDS_REVIEW`** (manual verification required).
  3. Else all criteria `MET` (or exempted) $\implies$ **`APPLY`** (fully qualified).
  - **`EXEMPTION_RULE` resolution:** Conditional waivers (e.g. IIT B.Tech CGPA $\ge 8.0$ exempts GATE) override the base requirement to `MET` before aggregation.
  - **DISJUNCTION semantics:** Alternative routes (e.g. 60% OR First Class OR CGPA 6.0) evaluate via logical OR (MET if any route is satisfied).

### 6. Citation Convention & Label Provenance (D-028, D-030)
- **Context:** Printed sheet numbers (folios) diverge from physical PDF page order due to unnumbered covers and separator sheets (e.g. IIT Kharagpur offset $-6$).
- **Decision:**
  - Always cite physical 1-indexed `page_number` alongside visible `folio` and `folio_offset` (`folio - page_number`).
  - Label provenance records `drafted_by`, `checked_by: Om`, `check_date`, `was_modified_by_om`, `original_draft_value`, and `minutes_spent`.
  - Labeller vendor is independent from pipeline LLM (Gemini).
