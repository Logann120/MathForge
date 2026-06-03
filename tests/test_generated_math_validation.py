"""Validation-oriented regression tests for generated math content."""

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
from validators.sympy_validator import (
    validate_equation_solution,
    validate_expression_equivalence,
    validate_numeric_answer,
)


@pytest.mark.parametrize("difficulty", ("easy", "medium", "hard"))
def test_generated_linear_equation_answers_satisfy_equations(
    difficulty: str,
) -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty=difficulty,
        count=5,
        start_id=f"validation-linear-{difficulty}",
    )

    for problem in worksheet.problems:
        result = validate_equation_solution(
            problem.metadata["equation"],
            problem.metadata["variable"],
            problem.answer,
        )

        assert result.is_valid is True


@pytest.mark.parametrize("difficulty", ("easy", "medium", "hard"))
def test_generated_quadratic_factoring_roots_satisfy_equations(
    difficulty: str,
) -> None:
    worksheet = generate_quadratic_factoring_worksheet(
        topic="Quadratic equations by factoring",
        difficulty=difficulty,
        count=5,
        start_id=f"validation-quadratic-{difficulty}",
    )

    for problem in worksheet.problems:
        for root_key in ("root_1", "root_2"):
            result = validate_equation_solution(
                problem.metadata["equation"],
                problem.metadata["variable"],
                problem.metadata[root_key],
            )

            assert result.is_valid is True


@pytest.mark.parametrize("difficulty", ("easy", "medium", "hard"))
def test_generated_factoring_answers_are_expression_equivalent(
    difficulty: str,
) -> None:
    worksheet = generate_factoring_techniques_worksheet(
        topic="Factoring techniques",
        difficulty=difficulty,
        count=6,
        start_id=f"validation-factoring-{difficulty}",
    )

    for problem in worksheet.problems:
        result = validate_expression_equivalence(
            problem.metadata["expression"],
            problem.answer,
        )

        assert result.is_valid is True


@pytest.mark.parametrize("difficulty", ("easy", "medium", "hard"))
def test_generated_system_solutions_satisfy_both_equations(
    difficulty: str,
) -> None:
    worksheet = generate_systems_of_equations_worksheet(
        topic="Systems of linear equations",
        difficulty=difficulty,
        count=5,
        start_id=f"validation-systems-{difficulty}",
    )

    for problem in worksheet.problems:
        # The public equation validator currently accepts one variable at a time.
        # Systems are validated here by substituting the generated ordered pair.
        assert _system_solution_satisfies_equations(problem.metadata)


@pytest.mark.parametrize("difficulty", ("easy", "medium", "hard"))
def test_generated_function_evaluation_answers_are_numeric_matches(
    difficulty: str,
) -> None:
    worksheet = generate_functions_basics_worksheet(
        topic="Functions basics",
        difficulty=difficulty,
        count=6,
        start_id=f"validation-functions-{difficulty}",
    )

    evaluation_problems = [
        problem
        for problem in worksheet.problems
        if problem.metadata["problem_type"] == "evaluate"
    ]

    assert evaluation_problems
    for problem in evaluation_problems:
        result = validate_numeric_answer(
            _evaluate_function_metadata(problem.metadata),
            problem.answer,
        )

        assert result.is_valid is True


@pytest.mark.parametrize("difficulty", ("easy", "medium", "hard"))
def test_generated_function_domain_answers_match_metadata(
    difficulty: str,
) -> None:
    worksheet = generate_functions_basics_worksheet(
        topic="Functions basics",
        difficulty=difficulty,
        count=6,
        start_id=f"validation-functions-{difficulty}",
    )

    domain_problems = [
        problem
        for problem in worksheet.problems
        if problem.metadata["problem_type"] == "domain"
    ]

    assert domain_problems
    for problem in domain_problems:
        # Domain answers are prose, so validate machine-readable metadata
        # rather than forcing a symbolic interval format.
        if problem.metadata.get("difficulty_pattern") == "square_root_domain":
            expected_answer = (
                f"All real numbers x >= {problem.metadata['domain_minimum']}"
            )
        elif (
            problem.metadata.get("difficulty_pattern")
            == "two_factor_denominator_domain"
        ):
            exclusions = problem.metadata["domain_exclusions"].split(",")
            expected_answer = (
                f"All real numbers except x = {exclusions[0]} and x = {exclusions[1]}"
            )
        else:
            expected_answer = (
                f"All real numbers except x = {problem.metadata['excluded_value']}"
            )
        assert problem.answer == expected_answer


@pytest.mark.parametrize("difficulty", ("easy", "medium", "hard"))
def test_function_notation_answers_match_metadata(difficulty: str) -> None:
    worksheet = generate_functions_basics_worksheet(
        topic="Functions basics",
        difficulty=difficulty,
        count=6,
        start_id=f"validation-functions-{difficulty}",
    )

    notation_problems = [
        problem
        for problem in worksheet.problems
        if problem.metadata["problem_type"] == "notation"
    ]

    if difficulty == "hard":
        assert not notation_problems
        return

    assert notation_problems
    for problem in notation_problems:
        # These answers intentionally remain prose until MathForge has a
        # structured representation for conceptual function-notation responses.
        if problem.metadata.get("difficulty_pattern") == "ordered_pair_interpretation":
            assert problem.answer == problem.metadata["ordered_pair"]
        else:
            assert problem.answer == "The input value"
        assert problem.metadata["input_value"].strip()
        assert problem.metadata["output_value"].strip()


def _system_solution_satisfies_equations(metadata: Mapping[str, str]) -> bool:
    """Return whether generated system metadata describes a valid solution."""
    x_symbol = Symbol("x")
    y_symbol = Symbol("y")
    x_value = sympify(metadata["x_value"])
    y_value = sympify(metadata["y_value"])

    for equation_key in ("equation_1", "equation_2"):
        left_text, right_text = metadata[equation_key].split("=")
        left_expr = sympify(left_text).subs({x_symbol: x_value, y_symbol: y_value})
        right_expr = sympify(right_text).subs({x_symbol: x_value, y_symbol: y_value})
        if simplify(left_expr - right_expr) != 0:
            return False

    return True


def _evaluate_function_metadata(metadata: Mapping[str, str]) -> str:
    """Evaluate generated function metadata and return a numeric string."""
    x_symbol = Symbol("x")

    if metadata.get("difficulty_pattern") == "composition_evaluation":
        inner_expression = sympify(metadata["inner_function_rule"])
        outer_expression = sympify(metadata["function_expression"])
        input_value = sympify(metadata["input_value"])
        inner_value = inner_expression.subs(x_symbol, input_value)
        return str(outer_expression.subs(x_symbol, inner_value))

    expression = sympify(metadata["function_expression"])
    input_value = sympify(metadata["input_value"])
    return str(expression.subs(x_symbol, input_value))
