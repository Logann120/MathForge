"""Tests for deterministic worksheet problem generation."""

from collections.abc import Mapping

import pytest
from sympy import Symbol, simplify, sympify

from generator.problem_generator import (
    generate_factoring_techniques_worksheet,
    generate_linear_equation_worksheet,
    generate_quadratic_factoring_worksheet,
    generate_systems_of_equations_worksheet,
)
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


def test_generate_quadratic_factoring_worksheet_returns_worksheet() -> None:
    worksheet = generate_quadratic_factoring_worksheet(
        topic="Quadratic equations by factoring",
        difficulty="easy",
        count=2,
        start_id="quadratic",
    )

    assert isinstance(worksheet, Worksheet)
    assert worksheet.title == "Quadratic equations by factoring Worksheet"
    assert worksheet.worksheet_id == "quadratic-worksheet"
    assert len(worksheet.problems) == 2
    assert len(worksheet.solutions) == 2
    assert worksheet.metadata["generator"] == "quadratic_factoring"


def test_generate_quadratic_factoring_worksheet_is_deterministic() -> None:
    first = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "easy",
        3,
        "quadratic",
    )
    second = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "easy",
        3,
        "quadratic",
    )

    assert first == second
    assert [problem.problem_id for problem in first.problems] == [
        "quadratic-001",
        "quadratic-002",
        "quadratic-003",
    ]


def test_generate_quadratic_factoring_worksheet_creates_expected_easy_problem() -> None:
    worksheet = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "easy",
        1,
        "quad",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert isinstance(problem, MathProblem)
    assert isinstance(solution, Solution)
    assert problem.prompt == "Solve by factoring: x**2 - 3*x + 2 = 0"
    assert problem.answer == "1, 2"
    assert problem.metadata["equation"] == "x**2 - 3*x + 2 = 0"
    assert problem.metadata["factored_form"] == "(x - 1)(x - 2)"
    assert solution.problem_id == problem.problem_id
    assert solution.final_answer == problem.answer


def test_generated_quadratic_roots_satisfy_generated_equations() -> None:
    worksheet = generate_quadratic_factoring_worksheet(
        topic="Quadratic equations by factoring",
        difficulty="advanced",
        count=4,
        start_id="advanced-quadratic",
    )

    for problem in worksheet.problems:
        for root_key in ("root_1", "root_2"):
            result = validate_equation_solution(
                problem.metadata["equation"],
                problem.metadata["variable"],
                problem.metadata[root_key],
            )
            assert result.is_valid is True


def test_generate_quadratic_factoring_worksheet_rejects_invalid_count() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        generate_quadratic_factoring_worksheet(
            "Quadratic equations by factoring",
            "easy",
            0,
            "quadratic",
        )


def test_generate_systems_of_equations_worksheet_returns_worksheet() -> None:
    worksheet = generate_systems_of_equations_worksheet(
        topic="Systems of linear equations",
        difficulty="easy",
        count=2,
        start_id="systems",
    )

    assert isinstance(worksheet, Worksheet)
    assert worksheet.title == "Systems of linear equations Worksheet"
    assert worksheet.worksheet_id == "systems-worksheet"
    assert len(worksheet.problems) == 2
    assert len(worksheet.solutions) == 2
    assert worksheet.metadata["generator"] == "systems_of_equations"


def test_generate_systems_of_equations_worksheet_is_deterministic() -> None:
    first = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "easy",
        3,
        "systems",
    )
    second = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "easy",
        3,
        "systems",
    )

    assert first == second
    assert [problem.problem_id for problem in first.problems] == [
        "systems-001",
        "systems-002",
        "systems-003",
    ]


