"""Tests for deterministic worksheet problem generation."""

from collections.abc import Mapping

import pytest
from sympy import Symbol, simplify, sympify

from generator.problem_generator import (
    generate_factoring_techniques_worksheet,
    generate_functions_basics_worksheet,
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
    assert problem.metadata == {
        "equation": "2*x + 1 = 3",
        "variable": "x",
        "coefficient_a": "2",
        "constant_b": "1",
        "constant_c": "3",
    }
    assert solution.problem_id == problem.problem_id
    assert solution.final_answer == problem.answer
    assert solution.steps == (
        "Start with 2*x + 1 = 3.",
        "Subtract 1 from both sides.",
        "Divide both sides by 2.",
        "x = 1.",
    )


def test_generate_linear_equation_medium_worksheet_is_deterministic() -> None:
    first = generate_linear_equation_worksheet(
        "Linear equations",
        "medium",
        3,
        "medium-linear",
    )
    second = generate_linear_equation_worksheet(
        "Linear equations",
        "medium",
        3,
        "medium-linear",
    )

    assert first == second
    assert [problem.prompt for problem in first.problems] == [
        "Solve for x: 5*x - 3 = -8",
        "Solve for x: 6*x - 5 = -17",
        "Solve for x: 7*x - 7 = -28",
    ]
    assert [problem.answer for problem in first.problems] == ["-1", "-2", "-3"]


def test_generate_linear_equation_medium_uses_negative_readable_values() -> None:
    worksheet = generate_linear_equation_worksheet(
        "Linear equations",
        "medium",
        1,
        "medium-linear",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert problem.metadata["difficulty_pattern"] == "negative_constant_or_solution"
    assert int(problem.metadata["coefficient_a"]) >= 5
    assert int(problem.metadata["constant_b"]) < 0
    assert int(problem.answer) < 0
    assert problem.prompt == "Solve for x: 5*x - 3 = -8"
    assert solution.steps == (
        "Start with 5*x - 3 = -8.",
        "Add 3 to both sides.",
        "Divide both sides by 5.",
        "x = -1.",
    )


def test_generate_linear_equation_hard_worksheet_is_deterministic() -> None:
    first = generate_linear_equation_worksheet(
        "Linear equations",
        "hard",
        3,
        "hard-linear",
    )
    second = generate_linear_equation_worksheet(
        "Linear equations",
        "hard",
        3,
        "hard-linear",
    )

    assert first == second
    assert [problem.prompt for problem in first.problems] == [
        "Solve for x: 5*x + 3 = 2*x + 9",
        "Solve for x: 6*x + 5 = 3*x + 14",
        "Solve for x: 7*x + 7 = 4*x + 19",
    ]
    assert [problem.answer for problem in first.problems] == ["2", "3", "4"]


def test_generate_linear_equation_hard_uses_variables_on_both_sides() -> None:
    worksheet = generate_linear_equation_worksheet(
        "Linear equations",
        "hard",
        1,
        "hard-linear",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]
    left_side, right_side = problem.metadata["equation"].split("=")

    assert problem.metadata["difficulty_pattern"] == "variables_on_both_sides"
    assert "x" in left_side
    assert "x" in right_side
    assert problem.prompt == "Solve for x: 5*x + 3 = 2*x + 9"
    assert solution.steps == (
        "Start with 5*x + 3 = 2*x + 9.",
        "Subtract 2*x from both sides.",
        "Subtract 3 from both sides.",
        "Divide both sides by 3.",
        "x = 2.",
    )


def test_generate_linear_equation_unknown_difficulty_uses_legacy_fallback() -> None:
    worksheet = generate_linear_equation_worksheet(
        "Linear equations",
        "practice",
        1,
        "fallback-linear",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert problem.prompt == "Solve for x: 3*x + 2 = 8"
    assert problem.answer == "2"
    assert problem.metadata == {
        "equation": "3*x + 2 = 8",
        "variable": "x",
        "coefficient_a": "3",
        "constant_b": "2",
        "constant_c": "8",
    }
    assert solution.steps == (
        "Start with 3*x + 2 = 8.",
        "Subtract 2 from both sides.",
        "Divide both sides by 3.",
        "x = 2.",
    )


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
    assert solution.steps == (
        "Start with x**2 - 3*x + 2 = 0.",
        "Factor the quadratic as (x - 1)(x - 2) = 0.",
        "Set each factor equal to zero.",
        "x = 1 or x = 2.",
    )


def test_generate_quadratic_factoring_medium_worksheet_is_deterministic() -> None:
    first = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "medium",
        3,
        "medium-quadratic",
    )
    second = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "medium",
        3,
        "medium-quadratic",
    )

    assert first == second
    assert [problem.prompt for problem in first.problems] == [
        "Solve by factoring: x**2 - 2*x - 3 = 0",
        "Solve by factoring: x**2 - 2*x - 8 = 0",
        "Solve by factoring: x**2 - 2*x - 15 = 0",
    ]
    assert [problem.answer for problem in first.problems] == [
        "-1, 3",
        "-2, 4",
        "-3, 5",
    ]


def test_generate_quadratic_factoring_medium_uses_mixed_sign_monic_roots() -> None:
    worksheet = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "medium",
        1,
        "medium-quadratic",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert problem.metadata["difficulty_pattern"] == "mixed_sign_monic_roots"
    assert problem.metadata["leading_coefficient"] == "1"
    assert int(problem.metadata["root_1"]) < 0
    assert int(problem.metadata["root_2"]) > 0
    assert problem.metadata["factored_form"] == "(x + 1)(x - 3)"
    assert solution.steps == (
        "Start with x**2 - 2*x - 3 = 0.",
        "Factor the quadratic as (x + 1)(x - 3) = 0.",
        "Set each factor equal to zero.",
        "x = -1 or x = 3.",
    )


def test_generate_quadratic_factoring_hard_worksheet_is_deterministic() -> None:
    first = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "hard",
        3,
        "hard-quadratic",
    )
    second = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "hard",
        3,
        "hard-quadratic",
    )

    assert first == second
    assert [problem.prompt for problem in first.problems] == [
        "Solve by factoring: 2*x**2 - 8*x + 6 = 0",
        "Solve by factoring: 3*x**2 - 18*x + 24 = 0",
        "Solve by factoring: 4*x**2 - 32*x + 60 = 0",
    ]
    assert [problem.answer for problem in first.problems] == [
        "1, 3",
        "2, 4",
        "3, 5",
    ]


