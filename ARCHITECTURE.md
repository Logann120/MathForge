# MathForge Architecture

MathForge is a Python and Streamlit MVP with deterministic College Algebra generation, SymPy-powered validation helpers, and export support for Markdown and accessible HTML.

This document describes the current implemented architecture. MathForge is no longer a planning-only repository: it has working generators, models, exporters, validators, a Streamlit interface, curriculum templates, and automated tests.

## Architecture Goals

- Keep the codebase approachable for open-source contributors.
- Separate user interface concerns from math generation logic.
- Make answer validation explicit and testable.
- Keep exports accessible and predictable.
- Allow new math topics and templates to be added without large rewrites.
- Preserve deterministic, instructor-reviewable generation.

## Technology Stack

- Python for application and domain logic.
- Streamlit for the web interface.
- SymPy for symbolic answer validation.
- Markdown for portable text exports.
- Semantic HTML for accessible browser-based exports.

## Current Architecture

The application separates responsibilities into clear modules so contributors and future AI coding agents can reason about changes safely.

### User Interface

Purpose:

- Present worksheet and resource-pack generation options.
- Offer built-in presets for common instructor workflows.
- Collect user configuration.
- Display worksheet, solution, and instructional resource previews.
- Trigger Markdown and HTML export actions.

Current implementation:

- `app/main.py` contains the Streamlit MVP.
- `app/presets.py` contains built-in preset metadata for default UI settings.
- Topic mode generates from a supported topic label.
- Learning Objective mode generates from the College Algebra template.
- The UI hands off to generator and exporter functions rather than embedding generation logic.

### Problem Generation

Purpose:

- Generate structured math problems from topic and difficulty settings.
- Produce problem prompts, expected answers, and solution steps.
- Keep generation deterministic and reviewable.

Current implementation:

- `generator/problem_generator.py` contains deterministic worksheet generators.
- Supported topics are linear equations, quadratic equations by factoring, systems of linear equations, factoring techniques, and functions basics.
- Generators return reusable worksheet models and do not depend on Streamlit.

### Resource Pack Generation

Purpose:

- Assemble complete instructional resource packs around generated worksheets.
- Provide study guides, common mistakes, tutor notes, and practice quizzes.
- Preserve deterministic output for supported topics.

Current implementation:

- `generator/resource_pack_generator.py` generates topic-based resource packs.
- `generator/curriculum_resource_pack_generator.py` generates resource packs from supported learning objectives.
- Generated resource content is deterministic and does not use AI or LLM services.

### Answer Validation

Purpose:

- Validate generated answers and equivalent answer forms.
- Use SymPy for symbolic equivalence checks where appropriate.
- Report validation failures clearly before export or display.

Current implementation:

- `validators/sympy_validator.py` contains dedicated validation functions.
- Validation functions return structured results for success, failure, and parse errors.
- Tests cover equivalent expressions, numeric answers, equation solutions, and invalid input.

### Models and Worksheet Assembly

Purpose:

- Represent generated content with typed dataclasses.
- Combine generated problems into worksheets.
- Pair worksheets with solution keys.
- Preserve stable ordering, identifiers, and metadata.

Current implementation:

- `models/content_models.py` defines worksheet, problem, solution, hint, and export dataclasses.
- `models/resource_pack.py` defines study guide, common mistakes, tutor notes, practice quiz, and resource-pack dataclasses.
- `models/curriculum.py` defines curriculum alignment dataclasses.
- Student-facing worksheet content and instructor-facing solution/resource sections are represented separately.

### Exporters

Purpose:

- Convert worksheets, solution keys, and resource packs into external formats.
- Support accessible HTML.
- Support readable Markdown.

Current implementation:

- `exporters/markdown_exporter.py` renders worksheets and full resource packs to Markdown.
- `exporters/html_exporter.py` renders worksheets and full resource packs to portable semantic HTML.
- `exporters/bundle_exporter.py` packages already-rendered exports into ZIP convenience downloads using Python standard-library tools.
- `exporters/download_filenames.py` creates instructor-friendly download filenames from export metadata without changing rendered export content.
- Exporters do not generate problems and reuse worksheet rendering behavior where appropriate. ZIP bundles do not replace individual Markdown or HTML exports.

### Supported Topic Registry

Purpose:

- Centralize supported topic labels, slugs, default problem ID prefixes, output types, generator routing, difficulty support, and curriculum metadata.
- Make supported topics easier to discover without scanning the UI, curriculum generator, and templates separately.
- Keep topic additions explicit and reviewable.

Current implementation:

