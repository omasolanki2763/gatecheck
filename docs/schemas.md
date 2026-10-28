# GateCheck Schema Contracts (`docs/schemas.md`)

This document defines the formal, field-by-field schema contracts for all data structures in the GateCheck pipeline. Every contract is implemented in Python using **Pydantic v2** (`BaseModel`, `Field`, `@model_validator`) and is enforced at runtime during extraction, evaluation, and observability recording.

---

## 1. Criterion & Typed Rule Parameters (`gatecheck.schemas.criteria`)

### 1.1 `Criterion` Model (Step 1 LLM Extraction Contract)
Represents a single atomic eligibility requirement extracted from an official born-digital notification or brochure.

| Field Name | Type | Constraints / Enums | Plain-Language Description |
|---|---|---|---|
| `criterion_id` | `str` | Format: `CRIT-[CAT]-[INDEX]` (e.g., `CRIT-AGE-01`, `CRIT-DEG-01`, `CRIT-GATE-01`) | Stable unique identifier for the criterion within a notice. |
| `category` | `CriterionCategory` | Enum: `AGE`, `QUALIFYING_DEGREE`, `GATE_SCORE`, `NATIONALITY`, `RESERVATION_CATEGORY`, `EXPERIENCE`, `OTHER` | The statutory category of the requirement. Determines which Step-2 deterministic Python checker evaluates it. |
| `description` | `str` | Non-empty string (max 300 chars) | Plain-English summary of what the notice requires. |
| `condition_type` | `ConditionType` | Enum: `THRESHOLD`, `DISJUNCTION`, `CONJUNCTION`, `EXEMPTION_RULE` | Mathematical structure of the condition. `THRESHOLD`: single cutoff (e.g. age <= 26). `DISJUNCTION`: alternative qualifying routes (A OR B). `CONJUNCTION`: all sub-clauses required (A AND B). `EXEMPTION_RULE`: conditional waiver (e.g. IIT CGPA >= 8.0 exempts GATE). |
| `raw_quote` | `str` | Min 10 chars | Exact verbatim excerpt from the PDF text establishing this rule. Must pass normalized grounding check. |
| `page_number` | `int` | $\ge 1$ (**1-indexed physical PDF page**) | The physical page order in the PDF document where `raw_quote` appears (measured via `pypdf`). |
| `folio` | `int | None` | Optional integer | The printed page number visible on the physical sheet. In real documents, printed folio often differs from PDF page (e.g. IITKGP folio 63 = PDF page 69). |
| `folio_offset` | `int` | Default: `0` | Calculated offset (`folio - page_number`). Recorded alongside every citation for human verification. |
| `is_machine_evaluable` | `bool` | `True` or `False` | Explicit flag: `True` if the rule can be evaluated purely by deterministic Python arithmetic. If `False`, Step 2 deterministically returns `NEEDS_REVIEW`. |
| `rule_parameters` | `RuleParameters | None` | Discriminated union matching `category` | Structured parameters block containing machine-checkable numerical cutoffs, dates, and lists. Null if `is_machine_evaluable=False`. |

> [!NOTE]
> **Cohort-Relative Rules & Selection Processes**:
> Selection-process rules (such as shortlisting ratios of 1:25, or cutoff scores defined relative to other candidates, e.g. *"GATE score not below 25% of the score of the top candidate"*) cannot be computed from a single candidate profile alone. These are flagged with `is_machine_evaluable=False` and evaluate deterministically to `NEEDS_REVIEW`.

---

### 1.2 Typed `RuleParameters` Blocks (Step 2 Arithmetic Dispatch)

#### A. `AgeRuleParameters` (Category: `AGE`)
Evaluated deterministically by `check_age_eligibility(candidate, rule)`:
- `cutoff_date` (`date | None`): The reference date against which candidate age is computed (e.g., `2026-08-01` for BARC OCES). If null, defaults to notice closing date.
- `min_age_years` (`int`, default: `18`): Statutory lower age floor (inclusive).
- `max_age_years` (`int`): General category upper age ceiling (e.g., `26` for BARC, `28` for DRDO RAC Scientist B).
- `category_relaxations` (`dict[CategoryEnum, int]`): Relaxations in years (e.g., `{"OBC_NCL": 3, "SC": 5, "ST": 5}`).
- `pwd_relaxation_years` (`int`, default: `10`): Statutory age relaxation for Persons with Disabilities per DoPT OM.
- `min_pwd_disability_percent` (`float`, default: `40.0`): Benchmark disability threshold. Candidates with `pwd_disability_percent < 40.0` receive 0 PwD relaxation.
- `pwd_stacks_with_category` (`bool`, default: `True`): Whether PwD relaxation adds onto category relaxation (e.g., SC + PwD = 5 + 10 = 15 years).
- `max_relaxed_age_cap` (`int | None`): Statutory hard ceiling on total relaxed age (if specified).

