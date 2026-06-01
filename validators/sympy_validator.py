"""SymPy-backed validation helpers for MathForge answers.

This module validates string inputs and returns structured results. It does not
depend on content models, worksheet generation, exporters, Streamlit, or AI
features.
"""

from __future__ import annotations

from dataclasses import dataclass

from sympy import Expr, Symbol, simplify, sympify
from sympy.core.sympify import SympifyError


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Structured result returned by answer validation helpers."""

    is_valid: bool
    message: str
    expected: str | None = None
    actual: str | None = None
    error: str | None = None


def validate_expression_equivalence(expected: str, actual: str) -> ValidationResult:
    """Validate whether two mathematical expression strings are equivalent."""
    try:
        expected_expr = _parse_expression(expected, "expected")
        actual_expr = _parse_expression(actual, "actual")
        is_equivalent = simplify(expected_expr - actual_expr) == 0
    except (TypeError, ValueError, SympifyError) as exc:
        return _invalid_result(
            "Unable to validate expression equivalence.",
            expected=expected,
            actual=actual,
            error=exc,
        )

    if is_equivalent:
        return ValidationResult(
            is_valid=True,
            message="Expressions are equivalent.",
            expected=expected,
            actual=actual,
        )

    return ValidationResult(
        is_valid=False,
        message="Expressions are not equivalent.",
        expected=expected,
        actual=actual,
    )


def validate_numeric_answer(
    expected: str,
    actual: str,
    *,
    tolerance: float = 1e-9,
) -> ValidationResult:
    """Validate whether two numeric answer strings match within a tolerance."""
    if tolerance < 0:
        return ValidationResult(
            is_valid=False,
            message="Tolerance must be non-negative.",
            expected=expected,
            actual=actual,
            error="invalid_tolerance",
        )

    try:
        expected_number = float(_parse_expression(expected, "expected").evalf())
        actual_number = float(_parse_expression(actual, "actual").evalf())
    except (TypeError, ValueError, SympifyError) as exc:
        return _invalid_result(
            "Unable to validate numeric answer.",
            expected=expected,
            actual=actual,
            error=exc,
        )

    if abs(expected_number - actual_number) <= tolerance:
        return ValidationResult(
            is_valid=True,
            message="Numeric answers match within tolerance.",
            expected=expected,
            actual=actual,
        )

    return ValidationResult(
        is_valid=False,
        message="Numeric answers do not match within tolerance.",
        expected=expected,
        actual=actual,
    )


def validate_equation_solution(
    equation: str,
    variable: str,
    proposed_solution: str,
) -> ValidationResult:
    """Validate whether a proposed solution satisfies an equation string.

    The equation must contain exactly one equals sign, such as ``x + 2 = 5``.
    The proposed solution is substituted for the named variable before the two
    sides are compared.
    """
    try:
        _require_text(equation, "equation")
        _require_text(variable, "variable")
        _require_text(proposed_solution, "proposed_solution")

        left_text, right_text = _split_equation(equation)
        variable_symbol = Symbol(variable.strip())
        solution_expr = _parse_expression(proposed_solution, "proposed_solution")
        left_expr = _parse_expression(left_text, "left side")
        right_expr = _parse_expression(right_text, "right side")

        substituted_left = left_expr.subs(variable_symbol, solution_expr)
        substituted_right = right_expr.subs(variable_symbol, solution_expr)
        is_solution = simplify(substituted_left - substituted_right) == 0
    except (TypeError, ValueError, SympifyError) as exc:
        return _invalid_result(
            "Unable to validate equation solution.",
            expected=equation,
            actual=proposed_solution,
            error=exc,
        )

    if is_solution:
        return ValidationResult(
            is_valid=True,
            message="Proposed solution satisfies the equation.",
            expected=equation,
            actual=proposed_solution,
        )

    return ValidationResult(
        is_valid=False,
        message="Proposed solution does not satisfy the equation.",
        expected=equation,
        actual=proposed_solution,
    )


def _parse_expression(value: str, field_name: str) -> Expr:
    """Parse a required string into a SymPy expression."""
    _require_text(value, field_name)
    return sympify(value)


def _require_text(value: str, field_name: str) -> None:
    """Validate that a value is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty.")


def _split_equation(equation: str) -> tuple[str, str]:
    """Split an equation string into left and right expression text."""
    parts = equation.split("=")
    if len(parts) != 2:
        raise ValueError("equation must contain exactly one equals sign.")

    left_text, right_text = parts[0].strip(), parts[1].strip()
    _require_text(left_text, "left side")
    _require_text(right_text, "right side")
    return left_text, right_text


def _invalid_result(
    message: str,
    *,
    expected: str,
    actual: str,
    error: Exception,
) -> ValidationResult:
    """Build a structured invalid result from a handled validation error."""
    return ValidationResult(
        is_valid=False,
        message=message,
        expected=expected,
        actual=actual,
        error=str(error),
    )