- `topics/registry.py` contains the supported-topic registry.
- `app/main.py` uses the registry for topic options, default problem ID prefixes, and topic routing.
- `generator/curriculum_resource_pack_generator.py` uses the registry for learning-objective topic routing.
- `templates/course_templates.py` uses the registry to construct the College Algebra modules and objectives.
- The registry is a small metadata table, not a plugin system.
- Topic additions should follow `docs/ADDING_TOPICS.md`.

### Curriculum Templates

Purpose:

- Provide deterministic course, module, and learning-objective structures.
- Support curriculum-aligned generation without Canvas or external systems.

Current implementation:

- `templates/course_templates.py` contains the College Algebra sample template.
- Supported objectives are built from the topic registry metadata.

### Tests

Purpose:

- Preserve generator, model, validator, exporter, curriculum, and Streamlit import behavior.
- Keep future changes reviewable.

Current implementation:

- `tests/` contains focused unit and smoke tests for the MVP modules.

## Conceptual Data Flow

1. A user selects worksheet or resource-pack options in Streamlit.
2. A built-in preset can provide editable starting defaults.
3. The UI passes structured options to the generation layer.
4. Problem generators create structured problem objects.
5. The validation layer checks generated answers with SymPy where practical.
6. Resource-pack generators optionally assemble study guides, common mistakes, tutor notes, and practice quizzes.
7. Exporters render Markdown or semantic HTML.
8. Download filename helpers derive clear filenames from export metadata.
9. Optional ZIP bundle helpers group related rendered exports.
10. The UI offers previews and download actions.

## Core Data Concepts

The current MVP uses dataclasses for:

- MathProblem: prompt, answer, topic, difficulty, hints, and metadata.
- HintSet: scaffolded hints for a problem.
- Solution: answer and solution steps paired with a problem identifier.
- Worksheet: title, instructions, problems, solutions, and metadata.
- ExportResult: rendered content, format, filename, and metadata.
- StudyGuide, CommonMistakes, TutorNotes, PracticeQuiz, and ResourcePack.
- LearningObjective, CourseModule, and CourseTemplate.

## Accessibility Architecture

Accessible output is designed into the export layer.

HTML exporters should:

- Use semantic headings.
- Preserve logical reading order.
- Keep problem and solution sections clearly labeled.
- Avoid layout structures that confuse assistive technologies.
- Avoid color-only meaning.
- Include document language and metadata when practical.
- Follow `docs/MANUAL_QA.md` for manual accessibility review.

Markdown exporters should:

- Use consistent heading levels.
- Use readable numbered lists.
- Separate worksheet content from solution keys.
- Avoid formatting that only works in a single rendering environment.

## Validation Strategy

SymPy is used to validate symbolic correctness in the core workflow.

The validation layer:

- Compares mathematically equivalent expressions where appropriate.
- Detects malformed expressions.
- Returns structured errors rather than crashing the UI.
- Distinguishes validation failures from unsupported validation cases.
- Is covered by focused automated tests.

## Current Non-Features

The MVP intentionally has no:

- AI or LLM integration.
- Canvas LMS integration.
- Database or persistence layer.
- Authentication or authorization.
- External API.
- Production deployment or hosting workflow.

Generated content is deterministic and instructor-reviewable. Future AI-assisted work should remain optional, transparent, and subject to instructor approval.

## Known Limitations

- Example exports should be periodically checked against current generated output.
- ZIP bundles currently include the rendered exports already available in the active export panel; they do not add separate generated artifacts.
- Built-in generation presets are fixed metadata only; there are no custom saved presets, accounts, persistence, or file-based configuration.
- Continuous integration runs the pytest suite on Python 3.11 and Python 3.12.
- There is no deployment workflow.
- Accessibility and browser QA are limited and should be expanded before broader release.
- Top-level topic routing is centralized in `topics/registry.py`; topic-specific generator internals remain explicit.
- `generator/solution_generator.py` remains a placeholder.

## Maintainability Principles

Future implementation should:

- Keep modules small and purpose-driven.
- Avoid coupling Streamlit widgets to core generation logic.
- Make supported topics easy to discover and extend.
- Add future topics through the supported-topic registry after adding deterministic generators and tests.
- Prefer explicit data structures over loosely shaped dictionaries when practical.
- Document assumptions for each problem generator.
- Add tests before expanding high-risk logic.

## Future Integration Considerations

Future Canvas LMS integration, question banks, AI-generated hints, AI-generated study guides, and broader course-specific templates should build on the same core concepts rather than bypassing them.

Integrations should treat validated worksheet content as the source of truth. AI-assisted features should remain reviewable by instructors and should never replace validation or instructor approval.