def test_generate_quadratic_factoring_hard_uses_non_monic_integer_roots() -> None:
    worksheet = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "hard",
        1,
        "hard-quadratic",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert problem.metadata["difficulty_pattern"] == "non_monic_integer_roots"
    assert int(problem.metadata["leading_coefficient"]) > 1
    assert problem.metadata["root_1"] == "1"
    assert problem.metadata["root_2"] == "3"
    assert problem.metadata["factored_form"] == "(2*x - 2)(x - 3)"
    assert _factored_form_matches_equation(
        problem.metadata["factored_form"],
        problem.metadata["equation"],
    )
    assert solution.steps == (
        "Start with 2*x**2 - 8*x + 6 = 0.",
        "Factor the quadratic as (2*x - 2)(x - 3) = 0.",
        "Set each factor equal to zero.",
        "x = 1 or x = 3.",
    )


def test_generate_quadratic_factoring_unknown_difficulty_uses_legacy_fallback() -> None:
    worksheet = generate_quadratic_factoring_worksheet(
        "Quadratic equations by factoring",
        "practice",
        1,
        "fallback-quadratic",
    )

    problem = worksheet.problems[0]

    assert problem.prompt == "Solve by factoring: x**2 - 6*x + 8 = 0"
    assert problem.answer == "2, 4"
    assert problem.metadata == {
        "equation": "x**2 - 6*x + 8 = 0",
        "variable": "x",
        "root_1": "2",
        "root_2": "4",
        "factored_form": "(x - 2)(x - 4)",
    }


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
    assert dict(problem.metadata) == {
        "equation_1": "x + y = 3",
        "equation_2": "x - y = -1",
        "variable_1": "x",
        "variable_2": "y",
        "x_value": "1",
        "y_value": "2",
    }
    assert solution.problem_id == problem.problem_id
    assert solution.final_answer == problem.answer
    assert solution.steps == (
        "Start with the system x + y = 3 and x - y = -1.",
        "Add the equations to eliminate y.",
        "Solve for x to get x = 1.",
        "Substitute x = 1 into one equation to get y = 2.",
        "The solution is (1, 2).",
    )


def test_generate_systems_of_equations_medium_worksheet_is_deterministic() -> None:
    first = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "medium",
        3,
        "medium-systems",
    )
    second = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "medium",
        3,
        "medium-systems",
    )

    assert first == second
    assert [problem.prompt for problem in first.problems] == [
        "Solve the system of equations:\n2*x + y = 7\nx - 2*y = -4",
        "Solve the system of equations:\n2*x + y = 10\nx - 2*y = -5",
        "Solve the system of equations:\n2*x + y = 13\nx - 2*y = -6",
    ]
    assert [problem.answer for problem in first.problems] == [
        "(2, 3)",
        "(3, 4)",
        "(4, 5)",
    ]


def test_generate_systems_of_equations_medium_requires_one_equation_scaling() -> None:
    worksheet = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "medium",
        1,
        "medium-systems",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert problem.metadata["difficulty_pattern"] == "one_equation_scaling"
    assert problem.metadata["recommended_method"] == "elimination"
    assert problem.metadata["scaling_equation"] == "equation_1"
    assert problem.metadata["scaling_factor"] == "2"
    assert problem.metadata["equation_1"] == "2*x + y = 7"
    assert problem.metadata["equation_2"] == "x - 2*y = -4"
    assert solution.steps == (
        "Start with the system 2*x + y = 7 and x - 2*y = -4.",
        "Multiply the first equation by 2 so the y-coefficients are opposites.",
        "Add the scaled first equation to the second equation to eliminate y.",
        "Solve for x to get x = 2.",
        "Substitute x = 2 into one equation to get y = 3.",
        "The solution is (2, 3).",
    )


def test_generate_systems_of_equations_hard_worksheet_is_deterministic() -> None:
    first = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "hard",
        3,
        "hard-systems",
    )
    second = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "hard",
        3,
        "hard-systems",
    )

    assert first == second
    assert [problem.prompt for problem in first.problems] == [
        "Solve the system of equations:\n-2*x + 3*y = -7\n4*x + y = 7",
        "Solve the system of equations:\n-2*x + 3*y = -12\n4*x + y = 10",
        "Solve the system of equations:\n-2*x + 3*y = -17\n4*x + y = 13",
    ]
    assert [problem.answer for problem in first.problems] == [
        "(2, -1)",
        "(3, -2)",
        "(4, -3)",
    ]


def test_generate_systems_of_equations_hard_uses_negative_coefficients_or_solution() -> None:
    worksheet = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "hard",
        1,
        "hard-systems",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert problem.metadata["difficulty_pattern"] == "negative_coefficients_or_solution"
    assert problem.metadata["recommended_method"] == "elimination"
    assert problem.metadata["scaling_equation"] == "equation_2"
    assert problem.metadata["scaling_factor"] == "-3"
    assert problem.metadata["equation_1"].startswith("-2*x")
    assert int(problem.metadata["y_value"]) < 0
    assert solution.steps == (
        "Start with the system -2*x + 3*y = -7 and 4*x + y = 7.",
        "Multiply the second equation by -3 so the y-coefficients are opposites.",
        "Add the equations to eliminate y.",
        "Solve for x to get x = 2.",
        "Substitute x = 2 into one equation to get y = -1.",
        "The solution is (2, -1).",
    )


