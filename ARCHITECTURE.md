# MathForge Architecture

MathForge will be a Python application with a Streamlit user interface, SymPy-powered validation, and export support for accessible HTML and Markdown.

This document describes the intended architecture before business logic or user interface code is added. The repository may contain placeholder packages that reserve the major architectural boundaries.

## Architecture Goals

- Keep the codebase approachable for open-source contributors.
- Separate user interface concerns from math generation logic.
- Make answer validation explicit and testable.
- Keep exports accessible and predictable.
- Allow new math topics and templates to be added without large rewrites.

## Proposed Technology Stack

- Python for application and domain logic.
- Streamlit for the web interface.
- SymPy for symbolic answer validation.
- Markdown for portable text exports.
- Semantic HTML for accessible browser-based exports.

## Proposed Module Boundaries

The eventual application should separate responsibilities into clear modules.

### User Interface

Purpose:

- Present worksheet generation options.
- Collect user configuration.
- Display worksheet and solution previews.
- Trigger validation and export actions.

Expected implementation direction:

- Streamlit pages and UI components.
- Minimal business logic in UI code.
- Clear handoff from UI state to core generation services.

### Problem Generation

Purpose:

- Generate structured math problems from topic and difficulty settings.
- Produce problem prompts, expected answers, and optional solution steps.
- Keep generation deterministic when a seed is provided.

Expected implementation direction:

- Topic-specific generators.
- Shared problem data structures.
- No direct dependency on Streamlit.

### Answer Validation

Purpose:

- Validate generated answers and equivalent student-facing answer forms.
- Use SymPy for symbolic equivalence checks where appropriate.
- Report validation failures clearly before export.

Expected implementation direction:

- Dedicated validation functions or services.
- Explicit result objects for success, failure, and warnings.
- Tests covering equivalent expressions and known invalid cases.

### Worksheet Assembly

Purpose:

- Combine generated problems into a complete worksheet.
- Pair worksheets with solution keys.
- Preserve stable ordering, numbering, and metadata.

Expected implementation direction:

- Worksheet-level data structures.
- Clear distinction between student-facing content and instructor-only solutions.

### Exporters

Purpose:

- Convert worksheets and solution keys into external formats.
- Support accessible HTML.
- Support Markdown.

Expected implementation direction:

- Separate exporter modules for each format.
- No problem generation inside exporters.
- Shared rendering helpers only when they improve consistency.

## Conceptual Data Flow

1. A user selects worksheet options in Streamlit.
2. The UI passes structured options to the generation layer.
3. Problem generators create structured problem objects.
4. The validation layer checks generated answers with SymPy.
5. Worksheet assembly creates a worksheet and solution key.
6. Exporters render accessible HTML and Markdown.
7. The UI offers previews and download actions.

## Suggested Core Data Concepts

Future implementation may define data structures such as:

- Problem: prompt, answer, topic, difficulty, metadata, and solution steps.
- SolutionStep: explanation text, mathematical expression, or transformation.
- Worksheet: title, instructions, problem list, and metadata.
- SolutionKey: worksheet reference, numbered answers, and solution steps.
- ValidationResult: status, messages, warnings, and failure details.
- ExportDocument: rendered content, format, filename, and metadata.

These concepts are planning guidance only. They should be refined during implementation.

## Accessibility Architecture

Accessible output should be designed into the export layer.

HTML exporters should:

- Use semantic headings.
- Preserve logical reading order.
- Keep problem and solution sections clearly labeled.
- Avoid layout structures that confuse assistive technologies.
- Avoid color-only meaning.
- Include document language and metadata when practical.

Markdown exporters should:

- Use consistent heading levels.
- Use readable numbered lists.
- Separate worksheet content from solution keys.
- Avoid formatting that only works in a single rendering environment.

## Validation Strategy

SymPy should be used to validate symbolic correctness in the core workflow.

The validation layer should:

- Compare mathematically equivalent expressions where appropriate.
- Detect malformed expressions.
- Return structured errors rather than crashing the UI.
- Distinguish validation failures from unsupported validation cases.
- Be covered by focused automated tests once application code exists.

## Maintainability Principles

Future implementation should:

- Keep modules small and purpose-driven.
- Avoid coupling Streamlit widgets to core generation logic.
- Make supported topics easy to discover and extend.
- Prefer explicit data structures over loosely shaped dictionaries when practical.
- Document assumptions for each problem generator.
- Add tests before expanding high-risk logic.

## Future Integration Considerations

Future Canvas LMS integration, question banks, AI-generated hints, AI-generated study guides, and course-specific templates should build on the same core concepts rather than bypassing them.

Integrations should treat validated worksheet content as the source of truth. AI-assisted features should remain reviewable by instructors and should never replace validation or instructor approval.
