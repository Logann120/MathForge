# MathForge

MathForge is an open-source platform for helping mathematics instructors generate high-quality instructional materials.

MathForge MVP 0.1 includes a Streamlit application for generating deterministic worksheets and instructional resource packs for linear equations, quadratic equations by factoring, systems of linear equations, factoring techniques, and functions basics. The project remains intentionally focused: the current MVP has no AI or LLM integration, no direct Canvas API integration, no direct LibGuides integration, no database, no authentication, no external API, no Docker setup, no plugin architecture, and no production deployment workflow.

## Mission

MathForge helps mathematics instructors create clear, accessible, and maintainable learning materials with less repetitive manual work.

The initial focus is on worksheet generation, detailed solution keys, accessible exports, and symbolic answer validation using Python, Streamlit, and SymPy.

## Target Users

- Community college instructors
- Math tutors
- Learning centers
- Students

## MVP Scope

The current MVP supports:

- Generating linear equation worksheets of the form `ax + b = c`
- Generating factorable quadratic equation worksheets
- Generating systems of linear equations worksheets
- Generating factoring techniques worksheets
- Generating functions basics worksheets
- Selecting topic-aware difficulty options: Easy for all topics, plus Medium
  and Hard for linear equations
- Selecting built-in generation presets for common instructor workflows
- Generating detailed solution keys
- Validating generated answers using SymPy
- Exporting worksheets to Markdown
- Exporting worksheets to print-friendly accessible HTML
- Exporting worksheets to LibGuides-safe embedded HTML
- Exporting worksheet problems to a Canvas-friendly manual-entry CSV
- Downloading worksheet Markdown and HTML together as a ZIP convenience bundle
- Generating full instructional resource packs with study guides, common mistakes, and tutor notes
- Generating practice quizzes inside full instructional resource packs
- Exporting full resource packs to Markdown
- Exporting full resource packs to print-friendly accessible HTML
- Exporting full resource packs to LibGuides-safe embedded HTML
- Exporting resource-pack practice quizzes to a Canvas-friendly manual-entry CSV
- Downloading resource-pack Markdown and HTML together as a ZIP convenience bundle
- Generating materials from sample College Algebra learning objectives for linear equations, quadratic equations by factoring, systems of linear equations, factoring techniques, and functions basics

## Future Direction

Near-term future work should focus on accessibility review, example maintenance, and maintainability. Later work may include richer difficulty levels, additional College Algebra topics, local question-bank experiments, or broader course templates.

AI features, direct Canvas API integration, direct LibGuides integration, persistence, databases, authentication, external APIs, deployment infrastructure, Docker, and plugin architecture remain out of scope unless explicitly requested.

## Technology Direction

MathForge is built with:

- Python for core application logic
- Streamlit for the user interface
- SymPy for symbolic math validation
- Accessible HTML and Markdown export formats
- Deterministic curriculum templates for alignment workflows

Implementation should prioritize maintainability, clear module boundaries, automated validation, and accessibility from the beginning.

## Current Architecture

MathForge is organized around small, testable Python modules:

- `app/` contains the Streamlit MVP interface, built-in generation presets, controls, rendering, downloads, and summary helpers.
- `generator/` contains deterministic worksheet, resource pack, curriculum-aligned generation, and topic-focused generator modules.
- `models/` contains dataclasses for worksheets, problems, solutions, exports, curriculum objects, and resource packs.
- `exporters/` contains Markdown, print-friendly standard HTML, LibGuides-safe HTML, Canvas-friendly manual-entry CSV exporters, standard-library ZIP bundle helpers, and deterministic download filename helpers.
- `validators/` contains SymPy-based validation helpers.
- `templates/` contains the deterministic College Algebra course template.
- `topics/` contains the supported-topic registry for topic labels, routing, defaults, and curriculum metadata.
- `tests/` contains unit and smoke tests for the implemented MVP behavior.
- `docs/` contains supplemental guides for topic additions and manual QA.

The app is intentionally deterministic and instructor-reviewable. It does not call AI services, persist user data, publish to Canvas, call the Canvas API, expose an API, or run as a deployed production service.

