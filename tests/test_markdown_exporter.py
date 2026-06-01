"""Tests for Markdown worksheet exports."""

import pytest

from exporters.markdown_exporter import export_worksheet_to_markdown
from generator.problem_generator import generate_linear_equation_worksheet
from models.content_models import ExportResult, MathProblem, Worksheet


def test_export_worksheet_to_markdown_returns_export_result() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_worksheet_to_markdown(worksheet)

    assert isinstance(result, ExportResult)
    assert result.format_name == "markdown"
    assert result.filename == "linear-worksheet.md"
    assert result.metadata["worksheet_id"] == "linear-worksheet"
    assert result.metadata["include_solutions"] == "False"


def test_export_worksheet_to_markdown_includes_title_instructions_and_problems() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=2,
        start_id="linear",
    )

    result = export_worksheet_to_markdown(worksheet)

    assert "# Linear equations Worksheet" in result.content
    assert "## Instructions" in result.content
    assert "Solve each equation for x." in result.content
    assert "## Problems" in result.content
    assert "1. Solve for x: 2\\*x + 1 = 3" in result.content
    assert "2. Solve for x: 3\\*x + 3 = 9" in result.content
    assert "## Solution Key" not in result.content


def test_export_worksheet_to_markdown_can_include_solution_key() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_worksheet_to_markdown(worksheet, include_solutions=True)

    assert "## Solution Key" in result.content
    assert "1. Answer: 1" in result.content
    assert "   - Start with 2\\*x + 1 = 3." in result.content
    assert "   - x = 1." in result.content
    assert result.metadata["include_solutions"] == "True"


def test_export_worksheet_to_markdown_omits_empty_instructions_section() -> None:
    problem = MathProblem(
        problem_id="p1",
        prompt="Solve x = 1.",
        answer="1",
    )
    worksheet = Worksheet(title="Practice", instructions="", problems=(problem,))

    result = export_worksheet_to_markdown(worksheet)

    assert "# Practice" in result.content
    assert "## Instructions" not in result.content
    assert "1. Solve x = 1." in result.content


def test_export_worksheet_to_markdown_escapes_markdown_sensitive_text() -> None:
    problem = MathProblem(
        problem_id="p1",
        prompt="Solve *x* = [1].",
        answer="1",
    )
    worksheet = Worksheet(title="Practice #1", problems=(problem,))

    result = export_worksheet_to_markdown(worksheet)

    assert "# Practice \\#1" in result.content
    assert "1. Solve \\*x\\* = \\[1\\]." in result.content


def test_export_worksheet_to_markdown_rejects_non_worksheet() -> None:
    with pytest.raises(TypeError, match="worksheet must be a Worksheet"):
        export_worksheet_to_markdown("not a worksheet")
