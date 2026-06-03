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


def test_generated_function_evaluation_answers_are_numeric_matches() -> None:
    worksheet = generate_functions_basics_worksheet(
        topic="Functions basics",
        difficulty="easy",
        count=6,
        start_id="validation-functions",
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


def test_generated_function_domain_answers_match_excluded_value_metadata() -> None:
    worksheet = generate_functions_basics_worksheet(
        topic="Functions basics",
        difficulty="easy",
        count=6,
        start_id="validation-functions",
    )

    domain_problems = [
        problem
        for problem in worksheet.problems
        if problem.metadata["problem_type"] == "domain"
    ]

    assert domain_problems
    for problem in domain_problems:
        # Domain answers are prose, so validate the machine-readable excluded
        # value metadata rather than forcing a symbolic interval format.
        expected_answer = (
            f"All real numbers except x = {problem.metadata['excluded_value']}"
        )
        assert problem.answer == expected_answer


def test_function_notation_answers_are_not_machine_validated_yet() -> None:
    worksheet = generate_functions_basics_worksheet(
        topic="Functions basics",
        difficulty="easy",
        count=6,
        start_id="validation-functions",
    )

    notation_problems = [
        problem
        for problem in worksheet.problems
        if problem.metadata["problem_type"] == "notation"
    ]

    assert notation_problems
    for problem in notation_problems:
        # These answers intentionally remain prose until MathForge has a
        # structured representation for conceptual function-notation responses.
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
    expression = sympify(metadata["function_expression"])
    input_value = sympify(metadata["input_value"])
    return str(expression.subs(x_symbol, input_value))
