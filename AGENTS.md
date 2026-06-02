# Agent Guidance for MathForge

This repository contains a working Python/Streamlit MVP for deterministic College Algebra instructional material generation.

Agents and contributors must preserve the implemented MVP unless the project owner explicitly requests behavior changes. Do not add AI integration, Canvas integration, persistence, authentication, APIs, deployment workflows, or new product features unless they are specifically requested.

## Current Scope

Useful work:

- Improve README.md.
- Improve PROJECT_SPEC.md.
- Improve ROADMAP.md.
- Improve ARCHITECTURE.md.
- Improve AGENTS.md.
- Improve CONTRIBUTING.md.
- Clarify requirements, risks, and acceptance criteria.
- Propose maintainability and accessibility improvements.
- Maintain the implemented module structure when explicitly requested.
- Add focused tests when implementation changes are requested.

Out of scope unless explicitly requested:

- New generator behavior.
- Streamlit UI behavior changes.
- Model, exporter, or validator behavior changes.
- Dependency installation or dependency changes.
- AI or LLM integration.
- Canvas integration.
- Database, authentication, API, or deployment code.

## Project Direction

MathForge is an open-source platform for generating high-quality mathematics instructional materials.

The current implementation stack is:

- Python
- Streamlit
- SymPy

The MVP supports:

- Math worksheet generation.
- Detailed solution key generation.
- Accessible HTML export.
- Markdown export.
- Answer validation using SymPy.
- Instructional resource packs with study guides, common mistakes, tutor notes, and practice quizzes.
- Curriculum-aligned generation from a deterministic College Algebra template.
- Optional ZIP export bundles for already-rendered Markdown and HTML outputs.
- Built-in generation presets for common instructor workflows.

## Current Architecture

- `app/` contains the Streamlit MVP interface and built-in generation presets.
- `generator/` contains deterministic worksheet, resource-pack, and curriculum-aligned generation.
- `models/` contains dataclasses for content, resource packs, and curriculum structures.
- `exporters/` contains Markdown, HTML, and ZIP bundle exporters.
- `validators/` contains SymPy validation helpers.
- `templates/` contains the College Algebra course template.
- `topics/` contains the supported-topic registry for labels, defaults, routing, difficulty support, and curriculum metadata.
- `tests/` contains unit and smoke tests.
- `docs/` contains supplemental documentation for topic additions and manual QA.

## Working Principles

When working in this repository:

- Preserve existing files unless the user explicitly asks for deletion.
- Keep documentation professional and suitable for a public GitHub project.
- Prioritize maintainability and accessibility.
- Separate confirmed requirements from future ideas.
- Avoid speculative implementation details that would constrain future work unnecessarily.
- Prefer clear, plain language over buzzwords.

## Accessibility Expectations

Documentation and implementation should treat accessibility as a core requirement.

Agents should preserve or improve guidance related to:

- Semantic HTML export.
- Logical heading structure.
- Readable Markdown.
- Screen-reader-friendly material structure.
- Avoiding color-only meaning.
- Instructor review of generated materials.

## Maintainability Expectations

Implementation work should preserve clear boundaries between:

- Streamlit user interface code.
- Problem generation logic.
- SymPy validation logic.
- Worksheet assembly.
- HTML and Markdown exporters.
- Curriculum templates and future integrations.

Future topic additions should update deterministic generators, add one `topics/registry.py` entry, update tests, and avoid scattering new label or prefix maps across the app.

Use `docs/ADDING_TOPICS.md` as the source checklist for supported-topic additions.

Use `docs/MANUAL_QA.md` for manual Streamlit, Markdown export, and HTML accessibility review before major user-facing changes.

## Change Discipline

Before editing, inspect the existing repository state and read relevant files.

For documentation-only tasks:

- Do not add code.
- Do not install dependencies.
- Do not run formatters that modify unrelated files.
- Do not delete existing files.
- Summarize intended file changes before making them when requested.

For implementation tasks:

- Confirm scope before adding new project structure.
- Add focused tests for core generation, validation, and export behavior.
- Keep UI behavior separate from reusable domain logic.
- Document any accessibility limitations that cannot be resolved immediately.

## Known Limitations

- Example exports should be periodically checked against current generated output.
- ZIP bundles are convenience downloads for already-rendered exports; individual Markdown and HTML exports remain available.
- Built-in generation presets are fixed starting defaults only; there are no saved custom presets or file-based preset configuration.
- CI runs the pytest suite on Python 3.11 and Python 3.12; deployment workflows are not configured.
- Accessibility and browser QA remain limited.
- Top-level topic routing now uses `topics/registry.py`; topic-specific generator internals remain explicit.
- There is no AI or LLM integration, Canvas integration, database, authentication, API, or production deployment.
