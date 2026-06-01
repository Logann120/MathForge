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

The MVP will provide a focused workflow for generating and exporting math practice materials.

### Worksheet Generation

Users should be able to generate math worksheets from selected topics, difficulty settings, and problem counts.

Expected capabilities:

- Select supported math topics.
- Choose the number of problems.
- Configure basic difficulty or variation options.
- Preview generated worksheet content before export.

### Detailed Solution Keys

Users should be able to generate solution keys that show correct answers and useful solution steps.

Expected capabilities:

- Pair each worksheet problem with a corresponding answer.
- Include step-by-step reasoning where appropriate.
- Keep solution formatting readable in both HTML and Markdown exports.

### Accessible HTML Export

Users should be able to export worksheets and solution keys as accessible HTML.

Expected capabilities:

- Use semantic document structure.
- Preserve heading order.
- Provide readable math content.
- Avoid relying on color alone to communicate meaning.
- Support keyboard and screen-reader-friendly navigation where possible.

### Markdown Export

Users should be able to export worksheets and solution keys as Markdown.

Expected capabilities:

- Produce portable Markdown that can be edited outside MathForge.
- Keep problem numbering stable.
- Keep solution sections clearly separated from student-facing content.

### SymPy Answer Validation

Users should be able to validate generated answers using SymPy.

Expected capabilities:

- Confirm symbolic equivalence where appropriate.
- Detect invalid or inconsistent generated answers.
- Flag validation failures before export.

## Non-Goals for the MVP

The MVP will not include:

- Canvas LMS integration.
- Persistent user accounts.
- Cloud hosting requirements.
- AI-generated hints or study guides.
- Full question-bank management.
- Course-specific template libraries.
- Real-time collaborative editing.

These capabilities may be considered after the core generation, validation, and export workflow is stable.

## Functional Requirements

- The application must be implemented in Python.
- The user interface must use Streamlit.
- Symbolic math validation must use SymPy.
- The system must generate worksheets and solution keys from structured problem definitions.
- The system must support accessible HTML export.
- The system must support Markdown export.
- The system must validate generated answers before export.
- The system must separate user interface code from generation, validation, and export logic.

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

The codebase should eventually:

- Keep core problem generation independent from Streamlit UI code.
- Keep export formatting independent from problem generation.
- Use typed data structures where practical.
- Include focused tests for generation, validation, and export behavior.
- Prefer small modules with clear responsibilities.
- Avoid hard-coded course assumptions in reusable logic.

## Quality Bar

MVP work should be considered complete when:

- A user can generate a worksheet for at least one supported math topic.
- A corresponding solution key can be generated.
- Generated answers are validated with SymPy.
- The worksheet and solution key can be exported to accessible HTML.
- The worksheet and solution key can be exported to Markdown.
- Exported materials are readable, structured, and suitable for classroom use.
- The architecture leaves a clear path for additional topics and future integrations.

## Future Features

Future versions may include:

- Canvas LMS integration.
- Reusable question banks.
- AI-generated hints.
- AI-generated study guides.
- Course-specific templates.
- Richer problem metadata and tagging.
- Import and export workflows for instructors maintaining existing material collections.