## Supported Topic Registry

Current topic metadata is centralized in `topics/registry.py`. The registry lists the supported topic slug, display label, default problem ID prefix, supported output types, generator functions, supported difficulty levels, and College Algebra learning-objective metadata.

When adding a future topic, contributors should add or update the deterministic worksheet/resource-pack generators first, then add one registry entry, update course-template coverage where appropriate, and add focused tests. The registry is intentionally a small explicit table, not a plugin architecture.

## How to Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app/main.py
```

Run the test suite:

```bash
python -B -m pytest -p no:cacheprovider tests
```

## Continuous Integration

GitHub Actions runs the existing pytest suite on Python 3.11 and Python 3.12 for pushes and pull requests. The workflow installs dependencies from `requirements.txt` and runs:

```bash
python -B -m pytest -p no:cacheprovider tests
```

## Screenshots

Screenshots will be added as the MVP interface stabilizes.

- Worksheet-only generation
- Full Resource Pack generation
- Markdown, standard HTML, LibGuides-safe HTML, Canvas CSV, and ZIP export previews

## Project Documentation

- [PROJECT_SPEC.md](PROJECT_SPEC.md) defines product goals, users, requirements, and MVP acceptance criteria.
- [ROADMAP.md](ROADMAP.md) describes planned phases from documentation through future integrations.
- [ARCHITECTURE.md](ARCHITECTURE.md) outlines the current MVP architecture and future integration boundaries.
- [AGENTS.md](AGENTS.md) provides guidance for contributors and coding agents working in this repository.
- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to contribute to the current MVP without weakening maintainability or accessibility.
- [docs/ADDING_TOPICS.md](docs/ADDING_TOPICS.md) explains how to add a supported topic through the registry.
- [docs/MANUAL_QA.md](docs/MANUAL_QA.md) provides manual QA and accessibility review guidance.

## Current Status

MathForge is at MVP 0.1 readiness review. The core worksheet flow for linear equations, quadratic equations by factoring, systems of linear equations, factoring techniques, and functions basics, built-in generation presets, resource pack generation with practice quizzes, SymPy validation, Markdown export, print-friendly standard HTML export, LibGuides-safe HTML export, Canvas-friendly manual-entry CSV export, optional ZIP export bundles, and demo-ready Streamlit UI are implemented and covered by automated tests.

Next work should focus on accessibility review, examples, and keeping the implementation small and maintainable. Broader medium/hard difficulty expansion for non-linear topics and additional topics should come later after explicit design and tests.

## Known Limitations

- Example files should be periodically checked against current generated output as topics and resource-pack sections evolve.
- ZIP export bundles are convenience downloads for already-rendered Markdown and HTML files; individual export buttons remain the source of each format.
- Standard HTML is designed to print cleanly from browser print preview, but MathForge does not generate PDF files.
- LibGuides-safe HTML is an embed-focused copy/paste format, not a direct LibGuides integration, and does not replace the standard HTML export.
- Canvas-friendly CSV exports are manual-entry/import-friendly files only; compatibility with Canvas quiz import workflows can vary by institution and may require instructor cleanup.
- Built-in presets provide starting defaults only; there are no saved custom presets or file-based preset configuration.
- Medium and Hard are currently exposed only for linear equations; all other topics remain Easy-only.
- Continuous integration currently runs the pytest suite on Python 3.11 and Python 3.12.
- There is no deployment workflow or production hosting configuration.
- Accessibility and browser behavior need broader manual QA beyond automated exporter tests.
- Some topic-specific generator internals remain explicit and topic-specific; the central registry now handles top-level topic discovery and routing.
- There is no AI or LLM integration, direct Canvas API integration, direct LibGuides integration, database, authentication, external API, Docker setup, plugin architecture, or production deployment.

## Contributing

Contributions are welcome, especially improvements to requirements, accessibility criteria, mathematical content design, documentation, tests, and maintainable topic expansion.

Before adding new application behavior, review the project specification, roadmap, architecture, and agent guidance. New implementation work should preserve accessibility and maintainability as first-class requirements.
