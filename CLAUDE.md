# CLAUDE.md

# Billinge Group Coding Standards

These instructions define the coding standards for this repository. Follow them for all code, tests, documentation, pull requests, and commit messages unless explicitly instructed otherwise.

## General Principles

- Prioritize consistency with the existing codebase over introducing new patterns.
- Search for similar implementations before writing new code.
- Minimize the scope of changes.
- Do not refactor unrelated code.
- Preserve backwards compatibility unless explicitly instructed otherwise.
- Design code to reduce long-term maintenance effort, not just short-term implementation effort.
- Be especially careful with changes that affect user-facing behavior.

---

# GitHub Workflow

## Commit Messages

Use Conventional Commits prefixes.

Examples:

- `feat: add PDF calibration workflow`
- `fix: handle divide by zero in DiffractionObject.scale_to`
- `docs: update installation instructions`
- `style: reformat test file`
- `refactor: simplify parser implementation`
- `perf: reduce memory usage during refinement`
- `test: add regression tests for PDF parser`
- `chore: update development dependencies`
- `build: update packaging configuration`
- `ci: improve GitHub Actions workflow`
- `revert: revert previous parser refactor`
- `release: prepare v3.2.0`
- `skpkg: update scikit-package template`

A good commit message should communicate:

- what changed
- why it changed
- where the important changes occurred

Avoid unnecessarily verbose commit messages.

---

## Pull Requests

When preparing code intended for a pull request:

- Keep each PR focused on a single theme.
- Prefer multiple small PRs over one large PR.
- Every PR should correspond to a GitHub issue.
- If no issue exists, recommend creating one.
- Use the repository's PR template.
- Include test results when appropriate.
- Highlight important inputs, outputs, screenshots, or behavior changes.
- Review the PR before requesting review.
- Address every review comment before requesting another review.
- If new work is discovered during review that is outside the PR scope, recommend creating a separate GitHub issue rather than expanding the PR.

When suggesting git operations:

- Prefer `git mv` when moving files.
- Prefer `git rm` when removing tracked files.
- Prefer `git restore` over manually undoing unstaged changes.
- Avoid recommending force pushes.
- Prefer `git revert` for undoing published commits.

---

# Documentation

## Docstrings

Follow the NumPy docstring standard.

Requirements:

- Begin with a one-line summary.
- Do not repeat the function name in the summary.
- Use imperative voice.

Prefer:

> Return a dictionary.

instead of:

> Returns a dictionary.

Parameter, attribute, and return descriptions should begin with "The".

Public functions should have complete docstrings.

Private helper functions do not require full docstrings.

---

## Tutorials

Tutorials should:

- provide step-by-step instructions
- include CLI commands
- include expected outputs where appropriate
- recommend standard workflows instead of reinventing existing tools

---

# Unit Tests

Tests document intended behavior.

When modifying tests, preserve the intended behavior instead of simply making the tests pass.

## Test Organization

Follow these conventions:

- Test comments begin with a capital letter.
- Include a high-level description before grouped test cases.
- Use numbered cases (`C1`, `C2`, etc.) for parameterized tests.
- Group similar cases together.
- Write case descriptions in the form:

```
conditions..., expect...
```

Example:

```
# C1: q input with wavelength, expect converted values
```

- Use descriptive expected variable names such as:

```
expected_xarray
expected_profile
expected_metadata
```

instead of generic names like:

```
expected
```

- Order tests from common behavior to edge cases.
- Move reusable fixtures into `conftest.py`.

See `tests/test_ratchet_model.py` for an example.
The tests should be easy to read and understand as a code maintainer.

---

# Naming Conventions

Use hyphens (`-`) for:

- repository names
- project names
- branch names
- documentation files
- markdown files
- YAML files
- images
- CLI options

Examples:

```
my-project
feature/new-parser
--output-file
```

Use underscores (`_`) for:

- Python modules
- package names
- Python filenames

Examples:

```
test_diffraction_objects.py

diffpy.utils.parsers
```

Follow tool-specific naming conventions where required by external tooling.

---

# Error Messages

Error messages should contain two parts:

1. Why the error occurred.
2. How the user can fix it.

Prefer:

```
Both release and pre-release were specified.
Please specify only one of these options.
```

Avoid cryptic or programmer-oriented messages.

Assume users may not be programmers.

---

# Code Generation

Before implementing new functionality:

1. Search for similar implementations in the repository.
2. Match existing architecture.
3. Match existing naming conventions.
4. Match surrounding coding style.
5. Match existing testing patterns.
6. Match existing documentation style.

If multiple implementation styles exist, follow the dominant pattern nearest to the code being modified.

Avoid introducing new abstractions unless they clearly simplify the design.

---

# Infrastructure

When making infrastructure or tooling changes:

- Minimize disruption to users.
- Avoid introducing technical debt.
- Prefer maintainability over cleverness.
- Optimize for developer productivity when runtime performance is not the primary constraint.
- When improving shared tooling, prefer fixing the root cause rather than adding project-specific workarounds.

---

# Default Behavior

Unless instructed otherwise, always:

- write idiomatic Python
- Don't add unnecessary empty lines between lines of code
- Generally comments in source code should not be necessary. The code should be human-readable.
- preserve existing APIs
- keep changes focused
- write or update tests for behavioral changes
- update documentation when behavior changes
- explain any significant design decisions when they are not obvious

# Coding conventions

- Python code should be **PEP 8** compliant.
- Prefer **verb-prefixed method names** (e.g. `compute_sdf()`, `get_overlap_score()`,
  `find_orientation_angle()`).
- Use **explicit but not excessive** variable naming — favor the table above over
  single-letter names outside of tight numerical expressions.
- Use `pathlib.Path` for file paths, not raw strings.
- Use **NumPy-style docstrings** for all public functions/classes.
- Avoid unnecessary boilerplate (e.g. don't add `from __future__ import annotations`
  unless it's actually needed).
