"""Deterministic systems-of-equations generators for MathForge."""

from __future__ import annotations

from sympy import Symbol, simplify, sympify

from models.content_models import MathProblem, Solution, Worksheet
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes

from .common import build_practice_quiz, require_positive_count, require_text


def generate_systems_of_equations_worksheet(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate deterministic systems of two linear equations in two variables."""
    require_text(topic, "topic")
    require_text(difficulty, "difficulty")
    require_text(start_id, "start_id")
    require_positive_count(count)

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


def generate_systems_of_equations_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic systems of equations worksheet resource pack."""
    worksheet = generate_systems_of_equations_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_systems_study_guide(topic, difficulty),
        common_mistakes=_build_systems_common_mistakes(topic, difficulty),
        tutor_notes=_build_systems_tutor_notes(topic, difficulty),
        practice_quiz=build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "systems_of_equations_resource_pack",
        },
    )


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


def _build_systems_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing guidance for systems of equations."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Solve a system by finding the ordered pair that makes both "
            "linear equations true at the same time."
        ),
        key_points=(
            "Learning objective: solve systems of linear equations in two variables.",
            "Key idea: the solution is an ordered pair (x, y).",
            "Key idea: elimination can remove one variable by adding equations.",
            "Key idea: check the solution in both original equations.",
        ),
        practice_tips=(
            "Worked-example guidance: line up like variables before eliminating.",
            "Worked-example guidance: add or subtract equations to solve for one variable.",
            "Worked-example guidance: substitute the known value to find the other variable.",
            "Worked-example guidance: verify the ordered pair in both equations.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_systems_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance for systems of equations."""
    return CommonMistakes(
        mistakes=(
            "Treating x and y values as separate answers instead of an ordered pair.",
            "Eliminating a variable but forgetting to solve for the second variable.",
            "Changing signs incorrectly when subtracting equations.",
            "Checking the ordered pair in only one equation.",
        ),
        corrections=(
            "Write the final answer as an ordered pair (x, y).",
            "After finding one variable, substitute it into either original equation.",
            "Keep columns aligned and distribute negative signs carefully.",
            "Substitute the ordered pair into both equations before finishing.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_systems_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts for systems of equations."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner what an ordered pair represents.",
            "Diagnostic question: which variable is easiest to eliminate first?",
            "Diagnostic question: did the learner check both equations?",
            "Intervention suggestion: have the learner stack equations in columns.",
            "Intervention suggestion: graph the intersection concept verbally before solving.",
        ),
        discussion_prompts=(
            "Why must the same ordered pair satisfy both equations?",
            "How does elimination reduce two equations to one variable?",
            "What can checking both equations reveal about arithmetic mistakes?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )
