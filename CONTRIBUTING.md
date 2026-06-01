# Contributing to MathForge

Thank you for your interest in contributing to MathForge.

MathForge is currently establishing its initial repository structure and project direction. Contributions should align with the documented mission: helping mathematics instructors generate high-quality instructional materials with maintainable, accessible open-source tools.

## Current Contribution Scope

At this stage, useful contributions include:

- Improving project documentation.
- Refining MVP requirements.
- Clarifying accessibility expectations.
- Reviewing architecture boundaries.
- Proposing maintainable approaches for future Python, Streamlit, and SymPy implementation.
- Adding placeholder structure only when it supports the documented architecture.

Do not add business logic, Streamlit UI, or AI integration until implementation work is explicitly requested.

## Project Principles

Contributions should prioritize:

- Maintainability.
- Accessibility.
- Mathematical correctness.
- Instructor control over generated materials.
- Clear separation between user interface, generation, validation, and export concerns.

## Repository Structure

The initial structure is organized around future responsibilities:

- `app/` for the future Streamlit interface.
- `generator/` for future problem and solution generation.
- `validators/` for future answer validation, including SymPy-based checks.
- `exporters/` for future HTML and Markdown exports.
- `templates/` for future worksheet or course templates.
- `tests/` for future automated tests.
- `docs/` for supplemental project documentation.

## Documentation Standards

Documentation should be clear, professional, and suitable for a public GitHub project.

When changing documentation:

- Prefer precise language over broad claims.
- Separate current scope from future plans.
- Keep accessibility and maintainability visible.
- Update related files when a requirement or architectural decision changes.

## Future Code Standards

When application code is approved, contributions should:

- Keep Streamlit UI code separate from reusable domain logic.
- Keep generation, validation, and export modules independently testable.
- Use SymPy for symbolic validation where appropriate.
- Add focused tests for new behavior.
- Document known limitations.

## Questions and Design Discussion

For larger changes, start with a proposal in documentation or an issue before implementing. This helps keep the project approachable for educators, tutors, students, and open-source contributors.
