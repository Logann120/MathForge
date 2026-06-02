# Adding a Supported Math Topic

This guide explains how to add a new supported math topic to MathForge using the supported-topic registry. Topic additions should remain deterministic, instructor-reviewable, and small enough to test thoroughly.

MathForge does not use AI, Canvas integration, persistence, authentication, an external API, or plugin loading for topic support.

## Guiding Principles

- Keep generated content deterministic for the same inputs.
- Keep prompts, answers, solutions, study guides, mistakes, tutor notes, and quizzes instructor-reviewable.
- Preserve existing public generator functions and existing topic behavior.
- Keep top-level topic routing centralized in `topics/registry.py`.
- Avoid broad aliases that could accidentally route a future topic.
- Do not change exporters unless the existing generic worksheet/resource-pack exporters cannot represent the new content.

## Files Usually Changed

### `generator/problem_generator.py`

Add the deterministic worksheet generator for the new topic. The generator should:

- Accept `topic`, `difficulty`, `count`, and `start_id`.
- Validate `count` and text inputs consistently with existing generators.
- Return a `Worksheet` containing `MathProblem` and `Solution` objects.
- Use stable problem IDs derived from `start_id`.
- Validate generated answers where practical, usually with SymPy or existing validation helpers.
- Avoid Streamlit, AI services, randomness without a fixed deterministic pattern, persistence, or network calls.

### `generator/resource_pack_generator.py`

Add the deterministic resource-pack generator if the topic supports full resource packs. The generator should:

- Reuse the worksheet generator.
- Return a `ResourcePack`.
- Include study guide, common mistakes, tutor notes, and a practice quiz when supported.
- Keep topic-specific instructional text explicit and reviewable.
- Avoid changing existing topic resource-pack content.

### `topics/registry.py`

Add one `SupportedTopic` entry after the generator functions exist. Include:

- `slug`: stable, lowercase, hyphenated identifier.
- `display_label`: user-visible label shown in Streamlit.
- `default_problem_id_prefix`: short stable prefix used for problem IDs.
- `supported_output_types`: usually `("worksheet", "resource_pack")`.
- `worksheet_generator` and `resource_pack_generator`.
- `supported_difficulty_levels`: include only levels that are actually implemented.
- curriculum metadata if the topic is part of the College Algebra template.
- `topic_aliases`: exact normalized aliases for learning-objective topic routing.

Labels, slugs, prefixes, and aliases are user-facing or routing-sensitive. Choose them deliberately and cover them with tests.

### `generator/curriculum_resource_pack_generator.py`

This file usually does not need topic-specific edits because it routes through `topics/registry.py`. Update it only if the new topic requires a genuinely different curriculum-to-resource-pack workflow.

### `templates/course_templates.py`

This file usually does not need topic-specific edits because the College Algebra template is built from registry metadata. Update it only if a topic needs a different course-template structure or if a new template is introduced.

### Exporters

Do not change `exporters/markdown_exporter.py` or `exporters/html_exporter.py` for a normal topic addition. The current exporters are generic for worksheets and resource packs.

Update exporters only when the new topic introduces content that cannot be represented by the existing `Worksheet` or `ResourcePack` models. Exporter changes should include Markdown and HTML tests.

### Tests

Add or update focused tests for:

- Worksheet generation for the new topic.
- Resource-pack generation for the new topic, if supported.
- Registry metadata, including label, slug, prefix, difficulty level, output type, objective metadata, and aliases.
- Curriculum template/objective coverage, if curriculum-aligned.
- Curriculum-based resource-pack generation, if curriculum-aligned.
- Streamlit import or smoke behavior to confirm the topic appears and routes correctly.
- Markdown and HTML export behavior only if exporter behavior changes.

Existing tests should continue to pass without changing expected output for existing topics.

### Examples

Add generated example exports under `examples/` when the topic is ready for repository browsing. Prefer both Markdown and HTML worksheet examples. Add a resource-pack example when useful, but avoid duplicating every possible resource pack if one representative example already demonstrates the generic export shape.

Refresh `examples/README.md` so future contributors know what each example demonstrates.

## What Not To Change

When adding a topic, do not:

- Add AI or LLM integration.
- Add Canvas integration.
- Add a database, authentication, public API, deployment workflow, or plugin architecture.
- Change existing generated math content.
- Change existing worksheet or resource-pack export formats unless required by new model needs.
- Add unsupported difficulty labels to the Streamlit UI or registry.
- Scatter topic label, prefix, slug, or alias maps outside the registry.
- Split generator modules unless that refactor is explicitly requested.

## Topic Addition Checklist

- [ ] Add deterministic worksheet generation in `generator/problem_generator.py`.
- [ ] Add focused worksheet generation tests.
- [ ] Add deterministic resource-pack generation in `generator/resource_pack_generator.py`, if supported.
- [ ] Add focused resource-pack tests, including practice quiz coverage when supported.
- [ ] Add one `SupportedTopic` entry in `topics/registry.py`.
- [ ] Add or update registry tests for slug, label, prefix, output type, difficulty, curriculum metadata, and aliases.
- [ ] Confirm aliases are exact and not broad fuzzy matches.
- [ ] Confirm the College Algebra template includes the topic if curriculum-aligned.
- [ ] Add curriculum-generation tests if the topic has a learning objective.
- [ ] Confirm Streamlit topic mode and learning-objective mode still smoke test successfully.
- [ ] Add or refresh examples for Markdown and HTML outputs.
- [ ] Run the full test suite.

## Final Review Questions

- Does the same input produce the same worksheet and resource pack every time?
- Can an instructor review every generated prompt, solution, and resource section?
- Are labels, slugs, prefixes, and aliases deliberate and tested?
- Did existing topics keep the same generated output and visible behavior?
- Did the change avoid new dependencies and integrations?
