"""Deterministic worksheet problem generation for MathForge."""

from __future__ import annotations

from sympy import Symbol, simplify, sympify

from models.content_models import MathProblem, Solution, Worksheet
from validators.sympy_validator import validate_equation_solution


def generate_linear_equation_worksheet(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate a deterministic worksheet of linear equations.

    Generated problems have the form ``a*x + b = c`` and integer solutions.
    Inputs are intentionally explicit and predictable so the generator is easy
    to test, review, and extend.
    """
    _require_text(topic, "topic")
    _require_text(difficulty, "difficulty")
    _require_text(start_id, "start_id")

    if not isinstance(count, int):
        raise TypeError("count must be an integer.")
    if count <= 0:
        raise ValueError("count must be positive.")

    problems: list[MathProblem] = []
    solutions: list[Solution] = []

    for index in range(count):
        problem_id = f"{start_id}-{index + 1:03d}"
        a, b, answer = _linear_equation_terms(difficulty, index)
        c = (a * answer) + b
        equation = f"{a}*x + {b} = {c}"
        answer_text = str(answer)

        validation = validate_equation_solution(equation, "x", answer_text)
        if not validation.is_valid:
            raise ValueError(
                f"generated answer failed validation for {problem_id}: "
                f"{validation.message}"
            )

        problems.append(
            MathProblem(
                problem_id=problem_id,
                prompt=f"Solve for x: {equation}",
                answer=answer_text,
                topic=topic,
                difficulty=difficulty,
                metadata={
                    "equation": equation,
                    "variable": "x",
                    "coefficient_a": str(a),
                    "constant_b": str(b),
                    "constant_c": str(c),
                },
            )
        )
        solutions.append(
            Solution(
                problem_id=problem_id,
                final_answer=answer_text,
                steps=(
                    f"Start with {equation}.",
                    f"Subtract {b} from both sides.",
                    f"Divide both sides by {a}.",
                    f"x = {answer_text}.",
                ),
            )
        )

    return Worksheet(
        title=f"{topic} Worksheet",
        worksheet_id=f"{start_id}-worksheet",
        instructions="Solve each equation for x.",
        problems=tuple(problems),
        solutions=tuple(solutions),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "linear_equation",
        },
    )


def generate_quadratic_factoring_worksheet(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate a deterministic worksheet of factorable quadratic equations."""
    _require_text(topic, "topic")
    _require_text(difficulty, "difficulty")
    _require_text(start_id, "start_id")

    if not isinstance(count, int):
        raise TypeError("count must be an integer.")
    if count <= 0:
        raise ValueError("count must be positive.")

    problems: list[MathProblem] = []
    solutions: list[Solution] = []

    for index in range(count):
        problem_id = f"{start_id}-{index + 1:03d}"
        first_root, second_root = _quadratic_roots(difficulty, index)
        equation = _quadratic_equation_text(first_root, second_root)
        answer_text = _quadratic_answer_text(first_root, second_root)

        for root in (first_root, second_root):
            validation = validate_equation_solution(equation, "x", str(root))
            if not validation.is_valid:
                raise ValueError(
                    f"generated root failed validation for {problem_id}: "
                    f"{validation.message}"
                )

        problems.append(
            MathProblem(
                problem_id=problem_id,
                prompt=f"Solve by factoring: {equation}",
                answer=answer_text,
                topic=topic,
                difficulty=difficulty,
                metadata={
                    "equation": equation,
                    "variable": "x",
                    "root_1": str(first_root),
                    "root_2": str(second_root),
                    "factored_form": _factored_form(first_root, second_root),
                },
            )
        )
        solutions.append(
            Solution(
                problem_id=problem_id,
                final_answer=answer_text,
                steps=(
                    f"Start with {equation}.",
                    f"Factor the quadratic as {_factored_form(first_root, second_root)} = 0.",
                    "Set each factor equal to zero.",
                    f"x = {first_root} or x = {second_root}.",
                ),
            )
        )

    return Worksheet(
        title=f"{topic} Worksheet",
        worksheet_id=f"{start_id}-worksheet",
        instructions="Solve each quadratic equation by factoring.",
        problems=tuple(problems),
        solutions=tuple(solutions),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "quadratic_factoring",
        },
    )


