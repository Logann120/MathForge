"""LibGuides-safe HTML export helpers for MathForge instructional content."""

from __future__ import annotations

from html import escape

from models.content_models import ExportResult, Solution, Worksheet
from models.resource_pack import (
    CommonMistakes,
    PracticeQuiz,
    ResourcePack,
    StudyGuide,
    TutorNotes,
)


def export_worksheet_to_libguides_html(
    worksheet: Worksheet,
    include_solutions: bool = False,
) -> ExportResult:
    """Render a worksheet as a scoped HTML fragment for LibGuides-style embeds."""
    if not isinstance(worksheet, Worksheet):
        raise TypeError("worksheet must be a Worksheet.")

    lines: list[str] = [
        '<div class="mathforge-libguides-export" data-mathforge-export="worksheet">',
        *_scoped_styles(),
    ]
    lines.extend(_format_worksheet(worksheet, include_solutions=include_solutions))
    lines.append("</div>")

    content = "\n".join(lines) + "\n"
    return ExportResult(
        content=content,
        format_name="libguides_html",
        filename=_libguides_html_filename(worksheet),
        metadata={
            "worksheet_id": worksheet.worksheet_id or "",
            "include_solutions": str(include_solutions),
            "resource_type": "worksheet",
            "topic": worksheet.metadata.get("topic", ""),
            "difficulty": worksheet.metadata.get("difficulty", ""),
            "problem_id_prefix": _problem_id_prefix(worksheet),
            "problem_count": str(len(worksheet.problems)),
        },
    )


def export_resource_pack_to_libguides_html(
    resource_pack: ResourcePack,
    include_solutions: bool = True,
) -> ExportResult:
    """Render a resource pack as a scoped HTML fragment for LibGuides-style embeds."""
    if not isinstance(resource_pack, ResourcePack):
        raise TypeError("resource_pack must be a ResourcePack.")

    lines: list[str] = [
        '<div class="mathforge-libguides-export" data-mathforge-export="resource-pack">',
        *_scoped_styles(),
        '  <div class="mathforge-lg-resource-pack">',
    ]
    lines.extend(_format_worksheet(resource_pack.worksheet, include_solutions=include_solutions))
    lines.extend(_format_study_guide(resource_pack.study_guide))
    lines.extend(_format_common_mistakes(resource_pack.common_mistakes))
    lines.extend(_format_tutor_notes(resource_pack.tutor_notes))
    if resource_pack.practice_quiz is not None:
        lines.extend(_format_practice_quiz(resource_pack.practice_quiz))
    lines.extend(["  </div>", "</div>"])

    content = "\n".join(lines) + "\n"
    return ExportResult(
        content=content,
        format_name="libguides_html",
        filename=_resource_pack_libguides_html_filename(resource_pack),
        metadata={
            "worksheet_id": resource_pack.worksheet.worksheet_id or "",
            "include_solutions": str(include_solutions),
            "resource_type": "resource_pack",
            "topic": resource_pack.metadata.get(
                "topic",
                resource_pack.worksheet.metadata.get("topic", ""),
            ),
            "difficulty": resource_pack.metadata.get(
                "difficulty",
                resource_pack.worksheet.metadata.get("difficulty", ""),
            ),
            "problem_id_prefix": _problem_id_prefix(resource_pack.worksheet),
            "problem_count": str(len(resource_pack.worksheet.problems)),
            "learning_objective": resource_pack.metadata.get(
                "learning_objective",
                "",
            ),
            "learning_objective_id": resource_pack.metadata.get(
                "learning_objective_id",
                "",
            ),
        },
    )


