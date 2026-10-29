# GateCheck Python Style Guide (`STYLE.md`)

Governs all Python code, tests, and reviews in GateCheck. Followed by all agents and Om. Enforced via CI in Phase S3.

## 1. Core Code Rules

### 1. Layout, Naming, Imports, Line Length
- **Rule**: Follow PEP 8 with line length 100. Use standard naming: `snake_case` functions/variables, `PascalCase` classes, `UPPER_CASE` constants. Imports grouped and sorted.
- **Why**: Consistent formatting eliminates bikeshedding and lets reviewers focus on business logic rather than whitespace or syntax choices.
- **Bad**: `def checkAge(x,y): return x>=y`
- **Good**:
```python
def is_age_eligible(age_years: int, cutoff_age: int) -> bool:
    """Checks whether candidate age falls within the cutoff limit.

    Args:
        age_years: Candidate age in completed whole years.
        cutoff_age: Maximum allowable age specified in the notice.

    Returns:
        True if applicant age is less than or equal to cutoff; False otherwise.
    """
    return age_years <= cutoff_age
```
- **Enforced by**: `ruff format` and `ruff check` (`E`, `W`, `F`, `I`, `N`). Sources: [PEP 8](https://peps.python.org/pep-0008/) (checked 2026-10-29), [Ruff Rules](https://docs.astral.sh/ruff/rules/) (checked 2026-10-29).

### 2. Docstrings on Modules, Classes, and Functions
- **Rule**: Every module, class, and function must have a docstring following Google Python Style Guide convention detailing what it does, `Args:`, `Returns:`, and `Raises:` (if any).
- **Why**: Om must understand and defend every module in interviews. Docstrings ensure every interface is self-documenting.
- **Bad**:
```python
def compute_age(dob, ref):
    return (ref - dob).days // 365
```
- **Good**:
```python
def compute_age_years(birth_date: date, reference_date: date) -> int:
    """Computes candidate age in completed whole years on the cutoff date.

    Args:
        birth_date: Candidate date of birth.
        reference_date: Cutoff reference date specified in the notification.

    Returns:
        Age in completed whole years.
    """
    return reference_date.year - birth_date.year - (
        (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day)
    )
```
- **Enforced by**: Ruff `D` rules (`convention = "google"`) enforce formatting; section completeness (`Args:`, `Returns:`, `Raises:`) is enforced via peer review (since Ruff D417 verifies arguments only after an `Args:` header is present). Sources: [PEP 257](https://peps.python.org/pep-0257/) (checked 2026-10-29), [Google Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) (checked 2026-10-29).

### 3. Type Hints Everywhere
- **Rule**: All function signatures, parameters, return types, and class attributes must have explicit type annotations. Never use untyped `Any` without a documented reason; prefer explicit types or `object` for arbitrary values.
- **Why**: Static typing prevents `NoneType` bugs, enables static verification in CI, and self-documents data contracts.
- **Bad**:
```python
def parse_score(data):
    return data["score"]
```
- **Good**:
```python
def parse_gate_score(raw_profile: dict[str, object]) -> int | None:
    """Extracts candidate GATE score from a raw deserialized input dictionary.

    Args:
        raw_profile: Deserialized profile dictionary mapping keys to values.

    Returns:
        Integer score if valid and present; None otherwise.
    """
    score_value = raw_profile.get("gate_score")
    if score_value is None:
        return None
    if isinstance(score_value, int):
        return score_value
    if isinstance(score_value, str) and score_value.isdigit():
        return int(score_value)
    return None
```
- **Enforced by**: `mypy --strict` (static type conformance; explicit `Any` is not disallowed by strict and is enforced via peer review). Sources: [PEP 484](https://peps.python.org/pep-0484/) (checked 2026-10-29), [Mypy Strict](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-strict) (checked 2026-10-29).

### 4. Booleans Read as Questions & Explicit Naming
- **Rule**: Boolean variables and functions must read as questions (`is_eligible`, `has_pwd`, `can_apply`). Never use vague variable names (`data`, `temp`, `obj`, `res`).
- **Why**: Booleans reading as questions avoid inverted logic errors; explicit names mean anyone reading code understands what entity is handled.
- **Bad**: `pwd = True; temp = verify(data)`
- **Good**: `has_pwd_concession = True; is_verified = verify_qualification(profile)`
- **Enforced by**: Peer code review. Source: Om's project brief (`CLAUDE.md`).

### 5. No Magic Numbers or Strings
- **Rule**: Extract numeric and string literals into named constants or enums (`AGE_CUTOFF_DATE`, `FIRST_CLASS_MIN_PERCENT`).
- **Why**: Named constants clarify business intent; raw values look arbitrary and make recruitment policy updates error-prone.
- **Bad**: `if percentage >= 60.0 and age > 28:`
- **Good**: `if percentage >= FIRST_CLASS_MIN_PERCENT and age_years > MAX_GENERAL_AGE_LIMIT:`
- **Enforced by**: Ruff `PLR2004` (flags magic numbers in comparisons only; magic numbers in arithmetic, assignments, or function arguments are enforced via peer review) + peer review (strings). Source: [Ruff PLR2004](https://docs.astral.sh/ruff/rules/magic-value-comparison/) (checked 2026-10-29).

### 6. "Why" Comments on Non-Obvious Logic
- **Rule**: Include comments explaining *why* a calculation or rule branch is taken, citing the specific brochure clause or policy reason.
- **Why**: Code explains *how*; comments explain *why*. Om must be able to explain the reasoning behind every rule to recruiters.
- **Bad**:
```python
# add 3 years
max_age += 3
```
- **Good**:
```python
# Illustrative: DRDO Advt 136 §1.2 allows 3-year age relaxation for OBC-NCL category
max_eligible_age = GENERAL_MAX_AGE + OBC_AGE_RELAXATION_YEARS
```
- **Enforced by**: Peer code review. Source: Om's project brief (`CLAUDE.md`).

### 7. Never Swallow Exceptions & Validate at Boundaries
- **Rule**: Never use bare `except:` or `except Exception: pass`. Catch specific exceptions or log with context. Validate data at ingestion boundaries (PDF text, LLM output, profile JSON), then trust typed internal models.
- **Why**: Silently ignored errors mask failures and corrupt downstream memo verdicts. Boundary validation ensures bugs are caught early.
- **Bad**:
```python
try:
    criteria = json.loads(llm_output)
except Exception:
    pass
```
- **Good**:
```python
try:
    return ExtractedCriteria.model_validate_json(llm_output)
except pydantic.ValidationError as err:
    raise ExtractionValidationError(f"Invalid criteria payload: {err}") from err
```
- **Enforced by**: Ruff `BLE001` (blind except), `S110` (try-except-pass) + peer review. Sources: [Ruff BLE](https://docs.astral.sh/ruff/rules/#flake8-blind-except-ble) (checked 2026-10-29), [Ruff S110](https://docs.astral.sh/ruff/rules/try-except-pass/) (checked 2026-10-29).

### 8. Small Single-Purpose Modules (YAGNI)
- **Rule**: Keep modules small (~200 lines max where practical), adhering strictly to single-responsibility. Do not build speculative abstractions.
- **Why**: Modular single-purpose code is easy to unit-test, review in Orca, and explain in technical interviews.
- **Bad**: Monolithic `engine.py` doing PDF parsing, scoring arithmetic, SQLite inserts, and prompt generation.
- **Good**: Separate modules: `gatecheck/ingest/pdf.py`, `gatecheck/scoring/age.py`, `gatecheck/storage/db.py`.
- **Enforced by**: Peer code review. Source: `CLAUDE.md`.

### 9. Test-Driven Development (TDD) & ≥85% Branch Coverage
- **Rule**: Every behaviour must have a test written first (red -> green -> refactor). CI enforces ≥85% branch coverage via `pytest --cov=gatecheck --cov-branch --cov-fail-under=85`. Local config uses `--cov=gatecheck --cov-branch` so targeted TDD runs pass without whole-repo coverage gates.
- **Why**: Writing tests first guarantees testability, catches edge cases before commit, and prevents untested regression paths.
- **Bad**: Writing implementation and backfilling a superficial smoke test.
- **Good**: Write test for 28th-birthday cutoff -> confirm failure -> write minimum logic -> confirm pass -> commit.
- **Enforced by**: `pytest --cov=gatecheck --cov-branch --cov-fail-under=85` in CI. Source: [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/config.html) (checked 2026-10-29).

### 10. Code Health & Review Standards
- **Rule**: Every review must evaluate whether the change improves overall code health. Reviewers must provide technical justifications. Non-blocking suggestions start with `Nit:`.
- **Why**: Ensures code quality continually improves without stalling delivery on subjective style preferences.
- **Bad**: "I don't like this structure. Change it."
- **Good**: "Nit: Rename `lim` to `age_limit` to follow the explicit naming convention in STYLE.md §1.4."
- **Enforced by**: Peer code review in Orca. Source: [Google Code Review Standard](https://google.github.io/eng-practices/review/reviewer/standard.html) (checked 2026-10-29).

### 11. Portable File I/O & Path Handling
- **Rule**: Always pass explicit `encoding="utf-8"` to `open()`, `Path.read_text()`, and `Path.write_text()`. Always use `pathlib.Path` instead of raw string concatenation or `os.path`.
- **Why**: Windows defaults to legacy code pages (e.g. `cp1252`), which silently corrupt or crash on non-ASCII characters such as rupee signs (`₹`), en-dashes (`–`), or accented names in official notices during cross-platform CI (Windows + Ubuntu).
- **Bad**:
```python
def load_notice(path):
    with open(path) as f:
        return f.read()
```
- **Good**:
```python
def load_notice_text(file_path: Path) -> str:
    """Reads notification text using explicit UTF-8 encoding.

    Args:
        file_path: Path to the extracted text file.

    Returns:
        Full decoded notification contents.
    """
    return file_path.read_text(encoding="utf-8")
```
- **Enforced by**: Ruff `PLW1514` (unspecified-encoding; enabled via `preview = true` + `explicit-preview-rules = true`) + peer review. Source: [Ruff PLW1514](https://docs.astral.sh/ruff/rules/unspecified-encoding/) (checked 2026-10-29).

---

## 2. Git & Testing Conventions

### Git Rules
- **Commit Messages**: Conventional Commits only (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `ci:`, `chore:`). One logical change per commit.
- **Branch Naming**: `task/T-0xx-name` (or `task/Sxx-name`).
- **Merge Method**: Rebase merge only (`gh pr merge --rebase`). Linear history on `main` is strictly enforced.
- **Attribution**: Commits must be authored by active repo-local git identity: `omasolanki2763 <251193805+omasolanki2763@users.noreply.github.com>`. Check with `git config --local user.email` before the first commit in any fresh clone or worktree (global git config points to a personal account). Never add `Co-Authored-By` lines.

### Test Rules
- **File & Function Naming**: Tests live in `tests/test_<module>.py`. Test functions named `test_<function_or_scenario>_<expected_outcome>()` (e.g. `test_age_on_cutoff_date_returns_met()`).
- **TDD Workflow**: Failing test first -> minimal passing implementation -> refactor and push.
- **Fixtures**: Use deterministic recorded replay fixtures (D-023) for regression tests; live API calls are opt-in smoke tests only.

---

## 3. Copy-Ready Tool Configurations (Phase S3 Reference)

The following configurations must be mirrored directly into `pyproject.toml` during Phase S3:

```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
preview = true
explicit-preview-rules = true
select = [
    "E",        # pycodestyle errors
    "W",        # pycodestyle warnings
    "F",        # Pyflakes
    "I",        # isort
    "N",        # pep8-naming
    "D",        # pydocstyle
    "UP",       # pyupgrade
    "B",        # flake8-bugbear
    "BLE",      # flake8-blind-except
    "S",        # flake8-bandit
    "PLR2004",  # magic-value-comparison
    "PLW1514",  # unspecified-encoding (preview rule)
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "PLR2004"]  # S101 allows assert; PLR2004 allows comparison literals in test assertions

[tool.mypy]
python_version = "3.13"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=gatecheck --cov-branch"
```
