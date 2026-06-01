# Agent Guidance for MathForge

This repository is currently in a planning and pre-implementation structure phase.

Agents and contributors must not add business logic, Streamlit UI, or AI integration until the project owner explicitly requests implementation work.

## Current Scope

Allowed work:

- Improve README.md.
- Improve PROJECT_SPEC.md.
- Improve ROADMAP.md.
- Improve ARCHITECTURE.md.
- Improve AGENTS.md.
- Improve CONTRIBUTING.md.
- Clarify requirements, risks, and acceptance criteria.
- Propose maintainability and accessibility improvements.
- Maintain placeholder package structure when explicitly requested.

Out of scope until explicitly requested:

- Python application modules.
- Streamlit app files.
- SymPy validation implementation.
- Dependency installation.
- Generated application assets.

## Project Direction

MathForge will be an open-source platform for generating high-quality mathematics instructional materials.

The planned implementation stack is:

- Python
- Streamlit
- SymPy

The MVP will support:

- Math worksheet generation.
- Detailed solution key generation.
- Accessible HTML export.
- Markdown export.
- Answer validation using SymPy.

## Working Principles

When working in this repository:

- Preserve existing files unless the user explicitly asks for deletion.
- Keep documentation professional and suitable for a public GitHub project.
- Prioritize maintainability and accessibility.
- Separate confirmed requirements from future ideas.
- Avoid speculative implementation details that would constrain the project too early.
- Prefer clear, plain language over buzzwords.

## Accessibility Expectations

Documentation and future implementation should treat accessibility as a core requirement.

Agents should preserve or improve guidance related to:

- Semantic HTML export.
- Logical heading structure.
- Readable Markdown.
- Screen-reader-friendly material structure.
- Avoiding color-only meaning.
- Instructor review of generated materials.

## Maintainability Expectations

Future implementation plans should preserve clear boundaries between:

- Streamlit user interface code.
- Problem generation logic.
- SymPy validation logic.
- Worksheet assembly.
- HTML and Markdown exporters.
- Future integrations.

## Change Discipline

Before editing, inspect the existing repository state and read relevant files.

For documentation-only tasks:

- Do not add code.
- Do not install dependencies.
- Do not run formatters that modify unrelated files.
- Do not delete existing files.
- Summarize intended file changes before making them when requested.

For future implementation tasks:

- Confirm scope before adding new project structure.
- Add focused tests for core generation, validation, and export behavior.
- Keep UI behavior separate from reusable domain logic.
- Document any accessibility limitations that cannot be resolved immediately.