def _scoped_styles() -> list[str]:
    """Return CSS scoped to the MathForge LibGuides wrapper."""
    return [
        "  <style>",
        "    .mathforge-libguides-export { font-family: system-ui, sans-serif; line-height: 1.5; }",
        "    .mathforge-libguides-export .mathforge-lg-title { margin: 0 0 0.75rem; }",
        "    .mathforge-libguides-export .mathforge-lg-heading { margin: 1rem 0 0.4rem; }",
        "    .mathforge-libguides-export .mathforge-lg-subheading { margin: 0.75rem 0 0.35rem; }",
        "    .mathforge-libguides-export .mathforge-lg-block { margin: 1rem 0; }",
        "    .mathforge-libguides-export .mathforge-lg-text { margin: 0.35rem 0; }",
        "    .mathforge-libguides-export .mathforge-lg-list { margin: 0.35rem 0 0.75rem 1.5rem; padding-left: 1rem; }",
        "    .mathforge-libguides-export .mathforge-lg-item { margin: 0.35rem 0; }",
        "  </style>",
    ]


def _format_worksheet(
    worksheet: Worksheet,
    *,
    include_solutions: bool,
) -> list[str]:
    """Format the worksheet body inside the scoped wrapper."""
    lines = [
        '  <div class="mathforge-lg-worksheet">',
        f'    <h3 class="mathforge-lg-title">{_escape_text(worksheet.title)}</h3>',
    ]

    if worksheet.instructions.strip():
        lines.extend(
            [
                '    <div class="mathforge-lg-block mathforge-lg-instructions">',
                '      <h4 class="mathforge-lg-heading">Instructions</h4>',
                f'      <p class="mathforge-lg-text">{_escape_text(worksheet.instructions)}</p>',
                "    </div>",
            ]
        )

    lines.extend(
        [
            '    <div class="mathforge-lg-block mathforge-lg-problems">',
            '      <h4 class="mathforge-lg-heading">Problems</h4>',
            '      <ol class="mathforge-lg-list">',
        ]
    )

    for problem in worksheet.problems:
        lines.append(f'        <li class="mathforge-lg-item">{_escape_text(problem.prompt)}</li>')

    lines.extend(["      </ol>", "    </div>"])

    if include_solutions:
        lines.extend(_format_solution_key(worksheet))

    lines.append("  </div>")
    return lines


def _format_solution_key(worksheet: Worksheet) -> list[str]:
    """Format the optional instructor-facing solution key."""
    lines = [
        '    <div class="mathforge-lg-block mathforge-lg-solution-key">',
        '      <h4 class="mathforge-lg-heading">Solution Key</h4>',
        '      <ol class="mathforge-lg-list">',
    ]
    solutions_by_problem_id = {
        solution.problem_id: solution for solution in worksheet.solutions
    }

    for problem in worksheet.problems:
        solution = solutions_by_problem_id.get(problem.problem_id)
        if solution is None:
            lines.append('        <li class="mathforge-lg-item">No solution provided.</li>')
            continue

        lines.extend(_format_solution(solution))

    lines.extend(["      </ol>", "    </div>"])
    return lines


def _format_solution(solution: Solution) -> list[str]:
    """Format one solution entry for the HTML solution key."""
    lines = [
        '        <li class="mathforge-lg-item">',
        (
            '          <p class="mathforge-lg-text"><strong>Answer:</strong> '
            f"{_escape_text(solution.final_answer)}</p>"
        ),
    ]

    if solution.steps:
        lines.append('          <ol class="mathforge-lg-list">')
        for step in solution.steps:
            lines.append(f'            <li class="mathforge-lg-item">{_escape_text(step)}</li>')
        lines.append("          </ol>")

    lines.append("        </li>")
    return lines


def _format_study_guide(study_guide: StudyGuide) -> list[str]:
    """Format a study guide section."""
    lines = [
        '    <div class="mathforge-lg-block mathforge-lg-study-guide">',
        '      <h3 class="mathforge-lg-title">Study Guide</h3>',
        f'      <h4 class="mathforge-lg-heading">{_escape_text(study_guide.title)}</h4>',
        f'      <p class="mathforge-lg-text">{_escape_text(study_guide.overview)}</p>',
    ]

    if study_guide.key_points:
        lines.extend(_format_text_list("Key Ideas", study_guide.key_points))

    if study_guide.practice_tips:
        lines.extend(
            _format_text_list("Worked-Example Guidance", study_guide.practice_tips)
        )

    lines.append("    </div>")
    return lines


