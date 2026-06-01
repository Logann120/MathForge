"""Accessible HTML export helpers for MathForge worksheets."""

from __future__ import annotations

from html import escape

from models.content_models import ExportResult, Solution, Worksheet


def export_worksheet_to_html(
    worksheet: Worksheet,
    include_solutions: bool = False,
) -> ExportResult:
    """Render a worksheet as a clean, portable HTML fragment.

    The export starts with an ``h2`` so it can be embedded in systems such as
    Canvas or LibGuides without creating duplicate page-level ``h1`` headings.
    """
    if not isinstance(worksheet, Worksheet):
        raise TypeError("worksheet must be a Worksheet.")

    lines: list[str] = [
        '<section class="mathforge-worksheet">',
        f"  <h2>{_escape_text(worksheet.title)}</h2>",
    ]

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

    content = "\n".join(lines) + "\n"
    return ExportResult(
        content=content,
        format_name="html",
        filename=_html_filename(worksheet),
        metadata={
            "worksheet_id": worksheet.worksheet_id or "",
            "include_solutions": str(include_solutions),
        },
    )


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


def _html_filename(worksheet: Worksheet) -> str:
    """Create a simple HTML filename from worksheet metadata."""
    base_name = worksheet.worksheet_id or worksheet.title
    safe_name = "".join(
        character.lower() if character.isalnum() else "-"
        for character in base_name.strip()
    ).strip("-")
    return f"{safe_name or 'worksheet'}.html"


def _escape_text(text: str) -> str:
    """Escape HTML-sensitive characters in text content."""
    return escape(text, quote=True)
