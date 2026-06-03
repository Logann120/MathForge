# Adding a Supported Math Topic

This guide explains how to add a new supported math topic to MathForge using the supported-topic registry. Topic additions should remain deterministic, instructor-reviewable, and small enough to test thoroughly.

MathForge does not use AI, direct Canvas API integration, direct LibGuides integration, persistence, authentication, an external API, or plugin loading for topic support.

## Guiding Principles

- Keep generated content deterministic for the same inputs.
- Keep prompts, answers, solutions, study guides, mistakes, tutor notes, and quizzes instructor-reviewable.
- Preserve existing public generator functions and existing topic behavior.
- Keep top-level topic routing centralized in `topics/registry.py`.
- Avoid broad aliases that could accidentally route a future topic.
- Do not change exporters unless the existing generic worksheet/resource-pack exporters cannot represent the new content.

## Files Usually Changed

### `generator/problem_generator.py`

Keep this file as the public worksheet generator API. For a new topic, add the deterministic worksheet generator implementation in a topic-focused module under `generator/topics/`, then re-export the public function from `generator/problem_generator.py`.

The generator should:

- Accept `topic`, `difficulty`, `count`, and `start_id`.
- Validate `count` and text inputs consistently with existing generators.
- Return a `Worksheet` containing `MathProblem` and `Solution` objects.
- Use stable problem IDs derived from `start_id`.
- Validate generated answers where practical, usually with SymPy or existing validation helpers.
- Avoid Streamlit, AI services, randomness without a fixed deterministic pattern, persistence, or network calls.

### `generator/resource_pack_generator.py`

Keep this file as the public resource-pack generator API. For a new topic, add the deterministic resource-pack generator implementation in the same topic-focused module under `generator/topics/`, then re-export the public function from `generator/resource_pack_generator.py`.

The generator should:

- Reuse the worksheet generator.
- Return a `ResourcePack`.
- Include study guide, common mistakes, tutor notes, and a practice quiz when supported.
- Keep topic-specific instructional text explicit and reviewable.
- Avoid changing existing topic resource-pack content.

### `generator/topics/`

Add one topic-focused module for the new topic, such as `generator/topics/exponential_equations.py`. Keep worksheet generation, resource-pack generation, and small topic-specific helper functions together when that makes the instructional logic easier to review.

Use `generator/topics/common.py` only for small shared helpers that are truly generic. Do not introduce a plugin system or broad abstraction layer for normal topic additions.

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

Do not change `exporters/markdown_exporter.py`, `exporters/html_exporter.py`, `exporters/libguides_html_exporter.py`, or `exporters/canvas_exporter.py` for a normal topic addition. The current exporters are generic for worksheets and resource packs.

Update exporters only when the new topic introduces content that cannot be represented by the existing `Worksheet` or `ResourcePack` models. Exporter changes should include Markdown and HTML tests.

### Tests

Add or update focused tests for:

- Worksheet generation for the new topic.
- Resource-pack generation for the new topic, if supported.
- Registry metadata, including label, slug, prefix, difficulty level, output type, objective metadata, and aliases.
- Curriculum template/objective coverage, if curriculum-aligned.
- Curriculum-based resource-pack generation, if curriculum-aligned.
- Streamlit import or smoke behavior to confirm the topic appears and routes correctly.
- Markdown, standard HTML, LibGuides-safe HTML, Canvas CSV, or ZIP behavior only if exporter behavior changes.

Existing tests should continue to pass without changing expected output for existing topics.

### Difficulty Expansion

Add new difficulty levels topic by topic. Do not add `medium` or `hard` to a topic's `supported_difficulty_levels` until that topic has deterministic generator behavior and focused tests for those levels.

For each new difficulty level:

- Preserve existing `easy` output exactly unless an explicit behavior change is requested.
- Define the pedagogical meaning of the level in the topic generator tests.
- Add deterministic generator tests for the new level.
- Add validation-oriented tests for generated answers where practical.
- Keep resource-pack metadata consistent with the worksheet difficulty.
- Avoid broad export snapshots for every difficulty unless exporter behavior changes.
- Do not expose the difficulty in Streamlit until UI behavior can be supported cleanly for the relevant topic or topics.

The current Medium/Hard pilot is limited to linear equations at the generator and registry level. The Streamlit UI and built-in presets remain Easy-only until topic-specific UI support is implemented.

### Examples

Add generated example exports under `examples/` when the topic is ready for repository browsing. Prefer both Markdown and HTML worksheet examples. Add a resource-pack example when useful, but avoid duplicating every possible resource pack if one representative example already demonstrates the generic export shape.

Refresh `examples/README.md` so future contributors know what each example demonstrates.

## What Not To Change

When adding a topic, do not:

- Add AI or LLM integration.
- Add direct Canvas API integration.
- Add a database, authentication, public API, deployment workflow, or plugin architecture.
- Change existing generated math content.
- Change existing worksheet or resource-pack export formats unless required by new model needs.
- Add unsupported difficulty labels to the Streamlit UI or registry.
- Add a difficulty label to the registry before the generator and validation tests prove it works for that topic.
- Scatter topic label, prefix, slug, or alias maps outside the registry.
- Add broad generator abstractions when a small topic-focused module is enough.

## Topic Addition Checklist

- [ ] Add deterministic worksheet generation in a topic-focused module under `generator/topics/`.
- [ ] Re-export the worksheet generator from `generator/problem_generator.py`.
- [ ] Add focused worksheet generation tests.
- [ ] Add focused difficulty tests if the topic supports more than Easy.
- [ ] Add deterministic resource-pack generation in the topic-focused module, if supported.
- [ ] Re-export the resource-pack generator from `generator/resource_pack_generator.py`.
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
