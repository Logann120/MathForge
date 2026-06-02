"""Tests for Canvas-friendly manual-entry CSV exports."""

from __future__ import annotations

import csv
from io import StringIO

import pytest

from exporters.canvas_exporter import (
    CANVAS_MANUAL_ENTRY_COLUMNS,
    export_resource_pack_quiz_to_canvas_csv,
    export_worksheet_to_canvas_csv,
)
from generator.problem_generator import generate_linear_equation_worksheet
from generator.resource_pack_generator import generate_linear_equation_resource_pack
from models.content_models import ExportResult, MathProblem, Solution, Worksheet
from models.resource_pack import ResourcePack


def test_export_worksheet_to_canvas_csv_returns_manual_entry_rows() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_worksheet_to_canvas_csv(worksheet)
    rows = _read_csv(result.content)

    assert isinstance(result, ExportResult)
    assert result.format_name == "canvas_csv"
    assert result.filename == "linear-worksheet-worksheet-canvas.csv"
    assert result.metadata["canvas_export_type"] == "manual_entry_csv"
    assert result.metadata["resource_type"] == "worksheet"
    assert result.metadata["problem_id_prefix"] == "linear"
    assert tuple(rows[0]) == CANVAS_MANUAL_ENTRY_COLUMNS
    assert rows[0]["question_title"] == "linear-001"
    assert rows[0]["question_prompt"] == "Solve for x: 2*x + 1 = 3"
    assert rows[0]["correct_answer"] == "1"
    assert "Subtract 1 from both sides." in rows[0]["solution_explanation"]
    assert rows[0]["topic"] == "Linear equations"
    assert rows[0]["difficulty"] == "easy"
    assert rows[0]["problem_id"] == "linear-001"
    assert rows[0]["source_type"] == "worksheet"
    assert rows[0]["source_id"] == "linear-worksheet"


def test_export_worksheet_to_canvas_csv_handles_commas_quotes_and_line_breaks() -> None:
    problem = MathProblem(
        problem_id="comma-001",
        prompt='Solve x = 1, then write "done".\nShow work.',
        answer='1, "done"',
        topic="CSV Topic",
        difficulty="easy",
    )
    solution = Solution(
        problem_id="comma-001",
        final_answer='1, "done"',
        steps=('Use the equation, then write "done".', "Check the result."),
    )
    worksheet = Worksheet(
        title="CSV Safety",
        worksheet_id="csv-safe-worksheet",
        problems=(problem,),
        solutions=(solution,),
        metadata={"topic": "CSV Topic", "difficulty": "easy"},
    )

    result = export_worksheet_to_canvas_csv(worksheet)
    rows = _read_csv(result.content)

    assert rows[0]["question_prompt"] == 'Solve x = 1, then write "done".\nShow work.'
    assert rows[0]["correct_answer"] == '1, "done"'
    assert rows[0]["solution_explanation"] == (
        'Use the equation, then write "done".\nCheck the result.'
    )


def test_export_resource_pack_quiz_to_canvas_csv_uses_practice_quiz() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=2,
        start_id="linear",
    )

    result = export_resource_pack_quiz_to_canvas_csv(resource_pack)
    rows = _read_csv(result.content)

    assert result.format_name == "canvas_csv"
    assert result.filename == "linear-worksheet-resource-pack-quiz-canvas.csv"
    assert result.metadata["resource_type"] == "resource_pack"
    assert result.metadata["canvas_export_type"] == "manual_entry_csv"
    assert result.metadata["problem_count"] == "3"
    assert len(rows) == 3
    assert rows[0]["question_title"] == "Linear equations Practice Quiz - Question 1"
    assert rows[0]["question_prompt"].startswith("Quiz question 1:")
    assert rows[0]["correct_answer"].startswith("1.")
    assert rows[0]["source_type"] == "practice_quiz"
    assert rows[0]["source_id"] == "linear-worksheet"


def test_export_resource_pack_quiz_to_canvas_csv_rejects_missing_quiz() -> None:
    generated_resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )
    resource_pack = ResourcePack(
        worksheet=generated_resource_pack.worksheet,
        study_guide=generated_resource_pack.study_guide,
        common_mistakes=generated_resource_pack.common_mistakes,
        tutor_notes=generated_resource_pack.tutor_notes,
    )

    with pytest.raises(ValueError, match="PracticeQuiz"):
        export_resource_pack_quiz_to_canvas_csv(resource_pack)


def test_canvas_exporters_reject_wrong_types() -> None:
    with pytest.raises(TypeError, match="Worksheet"):
        export_worksheet_to_canvas_csv("not a worksheet")

    with pytest.raises(TypeError, match="ResourcePack"):
        export_resource_pack_quiz_to_canvas_csv("not a resource pack")


def _read_csv(content: str) -> list[dict[str, str]]:
    """Read Canvas CSV content as dictionaries."""
    return list(csv.DictReader(StringIO(content)))
