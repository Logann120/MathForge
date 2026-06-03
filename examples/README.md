# MathForge Examples

This directory contains deterministic example exports generated from the current MathForge MVP. The examples are intended for repository browsing, documentation review, and future AI coding agents that need to understand the current output formats.

All files are generated from existing College Algebra generators and exporters. They do not use AI, direct Canvas API integration, direct LibGuides integration, persistence, an API, or a database.

## Worksheet Examples

Each worksheet example includes problems and the solution key in both Markdown and standard HTML. The standard HTML examples include the current browser print-preview CSS used by the standard HTML exporter:

- `linear_equations_worksheet.md` and `linear_equations_worksheet.html`: linear equations of the form `ax + b = c`.
- `quadratic_equations_by_factoring_worksheet.md` and `quadratic_equations_by_factoring_worksheet.html`: factorable quadratic equations.
- `systems_of_linear_equations_worksheet.md` and `systems_of_linear_equations_worksheet.html`: systems of two linear equations in two variables.
- `factoring_techniques_worksheet.md` and `factoring_techniques_worksheet.html`: greatest common factor, difference of squares, and simple trinomial factoring.
- `functions_basics_worksheet.md` and `functions_basics_worksheet.html`: introductory function notation, evaluation, and domain prompts.

The older `linear_equations_sample.md` and `linear_equations_sample.html` files are retained as aliases for the current linear equations worksheet example.

### Difficulty Pilot Examples

All current supported topics now support Easy, Medium, and Hard at the generator, registry, and Streamlit UI level. The standard worksheet examples above show Easy output. These additional Markdown examples demonstrate the deterministic Medium/Hard pilot without adding a full matrix of export formats:

- `linear_equations_medium_worksheet.md`: medium linear equations with negative constants and negative integer solutions.
- `linear_equations_hard_worksheet.md`: hard linear equations with variables on both sides.
- `quadratic_equations_by_factoring_medium_worksheet.md`: medium monic quadratic equations with mixed-sign integer roots.
- `quadratic_equations_by_factoring_hard_worksheet.md`: hard non-monic quadratic equations with integer roots.
- `systems_of_linear_equations_medium_worksheet.md`: medium systems requiring one equation scaling before elimination.
- `systems_of_linear_equations_hard_worksheet.md`: hard systems with negative coefficients and negative integer solutions.
- `factoring_techniques_medium_worksheet.md`: medium factoring with variable GCF, coefficient difference of squares, and mixed-sign trinomials.
- `factoring_techniques_hard_worksheet.md`: hard factoring with grouping and non-monic trinomials.
- `functions_basics_medium_worksheet.md`: medium function practice with quadratic evaluation, ordered-pair notation, and square-root domain reasoning.
- `functions_basics_hard_worksheet.md`: hard function practice with composition evaluation and two-factor denominator domain reasoning.

Medium/Hard examples are Markdown-only pilot examples, not a full export-format matrix. Do not add Medium/Hard examples for a topic until that topic has explicit deterministic generator behavior, registry metadata, UI exposure, and tests.

## Resource Pack Example

- `linear_equations_resource_pack.md` and `linear_equations_resource_pack.html`: a full instructional resource pack with worksheet, solution key, study guide, common mistakes, tutor notes, and practice quiz.

This resource pack demonstrates the current Markdown and print-friendly standard HTML resource-pack export shape. Other supported topics use the same exporter paths.

## LibGuides-Safe HTML Examples

- `linear_equations_worksheet_libguides.html`: a scoped, paste-friendly worksheet HTML fragment for LibGuides-style institutional pages.
- `linear_equations_resource_pack_libguides.html`: a scoped, paste-friendly resource-pack HTML fragment with worksheet, solution key, study guide, common mistakes, tutor notes, and practice quiz.

These examples demonstrate the separate LibGuides-safe exporter. They do not replace the standard HTML examples, are not included in ZIP bundles, and are not a direct LibGuides integration.

## Regeneration Notes

Most examples were generated with easy difficulty, a count of three problems, and deterministic problem ID prefixes. The Medium/Hard Markdown examples were generated with the same count and the current deterministic difficulty branches. Refresh these files through the existing generator and exporter functions rather than manually changing generated instructional content.
