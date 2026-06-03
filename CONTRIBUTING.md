# Contributing to MathForge

Thank you for your interest in contributing to MathForge.

MathForge currently has a working Python/Streamlit MVP for deterministic College Algebra instructional material generation. Contributions should align with the documented mission: helping mathematics instructors generate high-quality instructional materials with maintainable, accessible open-source tools.

## Current Contribution Scope

Useful contributions include:

- Improving project documentation.
- Refining MVP requirements and known limitations.
- Clarifying accessibility expectations.
- Reviewing architecture boundaries.
- Improving tests for implemented behavior.
- Proposing maintainable approaches for new supported topics.
- Refreshing examples and supplemental documentation.

Do not add or change business logic, Streamlit UI behavior, AI integration, direct Canvas API integration, direct LibGuides integration, persistence, authentication, APIs, or deployment code unless that implementation work is explicitly requested.

## Project Principles

Contributions should prioritize:

- Maintainability.
- Accessibility.
- Mathematical correctness.
- Instructor control over generated materials.
- Clear separation between user interface, generation, validation, and export concerns.

## Repository Structure

The structure is organized around current MVP responsibilities:

- `app/` for the Streamlit interface, built-in generation presets, input controls, rendering, downloads, and summary helpers.
- `generator/` for deterministic worksheet, resource-pack, curriculum-aligned generation, and topic-focused generator modules.
- `models/` for dataclasses representing content, resource packs, and curriculum structures.
- `validators/` for answer validation, including SymPy-based checks.
- `exporters/` for print-friendly standard HTML, LibGuides-safe HTML, Markdown, Canvas manual-entry CSV, and ZIP bundle exports.
- `templates/` for the College Algebra course template.
- `topics/` for the supported-topic registry.
- `tests/` for automated tests.
- `docs/` for supplemental project documentation.

## Documentation Standards

Documentation should be clear, professional, and suitable for a public GitHub project.

When changing documentation:

- Prefer precise language over broad claims.
- Separate current scope from future plans.
- Keep accessibility and maintainability visible.
- Update related files when a requirement or architectural decision changes.

## Code Standards

When application code changes are approved, contributions should:

- Keep Streamlit UI code separate from reusable domain logic.
- Keep generation, validation, and export modules independently testable.
- Use SymPy for symbolic validation where appropriate.
- Add focused tests for new behavior.
- Document known limitations.

## Continuous Integration

GitHub Actions runs the pytest suite on Python 3.11 and Python 3.12 for pushes and pull requests. The workflow installs dependencies from `requirements.txt` and runs `python -B -m pytest -p no:cacheprovider tests`.

When adding a supported topic, keep routing centralized in `topics/registry.py`. Add deterministic generator behavior, resource-pack behavior if supported, registry metadata, curriculum metadata, and tests together.

Preserve public generator imports in `generator/problem_generator.py` and `generator/resource_pack_generator.py`. Preserve existing export formats, including standard HTML print behavior, unless an exporter-format change is explicitly requested.

Easy, Medium, and Hard are supported for all current topics through the supported-topic registry. Built-in presets remain Easy-only. Do not change legacy unknown-difficulty fallback behavior unless that compatibility change is explicitly requested and tested.

Use [docs/ADDING_TOPICS.md](docs/ADDING_TOPICS.md) as the checklist for future topic additions.

Use [docs/MANUAL_QA.md](docs/MANUAL_QA.md) before major UI, exporter, or topic changes.

## Current Non-Features

The MVP intentionally has no AI or LLM integration, direct Canvas API integration, direct LibGuides integration, database, authentication, external API, production deployment workflow, or production hosting configuration.

## Known Limitations

- Example outputs should be periodically checked against current generated output.
- ZIP export bundles are convenience downloads for already-rendered Markdown and HTML files and should not replace individual export buttons.
- LibGuides-safe HTML exports are separate embed-focused downloads, not a direct LibGuides integration, and should not replace the standard HTML export.
- Canvas-friendly CSV exports are manual-entry/import-friendly files only; do not add Canvas API calls, OAuth, tokens, secrets, or network behavior without an explicit request.
- Built-in generation presets are fixed defaults only; do not add persistence, accounts, or file-based preset configuration without an explicit request.
- CI runs the pytest suite on Python 3.11 and Python 3.12; deployment workflows are not configured.
- Accessibility and browser QA need more coverage before broader release.
- Top-level topic routing now uses `topics/registry.py`; topic-specific generator internals remain explicit and should stay small.

## Questions and Design Discussion

For larger changes, start with a proposal in documentation or an issue before implementing. This helps keep the project approachable for educators, tutors, students, and open-source contributors.
