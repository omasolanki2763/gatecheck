# GateCheck Labelling Guide (`docs/labelling-guide.md`)

This document defines **what a label is, how to produce one, and how to verify one** for the
GateCheck evaluation corpus. A label is the ground-truth answer for one candidate against one
notice: the set of machine-readable eligibility criteria extracted from the notice, plus the
MET / NOT_MET / NEEDS_REVIEW verdict for each checkable rule and for the candidate overall.

The labels are the yardstick. The pipeline (Step 1 extraction, Step 2 deterministic verdict,
Step 3 memo) is evaluated against these labels, so a label must be:

- **Exact** — every number quoted verbatim from the source PDF, with a precise citation,
- **Reproducible** — a second person can re-derive the same verdict from the same PDF alone,
- **Scoped** — containing eligibility rules only, not application procedure or selection process.

Ownership per decision D-007: the labeller drafts; **Om checks every label against the PDF**
and records minutes spent. The pipeline LLM is **Gemini** (CLAUDE.md, D-009); the labeller
must be a different vendor from the pipeline, so the labeller vendor must NOT be Gemini —
this guide is written so any allowed vendor can produce labels unassisted.

The schema contracts this guide fills are in `docs/schemas.md` (D-029) — field definitions and
types live there; this guide is the *how to fill them* manual.

---

## 1. Scope: what gets labelled, and what does not

GateCheck Version 1 scope (b) covers **eligibility rules only**. A rule is an *eligibility
rule* when it is a threshold, window, or alternative condition that a candidate either does or
does not satisfy at application time, independently of other candidates.

**Label these:**

- Age limits, floors, and relaxations (category, PwD, ex-servicemen, government service).
- Qualifying-degree requirements (degree title, discipline, First Class, minimum percentage/CGPA).
- GATE requirements (valid exam years, paper codes, minimum score, IIT CGPA waivers).
- Nationality and, where stated, domicile/residence requirements.
- Experience thresholds expressed in months/years of a stated type.
- Explicit flags where the notice waives a requirement for a defined class.

**Do NOT label — record only as a note, never as a criterion:**

- Application mechanics: fees, upload steps, NOC/CCA declarations, admit cards, lock deadlines.
- Selection process: shortlisting ratios (1:25, 1:5), interview weights, descriptive-exam stages.
- **Cohort-relative rules**: any cutoff defined against *other candidates*, e.g. "GATE score not
  below 25% of the score of the first shortlisted candidate". The verdict for such a rule CANNOT
  be computed from the candidate's profile alone, so it is not machine-evaluable; set
  `is_machine_evaluable=false` and the pipeline returns `NEEDS_REVIEW` (worked example D).
- Medical/bond requirements, service liability.
- **Collection-only documents**: files that carry no eligibility text (e.g. `IISc
  MTech_MDes_seat_matrix.pdf` is a seat table, not eligibility text — per the D-028 Claude
  review note, keep it in the collection set only, never in the labelled set).

The borderline test: *would the answer change if I knew nothing about any other applicant?*
If no, it is eligibility. If yes, it is selection — and it is out of scope.

---

## 2. The label record

A label is authored as JSON (serialised from the Pydantic contracts in `docs/schemas.md`).
Mandatory fields per label — one record per criterion, one file per notice:

| Field | Meaning | Source of truth |
|---|---|---|
| `criterion_id` | `CRIT-[CAT]-[INDEX]` unique within this notice | schemas.md §1.1 |
| `category` | `AGE`, `QUALIFYING_DEGREE`, `GATE_SCORE`, `NATIONALITY`, `RESERVATION_CATEGORY`, `EXPERIENCE`, `OTHER` | schemas.md §1.1 |
| `condition_type` | `THRESHOLD`, `DISJUNCTION`, `CONJUNCTION`, `EXEMPTION_RULE` | schemas.md §1.1 |
| `description` | one plain-English sentence the labeller writes | schemas.md §1.1 |
| `raw_quote` | verbatim excerpt from the PDF, >= 10 chars | must appear in extracted text |
| `page_number` | **1-indexed physical PDF page** (page order in the file) | measured with pypdf |
| `folio` | printed page number on that sheet, if visible (may differ) | visual/manual |
| `folio_offset` | `folio - page_number`, measured per document | this guide §3 |
| `is_machine_evaluable` | `true` if Step 2 can decide from the profile alone | this guide §1 |
| `rule_parameters` | typed block matching `category` | schemas.md §1.2 |
| `verdict` | per-criterion: `MET`, `NOT_MET`, or `NEEDS_REVIEW` for a candidate | this guide §4 |
| `final_verdict` | overall: `APPLY`, `SKIP`, or `NEEDS_REVIEW` for the candidate against the notice | this guide §4.2 |
| `provenance` | `drafted_by`, `checked_by`, `check_date`, `was_modified_by_om`, `original_draft_value`, `minutes_spent` | D-007, CLAUDE.md |

