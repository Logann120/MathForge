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

Do not add or change business logic, Streamlit UI behavior, AI integration, Canvas integration, persistence, authentication, APIs, or deployment code unless that implementation work is explicitly requested.

## Project Principles

Contributions should prioritize:

- Maintainability.
- Accessibility.
- Mathematical correctness.
- Instructor control over generated materials.
- Clear separation between user interface, generation, validation, and export concerns.

## Repository Structure

The structure is organized around current MVP responsibilities:

- `app/` for the Streamlit interface.
- `generator/` for deterministic worksheet, resource-pack, and curriculum-aligned generation.
- `models/` for dataclasses representing content, resource packs, and curriculum structures.
- `validators/` for answer validation, including SymPy-based checks.
- `exporters/` for HTML and Markdown exports.
- `templates/` for the College Algebra course template.
- `topics/` for the supported-topic registry.
- `tests/` for automated tests.
- `docs/` for future supplemental project documentation.

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

When adding a supported topic, keep routing centralized in `topics/registry.py`. Add deterministic generator behavior, resource-pack behavior if supported, registry metadata, curriculum metadata, and tests together.

Use [docs/ADDING_TOPICS.md](docs/ADDING_TOPICS.md) as the checklist for future topic additions.

## Current Non-Features

The MVP intentionally has no AI or LLM integration, Canvas integration, database, authentication, external API, production deployment, CI workflow, or production hosting configuration.

## Known Limitations

- Example outputs are stale and do not yet show the current full resource-pack flow.
- `docs/` is currently a placeholder folder.
- CI and deployment workflows are not configured.
- Accessibility and browser QA need more coverage before broader release.
- Top-level topic routing now uses `topics/registry.py`; topic-specific generator internals remain explicit and should stay small.

## Questions and Design Discussion

For larger changes, start with a proposal in documentation or an issue before implementing. This helps keep the project approachable for educators, tutors, students, and open-source contributors.
