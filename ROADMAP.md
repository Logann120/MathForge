# MathForge Roadmap

This roadmap describes the planned progression from documentation through the MVP and future platform features. Dates are intentionally omitted until the project has active implementation capacity.

## Phase 0: Planning and Project Foundation

Status: In progress

Goals:

- Define the project mission and target users.
- Document MVP requirements.
- Establish architecture principles before implementation.
- Clarify contributor and agent expectations.
- Establish the initial repository structure without business logic.
- Keep the repository pre-implementation until the initial design is accepted.

Deliverables:

- README.md
- PROJECT_SPEC.md
- ROADMAP.md
- ARCHITECTURE.md
- AGENTS.md
- CONTRIBUTING.md
- Initial Python package placeholders
- Project metadata and MIT license

## Phase 1: MVP Prototype

Status: Planned

Goals:

- Build a minimal Streamlit interface.
- Implement one or more worksheet generators for initial math topics.
- Generate corresponding detailed solution keys.
- Validate generated answers with SymPy.
- Export worksheets and solution keys to Markdown.
- Export worksheets and solution keys to accessible HTML.

Success criteria:

- Instructors can generate a usable worksheet.
- The solution key is accurate and readable.
- SymPy validation catches incorrect generated answers.
- HTML and Markdown exports are suitable for classroom review.

## Phase 2: MVP Hardening

Status: Planned

Goals:

- Expand topic coverage.
- Add focused automated tests for generation, validation, and export workflows.
- Improve accessibility of the Streamlit interface and exported HTML.
- Refine error messages and validation feedback.
- Establish stable data structures for problems, worksheets, and solution keys.

Success criteria:

- The project has a reliable core workflow.
- Contributors can add new problem types without changing unrelated systems.
- Exported materials remain consistent across supported problem types.

## Phase 3: Instructor Workflow Improvements

Status: Planned

Goals:

- Add reusable worksheet settings.
- Support richer difficulty controls.
- Improve preview and export review flows.
- Add metadata for topics, learning objectives, and estimated difficulty.
- Explore import and export conventions for reusable material collections.

Success criteria:

- Instructors can create materials faster across repeated class sessions.
- Materials are easier to organize and revise.
- The application remains simple enough for tutors and learning centers.

## Phase 4: Question Banks and Templates

Status: Future

Goals:

- Introduce question-bank management.
- Add course-specific templates.
- Support curated problem sets by topic or objective.
- Allow instructors to reuse and adapt generated content.

Success criteria:

- MathForge supports both generated and curated content.
- Templates reduce setup time for common courses.
- Question banks remain portable and maintainable.

## Phase 5: Integrations and AI-Assisted Features

Status: Future

Goals:

- Add Canvas LMS integration.
- Explore AI-generated hints.
- Explore AI-generated study guides.
- Support instructor review before any AI-generated material is published.

Success criteria:

- Integrations fit instructor workflows without weakening the core export workflow.
- AI-assisted features remain transparent, reviewable, and optional.
- Mathematical correctness and accessibility remain required quality gates.

## Ongoing Priorities

Across all phases, MathForge should continue to prioritize:

- Maintainable Python architecture.
- Accessibility for students and instructors.
- Reliable symbolic validation with SymPy.
- Clear open-source documentation.
- Instructor control over generated materials.