def generate_systems_of_equations_worksheet(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate deterministic systems of two linear equations in two variables."""
    _require_text(topic, "topic")
    _require_text(difficulty, "difficulty")
    _require_text(start_id, "start_id")

    if not isinstance(count, int):
        raise TypeError("count must be an integer.")
    if count <= 0:
        raise ValueError("count must be positive.")

    problems: list[MathProblem] = []
    solutions: list[Solution] = []

    for index in range(count):
        problem_id = f"{start_id}-{index + 1:03d}"
        x_value, y_value = _system_solution(difficulty, index)
        first_equation, second_equation = _system_equations(x_value, y_value)
        answer_text = f"({x_value}, {y_value})"

        if not _validate_system_solution(
            (first_equation, second_equation),
            x_value,
            y_value,
        ):
            raise ValueError(f"generated system failed validation for {problem_id}.")

        problems.append(
            MathProblem(
                problem_id=problem_id,
                prompt=(
                    "Solve the system of equations:\n"
                    f"{first_equation}\n"
                    f"{second_equation}"
                ),
                answer=answer_text,
                topic=topic,
                difficulty=difficulty,
                metadata={
                    "equation_1": first_equation,
                    "equation_2": second_equation,
                    "variable_1": "x",
                    "variable_2": "y",
                    "x_value": str(x_value),
                    "y_value": str(y_value),
                },
            )
        )
        solutions.append(
            Solution(
                problem_id=problem_id,
                final_answer=answer_text,
                steps=(
                    f"Start with the system {first_equation} and {second_equation}.",
                    "Add the equations to eliminate y.",
                    f"Solve for x to get x = {x_value}.",
                    f"Substitute x = {x_value} into one equation to get y = {y_value}.",
                    f"The solution is {answer_text}.",
                ),
            )
        )

    return Worksheet(
        title=f"{topic} Worksheet",
        worksheet_id=f"{start_id}-worksheet",
        instructions="Solve each system of equations for x and y.",
        problems=tuple(problems),
        solutions=tuple(solutions),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "systems_of_equations",
        },
    )


def _linear_equation_terms(difficulty: str, index: int) -> tuple[int, int, int]:
    """Return deterministic ``a``, ``b``, and solution values."""
    normalized_difficulty = difficulty.strip().lower()

    if normalized_difficulty in {"easy", "introductory", "beginner"}:
        coefficient_base = 2
        constant_base = 1
        answer_base = 1
    elif normalized_difficulty in {"hard", "advanced"}:
        coefficient_base = 4
        constant_base = 5
        answer_base = 3
    else:
        coefficient_base = 3
        constant_base = 2
        answer_base = 2

    a = coefficient_base + index
    b = constant_base + (2 * index)
    answer = answer_base + index
    return a, b, answer


def _quadratic_roots(difficulty: str, index: int) -> tuple[int, int]:
    """Return deterministic integer roots for a factorable quadratic."""
    normalized_difficulty = difficulty.strip().lower()

    if normalized_difficulty in {"easy", "introductory", "beginner"}:
        return index + 1, index + 2
    if normalized_difficulty in {"hard", "advanced"}:
        return -(index + 1), index + 3
    return index + 2, index + 4


def _quadratic_equation_text(first_root: int, second_root: int) -> str:
    """Return expanded equation text for roots of a monic quadratic."""
    linear_coefficient = -(first_root + second_root)
    constant = first_root * second_root
    terms = ["x**2"]

    if linear_coefficient:
        terms.append(_signed_term(linear_coefficient, "x"))
    if constant:
        terms.append(_signed_term(constant, ""))

    return " ".join(terms) + " = 0"


def _signed_term(coefficient: int, variable: str) -> str:
    """Format a signed polynomial term."""
    sign = "+" if coefficient > 0 else "-"
    magnitude = abs(coefficient)

    if variable:
        value = variable if magnitude == 1 else f"{magnitude}*{variable}"
    else:
        value = str(magnitude)

    return f"{sign} {value}"


def _quadratic_answer_text(first_root: int, second_root: int) -> str:
    """Return a readable answer string for two roots."""
    return f"{first_root}, {second_root}"


def _factored_form(first_root: int, second_root: int) -> str:
    """Return factored form for two roots."""
    return f"{_factor_for_root(first_root)}{_factor_for_root(second_root)}"


def _factor_for_root(root: int) -> str:
    """Return a linear factor for a root."""
    if root < 0:
        return f"(x + {abs(root)})"
    return f"(x - {root})"


def _system_solution(difficulty: str, index: int) -> tuple[int, int]:
    """Return deterministic integer solutions for a linear system."""
    normalized_difficulty = difficulty.strip().lower()

    if normalized_difficulty in {"easy", "introductory", "beginner"}:
        return index + 1, index + 2
    if normalized_difficulty in {"hard", "advanced"}:
        return index + 3, -(index + 1)
    return index + 2, index + 3


def _system_equations(x_value: int, y_value: int) -> tuple[str, str]:
    """Return an elimination-friendly system for a known solution."""
    return (
        f"x + y = {x_value + y_value}",
        f"x - y = {x_value - y_value}",
    )


def _validate_system_solution(
    equations: tuple[str, str],
    x_value: int,
    y_value: int,
) -> bool:
    """Validate that a solution satisfies both equations in a system."""
    x_symbol = Symbol("x")
    y_symbol = Symbol("y")

    for equation in equations:
        left_text, right_text = _split_equation_text(equation)
        left_expr = sympify(left_text).subs(
            {x_symbol: x_value, y_symbol: y_value}
        )
        right_expr = sympify(right_text).subs(
            {x_symbol: x_value, y_symbol: y_value}
        )
        if simplify(left_expr - right_expr) != 0:
            return False

    return True


def _split_equation_text(equation: str) -> tuple[str, str]:
    """Split simple equation text into left and right sides."""
    parts = equation.split("=")
    if len(parts) != 2:
        raise ValueError("equation must contain exactly one equals sign.")
    return parts[0].strip(), parts[1].strip()


def _require_text(value: str, field_name: str) -> None:
    """Validate that a generator input is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty.")
