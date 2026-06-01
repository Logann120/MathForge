"""Tests for SymPy-backed answer validation helpers."""

from validators.sympy_validator import (
    ValidationResult,
    validate_equation_solution,
    validate_expression_equivalence,
    validate_numeric_answer,
)


def test_validate_expression_equivalence_accepts_equivalent_expressions() -> None:
    result = validate_expression_equivalence("x + x", "2*x")

    assert result == ValidationResult(
        is_valid=True,
        message="Expressions are equivalent.",
        expected="x + x",
        actual="2*x",
    )


def test_validate_expression_equivalence_rejects_different_expressions() -> None:
    result = validate_expression_equivalence("x + 1", "x + 2")

    assert result.is_valid is False
    assert result.message == "Expressions are not equivalent."
    assert result.error is None


def test_validate_expression_equivalence_handles_invalid_expression() -> None:
    result = validate_expression_equivalence("x +", "x")

    assert result.is_valid is False
    assert result.message == "Unable to validate expression equivalence."
    assert result.error


def test_validate_numeric_answer_accepts_close_values() -> None:
    result = validate_numeric_answer("1/3", "0.3333333", tolerance=1e-6)

    assert result.is_valid is True
    assert result.message == "Numeric answers match within tolerance."


def test_validate_numeric_answer_rejects_values_outside_tolerance() -> None:
    result = validate_numeric_answer("1/3", "0.3", tolerance=1e-6)

    assert result.is_valid is False
    assert result.message == "Numeric answers do not match within tolerance."


def test_validate_numeric_answer_handles_invalid_input() -> None:
    result = validate_numeric_answer("not a number", "3")

    assert result.is_valid is False
    assert result.message == "Unable to validate numeric answer."
    assert result.error


def test_validate_numeric_answer_rejects_negative_tolerance() -> None:
    result = validate_numeric_answer("1", "1", tolerance=-1)

    assert result.is_valid is False
    assert result.message == "Tolerance must be non-negative."
    assert result.error == "invalid_tolerance"


def test_validate_equation_solution_accepts_solution() -> None:
    result = validate_equation_solution("x + 2 = 5", "x", "3")

    assert result.is_valid is True
    assert result.message == "Proposed solution satisfies the equation."


def test_validate_equation_solution_rejects_wrong_solution() -> None:
    result = validate_equation_solution("x + 2 = 5", "x", "4")

    assert result.is_valid is False
    assert result.message == "Proposed solution does not satisfy the equation."


def test_validate_equation_solution_handles_malformed_equation() -> None:
    result = validate_equation_solution("x + 2", "x", "3")

    assert result.is_valid is False
    assert result.message == "Unable to validate equation solution."
    assert result.error
