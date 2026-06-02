# MathForge

MathForge is an open-source platform for helping mathematics instructors generate high-quality instructional materials.

MathForge MVP 0.1 includes a Streamlit application for generating deterministic worksheets and instructional resource packs for linear equations, quadratic equations by factoring, systems of linear equations, factoring techniques, and functions basics. The project remains intentionally focused: the current MVP has no AI or LLM integration, no Canvas integration, no database, no authentication, no external API, and no production deployment workflow.

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
- Selecting built-in generation presets for common instructor workflows
- Generating detailed solution keys
- Validating generated answers using SymPy
- Exporting worksheets to Markdown
- Exporting worksheets to accessible HTML
- Downloading worksheet Markdown and HTML together as a ZIP convenience bundle
- Generating full instructional resource packs with study guides, common mistakes, and tutor notes
- Generating practice quizzes inside full instructional resource packs
- Exporting full resource packs to Markdown
- Exporting full resource packs to accessible HTML
- Downloading resource-pack Markdown and HTML together as a ZIP convenience bundle
- Generating materials from sample College Algebra learning objectives for linear equations, quadratic equations by factoring, systems of linear equations, factoring techniques, and functions basics

## Future Direction

Planned future capabilities include:

- Canvas LMS integration
- Question banks
- AI-generated hints
- AI-generated study guides
- Course-specific templates

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

- `app/` contains the Streamlit MVP interface and built-in generation presets.
- `generator/` contains deterministic worksheet, resource pack, and curriculum-aligned generation.
- `models/` contains dataclasses for worksheets, problems, solutions, exports, curriculum objects, and resource packs.
- `exporters/` contains Markdown and accessible HTML exporters for worksheets and resource packs, plus standard-library ZIP bundle helpers for grouping already-rendered exports.
- `validators/` contains SymPy-based validation helpers.
- `templates/` contains the deterministic College Algebra course template.
- `topics/` contains the supported-topic registry for topic labels, routing, defaults, and curriculum metadata.
- `tests/` contains unit and smoke tests for the implemented MVP behavior.
- `docs/` contains supplemental guides for topic additions and manual QA.

The app is intentionally deterministic and instructor-reviewable. It does not call AI services, persist user data, publish to Canvas, expose an API, or run as a deployed production service.

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
pytest
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
- Markdown and HTML export previews

## Project Documentation

- [PROJECT_SPEC.md](PROJECT_SPEC.md) defines product goals, users, requirements, and MVP acceptance criteria.
- [ROADMAP.md](ROADMAP.md) describes planned phases from documentation through future integrations.
- [ARCHITECTURE.md](ARCHITECTURE.md) outlines the current MVP architecture and future integration boundaries.
- [AGENTS.md](AGENTS.md) provides guidance for contributors and coding agents working in this repository.
- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to contribute to the current MVP without weakening maintainability or accessibility.
- [docs/ADDING_TOPICS.md](docs/ADDING_TOPICS.md) explains how to add a supported topic through the registry.
- [docs/MANUAL_QA.md](docs/MANUAL_QA.md) provides manual QA and accessibility review guidance.

## Current Status

MathForge is at MVP 0.1 readiness review. The core worksheet flow for linear equations, quadratic equations by factoring, systems of linear equations, factoring techniques, and functions basics, built-in generation presets, resource pack generation with practice quizzes, SymPy validation, Markdown export, HTML export, optional ZIP export bundles, and demo-ready Streamlit UI are implemented and covered by automated tests.

Current work includes a curriculum-alignment milestone with a deterministic College Algebra template. Next work should focus on hardening, documentation, accessibility review, careful topic expansion, and keeping the implementation small and maintainable.

## Known Limitations

- Example files should be periodically checked against current generated output as topics and resource-pack sections evolve.
- ZIP export bundles are convenience downloads for already-rendered Markdown and HTML files; individual export buttons remain the source of each format.
- Built-in presets provide starting defaults only; there are no saved custom presets or file-based preset configuration.
- Continuous integration currently runs the pytest suite on Python 3.11 and Python 3.12.
- There is no deployment workflow or production hosting configuration.
- Accessibility and browser behavior need broader manual QA beyond automated exporter tests.
- Some topic-specific generator internals remain explicit and topic-specific; the central registry now handles top-level topic discovery and routing.
- There is no AI or LLM integration, Canvas integration, database, authentication, external API, or production deployment.

## Contributing

Contributions are welcome, especially improvements to requirements, accessibility criteria, mathematical content design, documentation, tests, and maintainable topic expansion.

Before adding new application behavior, review the project specification, roadmap, architecture, and agent guidance. New implementation work should preserve accessibility and maintainability as first-class requirements.