#### B. `DegreeRuleParameters` (Category: `QUALIFYING_DEGREE`)
Evaluated deterministically by `check_degree_eligibility(candidate, rule)`:
- `allowed_degrees` (`list[str]`): Qualifying degree titles (e.g., `["B.E.", "B.Tech", "Integrated M.Tech", "B.Sc. (Engg)"]`).
- `allowed_disciplines` (`list[str]`): Eligible branches of study (e.g., `["Computer Science & Engineering", "Information Technology", "Computer Technology"]`).
- `min_percentage` (`float | None`): Minimum required aggregate percentage (e.g., `60.0`).
- `min_cgpa_10` (`float | None`): Minimum required CGPA on 10.0 scale (e.g., `6.0`).
- `cgpa_conversion_formula` (`str | None`): Official university or notice conversion equation (e.g., `"(CGPA - 0.75) * 10"`).
- `requires_first_class` (`bool`, default: `False`): Explicit First Class / Division requirement.
- `final_year_eligible` (`bool`, default: `True`): Whether candidates currently appearing in their final semester are provisionally eligible.
- `marksheet_submission_deadline` (`date | None`): Deadline by which final degree marksheet/proof must be submitted.

> [!IMPORTANT]
> **DISJUNCTION Semantics (Alternative Routes Rule)**:
> When a notice specifies alternative routes to satisfy degree requirements (e.g., IIT Bombay clause A.5.1: *"60% marks OR First Class OR CGPA 6.0/10"*), the candidate is evaluated against each route independently, and the criterion is `MET` if **ANY** route is satisfied.
> The `cgpa_conversion_formula` applies **ONLY** when the notice mandates a specific formula and does not offer an independent CGPA cutoff option.

#### C. `GateRuleParameters` (Category: `GATE_SCORE`)
Evaluated deterministically by `check_gate_eligibility(candidate, rule)`:
- `valid_gate_years` (`list[int]`): List of acceptable GATE examination years (e.g., `[2024, 2025, 2026]`).
- `allowed_paper_codes` (`list[str]`): Qualifying GATE paper codes (e.g., `["CS", "DA"]`).
- `min_gate_score` (`int | None`): Minimum normalized GATE score cutoff (out of 1000).
- `min_gate_marks` (`float | None`): Minimum raw qualifying marks (out of 100).
- `iit_btech_cgpa_exemption_threshold` (`float | None`, e.g. `8.0`): Statutory IIT graduate GATE waiver floor (candidates with B.Tech from IIT with CGPA $\ge 8.0$ are exempt from GATE score requirements).

#### D. `ExperienceRuleParameters` (Category: `EXPERIENCE`)
Evaluated deterministically by `check_experience_eligibility(candidate, rule)`:
- `min_months_post_qualification` (`int`): Required cumulative months of professional/research experience post-degree.
- `allowed_experience_types` (`list[str]`): Recognized domains (e.g., `["Research", "Industrial", "Teaching"]`).

---

## 2. Candidate Profile (`gatecheck.schemas.profile`)

Represents a student applicant applying for a recruitment vacancy or postgraduate program.

### 2.1 `CandidateProfile` Structure

| Field Name | Type | Constraints / Defaults | Plain-Language Description |
|---|---|---|---|
| `candidate_id` | `str` | Format: `PROF-[ID]` (e.g. `PROF-01-BASELINE-OM`) | Unique applicant profile identifier. |
| `full_name` | `str` | Non-empty | Candidate full name. |
| `dob` | `date | None` | ISO format `YYYY-MM-DD` (Optional for draft/placeholder profiles) | Date of birth used for exact age calculation at cutoff. If null, age criteria evaluate to `NEEDS_REVIEW`. |
| `category` | `CategoryEnum | None` | `GENERAL`, `OBC_NCL`, `SC`, `ST`, `EWS` (Optional for draft) | Social reservation category for relaxation eligibility. If null, evaluated as General without relaxation. |
| `is_indian_citizen` | `bool` | Default: `True` | Citizenship verification matching statutory `NATIONALITY` criteria (BARC §4.4, DRDO RAC). |
| `is_pwd` | `bool` | Default: `False` | Whether candidate is a Person with Disability. |
| `pwd_disability_percent` | `float` | `0.0` to `100.0` (default `0.0`) | Measured disability percentage. Must be $\ge 40.0$ for statutory reservation. |
| `pwd_category` | `PwdCategoryEnum` | `NONE`, `LOCOMOTOR`, `VISUAL`, `HEARING`, `OTHER` | Specific functional classification of disability. |
| `is_iit_graduate` | `bool` | Default: `False` | True if candidate graduated B.Tech from an Indian Institute of Technology. |
| `qualifications` | `list[Qualification]` | Min length: 1 | Academic degree history (undergraduate and postgraduate degrees). |
| `gate_records` | `list[GateRecord]` | List of attempts (can be empty) | Historical GATE examination scorecards. |
| `experience_months` | `int` | $\ge 0$ (default: `0`) | Total verifiable post-qualification work experience in months. |

