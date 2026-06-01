"""Deterministic worksheet problem generation for MathForge."""

from __future__ import annotations

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


def _require_text(value: str, field_name: str) -> None:
    """Validate that a generator input is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty.")
