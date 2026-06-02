# MathForge Roadmap

This roadmap describes the planned progression from documentation through the MVP and future platform features. Dates are intentionally omitted until the project has active implementation capacity.

## Phase 0: Planning and Project Foundation

Status: Completed

Goals:

- Completed: Define the project mission and target users.
- Completed: Document MVP requirements.
- Completed: Establish architecture principles before implementation.
- Completed: Clarify contributor and agent expectations.
- Completed: Establish the initial repository structure.

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

Status: Completed for MVP 0.1

Goals:

- Completed: Build a minimal Streamlit interface.
- Completed: Implement a deterministic linear equation worksheet generator.
- Completed: Generate corresponding detailed solution keys.
- Completed: Validate generated answers with SymPy.
- Completed: Export worksheets and solution keys to Markdown.
- Completed: Export worksheets and solution keys to accessible HTML.
- Completed: Generate deterministic instructional resource packs.
- Completed: Export full resource packs to Markdown.
- Completed: Export full resource packs to accessible HTML.

Success criteria:

- Completed: Instructors can generate a usable linear equation worksheet.
- Completed: The solution key is accurate and readable.
- Completed: SymPy validation catches incorrect generated answers.
- Completed: HTML and Markdown exports are suitable for classroom review.
- Completed: Resource packs include study guides, common mistakes, and tutor notes.

## Phase 2: MVP Hardening

Status: Next

Goals:

- Completed: Add initial curriculum-aligned generation with a College Algebra linear equations objective.
- Completed: Expand topic coverage to quadratic equations by factoring.
- Completed: Expand College Algebra coverage to systems of linear equations.
- Completed: Expand College Algebra coverage to factoring techniques.
- Completed: Expand College Algebra coverage to functions basics.
- Completed: Add practice quizzes to instructional resource packs.
- Completed: Polish the Streamlit UI for MVP demo readiness.
- Continue careful topic expansion beyond the current College Algebra topics.
- Continue focused automated tests for generation, validation, resource packs, and export workflows.
- Review accessibility of the Streamlit interface and exported HTML.
- Refine error messages and validation feedback.
- Stabilize data structures for problems, worksheets, solution keys, and instructional resource packs.

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
