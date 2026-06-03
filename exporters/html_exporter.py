"""Accessible HTML export helpers for MathForge instructional content."""

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


def export_worksheet_to_html(
    worksheet: Worksheet,
    include_solutions: bool = False,
) -> ExportResult:
    """Render a worksheet as a clean, portable HTML fragment.

    Export headings start at ``h2`` so the fragment can be embedded in systems
    such as Canvas without creating duplicate page-level ``h1`` headings.
    """
    if not isinstance(worksheet, Worksheet):
        raise TypeError("worksheet must be a Worksheet.")

    lines = _format_worksheet_html(
        worksheet,
        include_solutions=include_solutions,
        include_styles=True,
    )

    content = "\n".join(lines) + "\n"
    return ExportResult(
        content=content,
        format_name="html",
        filename=_html_filename(worksheet),
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


def export_resource_pack_to_html(
    resource_pack: ResourcePack,
    include_solutions: bool = True,
) -> ExportResult:
    """Render a full instructional resource pack as a semantic HTML fragment."""
    if not isinstance(resource_pack, ResourcePack):
        raise TypeError("resource_pack must be a ResourcePack.")

    lines: list[str] = [
        '<section class="mathforge-resource-pack">',
        *_standard_html_styles(),
        *_format_worksheet_html(
            resource_pack.worksheet,
            include_solutions=include_solutions,
            include_styles=False,
        ),
    ]
    lines.extend(_format_study_guide(resource_pack.study_guide))
    lines.extend(_format_common_mistakes(resource_pack.common_mistakes))
    lines.extend(_format_tutor_notes(resource_pack.tutor_notes))
    if resource_pack.practice_quiz is not None:
        lines.extend(_format_practice_quiz(resource_pack.practice_quiz))
    lines.append("</section>")

    content = "\n".join(lines) + "\n"
    return ExportResult(
        content=content,
        format_name="html",
        filename=_resource_pack_html_filename(resource_pack),
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


def _format_worksheet_html(
    worksheet: Worksheet,
    *,
    include_solutions: bool,
    include_styles: bool,
) -> list[str]:
    """Format worksheet HTML with optional standard export styles."""
    lines: list[str] = [
        '<section class="mathforge-worksheet">',
    ]
    if include_styles:
        lines.extend(_standard_html_styles())
    lines.append(f"  <h2>{_escape_text(worksheet.title)}</h2>")

    if worksheet.instructions.strip():
        lines.extend(
            [
                '  <section class="mathforge-instructions">',
                "    <h3>Instructions</h3>",
                f"    <p>{_escape_text(worksheet.instructions)}</p>",
                "  </section>",
            ]
        )

    lines.extend(
        [
            '  <section class="mathforge-problems">',
            "    <h3>Problems</h3>",
            "    <ol>",
        ]
    )

    for problem in worksheet.problems:
        lines.append(f"      <li>{_escape_text(problem.prompt)}</li>")

    lines.extend(["    </ol>", "  </section>"])

    if include_solutions:
        lines.extend(_format_solution_key(worksheet))

    lines.append("</section>")
    return lines


def _standard_html_styles() -> list[str]:
    """Return CSS for readable browser display and print output."""
    return [
        "  <style>",
        "    .mathforge-worksheet, .mathforge-resource-pack { line-height: 1.5; }",
        "    .mathforge-worksheet section, .mathforge-resource-pack section { margin: 1rem 0; }",
        "    .mathforge-worksheet li, .mathforge-resource-pack li { margin: 0.25rem 0; }",
        "    @media print {",
        "      .mathforge-worksheet, .mathforge-resource-pack { color: #000; font-size: 11pt; line-height: 1.35; }",
        "      .mathforge-worksheet h2, .mathforge-resource-pack h2, .mathforge-worksheet h3, .mathforge-resource-pack h3 { break-after: avoid; page-break-after: avoid; }",
        "      .mathforge-worksheet li, .mathforge-resource-pack li { break-inside: avoid; page-break-inside: avoid; }",
        "      .mathforge-worksheet .mathforge-solution-key, .mathforge-resource-pack > .mathforge-study-guide { break-before: page; page-break-before: always; }",
        "      .mathforge-resource-pack > .mathforge-common-mistakes, .mathforge-resource-pack > .mathforge-tutor-notes, .mathforge-resource-pack > .mathforge-practice-quiz { break-before: auto; page-break-before: auto; }",
        "    }",
        "  </style>",
    ]


def _format_solution_key(worksheet: Worksheet) -> list[str]:
    """Format the optional instructor-facing solution key."""
    lines = [
        '  <section class="mathforge-solution-key">',
        "    <h3>Solution Key</h3>",
        "    <ol>",
    ]
    solutions_by_problem_id = {
        solution.problem_id: solution for solution in worksheet.solutions
    }

    for problem in worksheet.problems:
        solution = solutions_by_problem_id.get(problem.problem_id)
        if solution is None:
            lines.append("      <li>No solution provided.</li>")
            continue

        lines.extend(_format_solution(solution))

    lines.extend(["    </ol>", "  </section>"])
    return lines


def _format_solution(solution: Solution) -> list[str]:
    """Format one solution entry for the HTML solution key."""
    lines = [
        "      <li>",
        f"        <p><strong>Answer:</strong> {_escape_text(solution.final_answer)}</p>",
    ]

    if solution.steps:
        lines.append("        <ol>")
        for step in solution.steps:
            lines.append(f"          <li>{_escape_text(step)}</li>")
        lines.append("        </ol>")

    lines.append("      </li>")
    return lines


def _format_study_guide(study_guide: StudyGuide) -> list[str]:
    """Format a study guide section."""
    lines = [
        '  <section class="mathforge-study-guide">',
        "    <h2>Study Guide</h2>",
        f"    <h3>{_escape_text(study_guide.title)}</h3>",
        f"    <p>{_escape_text(study_guide.overview)}</p>",
    ]

    if study_guide.key_points:
        lines.extend(_format_text_list("Key Ideas", study_guide.key_points))

    if study_guide.practice_tips:
        lines.extend(
            _format_text_list("Worked-Example Guidance", study_guide.practice_tips)
        )

    lines.append("  </section>")
    return lines


def _format_common_mistakes(common_mistakes: CommonMistakes) -> list[str]:
    """Format common mistakes and corrections."""
    lines = [
        '  <section class="mathforge-common-mistakes">',
        "    <h2>Common Mistakes</h2>",
    ]
    lines.extend(_format_text_list("Mistakes to Watch For", common_mistakes.mistakes))

    if common_mistakes.corrections:
        lines.extend(
            _format_text_list(
                "Corrections and Interventions",
                common_mistakes.corrections,
            )
        )

    lines.append("  </section>")
    return lines


def _format_tutor_notes(tutor_notes: TutorNotes) -> list[str]:
    """Format tutor-facing notes and prompts."""
    lines = [
        '  <section class="mathforge-tutor-notes">',
        "    <h2>Tutor Notes</h2>",
    ]
    lines.extend(_format_text_list("Notes", tutor_notes.notes))

    if tutor_notes.discussion_prompts:
        lines.extend(
            _format_text_list("Discussion Prompts", tutor_notes.discussion_prompts)
        )

    lines.append("  </section>")
    return lines


def _format_practice_quiz(practice_quiz: PracticeQuiz) -> list[str]:
    """Format a practice quiz section."""
    lines = [
        '  <section class="mathforge-practice-quiz">',
        "    <h2>Practice Quiz</h2>",
        f"    <h3>{_escape_text(practice_quiz.title)}</h3>",
        "    <h3>Questions</h3>",
        "    <ol>",
    ]
    for question in practice_quiz.questions:
        lines.append(f"      <li>{_escape_text(question)}</li>")
    lines.extend(["    </ol>", "    <h3>Answer Key</h3>", "    <ul>"])
    for answer in practice_quiz.answer_key:
        lines.append(f"      <li>{_escape_text(answer)}</li>")
    lines.extend(["    </ul>", "  </section>"])
    return lines


def _format_text_list(heading: str, items: tuple[str, ...]) -> list[str]:
    """Format a titled unordered list of escaped text items."""
    lines = [
        f"    <h3>{_escape_text(heading)}</h3>",
        "    <ul>",
    ]
    for item in items:
        lines.append(f"      <li>{_escape_text(item)}</li>")
    lines.append("    </ul>")
    return lines


def _html_filename(worksheet: Worksheet) -> str:
    """Create a simple HTML filename from worksheet metadata."""
    base_name = worksheet.worksheet_id or worksheet.title
    safe_name = "".join(
        character.lower() if character.isalnum() else "-"
        for character in base_name.strip()
    ).strip("-")
    return f"{safe_name or 'worksheet'}.html"


def _resource_pack_html_filename(resource_pack: ResourcePack) -> str:
    """Create an HTML filename for a resource pack."""
    worksheet_filename = _html_filename(resource_pack.worksheet)
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