### 2.2 Sub-models (`Qualification` & `GateRecord`)

#### `Qualification`
- `degree_title` (`str`): Name of degree (e.g., `"B.Tech"`, `"B.E."`, `"Integrated M.Tech"`).
- `discipline` (`str`): Branch of study (e.g., `"Computer Science & Engineering"`, `"Information Technology"`).
- `percentage` (`float | None`): Aggregate percentage score (e.g., `68.5`).
- `cgpa` (`float | None`): Cumulative Grade Point Average (e.g., `7.2`).
- `cgpa_scale` (`float`, default: `10.0`): Maximum scale for CGPA (e.g., `10.0` or `4.0`).
- `university_conversion_formula` (`str | None`): Official conversion formula (e.g., `"(CGPA - 0.75) * 10"`).
- `is_first_class` (`bool | None`): Explicit First Class award indicator.
- `is_appearing` (`bool`, default: `False`): `True` if candidate is in final year and awaiting final results.
- `expected_completion_date` (`date | None`): Expected degree completion date.

#### `GateRecord`
- `year` (`int`): Year of GATE examination (e.g., `2026`).
- `paper_code` (`str`): Two-letter paper code (e.g., `"CS"`, `"DA"`).
- `score` (`int`): Normalized GATE score (out of 1000, e.g., `380` or `750`).
- `marks` (`float`): Raw marks scored out of 100.
- `all_india_rank` (`int | None`): All India Rank (AIR).
- `is_qualified` (`bool`, default: `True`): Whether score exceeded category qualifying cutoff.

---

## 3. Eligibility Memo & Final Verdict Aggregation (`gatecheck.schemas.memo`)

The final output produced by GateCheck evaluating one candidate against one notice.

### 3.1 `EligibilityMemo` Structure

| Field Name | Type | Constraints / Defaults | Plain-Language Description |
|---|---|---|---|
| `memo_id` | `str` | Format: `MEMO-[UUID]` | Unique identifier for this evaluation run. |
| `notice_id` | `str` | Matches `NoticeMetadata.notice_id` | Identifier of the notice evaluated (e.g. `BARC-OCES-2026`). |
| `candidate_id` | `str` | Matches `CandidateProfile.candidate_id` | Identifier of the applicant evaluated. |
| `final_verdict` | `FinalVerdictEnum` | `APPLY`, `SKIP`, `NEEDS_REVIEW` | Overall final recommendation produced by the aggregation engine. |
| `confidence` | `ConfidenceEnum` | `DETERMINISTIC_PASS`, `DETERMINISTIC_FAIL`, `REQUIRES_HUMAN_INSPECTION` | Reliability assessment of the final verdict. |
| `evaluated_at` | `datetime` | ISO 8601 UTC timestamp | Exact timestamp when screening was executed. |
| `criteria_results` | `list[CriterionResult]` | Non-empty list | Detailed evaluation result for every extracted criterion. |
| `justification` | `str` | Non-empty prose summary | Structured, plain-English explanation citing exact page numbers and evidence. |

---

### 3.2 Final Verdict Aggregation & Exemption Semantics

Step 2 aggregates individual `CriterionResult` statuses into `final_verdict` using a strict three-tier deterministic decision tree:

```
[Exemption Resolution]
      │
      ▼
Is any criterion NOT_MET? ─────────► YES ──► final_verdict = SKIP
      │
      ▼ NO
Is any criterion NEEDS_REVIEW? ────► YES ──► final_verdict = NEEDS_REVIEW
      │
      ▼ NO
Are all criteria MET / EXEMPTED? ──► YES ──► final_verdict = APPLY
```

1. **Exemption Rule Resolution (`EXEMPTION_RULE`)**:
   - If a notice provides a conditional waiver (e.g. `CRIT-GATE-02`: *IIT B.Tech with CGPA $\ge 8.0$ exempt from GATE*), the checker tests the exemption rule first.
   - If the candidate satisfies the exemption condition (`is_iit_graduate=True` and `cgpa >= 8.0`), the corresponding standard requirement (`CRIT-GATE-01`) is marked `MET` with reason `"EXEMPTED_BY_CRIT-GATE-02"`.