---

## 3. Page citation rule (the trap this guide exists to avoid)

The printed page number on a sheet (the **folio**) is NOT always the physical PDF page.
Measured in the actual corpus:

| Document | Example location | PDF page (1-based) | printed folio | offset |
|---|---|---|---|---|
| `BARC-OCES-2026` | §4.3 Age Limit | 17 | 17 | 0 |
| `DRDO-RAC-136` | §1.2 Age Limit | 3 | 2 | -1 |
| `IITKGP-JMP-2025` | OR-rule text | 69 | 63 | -6 |

Why: brochures and notices routinely have unnumbered cover pages, separator sheets (IITKGP has
three zero-text separator pages at pp. 2, 4, 74), or folio restarts.

**Rule: `page_number` is the physical 1-based index in the PDF file (what pypdf reports + 1).
Record the printed `folio` and the derived `folio_offset` for every citation.** A reader
re-produces the quote by opening PDF page `page_number`; the folio is the human-visible anchor.
Never record a citation by folio alone, and never assume folio == page_number.

---

## 4. Verdicts: how to decide MET / NOT_MET / NEEDS_REVIEW

The verdict is computed deterministically (the same arithmetic Step 2 runs), from the
`rule_parameters` against a candidate profile:

- **`MET`** — the candidate's attributes satisfy the rule.
- **`NOT_MET`** — the candidate's attributes fail the rule, and there is no alternative route.
- **`NEEDS_REVIEW`** — the rule is not machine-evaluable, OR the candidate profile lacks a value
  needed to decide, OR the notice is self-contradictory and the contradiction is not resolved.

Threshold arithmetic:

- **Age:** resolve the maximum allowed age by applying `category_relaxations`, then
  `pwd_relaxation_years` if the candidate is PwD with disability >= `min_pwd_disability_percent`
  and `pwd_stacks_with_category` is true. Compare the candidate's age at `cutoff_date`
  (default: notice closing date) against `min_age_years` .. `max_relaxed`.
- **Degree:** match `allowed_degrees`/`allowed_disciplines` first; then compare either
  `percentage` against `min_percentage` OR `cgpa` against `min_cgpa_10`. If the notice gives a
  CGPA cutoff, the candidate's CGPA *as reported on the transcript* is compared directly —
  **no percentage conversion is performed** when an independent CGPA threshold exists. If the
  candidate's institute reports marks in percentages only and the notice has no CGPA cutoff,
  convert using the notice's own stated formula if any (`cgpa_conversion_formula`), else
  `NEEDS_REVIEW`.
- **GATE:** the candidate must hold a GATE record whose `year` is in `valid_gate_years` AND
  whose `paper_code` is in `allowed_paper_codes`, AND pass any stated `min_gate_score`/
  `min_gate_marks`. If the candidate is an IIT graduate with CGPA >= the stated
  `iit_btech_cgpa_exemption_threshold`, that route is exempt per `EXEMPTION_RULE`.

**Disjunction semantics (the rule Claude carried into PLAN.md):** when a notice offers
alternative routes — "60% OR First Class OR CGPA 6.0" — evaluate every route independently and
return `MET` if ANY route is satisfied. A candidate who fails one arm but passes another is
`MET`, never `NOT_MET`. (Worked example C.)

**Overall verdict aggregation (`final_verdict`, exactly as the pipeline computes it):**
combine all per-criterion verdicts in this priority order:

1. Any criterion `NOT_MET`  → overall **`SKIP`**.
2. Else any criterion `NEEDS_REVIEW`  → overall **`NEEDS_REVIEW`**.
3. Else all criteria `MET`  → overall **`APPLY`**.

The `final_verdict` is what the candidate acts on (apply vs skip vs unresolved). Note the
priority: a single `NOT_MET` makes the overall verdict `SKIP` even if other criteria are
`NEEDS_REVIEW`; `NEEDS_REVIEW` only wins when every criterion is `MET` or `NEEDS_REVIEW`.

**How `EXEMPTION_RULE` criteria interact with aggregation:** an exemption does not add a new
verdict — it overrides the criterion it exempts. If the exemption rule holds for the
candidate, the exempted criterion's verdict at Step 2 is forced to `MET` before aggregation
(e.g. the IIT CGPA ≥ 8 route makes the GATE criterion `MET` even with no GATE record). An
exemption that does not hold leaves the criterion as its normal verdict. Then the 1-2-3
aggregation above runs. Never sum an exemption as a standalone criterion.

