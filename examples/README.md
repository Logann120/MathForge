# MathForge Examples

This directory contains deterministic example exports generated from the current MathForge MVP. The examples are intended for repository browsing, documentation review, and future AI coding agents that need to understand the current output formats.

All files are generated from existing College Algebra generators and exporters. They do not use AI, direct Canvas API integration, direct LibGuides integration, persistence, an API, or a database.

## Worksheet Examples

Each worksheet example includes problems and the solution key in both Markdown and HTML:

- `linear_equations_worksheet.md` and `linear_equations_worksheet.html`: linear equations of the form `ax + b = c`.
- `quadratic_equations_by_factoring_worksheet.md` and `quadratic_equations_by_factoring_worksheet.html`: factorable quadratic equations.
- `systems_of_linear_equations_worksheet.md` and `systems_of_linear_equations_worksheet.html`: systems of two linear equations in two variables.
- `factoring_techniques_worksheet.md` and `factoring_techniques_worksheet.html`: greatest common factor, difference of squares, and simple trinomial factoring.
- `functions_basics_worksheet.md` and `functions_basics_worksheet.html`: introductory function notation, evaluation, and domain prompts.

The older `linear_equations_sample.md` and `linear_equations_sample.html` files are retained as aliases for the current linear equations worksheet example.

## Resource Pack Example

- `linear_equations_resource_pack.md` and `linear_equations_resource_pack.html`: a full instructional resource pack with worksheet, solution key, study guide, common mistakes, tutor notes, and practice quiz.

This resource pack demonstrates the current Markdown and HTML resource-pack export shape. Other supported topics use the same exporter paths.

## LibGuides-Safe HTML Examples

- `linear_equations_worksheet_libguides.html`: a scoped, paste-friendly worksheet HTML fragment for LibGuides-style institutional pages.
- `linear_equations_resource_pack_libguides.html`: a scoped, paste-friendly resource-pack HTML fragment with worksheet, solution key, study guide, common mistakes, tutor notes, and practice quiz.

These examples demonstrate the separate LibGuides-safe exporter. They do not replace the standard HTML examples, are not included in ZIP bundles, and are not a direct LibGuides integration.

## Regeneration Notes

The examples were generated with easy difficulty, a count of three problems, and deterministic problem ID prefixes. Refresh these files through the existing generator and exporter functions rather than manually changing generated instructional content.
