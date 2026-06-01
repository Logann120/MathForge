"""Tests for deterministic worksheet problem generation."""

import pytest

from generator.problem_generator import generate_linear_equation_worksheet
from models.content_models import MathProblem, Solution, Worksheet
from validators.sympy_validator import validate_equation_solution


def test_generate_linear_equation_worksheet_returns_worksheet() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=2,
        start_id="linear",
    )

    assert isinstance(worksheet, Worksheet)
    assert worksheet.title == "Linear equations Worksheet"
    assert worksheet.worksheet_id == "linear-worksheet"
    assert len(worksheet.problems) == 2
    assert len(worksheet.solutions) == 2


def test_generate_linear_equation_worksheet_is_deterministic() -> None:
    first = generate_linear_equation_worksheet("Linear equations", "easy", 3, "linear")
    second = generate_linear_equation_worksheet("Linear equations", "easy", 3, "linear")

    assert first == second
    assert [problem.problem_id for problem in first.problems] == [
        "linear-001",
        "linear-002",
        "linear-003",
    ]


def test_generate_linear_equation_worksheet_creates_expected_easy_problem() -> None:
    worksheet = generate_linear_equation_worksheet("Linear equations", "easy", 1, "lin")

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert isinstance(problem, MathProblem)
    assert isinstance(solution, Solution)
    assert problem.prompt == "Solve for x: 2*x + 1 = 3"
    assert problem.answer == "1"
    assert problem.metadata["equation"] == "2*x + 1 = 3"
    assert solution.problem_id == problem.problem_id
    assert solution.final_answer == problem.answer


def test_generated_answers_satisfy_generated_equations() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="advanced",
        count=4,
        start_id="advanced-linear",
    )

    for problem in worksheet.problems:
        result = validate_equation_solution(
            problem.metadata["equation"],
            problem.metadata["variable"],
            problem.answer,
        )
        assert result.is_valid is True


def test_generate_linear_equation_worksheet_rejects_zero_count() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        generate_linear_equation_worksheet("Linear equations", "easy", 0, "linear")


def test_generate_linear_equation_worksheet_rejects_negative_count() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        generate_linear_equation_worksheet("Linear equations", "easy", -1, "linear")


def test_generate_linear_equation_worksheet_rejects_non_integer_count() -> None:
    with pytest.raises(TypeError, match="count must be an integer"):
        generate_linear_equation_worksheet("Linear equations", "easy", 1.5, "linear")


def test_generate_linear_equation_worksheet_rejects_empty_start_id() -> None:
    with pytest.raises(ValueError, match="start_id"):
        generate_linear_equation_worksheet("Linear equations", "easy", 1, " ")