2. **Final Verdict Decision Hierarchy**:
   - **`SKIP` (Hard Disqualification)**: If **ANY** mandatory criterion evaluates to `NOT_MET` (and no alternative arm/exemption satisfies it), the candidate is ineligible. `final_verdict` is set to `SKIP`. (Even if other criteria are `NEEDS_REVIEW`, a single confirmed disqualification halts the application).
   - **`NEEDS_REVIEW` (Human Inspection Required)**: If no criterion is `NOT_MET`, but **ANY** criterion evaluates to `NEEDS_REVIEW` (due to subjective prose, unexpressed parameters, or missing candidate profile data), `final_verdict` is set to `NEEDS_REVIEW`.
   - **`APPLY` (Full Qualification)**: If and only if **ALL** criteria evaluate to `MET` (or `EXEMPTED`), the candidate is fully qualified. `final_verdict` is set to `APPLY`.

---

### 3.3 `CriterionResult` Breakdown
- `criterion_id` (`str`): Stable identifier matching `Criterion.criterion_id`.
- `category` (`CriterionCategory`): Category of criterion evaluated.
- `status` (`RuleStatusEnum`): `MET`, `NOT_MET`, `NEEDS_REVIEW`.
- `candidate_value` (`str`): Stringified candidate attribute (e.g., `"Age: 27 yrs 4 mos (OBC-NCL)"`).
- `required_threshold` (`str`): Stringified requirement (e.g., `"Max Age: 29 yrs (26 + 3 yr relaxation)"`).
- `citation_page` (`int`): Physical 1-indexed PDF page where rule was quoted.
- `citation_folio` (`int | None`): Printed folio on the physical sheet if present.
- `citation_quote` (`str`): Verbatim quote supporting the rule.
- `reason` (`str`): Mathematical or rule justification for the individual status.

---

## 4. Run Trace Record (`gatecheck.schemas.trace`)

Observability record captured per pipeline step in `TraceSink` (written to raw JSONL traces and indexed in SQLite).

| Field Name | Type | Constraints | Plain-Language Description |
|---|---|---|---|
| `trace_id` | `str` | UUID4 string | Unique identifier for the individual step trace. |
| `pipeline_run_id` | `str` | UUID4 string | Shared ID linking Step 1, Step 2, and Step 3 for a single execution. |
| `step` | `PipelineStep` | `STEP_1_EXTRACTION`, `STEP_2_VERDICT`, `STEP_3_MEMO` | Current pipeline stage being executed. |
| `notice_id` | `str` | Valid notice ID | Document under evaluation. |
| `candidate_id` | `str | None` | Null in Step 1 (notice-only); populated in Steps 2 & 3. |
| `model_name` | `str` | E.g. `gemini-2.5-flash` or `python-deterministic-engine` | Engine executing the step. |
| `input_tokens` | `int` | $\ge 0$ (0 for Step 2) | Exact input token count reported by API. |
| `output_tokens` | `int` | $\ge 0$ (0 for Step 2) | Exact output token count reported by API. |
| `latency_ms` | `float` | $\ge 0.0$ | Wall-clock execution time in milliseconds. |
| `cost_inr` | `float` | Always `0.00` on free tier | Cost incurred in Indian Rupees (tracked for zero-spend verification). |
| `raw_input` | `str` | Non-empty | Exact prompt text or serialized input dictionary. |
| `raw_output` | `str` | Non-empty | Exact raw text returned by the model or engine. |
| `validated_output` | `dict | None` | Validated JSON structure | Pydantic-validated payload dictionary, or null if validation failed. |
| `retry_count` | `int` | `0`, `1`, `2` | Number of validation/grounding retries triggered (max 2). |
| `error_type` | `TraceErrorType` | `NONE`, `JSON_DECODE_ERROR`, `SCHEMA_VALIDATION_ERROR`, `QUOTE_GROUNDING_ERROR`, `RATE_LIMIT_429` | Error taxonomy classification if step encountered a recoverable or terminal fault. |
| `created_at` | `datetime` | ISO 8601 UTC timestamp | Record creation timestamp. |

---

## 5. Provenance Record (`gatecheck.schemas.provenance`)

Tracks ground truth label auditing and human verification per `CLAUDE.md` and `D-007`.

| Field Name | Type | Constraints | Plain-Language Description |
|---|---|---|---|
| `drafted_by` | `str` | Non-empty (e.g. `opencode/big-pickle`) | Model/agent identity that drafted the initial criteria and verdicts. |
| `checked_by` | `str` | Exact string: `Om` | Human auditor who verified the label against the source PDF. |
| `check_date` | `date` | ISO format `YYYY-MM-DD` | Date of human verification. |
| `was_modified_by_om` | `bool` | `True` or `False` | Whether Om modified the drafted label during audit. |
| `original_draft_value` | `str | None` | Populated if `was_modified_by_om=True` | Original value prior to Om's correction (retained for labeller error tracking). |
| `minutes_spent` | `int` | $\ge 0$ | Exact minutes spent by Om checking the document against the PDF. |
