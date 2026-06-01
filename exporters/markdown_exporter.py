"""Markdown export helpers for MathForge worksheets."""

from __future__ import annotations

from models.content_models import ExportResult, Solution, Worksheet


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


def _markdown_filename(worksheet: Worksheet) -> str:
    """Create a simple Markdown filename from worksheet metadata."""
    base_name = worksheet.worksheet_id or worksheet.title
    safe_name = "".join(
        character.lower() if character.isalnum() else "-"
        for character in base_name.strip()
    ).strip("-")
    return f"{safe_name or 'worksheet'}.md"


def _escape_markdown_text(text: str) -> str:
    """Escape common Markdown control characters in plain text."""
    escape_characters = "\\`*_{}[]<>#|"
    return "".join(
        f"\\{character}" if character in escape_characters else character
        for character in text
    )