---

## 5. Worked examples (real quotes from the verified corpus)

### A. BARC-OCES-2026 — age threshold with category and PwD relaxations

Source: `BARC-OCES-2026`, PDF page 17 (folio 17). Section 4.3, extracted text verbatim:

> 4.3. Maximum Age Limit (Maximum Age as on August 1, 2026) - (Refer Table -5)
> i. General category - 26 years,
> ii. OBC (Non-Creamy Layer) - 29 years,
> iii. SC/ST - 31 years,
> ...
> vi. Physically challenged persons of all categories are eligible for age relaxation of
> 10 years. Person with physical disability with extent of disability 40% or more will be
> considered for age relaxation and may be permitted a scribe.
> vii. The minimum age limit for all the applicants is 18 years as on August 1, 2026.

Label:

```
criterion_id:   CRIT-AGE-01
category:       AGE
condition_type: THRESHOLD
description:    Age between 18 and the category maximum, as on Aug 1 2026, with PwD 10-yr relaxation.
raw_quote:      [verbatim text above, section 4.3]
page_number:    17
folio:          17
folio_offset:   0
is_machine_evaluable: true
rule_parameters:
  cutoff_date:               2026-08-01
  min_age_years:             18
  max_age_years:             26
  category_relaxations:      { OBC_NCL: 3, SC: 5, ST: 5 }
  pwd_relaxation_years:      10
  min_pwd_disability_percent: 40.0
  pwd_stacks_with_category:  true
```

Verdict checks (CandidateProfile as per schemas.md §2):
- Om profile: born 2004-02-14, GENERAL, not PwD. Age at 2026-08-01 = 22 years 5 months.
  `18 <= 22.4 <= 26` → **MET**.
- A candidate born 1995-09-01, OBC-NCL, not PwD: age = 30 years 11 months. General cap 26 +
  3 (OBC) = 29, age 30.9 > 29 → **NOT_MET**.
- Same candidate but PwD (locomotor, 45%): 26 + 3 + 10 = 39 → **MET**.

Overall `final_verdict`: single criterion, so Om: MET → **APPLY**; NOT_MET → **SKIP**.

### B. DRDO-RAC-136 — GATE + degree conjunction, with an alternative (Category II) route

Source: `DRDO-RAC-136`, PDF page 2 (folio 1) Table 1 Part-II, e.g. Chemical Engg row; and
PDF page 3 (folio 2) section 1.2. Extracted verbatim:

> Essential Qualification#: At least First Class Bachelor's Degree in Engineering or Technology
> in Chemical Engg from a recognized university or equivalent.
> GATE Qualification: Valid GATE score in Chemical Engineering [Paper code : CH]
> ...
> OR Category II: Candidates should possess the requisite Essential Qualification (EQ) from
> IITs/NITs with minimum aggregate 80% marks (Category II eligibility criteria is not applicable
> for GAETEC posts).
> Valid GATE 2017/2018/2019

Labels:

```
criterion_id:   CRIT-DEG-01         CRIT-GATE-01
category:       QUALIFYING_DEGREE   GATE_SCORE
condition_type: CONJUNCTION         CONJUNCTION  (DEG-01 AND GATE-01; GATE-01 has an
                                          alternative arm, see GATE-02 below)
rule_parameters:
  allowed_degrees: [B.E., B.Tech]     valid_gate_years: [2017, 2018, 2019]
  allowed_disciplines: [Chemical      allowed_paper_codes: [CH]
    Engg, Chemical Technology,        min_gate_score: (none absolute)
    Chemical Plant Engg, ...]
  requires_first_class: true
```

```
criterion_id:   CRIT-GATE-02     (the ALTERNATIVE arm of the GATE requirement)
category:       GATE_SCORE
condition_type: EXEMPTION_RULE
raw_quote:      [Category II text above]
description:    IIT/NIT graduates with 80%+ aggregate in the EQ degree are exempt from GATE.
rule_parameters:
  allowed_degrees:                     [B.E., B.Tech]
  min_percentage:                      80.0
  iit_btech_cgpa_exemption_threshold:  (none)
```

Verdict (Chemical Engg row): a candidate with B.Tech Chemical and a valid GATE-2018 CH score:
DEG-01 MET, GATE-01 MET → overall **APPLY**. A candidate with B.Tech Chemical, 85% aggregate from
NIT, no GATE: DEG-01 MET, GATE-01 NOT_MET but GATE-02 (exemption) holds → GATE-01 is overridden
to MET → overall **APPLY** (alternative arm). A candidate with 55% First Year marks, no GATE,
not IIT/NIT: DEG-01 NOT_MET → overall **SKIP** (any NOT_MET wins).

