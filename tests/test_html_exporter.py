"""Tests for accessible HTML worksheet exports."""

import pytest

from exporters.html_exporter import export_worksheet_to_html
from generator.problem_generator import generate_linear_equation_worksheet
from models.content_models import ExportResult, MathProblem, Worksheet


def test_export_worksheet_to_html_returns_export_result() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_worksheet_to_html(worksheet)

    assert isinstance(result, ExportResult)
    assert result.format_name == "html"
    assert result.filename == "linear-worksheet.html"
    assert result.metadata["worksheet_id"] == "linear-worksheet"
    assert result.metadata["include_solutions"] == "False"


def test_export_worksheet_to_html_uses_semantic_structure_without_h1() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=2,
        start_id="linear",
    )

    result = export_worksheet_to_html(worksheet)

    assert '<section class="mathforge-worksheet">' in result.content
    assert "<h1" not in result.content
    assert "<h2>Linear equations Worksheet</h2>" in result.content
    assert "<h3>Instructions</h3>" in result.content
    assert "<h3>Problems</h3>" in result.content
    assert "<ol>" in result.content
    assert "<li>Solve for x: 2*x + 1 = 3</li>" in result.content
    assert "<li>Solve for x: 3*x + 3 = 9</li>" in result.content
    assert "<h3>Solution Key</h3>" not in result.content


def test_export_worksheet_to_html_can_include_solution_key() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_worksheet_to_html(worksheet, include_solutions=True)

    assert '<section class="mathforge-solution-key">' in result.content
    assert "<h3>Solution Key</h3>" in result.content
    assert "<strong>Answer:</strong> 1" in result.content
    assert "<li>Start with 2*x + 1 = 3.</li>" in result.content
    assert "<li>x = 1.</li>" in result.content
    assert result.metadata["include_solutions"] == "True"


def test_export_worksheet_to_html_omits_empty_instructions_section() -> None:
    problem = MathProblem(
        problem_id="p1",
        prompt="Solve x = 1.",
        answer="1",
    )
    worksheet = Worksheet(title="Practice", instructions="", problems=(problem,))

    result = export_worksheet_to_html(worksheet)

    assert "<h2>Practice</h2>" in result.content
    assert "<h3>Instructions</h3>" not in result.content
    assert "<li>Solve x = 1.</li>" in result.content


def test_export_worksheet_to_html_escapes_html_sensitive_text() -> None:
    problem = MathProblem(
        problem_id="p1",
        prompt='Solve <x> & "show work".',
        answer="1",
    )
    worksheet = Worksheet(title="Practice <One>", problems=(problem,))

    result = export_worksheet_to_html(worksheet)

    assert "<h2>Practice &lt;One&gt;</h2>" in result.content
    assert "<li>Solve &lt;x&gt; &amp; &quot;show work&quot;.</li>" in result.content


def test_export_worksheet_to_html_rejects_non_worksheet() -> None:
    with pytest.raises(TypeError, match="worksheet must be a Worksheet"):
        export_worksheet_to_html("not a worksheet")
