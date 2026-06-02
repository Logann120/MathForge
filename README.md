# MathForge

MathForge is an open-source platform for helping mathematics instructors generate high-quality instructional materials.

MathForge MVP 0.1 includes a small Streamlit application for generating deterministic worksheets and instructional resource packs for linear equations, quadratic equations by factoring, systems of linear equations, and factoring techniques. The project remains intentionally focused: no AI integration, no Canvas integration, and no account system are included in the current MVP.

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
- Generating detailed solution keys
- Validating generated answers using SymPy
- Exporting worksheets to Markdown
- Exporting worksheets to accessible HTML
- Generating full instructional resource packs with study guides, common mistakes, and tutor notes
- Exporting full resource packs to Markdown
- Exporting full resource packs to accessible HTML
- Generating materials from sample College Algebra learning objectives for linear equations, quadratic equations by factoring, systems of linear equations, and factoring techniques

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

## Screenshots

Screenshots will be added as the MVP interface stabilizes.

- Worksheet-only generation
- Full Resource Pack generation
- Markdown and HTML export previews

## Project Documentation

- [PROJECT_SPEC.md](PROJECT_SPEC.md) defines product goals, users, requirements, and MVP acceptance criteria.
- [ROADMAP.md](ROADMAP.md) describes planned phases from documentation through future integrations.
- [ARCHITECTURE.md](ARCHITECTURE.md) outlines the intended technical design before code is written.
- [AGENTS.md](AGENTS.md) provides guidance for contributors and coding agents working in this repository.
- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to contribute while the project is still in its pre-implementation phase.

## Current Status

MathForge is at MVP 0.1 readiness review. The core worksheet flow for linear equations, quadratic equations by factoring, systems of linear equations, and factoring techniques, resource pack generation, SymPy validation, Markdown export, HTML export, and demo-ready Streamlit UI are implemented and covered by automated tests.

Current work includes a curriculum-alignment milestone with a deterministic College Algebra template. Next work should focus on hardening, documentation, accessibility review, careful topic expansion, and keeping the implementation small and maintainable.

## Contributing

Contributions are welcome, especially improvements to requirements, accessibility criteria, mathematical content design, documentation, tests, and maintainable topic expansion.

Before adding application code, review the project specification, roadmap, architecture plan, and agent guidance. New implementation work should preserve accessibility and maintainability as first-class requirements.
