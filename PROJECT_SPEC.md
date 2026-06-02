# MathForge Project Specification

## Overview

MathForge is an open-source platform that helps mathematics instructors generate high-quality instructional materials. The project is intended for educators and support teams who need reliable, reusable, accessible materials for mathematics instruction.

The product should reduce repetitive material creation work while preserving instructor control over mathematical accuracy, formatting, and pedagogy.

## Mission

MathForge helps mathematics instructors generate clear worksheets, detailed solution keys, and accessible exports using maintainable open-source tools.

## Target Users

- Community college instructors who need course-ready worksheets and solution keys.
- Math tutors who need targeted practice material for individual learners.
- Learning centers that support many students across multiple math topics.
- Students who benefit from accessible practice materials and detailed worked solutions.

## MVP Features

The current MVP provides a focused workflow for generating and exporting deterministic College Algebra practice materials. It includes worksheet generation, solution keys, instructional resource packs, practice quizzes, Markdown export, HTML export, curriculum-aligned generation, and SymPy-backed validation helpers.

### Worksheet Generation

Users can generate math worksheets from selected supported topics, difficulty settings, and problem counts.

Current capabilities:

- Select supported College Algebra topics.
- Choose the number of problems.
- Use the currently supported easy difficulty.
- Preview generated worksheet content before export.

### Detailed Solution Keys

Users can generate solution keys that show correct answers and useful solution steps.

Current capabilities:

- Pair each worksheet problem with a corresponding answer.
- Include step-by-step reasoning where appropriate.
- Keep solution formatting readable in both HTML and Markdown exports.

### Instructional Resource Packs

Users can generate full instructional resource packs for supported topics and learning objectives.

Current capabilities:

- Include a worksheet and solution key.
- Include a study guide.
- Include common mistakes.
- Include tutor notes.
- Include a deterministic practice quiz.
- Export the full resource pack to Markdown or HTML.

### Accessible HTML Export

Users can export worksheets, solution keys, and full resource packs as accessible HTML.

Current capabilities:

- Use semantic document structure.
- Preserve heading order.
- Provide readable math content.
- Avoid relying on color alone to communicate meaning.
- Support keyboard and screen-reader-friendly navigation where possible.

### Markdown Export

Users can export worksheets, solution keys, and full resource packs as Markdown.

Current capabilities:

- Produce portable Markdown that can be edited outside MathForge.
- Keep problem numbering stable.
- Keep solution sections clearly separated from student-facing content.

### SymPy Answer Validation

The validation layer uses SymPy for symbolic and numeric answer checks where appropriate.

Current capabilities:

- Confirm symbolic equivalence where appropriate.
- Detect invalid or inconsistent generated answers.
- Flag validation failures before export.

## Non-Goals for the MVP

The MVP will not include:

- Canvas LMS integration.
- AI or LLM integration.
- Persistent user accounts.
- Authentication or authorization.
- A database or persistence layer.
- A public API.
- Production deployment or hosting workflow.
- Cloud hosting requirements.
- AI-generated hints, study guides, quizzes, or tutor notes.
- Full question-bank management.
- Broad course-specific template libraries beyond the deterministic College Algebra sample template.
- Real-time collaborative editing.

These capabilities may be considered after the core generation, validation, and export workflow is stable.

## Functional Requirements

- The application must be implemented in Python.
- The user interface must use Streamlit.
- Symbolic math validation must use SymPy.
- The system must generate worksheets, solution keys, and instructional resource packs from structured problem definitions.
- The system must support accessible HTML export.
- The system must support Markdown export.
- The system must validate generated answers where practical before export.
- The system must separate user interface code from generation, validation, and export logic.

## Supported MVP Topics

The implemented College Algebra MVP supports:

- Linear equations.
- Quadratic equations by factoring.
- Systems of linear equations.
- Factoring techniques.
- Functions basics.

The implemented sample curriculum template is College Algebra. It supports topic mode and learning-objective mode in the Streamlit app.

## Accessibility Requirements

Accessibility is a core requirement, not a final polish step.

MathForge should:

- Prefer semantic HTML exports.
- Use descriptive headings and consistent document structure.
- Avoid visual-only cues.
- Produce readable content at default browser zoom levels.
- Support keyboard navigation in the Streamlit interface where Streamlit allows it.
- Keep exported materials usable by students with assistive technologies.
- Document any known accessibility limitations.

## Maintainability Requirements

MathForge should be easy for open-source contributors to understand and extend.

The codebase should:

- Keep core problem generation independent from Streamlit UI code.
- Keep export formatting independent from problem generation.
- Use typed data structures where practical.
- Include focused tests for generation, validation, and export behavior.
- Prefer small modules with clear responsibilities.
- Avoid hard-coded course assumptions in reusable logic.

## Quality Bar

MVP 0.1 work is considered complete when:

- A user can generate worksheets for the supported College Algebra topics.
- A corresponding solution key can be generated.
- Generated answers are validated with SymPy.
- The worksheet and solution key can be exported to accessible HTML.
- The worksheet and solution key can be exported to Markdown.
- Full resource packs can be generated and exported.
- Exported materials are readable, structured, and suitable for classroom use.
- The architecture leaves a clear path for additional topics and future integrations.

## Known Limitations

- Example exports are stale and currently show an older linear-equations worksheet sample.
- `docs/` exists as a placeholder folder and does not yet contain supplemental guides.
- Continuous integration runs the pytest suite on Python 3.11 and Python 3.12.
- There is no deployment workflow.
- Accessibility and browser QA are limited beyond automated tests and Streamlit smoke coverage.
- Top-level topic discovery and routing now use a supported-topic registry; topic-specific generator internals remain explicit and should stay small.
- There is no AI or LLM integration, Canvas integration, database, authentication, API, or production deployment.

## Future Features

Future versions may include:

- Canvas LMS integration.
- Reusable question banks.
- AI-generated hints.
- AI-generated study guides.
- Course-specific templates.
- Richer problem metadata and tagging.
- Import and export workflows for instructors maintaining existing material collections.