def test_generate_systems_of_equations_unknown_difficulty_uses_legacy_fallback() -> None:
    worksheet = generate_systems_of_equations_worksheet(
        "Systems of linear equations",
        "practice",
        1,
        "fallback-systems",
    )

    problem = worksheet.problems[0]
    solution = worksheet.solutions[0]

    assert problem.prompt == (
        "Solve the system of equations:\n"
        "x + y = 5\n"
        "x - y = -1"
    )
    assert problem.answer == "(2, 3)"
    assert dict(problem.metadata) == {
        "equation_1": "x + y = 5",
        "equation_2": "x - y = -1",
        "variable_1": "x",
        "variable_2": "y",
        "x_value": "2",
        "y_value": "3",
    }
    assert solution.steps == (
        "Start with the system x + y = 5 and x - y = -1.",
        "Add the equations to eliminate y.",
        "Solve for x to get x = 2.",
        "Substitute x = 2 into one equation to get y = 3.",
        "The solution is (2, 3).",
    )


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
    assert [problem.prompt for problem in worksheet.problems] == [
        "Factor completely: 6*x + 8",
        "Factor completely: x**2 - 4",
        "Factor completely: x**2 + 5*x + 6",
    ]
    assert [dict(problem.metadata) for problem in worksheet.problems] == [
        {
            "expression": "6*x + 8",
            "factored_form": "2*(3*x + 4)",
            "strategy": "greatest common factor",
            "variable": "x",
        },
        {
            "expression": "x**2 - 4",
            "factored_form": "(x - 2)*(x + 2)",
            "strategy": "difference of squares",
            "variable": "x",
        },
        {
            "expression": "x**2 + 5*x + 6",
            "factored_form": "(x + 2)*(x + 3)",
            "strategy": "simple trinomial",
            "variable": "x",
        },
    ]


def test_generate_factoring_techniques_medium_worksheet_is_deterministic() -> None:
    first = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "medium",
        3,
        "medium-factoring",
    )
    second = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "medium",
        3,
        "medium-factoring",
    )

    assert first == second
    assert [problem.prompt for problem in first.problems] == [
        "Factor completely: 6*x**2 + 8*x",
        "Factor completely: 4*x**2 - 9",
        "Factor completely: x**2 + x - 6",
    ]
    assert [problem.answer for problem in first.problems] == [
        "2*x*(3*x + 4)",
        "(2*x - 3)*(2*x + 3)",
        "(x - 2)*(x + 3)",
    ]


def test_generate_factoring_techniques_medium_uses_extended_patterns() -> None:
    worksheet = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "medium",
        3,
        "medium-factoring",
    )

    assert [problem.metadata["difficulty_pattern"] for problem in worksheet.problems] == [
        "variable_gcf",
        "coefficient_difference_of_squares",
        "mixed_sign_trinomial",
    ]
    assert worksheet.problems[0].metadata["strategy"] == (
        "greatest common factor with variable"
    )
    assert worksheet.problems[1].metadata["strategy"] == (
        "coefficient difference of squares"
    )
    assert worksheet.problems[2].metadata["strategy"] == "mixed-sign simple trinomial"


def test_generate_factoring_techniques_hard_worksheet_is_deterministic() -> None:
    first = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "hard",
        4,
        "hard-factoring",
    )
    second = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "hard",
        4,
        "hard-factoring",
    )

    assert first == second
    assert [problem.prompt for problem in first.problems] == [
        "Factor completely: x**3 + 3*x**2 + 2*x + 6",
        "Factor completely: 2*x**2 + 7*x + 3",
        "Factor completely: x**3 + 4*x**2 + 3*x + 12",
        "Factor completely: 3*x**2 + 13*x + 4",
    ]
    assert [problem.answer for problem in first.problems] == [
        "(x + 3)*(x**2 + 2)",
        "(2*x + 1)*(x + 3)",
        "(x + 4)*(x**2 + 3)",
        "(3*x + 1)*(x + 4)",
    ]


def test_generate_factoring_techniques_hard_uses_grouping_or_non_monic_patterns() -> None:
    worksheet = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "hard",
        2,
        "hard-factoring",
    )

    assert [problem.metadata["difficulty_pattern"] for problem in worksheet.problems] == [
        "grouping",
        "non_monic_trinomial",
    ]
    assert worksheet.problems[0].metadata["strategy"] == "factor by grouping"
    assert worksheet.problems[1].metadata["strategy"] == "non-monic trinomial"