def _format_common_mistakes(common_mistakes: CommonMistakes) -> list[str]:
    """Format common mistakes and corrections."""
    lines = [
        '    <div class="mathforge-lg-block mathforge-lg-common-mistakes">',
        '      <h3 class="mathforge-lg-title">Common Mistakes</h3>',
    ]
    lines.extend(_format_text_list("Mistakes to Watch For", common_mistakes.mistakes))

    if common_mistakes.corrections:
        lines.extend(
            _format_text_list(
                "Corrections and Interventions",
                common_mistakes.corrections,
            )
        )

    lines.append("    </div>")
    return lines


def _format_tutor_notes(tutor_notes: TutorNotes) -> list[str]:
    """Format tutor-facing notes and prompts."""
    lines = [
        '    <div class="mathforge-lg-block mathforge-lg-tutor-notes">',
        '      <h3 class="mathforge-lg-title">Tutor Notes</h3>',
    ]
    lines.extend(_format_text_list("Notes", tutor_notes.notes))

    if tutor_notes.discussion_prompts:
        lines.extend(
            _format_text_list("Discussion Prompts", tutor_notes.discussion_prompts)
        )

    lines.append("    </div>")
    return lines


def _format_practice_quiz(practice_quiz: PracticeQuiz) -> list[str]:
    """Format a practice quiz section."""
    lines = [
        '    <div class="mathforge-lg-block mathforge-lg-practice-quiz">',
        '      <h3 class="mathforge-lg-title">Practice Quiz</h3>',
        f'      <h4 class="mathforge-lg-heading">{_escape_text(practice_quiz.title)}</h4>',
        '      <h4 class="mathforge-lg-heading">Questions</h4>',
        '      <ol class="mathforge-lg-list">',
    ]
    for question in practice_quiz.questions:
        lines.append(f'        <li class="mathforge-lg-item">{_escape_text(question)}</li>')
    lines.extend(
        [
            "      </ol>",
            '      <h4 class="mathforge-lg-heading">Answer Key</h4>',
            '      <ul class="mathforge-lg-list">',
        ]
    )
    for answer in practice_quiz.answer_key:
        lines.append(f'        <li class="mathforge-lg-item">{_escape_text(answer)}</li>')
    lines.extend(["      </ul>", "    </div>"])
    return lines


def _format_text_list(heading: str, items: tuple[str, ...]) -> list[str]:
    """Format a titled unordered list of escaped text items."""
    lines = [
        f'      <h4 class="mathforge-lg-heading">{_escape_text(heading)}</h4>',
        '      <ul class="mathforge-lg-list">',
    ]
    for item in items:
        lines.append(f'        <li class="mathforge-lg-item">{_escape_text(item)}</li>')
    lines.append("      </ul>")
    return lines


def _libguides_html_filename(worksheet: Worksheet) -> str:
    """Create a simple LibGuides HTML filename from worksheet metadata."""
    base_name = worksheet.worksheet_id or worksheet.title
    safe_name = "".join(
        character.lower() if character.isalnum() else "-"
        for character in base_name.strip()
    ).strip("-")
    return f"{safe_name or 'worksheet'}-libguides.html"


def _resource_pack_libguides_html_filename(resource_pack: ResourcePack) -> str:
    """Create a LibGuides HTML filename for a resource pack."""
    worksheet_filename = _libguides_html_filename(resource_pack.worksheet)
    return worksheet_filename.replace(".html", "-resource-pack.html")


def _problem_id_prefix(worksheet: Worksheet) -> str:
    """Return the problem ID prefix used by a worksheet."""
    if worksheet.worksheet_id and worksheet.worksheet_id.endswith("-worksheet"):
        return worksheet.worksheet_id.removesuffix("-worksheet")
    if worksheet.problems:
        return worksheet.problems[0].problem_id.rsplit("-", maxsplit=1)[0]
    return ""


def _escape_text(text: str) -> str:
    """Escape HTML-sensitive characters in text content."""
    return escape(text, quote=True)
