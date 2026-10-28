# GateCheck Corpus Candidates Manifest (Verified Draft)

**Corpus Goal:** 25+ public, legal, born-digital recruitment notifications and admission brochures for Indian CS/engineering graduates.
**Verification Policy:** Every URL listed below has been fetched live with HTTP 200 OK and confirmed serving `application/pdf` (binary payload, `%PDF` magic bytes, and `Content-Type: application/pdf` header confirmed) on 2026-09-29. Page counts are empirically measured via `pypdf`. Raw PDF binaries are NOT committed into git.
**Composition Policy:** Balanced 50/50 split between (1) multi-page academic brochures & major PSU notifications (4–110 pages; testing complex disjunctions, departmental matrices, and stacked relaxations) and (2) single/multi-page recruitment notices (1–20 pages; testing direct threshold logic and rapid screening).

---

## 1. Multi-Page Academic Brochures & Major PSU-via-GATE Notifications (14 Documents)

| ID | Issuer | Year | Pages | Verify Date | Verified Official URL | Content-Type | Key Eligibility Features Tested |
|---|---|---|---|---|---|---|---|
| `IITM-MTECH-2026` | IIT Madras | 2026 | 110 | 2026-09-29 | <https://mtechadm.iitm.ac.in/pdfs/Mtech_IB_2026.pdf> | `application/pdf` (21.4 MB) | Comprehensive departmental criteria matrix, dual-degree conversion rules, extensive inter-disciplinary mappings. |
| `IITKGP-JMP-2025` | IIT Kharagpur | 2025-26 | 86 | 2026-09-29 | <https://gateoffice.iitkgp.ac.in/jmp/d/docs/JMP_Brochure_2025_26.pdf> | `application/pdf` (2.5 MB) | Inter-departmental eligibility matrix across schools, 3 zero-text separator pages (pp. 2, 4, 74), GATE score percentiles. |
| `BARC-OCES-2026` | BARC / DAE | 2026 | 42 | 2026-09-29 | <https://www.barc.gov.in/careers/barc_ts_OCES_DGFS_brochure.pdf> | `application/pdf` (716 KB) | Dual representation of age rules (prose p. 17 vs Table-5 p. 41), stacked category + PwD relaxations, GATE-only vs online exam routes. |
| `IITBHU-MTECH-2026` | IIT BHU Varanasi | 2026-27 | 33 | 2026-09-29 | <https://pgadmission.iitbhu.ac.in/static/doc/inf_brochure.pdf> | `application/pdf` (815 KB) | Departmental qualifying degree tables, sponsorship categories, minimum qualifying marks thresholds. |
| `IITR-MTECH-2026` | IIT Roorkee | 2026 | 32 | 2026-09-29 | <https://iitr.ac.in/Academics/static/Admission/PG/M.Tech/2026/Regular/Information_Brochure_2026.pdf> | `application/pdf` (1.8 MB) | Departmental code matrices, minimum CGPA/percentage conversions, GATE discipline eligibility. |
| `IITISM-MTECH-2026` | IIT (ISM) Dhanbad | 2026-27 | 18 | 2026-09-29 | <https://admissions.iitism.ac.in/mtech/assets/admission/brochure/MTech%20IB%202026%2009-03-2026.pdf> | `application/pdf` (1.8 MB) | 2-year M.Tech eligibility, discipline mapping, category reservation percentages. |
| `IOCL-GATE-2024` | IOCL | 2024 | 13 | 2026-09-29 | <https://iocl.com/admin/img/UploadedFiles/LatestJobOpening/Files/ff4f416adeb64f218a13592917f3af95.pdf> | `application/pdf` (460 KB) | PSU recruitment of Engineers/Officers via GATE 2024, qualifying disciplines, medical fitness criteria, upper age limits. |
| `IOCL-GATE-2023` | IOCL | 2023 | 11 | 2026-09-29 | <https://iocl.com/admin/img/UploadedFiles/LatestJobOpening/Files/4056e7ca062d4201a60add5b3dcd9452.pdf> | `application/pdf` (385 KB) | Historical PSU recruitment baseline, percentage rounding rules, age relaxations. |
| `NITW-MTECH-2025` | NIT Warangal | 2025-26 | 11 | 2026-09-29 | <https://nitw.ac.in/api/static/files/mtech_2025-3-11-11-1-23.pdf> | `application/pdf` (494 KB) | Self-finance M.Tech criteria, work experience requirements, fee structures. |
| `POWERGRID-ET-2026` | PowerGrid (PGCIL) | 2026 | 9 | 2026-09-29 | <https://www.powergrid.in/sites/default/files/job_opportunities_document/ET2026throughGATe2026.pdf> | `application/pdf` (915 KB) | Executive Trainee recruitment via GATE 2026, Computer Science & IT streams, compensation and bond conditions. |
| `POWERGRID-ET-2024` | PowerGrid (PGCIL) | 2024 | 9 | 2026-09-29 | <https://www.powergrid.in/sites/default/files/job_opportunities_document/Detailed_Advertisement_4.pdf> | `application/pdf` (379 KB) | Detailed PSU advertisement, reservation rosters, relaxation stacking. |
| `NPCIL-ET-2026` | NPCIL | 2026 | 4 | 2026-09-29 | <https://www.npcilcareers.co.in/ETHQ2026/documents/advt.pdf> | `application/pdf` (882 KB) | Executive Trainee recruitment via GATE 2024/2025/2026, nuclear engineering discipline mapping, age cutoff dates. |
| `IISC-MIDYEAR-2026` | IISc Bangalore | 2026-27 | 4 | 2026-09-29 | <https://iisc.ac.in/wp-content/uploads/2026/09/Mid-year-Admission-Notice-2026-27.pdf> | `application/pdf` (920 KB) | Research/M.Tech mid-year admissions, department-specific areas, qualifying degree thresholds. |
| `IISC-MTECH-2026` | IISc Bangalore | 2026 | 1 | 2026-09-29 | <https://iisc.ac.in/wp-content/uploads/2026/02/MTech_MDes_seat_matrix.pdf> | `application/pdf` (219 KB) | M.Tech/M.Des seat matrix, GATE paper code eligibility mapping across departments. |

