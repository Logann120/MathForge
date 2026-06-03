# MathForge Roadmap

This roadmap reflects the current implemented MathForge MVP. Dates are intentionally omitted. Future work should preserve deterministic generation, instructor review, local usability, accessibility, and low operational complexity.

## Current Status

Status: Working MVP / Phase 5C export-hardening checkpoint

MathForge currently supports deterministic College Algebra worksheet and resource-pack generation for:

- Linear equations.
- Quadratic equations by factoring.
- Systems of linear equations.
- Factoring techniques.
- Functions basics.

Current export paths:

- Markdown.
- Print-friendly standard HTML.
- LibGuides-safe HTML.
- ZIP bundles containing Markdown plus standard HTML.
- Canvas-friendly manual-entry CSV.

Current non-features:

- No AI or LLM integration.
- No direct Canvas API integration.
- No direct LibGuides API integration.
- No persistence, database, authentication, accounts, external API, deployment workflow, Docker, or plugin architecture.

## Phase 0: Foundation

Status: Completed

Completed work:

- Project mission and target users.
- MVP requirements and repository documentation.
- Initial architecture boundaries.
- Contributor and agent guidance.
- Python package structure.
- Project metadata and MIT license.

## Phase 1: Core MVP

Status: Completed

Completed work:

- Streamlit app.
- Core dataclass models.
- Deterministic worksheet generation.
- Detailed solution keys.
- SymPy validation helpers.
- Markdown export.
- Standard HTML export.
- Initial tests.

## Phase 2: Instructional Resource Packs and Curriculum Alignment

Status: Completed

Completed work:

- Resource-pack models.
- Study guides, common mistakes, tutor notes, and practice quizzes.
- Deterministic resource-pack generation.
- College Algebra curriculum template.
- Learning Objective mode.
- Curriculum-based resource-pack generation.

## Phase 3: Topic Coverage and Registry Hardening

Status: Completed

Completed work:

- Quadratic equations by factoring.
- Systems of linear equations.
- Factoring techniques.
- Functions basics.
- Supported-topic registry.
- Registry-backed Streamlit routing.
- Registry-backed curriculum template construction.
- Topic-registry documentation.
- Registry tests and snapshot-style safeguards.

## Phase 4: Stabilization and Maintainability

Status: Completed

Completed work:

- Refreshed examples.
- GitHub Actions pytest CI on Python 3.11 and Python 3.12.
- Export regression tests.
- Generator regression tests across supported topics.
- Generated math validation tests.
- Manual QA and accessibility guide.
- Topic-focused generator module split.
- Streamlit app module split.
- App helper unit tests.

## Phase 5A: Instructor Workflow Improvements

Status: Completed

Completed work:

- Optional ZIP export bundles.
- Built-in generation presets.
- Clear deterministic download filenames.
- Generated-output summaries.
- Improved Learning Objective mode context.

## Phase 5B: Targeted Export Integrations

Status: Completed for current scope

Completed work:

- Canvas-friendly manual-entry CSV export for worksheet problems and practice quizzes.
- LibGuides-safe HTML export for worksheets and resource packs.
- LibGuides-safe example exports.
- Documentation and manual QA guidance for paste-friendly institutional-page workflows.

Scope boundaries:

- Canvas CSV is not Canvas API integration.
- LibGuides-safe HTML is not direct LibGuides integration.
- ZIP bundles remain Markdown plus standard HTML only.

## Phase 5C: Print-Friendly Standard HTML Polish

Status: Completed for current scope

Completed work:

- Print-focused CSS in the standard HTML exporter.
- Page-break handling for headings, list items, solution keys, and major resource-pack sections.
- Tests confirming standard HTML print CSS and LibGuides-safe separation.
- Manual QA guidance for browser print preview.

Scope boundaries:

- This is not PDF generation.
- ZIP bundles remain Markdown plus standard HTML only.
- Markdown, Canvas CSV, and LibGuides-safe HTML formats remain separate.

## Recommended Next Phase: Accessibility and Example Maintenance

Status: Recommended next implementation direction

Recommended goals:

- Run manual browser, print-preview, and accessibility review against representative generated outputs.
- Refresh examples only when exporter behavior or topic coverage changes.
- Keep PDF generation out of scope unless explicitly requested.
- Keep ZIP bundle behavior unchanged unless explicitly requested.

Why this is next:

- It fits existing export-first instructor workflows.
- It avoids new dependencies and service integrations.
- It improves confidence in classroom usability without adding persistence, accounts, APIs, or platform complexity.

## Later Possible Direction: Difficulty Expansion

Status: Linear-equations pilot started; broader expansion later

Potential goals:

- Add meaningful medium and hard difficulty levels for supported topics.
- Make difficulty behavior explicit and tested per topic.
- Update registry metadata only when difficulty levels are actually implemented.
- Preserve existing easy-output behavior.
- Keep the Streamlit UI and presets Easy-only until topic-specific difficulty support can be exposed cleanly.

Risks:

- Difficulty is not just UI metadata; it requires topic-specific math design, validation, examples, and regression tests.
- Adding difficulty too early could obscure current deterministic behavior.
- Unknown generator difficulty strings currently have legacy fallback behavior in some generators; changing that should be a deliberate compatibility decision.

## Later Possible Direction: Topic Expansion

Status: Later

Potential goals:

- Add more College Algebra topics through the supported-topic registry.
- Keep new topic generation in `generator/topics/`.
- Preserve public generator APIs.
- Add examples and tests for each topic.

Risks:

- Topic expansion should not reintroduce branch-heavy app or generator code.
- New topics must remain deterministic and instructor-reviewable.

## Later Possible Direction: Local Question Bank Exploration

Status: Later / design first

Potential goals:

- Explore optional local file-based question banks.
- Keep storage local and explicit if implemented.
- Avoid accounts, databases, hosted services, or synchronization.

Risks:

- Even local persistence increases schema, migration, validation, and UX complexity.
- This should not happen before export and topic-generation behavior are stable.

## Not Yet: Direct Integrations and AI

Status: Out of scope unless explicitly requested

Do not add without explicit instruction:

- AI or LLM-generated content.
- Direct Canvas API integration.
- Direct LibGuides API integration.
- OAuth, tokens, secrets, network publishing, or LMS writeback.
- Database or persistence layer.
- Authentication or user accounts.
- External API.
- Deployment infrastructure.
- Docker.
- Plugin architecture.

## Ongoing Priorities

Across all phases, MathForge should continue to prioritize:

- Deterministic generation.
- Instructor-reviewable content.
- Mathematical correctness.
- Accessibility.
- Stable public APIs.
- Stable export formats.
- Small modules with clear responsibilities.
- Focused tests before behavior expansion.
