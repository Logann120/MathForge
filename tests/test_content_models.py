"""Tests for MathForge core content models."""

import pytest

from models.content_models import (
    ExportResult,
    HintSet,
    MathProblem,
    Solution,
    Worksheet,
)


def test_math_problem_creation_with_hints_and_metadata() -> None:
    hint_set = HintSet(hints=("Isolate the variable.",), metadata={"level": "1"})

    problem = MathProblem(
        problem_id="linear-001",
        prompt="Solve x + 2 = 5.",
        answer="3",
        topic="Linear equations",
        difficulty="introductory",
        hints=hint_set,
        metadata={"course": "algebra"},
    )

    assert problem.problem_id == "linear-001"
    assert problem.hints == hint_set
    assert problem.metadata["course"] == "algebra"


def test_math_problem_requires_non_empty_prompt() -> None:
    with pytest.raises(ValueError, match="prompt"):
        MathProblem(problem_id="p1", prompt=" ", answer="3")


def test_solution_creation_with_steps() -> None:
    solution = Solution(
        problem_id="linear-001",
        final_answer="3",
        steps=("Subtract 2 from both sides.", "x = 3."),
    )

    assert solution.steps == ("Subtract 2 from both sides.", "x = 3.")


def test_worksheet_creation_with_matching_solution() -> None:
    problem = MathProblem(
        problem_id="linear-001",
        prompt="Solve x + 2 = 5.",
        answer="3",
    )
    solution = Solution(problem_id="linear-001", final_answer="3")

    worksheet = Worksheet(
        title="Linear Equations Practice",
        worksheet_id="worksheet-001",
        instructions="Show your work.",
        problems=(problem,),
        solutions=(solution,),
    )

    assert worksheet.title == "Linear Equations Practice"
    assert worksheet.problems == (problem,)
    assert worksheet.solutions == (solution,)


def test_worksheet_requires_at_least_one_problem() -> None:
    with pytest.raises(ValueError, match="at least one"):
        Worksheet(title="Empty Worksheet", problems=())


def test_worksheet_rejects_duplicate_problem_ids() -> None:
    first = MathProblem(problem_id="p1", prompt="Solve x = 1.", answer="1")
    second = MathProblem(problem_id="p1", prompt="Solve x = 2.", answer="2")

    with pytest.raises(ValueError, match="duplicate problem_id"):
        Worksheet(title="Duplicate Problems", problems=(first, second))


def test_worksheet_rejects_solution_for_unknown_problem() -> None:
    problem = MathProblem(problem_id="p1", prompt="Solve x = 1.", answer="1")
    solution = Solution(problem_id="p2", final_answer="2")

    with pytest.raises(ValueError, match="unknown problem_id"):
        Worksheet(title="Mismatched Solution", problems=(problem,), solutions=(solution,))


def test_export_result_creation() -> None:
    result = ExportResult(
        content="# Worksheet",
        format_name="markdown",
        filename="worksheet.md",
        metadata={"kind": "worksheet"},
    )

    assert result.format_name == "markdown"
    assert result.filename == "worksheet.md"


def test_metadata_requires_string_values() -> None:
    with pytest.raises(TypeError, match="metadata values"):
        MathProblem(
            problem_id="p1",
            prompt="Solve x = 1.",
            answer="1",
            metadata={"points": 1},
        )
