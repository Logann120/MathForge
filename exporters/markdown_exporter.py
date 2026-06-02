"""Markdown export helpers for MathForge instructional content."""

from __future__ import annotations

from models.content_models import ExportResult, Solution, Worksheet
from models.resource_pack import (
    CommonMistakes,
    PracticeQuiz,
    ResourcePack,
    StudyGuide,
    TutorNotes,
)


def export_worksheet_to_markdown(
    worksheet: Worksheet,
    include_solutions: bool = False,
) -> ExportResult:
    """Render a worksheet as readable Markdown.

    The export includes the worksheet title, optional instructions, numbered
    problems, and an optional instructor-facing solution key.
    """
    if not isinstance(worksheet, Worksheet):
        raise TypeError("worksheet must be a Worksheet.")

    lines: list[str] = [
        f"# {_escape_markdown_text(worksheet.title)}",
        "",
    ]

    if worksheet.instructions.strip():
        lines.extend(
            [
                "## Instructions",
                "",
                _escape_markdown_text(worksheet.instructions),
                "",
            ]
        )

    lines.extend(["## Problems", ""])

    for index, problem in enumerate(worksheet.problems, start=1):
        lines.append(f"{index}. {_escape_markdown_text(problem.prompt)}")

    if include_solutions:
        lines.extend(["", "## Solution Key", ""])
        solutions_by_problem_id = {
            solution.problem_id: solution for solution in worksheet.solutions
        }

        for index, problem in enumerate(worksheet.problems, start=1):
            solution = solutions_by_problem_id.get(problem.problem_id)
            if solution is None:
                lines.append(f"{index}. No solution provided.")
                continue

            lines.extend(_format_solution(index, solution))

    content = "\n".join(lines).rstrip() + "\n"
    return ExportResult(
        content=content,
        format_name="markdown",
        filename=_markdown_filename(worksheet),
        metadata={
            "worksheet_id": worksheet.worksheet_id or "",
            "include_solutions": str(include_solutions),
        },
    )


def export_resource_pack_to_markdown(
    resource_pack: ResourcePack,
    include_solutions: bool = True,
) -> ExportResult:
    """Render a full instructional resource pack as readable Markdown."""
    if not isinstance(resource_pack, ResourcePack):
        raise TypeError("resource_pack must be a ResourcePack.")

    worksheet_export = export_worksheet_to_markdown(
        resource_pack.worksheet,
        include_solutions=include_solutions,
    )
    lines: list[str] = [
        worksheet_export.content.rstrip(),
        "",
        "## Study Guide",
        "",
    ]
    lines.extend(_format_study_guide(resource_pack.study_guide))
    lines.extend(["", "## Common Mistakes", ""])
    lines.extend(_format_common_mistakes(resource_pack.common_mistakes))
    lines.extend(["", "## Tutor Notes", ""])
    lines.extend(_format_tutor_notes(resource_pack.tutor_notes))
    if resource_pack.practice_quiz is not None:
        lines.extend(["", "## Practice Quiz", ""])
        lines.extend(_format_practice_quiz(resource_pack.practice_quiz))

    content = "\n".join(lines).rstrip() + "\n"
    return ExportResult(
        content=content,
        format_name="markdown",
        filename=_resource_pack_markdown_filename(resource_pack),
        metadata={
            "worksheet_id": resource_pack.worksheet.worksheet_id or "",
            "include_solutions": str(include_solutions),
            "resource_type": "resource_pack",
        },
    )


def _format_solution(index: int, solution: Solution) -> list[str]:
    """Format a solution entry for the Markdown solution key."""
    lines = [
        f"{index}. Answer: {_escape_markdown_text(solution.final_answer)}",
    ]

    if solution.steps:
        lines.append("")
        for step in solution.steps:
            lines.append(f"   - {_escape_markdown_text(step)}")

    return lines


def _format_study_guide(study_guide: StudyGuide) -> list[str]:
    """Format a study guide section."""
    lines = [
        f"### {_escape_markdown_text(study_guide.title)}",
        "",
        _escape_markdown_text(study_guide.overview),
    ]

    if study_guide.key_points:
        lines.extend(["", "#### Key Ideas", ""])
        lines.extend(_format_bullets(study_guide.key_points))

    if study_guide.practice_tips:
        lines.extend(["", "#### Worked-Example Guidance", ""])
        lines.extend(_format_bullets(study_guide.practice_tips))

    return lines


def _format_common_mistakes(common_mistakes: CommonMistakes) -> list[str]:
    """Format common mistakes and corrections."""
    lines = ["### Mistakes to Watch For", ""]
    lines.extend(_format_bullets(common_mistakes.mistakes))

    if common_mistakes.corrections:
        lines.extend(["", "### Corrections and Interventions", ""])
        lines.extend(_format_bullets(common_mistakes.corrections))

    return lines


def _format_tutor_notes(tutor_notes: TutorNotes) -> list[str]:
    """Format tutor-facing notes and prompts."""
    lines = ["### Notes", ""]
    lines.extend(_format_bullets(tutor_notes.notes))

    if tutor_notes.discussion_prompts:
        lines.extend(["", "### Discussion Prompts", ""])
        lines.extend(_format_bullets(tutor_notes.discussion_prompts))

    return lines


def _format_practice_quiz(practice_quiz: PracticeQuiz) -> list[str]:
    """Format a practice quiz section."""
    lines = [
        f"### {_escape_markdown_text(practice_quiz.title)}",
        "",
        "#### Questions",
        "",
    ]
    lines.extend(_format_numbered_items(practice_quiz.questions))
    lines.extend(["", "#### Answer Key", ""])
    lines.extend(_format_bullets(practice_quiz.answer_key))
    return lines


def _format_bullets(items: tuple[str, ...]) -> list[str]:
    """Format text items as escaped Markdown bullets."""
    return [f"- {_escape_markdown_text(item)}" for item in items]


def _format_numbered_items(items: tuple[str, ...]) -> list[str]:
    """Format text items as escaped Markdown numbered items."""
    return [
        f"{index}. {_escape_markdown_text(item)}"
        for index, item in enumerate(items, start=1)
    ]


def _markdown_filename(worksheet: Worksheet) -> str:
    """Create a simple Markdown filename from worksheet metadata."""
    base_name = worksheet.worksheet_id or worksheet.title
    safe_name = "".join(
        character.lower() if character.isalnum() else "-"
        for character in base_name.strip()
    ).strip("-")
    return f"{safe_name or 'worksheet'}.md"


def _resource_pack_markdown_filename(resource_pack: ResourcePack) -> str:
    """Create a Markdown filename for a resource pack."""
    worksheet_filename = _markdown_filename(resource_pack.worksheet)
    return worksheet_filename.replace(".md", "-resource-pack.md")


def _escape_markdown_text(text: str) -> str:
    """Escape common Markdown control characters in plain text."""
    escape_characters = "\\`*_{}[]<>#|"
    return "".join(
        f"\\{character}" if character in escape_characters else character
        for character in text
    )