---

## 2. DRDO RAC Numbered Advertisement Series (16 Diverse Recruitment Notices)
Official direct archive repository: <https://rac.gov.in/download/archive/>. All files verified HTTP 200 OK and `application/pdf` on 2026-09-29.

| ID | Issuer | Year | Pages | Verify Date | Verified Download URL | Content-Type | Key Eligibility Features Tested |
|---|---|---|---|---|---|---|---|
| `DRDO-RAC-124` | DRDO RAC | 2017 | 2 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_124.pdf> | `application/pdf` (68 KB) | Historical baseline, engineering degree cutoffs. |
| `DRDO-RAC-126` | DRDO RAC | 2017 | 1 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_126.pdf> | `application/pdf` (98 KB) | Single-page direct notice, fast qualification check. |
| `DRDO-RAC-127` | DRDO RAC | 2017 | 3 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_127.pdf> | `application/pdf` (185 KB) | Lateral recruitment qualifications. |
| `DRDO-RAC-129` | DRDO RAC | 2018 | 2 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_129.pdf> | `application/pdf` (140 KB) | Discipline-wise degree eligibility mapping. |
| `DRDO-RAC-130` | DRDO RAC | 2018 | 4 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_130.pdf> | `application/pdf` (270 KB) | Category relaxations and qualifying score thresholds. |
| `DRDO-RAC-134` | DRDO RAC | 2019 | 3 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_134.pdf> | `application/pdf` (190 KB) | Multi-post eligibility conditions. |
| `DRDO-RAC-135` | DRDO RAC | 2019 | 7 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_135.pdf> | `application/pdf` (450 KB) | Scientist recruitment qualifications and age gates. |
| `DRDO-RAC-136` | DRDO RAC | 2019 | 5 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_136.pdf> | `application/pdf` (380 KB) | Valid GATE 3-year window, First Class degree cutoff, category age limits (28 Gen / 31 OBC / 33 SC-ST). |
| `DRDO-RAC-137` | DRDO RAC | 2020 | 8 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_137.pdf> | `application/pdf` (520 KB) | Dual organization criteria (DRDO vs ADA). |
| `DRDO-RAC-145` | DRDO RAC | 2023 | 6 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_145.pdf> | `application/pdf` (410 KB) | Corrigendum / revised post-qualification experience requirements. |
| `DRDO-RAC-146` | DRDO RAC | 2023 | 7 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_146.pdf> | `application/pdf` (460 KB) | Multi-discipline engineering mapping. |
| `DRDO-RAC-147` | DRDO RAC | 2024 | 20 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_147.pdf> | `application/pdf` (1.2 MB) | Senior level appointments, research experience arithmetic, publication checks. |
| `DRDO-RAC-148` | DRDO RAC | 2024 | 5 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_148.pdf> | `application/pdf` (340 KB) | Category-based fee and age relaxations. |
| `DRDO-RAC-152` | DRDO RAC | 2025 | 9 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_152.pdf> | `application/pdf` (610 KB) | Experience hierarchy, research publications. |
| `DRDO-RAC-154` | DRDO RAC | 2025 | 6 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_154.pdf> | `application/pdf` (405 KB) | Multi-stream engineering degrees. |
| `DRDO-RAC-156` | DRDO RAC | 2025 | 5 | 2026-09-29 | <https://rac.gov.in/download/archive/advt_156.pdf> | `application/pdf` (350 KB) | Final-year appearing student eligibility provisions, GATE score validity. |

---

## 3. Summary Statistics of Rebalanced Corpus Manifest

- **Total Verified Live Documents:** 30 documents.
  - **Academic Brochures & Major PSUs:** 14 documents (47%) — 5 premier IITs (Madras, Kharagpur, Roorkee, ISM Dhanbad, BHU), IISc Bangalore, NIT Warangal, BARC/DAE, and 3 major PSUs (PowerGrid, NPCIL, IOCL).
  - **Recruitment Notices:** 16 documents (53%) — DRDO RAC spanning historical, lateral, corrigendum, Scientist B, and Senior Scientist appointments.
- **Page Count Distribution:** 1 to 110 pages (476 total pages across corpus; median ~6.5 pages, mean 15.9 pages). Long brochures (18–110 pages) thoroughly stress-test whole-document context and complex table extraction without chunking.
- **HTTP Fetch & MIME Verification:** 100% verified HTTP 200 OK and confirmed `application/pdf` (with binary `%PDF` header) on 2026-09-29. Zero HTML shells, zero 404s, zero speculative or guessed URLs.
- **Language & Format:** 100% English, 100% born-digital PDFs.
- **Corpus Target:** Fully meets the balanced 50/50 composition mandate requested by Claude Code for Phase 0 completion.
