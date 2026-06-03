# MathForge Project Specification

## Overview

MathForge is a working deterministic Python/Streamlit MVP for generating College Algebra instructional materials. It helps instructors, tutors, learning centers, and students create instructor-reviewable worksheets, solution keys, and supporting instructional resources without relying on AI-generated content or external services.

MathForge is not a planning-only repository. The current implementation includes generators, models, exporters, validators, a Streamlit app, curriculum templates, examples, CI, and automated tests.

## Mission

MathForge helps mathematics instructors create clear, accessible, maintainable learning materials with less repetitive manual work.

The current product direction prioritizes deterministic generation, instructor review, local usability, accessibility, and low operational complexity.

## Target Users

- Community college instructors who need course-ready worksheets and solution keys.
- Math tutors who need targeted practice material and support notes.
- Learning centers that support students across recurring College Algebra topics.
- Students who benefit from accessible practice materials and worked solutions.

## Current Supported Topics

The implemented College Algebra MVP supports:

- Linear equations.
- Quadratic equations by factoring.
- Systems of linear equations.
- Factoring techniques.
- Functions basics.

The supported-topic registry in `topics/registry.py` stores topic labels, slugs, default problem ID prefixes, supported difficulty levels, generator routing, and College Algebra learning-objective metadata.

## Current Output Types

MathForge currently generates:

- Worksheets.
- Detailed solution keys.
- Full instructional resource packs.
- Study guides.
- Common mistakes.
- Tutor notes.
- Practice quizzes.
- Curriculum-aligned resource packs from the deterministic College Algebra template.

Generation is deterministic for the same inputs and remains instructor-reviewable.

## Current Export Formats

MathForge currently supports:

- Markdown exports for worksheets and resource packs.
- Standard HTML exports for worksheets and resource packs.
- LibGuides-safe HTML exports for paste-friendly institutional-page embeds.
- ZIP bundles containing Markdown plus standard HTML.
- Canvas-friendly manual-entry CSV exports for worksheet problems and resource-pack practice quizzes.

Important export boundaries:

- Standard HTML and LibGuides-safe HTML are separate export paths.
- LibGuides-safe HTML is a paste-friendly fragment, not a direct LibGuides integration.
- Canvas-friendly CSV is manual-entry/import-friendly only, not Canvas API integration.
- ZIP bundles include Markdown plus standard HTML only.

## Current Application Workflow

The Streamlit app supports:

- Built-in generation presets.
- Topic mode.
- Learning Objective mode.
- Worksheet-only output.
- Full Resource Pack output.
- Configurable problem count.
- Easy difficulty.
- Advanced problem ID prefix editing.
- Generated-output summaries.
- Download controls for all current export paths.

## Functional Requirements

- The application must be implemented in Python.
- The user interface must use Streamlit.
- Symbolic validation must use SymPy where practical.
- Core generation must remain deterministic.
- Generated content must remain instructor-reviewable.
- Public generator APIs should remain backward-compatible unless a change is explicitly requested.
- Existing export formats should not change unless an explicit exporter-format change is requested.
- The system must separate Streamlit UI code from generation, validation, models, templates, and exporters.

## Current Architecture Requirements

- `topics/registry.py` remains the source of supported-topic metadata and top-level topic routing.
- `generator/topics/` contains topic-focused deterministic generator implementations.
- `generator/problem_generator.py` and `generator/resource_pack_generator.py` preserve public generator API imports.
- `app/main.py` remains the Streamlit entry point.
- `app/controls.py`, `app/rendering.py`, `app/downloads.py`, and `app/generation_context.py` keep app concerns separated.
- Exporters should not generate math content.
- Validators should not depend on Streamlit.

## Current Non-Features

MathForge currently has no:

- AI or LLM integration.
- Direct Canvas API integration.
- Canvas OAuth, tokens, secrets, network publishing, or LMS writeback.
- Direct LibGuides API integration.
- Database or persistence layer.
- Authentication or user accounts.
- External API.
- Production deployment workflow.
- Docker configuration.
- Plugin architecture.
- Medium or hard difficulty generation exposed in the UI.
- PDF generation.

These areas are out of scope unless explicitly requested.

## Quality Bar

Current MVP quality expectations:

- Supported topics generate deterministic worksheets.
- Each worksheet includes matching solution data.
- Resource packs include study guides, common mistakes, tutor notes, and practice quizzes.
- SymPy validation is used where practical for generated math content.
- Markdown, standard HTML, LibGuides-safe HTML, Canvas-friendly CSV, and ZIP bundle behavior are covered by focused tests.
- Streamlit app behavior is covered by smoke tests.
- Manual QA guidance exists for UI workflow, exports, accessibility, and institutional paste workflows.
- CI runs pytest on Python 3.11 and Python 3.12.

## Known Limitations

- Only easy difficulty is fully exposed in the Streamlit UI.
- Topic coverage is limited to five College Algebra topics.
- Plain-text math notation is readable but not equivalent to MathML or fully accessible equation rendering.
- Browser and accessibility QA remain primarily manual.
- LibGuides-safe HTML compatibility can vary by institutional editor policies.
- Canvas CSV compatibility can vary by institution and may require instructor cleanup.
- ZIP bundles intentionally omit Canvas CSV and LibGuides-safe HTML.
- Examples should be periodically refreshed when exporter behavior changes.
- There is no deployment workflow or production hosting configuration.

## Future Directions

Near-term work should focus on export and usability hardening rather than broad platform expansion:

- Print-friendly standard HTML improvements.
- More explicit browser/print manual QA.
- Continued documentation and example refreshes.
- Careful accessibility improvements.

Later work may include:

- Medium and hard difficulty levels.
- Additional College Algebra topics.
- Optional local file-based question-bank experiments.
- Broader course templates.

AI-assisted features, direct Canvas API integration, direct LibGuides integration, persistence, authentication, databases, external APIs, deployment infrastructure, Docker, and plugin architecture should remain out of scope unless explicitly requested.