def test_generate_systems_of_equations_worksheet_creates_expected_easy_problem() -> None:
    worksheet = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "easy",
        1,
        "sys",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert isinstance(problem, MathProblem)
    assert isinstance(solution, Solution)
    assert problem.prompt == (
        "Solve the system of equations:\n"
        "x + y = 3\n"
        "x - y = -1"
    )
    assert problem.answer == "(1, 2)"
    assert problem.metadata["equation_1"] == "x + y = 3"
    assert problem.metadata["equation_2"] == "x - y = -1"
    assert solution.problem_id == problem.problem_id
    assert solution.final_answer == problem.answer


def test_generated_system_solutions_satisfy_generated_equations() -> None:
    worksheet = generate_systems_of_equations_worksheet(
        topic="Systems of linear equations",
        difficulty="advanced",
        count=4,
        start_id="advanced-systems",
    )

    for problem in worksheet.problems:
        assert _system_solution_is_valid(problem.metadata)


def test_generate_systems_of_equations_worksheet_rejects_invalid_count() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        generate_systems_of_equations_worksheet(
            "Systems of linear equations",
            "easy",
            0,
            "systems",
        )


def test_generate_factoring_techniques_worksheet_returns_worksheet() -> None:
    worksheet = generate_factoring_techniques_worksheet(
        topic="Factoring techniques",
        difficulty="easy",
        count=3,
        start_id="factoring",
    )

    assert isinstance(worksheet, Worksheet)
    assert worksheet.title == "Factoring techniques Worksheet"
    assert worksheet.worksheet_id == "factoring-worksheet"
    assert len(worksheet.problems) == 3
    assert len(worksheet.solutions) == 3
    assert worksheet.metadata["generator"] == "factoring_techniques"


def test_generate_factoring_techniques_worksheet_is_deterministic() -> None:
    first = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "easy",
        4,
        "factoring",
    )
    second = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "easy",
        4,
        "factoring",
    )

    assert first == second
    assert [problem.problem_id for problem in first.problems] == [
        "factoring-001",
        "factoring-002",
        "factoring-003",
        "factoring-004",
    ]


def test_generate_factoring_techniques_worksheet_creates_expected_strategies() -> None:
    worksheet = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "easy",
        3,
        "factor",
    )

    strategies = [problem.metadata["strategy"] for problem in worksheet.problems]

    assert strategies == [
        "greatest common factor",
        "difference of squares",
        "simple trinomial",
    ]
    assert worksheet.problems[0].prompt == "Factor completely: 6*x + 8"
    assert worksheet.problems[0].answer == "2*(3*x + 4)"
    assert worksheet.problems[1].answer == "(x - 2)*(x + 2)"
    assert worksheet.problems[2].answer == "(x + 2)*(x + 3)"


def test_generated_factoring_answers_expand_to_original_expressions() -> None:
    worksheet = generate_factoring_techniques_worksheet(
        topic="Factoring techniques",
        difficulty="easy",
        count=6,
        start_id="factoring",
    )

    for problem in worksheet.problems:
        assert _factoring_answer_is_valid(
            problem.metadata["expression"],
            problem.metadata["factored_form"],
        )


def test_generate_factoring_techniques_worksheet_rejects_invalid_count() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        generate_factoring_techniques_worksheet(
            "Factoring techniques",
            "easy",
            0,
            "factoring",
        )


def _system_solution_is_valid(metadata: Mapping[str, str]) -> bool:
    """Return whether generated system metadata describes a valid solution."""
    x_symbol = Symbol("x")
    y_symbol = Symbol("y")
    x_value = int(metadata["x_value"])
    y_value = int(metadata["y_value"])

    for equation_key in ("equation_1", "equation_2"):
        left_text, right_text = metadata[equation_key].split("=")
        left_expr = sympify(left_text).subs({x_symbol: x_value, y_symbol: y_value})
        right_expr = sympify(right_text).subs({x_symbol: x_value, y_symbol: y_value})
        if simplify(left_expr - right_expr) != 0:
            return False

    return True


def _factoring_answer_is_valid(expression: str, factored_form: str) -> bool:
    """Return whether a generated factorization expands correctly."""
    return simplify(sympify(expression) - sympify(factored_form).expand()) == 0