### C. IITKGP-JMP-2025 — percentage OR CGPA disjunction

Source: `IITKGP-JMP-2025`, PDF page 69 (folio 63). Extracted verbatim:

> GE/OBC/EWS: Minimum of 60% marks (OR a CGPA of 6.5 on a 10 point scale)
> SC/ST/PwD: Minimum of 55% marks (OR a CGPA of 6.0 on a 10 point scale)
> - CGPA will not be converted to percentage if the degree awarding Institute provides marks
> in CGPA system.

Labels: two `QUALIFYING_DEGREE` criteria (one per category block), both `condition_type:
DISJUNCTION`.

```
criterion_id:   CRIT-DEG-01  (GE/OBC/EWS)
rule_parameters:
  min_percentage: 60.0
  min_cgpa_10:    6.5
  cgpa_conversion_formula: null     <- NO conversion; CGPA cutoff exists
criterion_id:   CRIT-DEG-02  (SC/ST/PwD)
rule_parameters:
  min_percentage: 55.0
  min_cgpa_10:    6.0
  cgpa_conversion_formula: null
```

Verdict: each category-block criterion is evaluated ONLY for candidates in that block; the
non-applicable block is not scored at all (no NOT_MET is produced from a block the candidate is
not in). GE/OBC/EWS candidate, percentage 58%, CGPA 6.4: 58 < 60 AND 6.4 < 6.5 → **NOT_MET**.
Same candidate, CGPA 6.7 with percentage 58: 6.7 >= 6.5 → **MET** (the CGPA arm alone
satisfies the disjunction; the 58% does not need to cross 60%). An SC candidate with 55% and
CGPA 5.5: only CRIT-DEG-02 (SC) is scored, 55 >= 55 → **MET**.

Overall `final_verdict` per candidate: case 1 (58% / 6.4, GE) NOT_MET → **SKIP**. Case 2
(58% / 6.7, GE) MET → **APPLY**. Case 3 (55% / 5.5, SC) MET → **APPLY**.

### D. DRDO-RAC-136 — a cohort-relative rule that must NOT be machine-evaluated

Source: `DRDO-RAC-136`, PDF page 4 (folio 2), section 5 Screening/Shortlisting. Verbatim:

> Category I: Eligible candidates will be shortlisted for a Descriptive Examination on the basis
> of valid GATE score in the ratio of 1:25, subject to their GATE score not being below 25% of
> the GATE score of the first shortlisted candidate.

This is a **selection-process rule** (per section 1 it is NOT labelled as a criterion). If a
notice requires it for eligibility nevertheless, it is recorded with:

```
is_machine_evaluable: false
description:  Cutoff is relative to the cohort's top GATE score; not decidable from the profile.
```

The pipeline returns `NEEDS_REVIEW` for this criterion; a human compares the candidate's GATE
score against the shortlist cutoff determined by the notice authority. Overall: with this
criterion `NEEDS_REVIEW` and all others `MET`, `final_verdict` = **NEEDS_REVIEW**.

---

## 6. Checking a label (Om's workflow, per D-007)

For every label, in order, flag `checked` only when all pass:

1. **Open** PDF page `page_number` (physical 1-based) and confirm the printed `folio` matches.
2. **Match** the `raw_quote` verbatim against the text on that page (space-collapse tolerance only).
3. **Recompute** the verdicts for at least one MET and one NOT_MET candidate from §4 arithmetic,
   using the recorded `rule_parameters`. If the arithmetic disagrees, fix the label.
4. **Confirm scope** per section 1 — no selection-process or cohort-relative rule was labelled
   as a machine-evaluable criterion.
5. **Record provenance**: `checked_by: Om`, `check_date`, `minutes_spent`, and the
   `was_modified_by_om` field — `false` if the label stands exactly as drafted, `true` with
   `original_draft_value` (what the drafted label said) if Om altered any field while checking.

A label that fails any step returns to the labeller with the failing step named. Nothing is
ever "approximately quoted"; if the quote cannot be found verbatim, it is a broken citation,
not a soft edit.

---

## 7. Versioning

- This guide is itself a Phase 0 document (D-030). Changes require a peer review round, a
  decision-log entry, and after agreement a single batch ping to Claude (one ping per document
  round, per team protocol).
- Worked examples must always come from the live verified corpus with real measured page/folio
  citations (section 3); synthetic examples are only allowed where a corpus document does not
  exhibit the structure, and must be marked as such.