def test_generate_factoring_techniques_unknown_difficulty_uses_legacy_fallback() -> None:
    worksheet = generate_factoring_techniques_worksheet(
        "Factoring techniques",
        "practice",
        3,
        "fallback-factoring",
    )

    assert [problem.prompt for problem in worksheet.problems] == [
        "Factor completely: 6*x + 8",
        "Factor completely: x**2 - 4",
        "Factor completely: x**2 + 5*x + 6",
    ]
    assert [problem.answer for problem in worksheet.problems] == [
        "2*(3*x + 4)",
        "(x - 2)*(x + 2)",
        "(x + 2)*(x + 3)",
    ]
    assert [dict(problem.metadata) for problem in worksheet.problems] == [
        {
            "expression": "6*x + 8",
            "factored_form": "2*(3*x + 4)",
            "strategy": "greatest common factor",
            "variable": "x",
        },
        {
            "expression": "x**2 - 4",
            "factored_form": "(x - 2)*(x + 2)",
            "strategy": "difference of squares",
            "variable": "x",
        },
        {
            "expression": "x**2 + 5*x + 6",
            "factored_form": "(x + 2)*(x + 3)",
            "strategy": "simple trinomial",
            "variable": "x",
        },
    ]


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


def test_generate_functions_basics_worksheet_returns_worksheet() -> None:
    worksheet = generate_functions_basics_worksheet(
        topic="Functions basics",
        difficulty="easy",
        count=3,
        start_id="functions",
    )

    assert isinstance(worksheet, Worksheet)
    assert worksheet.title == "Functions basics Worksheet"
    assert worksheet.worksheet_id == "functions-worksheet"
    assert len(worksheet.problems) == 3
    assert len(worksheet.solutions) == 3
    assert worksheet.metadata["generator"] == "functions_basics"


def test_generate_functions_basics_worksheet_is_deterministic() -> None:
    first = generate_functions_basics_worksheet(
        "Functions basics",
        "easy",
        4,
        "functions",
    )
    second = generate_functions_basics_worksheet(
        "Functions basics",
        "easy",
        4,
        "functions",
    )

    assert first == second
    assert [problem.problem_id for problem in first.problems] == [
        "functions-001",
        "functions-002",
        "functions-003",
        "functions-004",
    ]


def test_generate_functions_basics_worksheet_creates_expected_problem_types() -> None:
    worksheet = generate_functions_basics_worksheet(
        "Functions basics",
        "easy",
        3,
        "func",
    )

    problem_types = [problem.metadata["problem_type"] for problem in worksheet.problems]

    assert problem_types == ["evaluate", "notation", "domain"]
    assert worksheet.problems[0].prompt == (
        "Given f(x) = 2*x + 1, evaluate f(3)."
    )
    assert worksheet.problems[0].answer == "7"
    assert worksheet.problems[1].answer == "The input value"
    assert worksheet.problems[2].answer == "All real numbers except x = 2"


def test_generated_function_evaluations_are_correct() -> None:
    worksheet = generate_functions_basics_worksheet(
        topic="Functions basics",
        difficulty="easy",
        count=6,
        start_id="functions",
    )

    for problem in worksheet.problems:
        if problem.metadata["problem_type"] == "evaluate":
            assert _function_evaluation_is_valid(problem.metadata)


def test_generate_functions_basics_worksheet_rejects_invalid_count() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        generate_functions_basics_worksheet(
            "Functions basics",
            "easy",
            0,
            "functions",
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


def _factored_form_matches_equation(factored_form: str, equation: str) -> bool:
    """Return whether a displayed factored form expands to equation left side."""
    left_side, right_side = equation.split("=")
    parseable_factored_form = factored_form.replace(")(", ")*(")
    return (
        simplify(
            sympify(parseable_factored_form).expand()
            - (sympify(left_side) - sympify(right_side))
        )
        == 0
    )


def _function_evaluation_is_valid(metadata: Mapping[str, str]) -> bool:
    """Return whether a generated function evaluation is correct."""
    x_symbol = Symbol("x")
    expression = sympify(metadata["function_expression"])
    input_value = sympify(metadata["input_value"])
    expected_value = sympify(metadata["expected_value"])
    return simplify(expression.subs(x_symbol, input_value) - expected_value) == 0
