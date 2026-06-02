"""Deterministic quadratic-factoring generators for MathForge."""

from __future__ import annotations

from models.content_models import MathProblem, Solution, Worksheet
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes
from validators.sympy_validator import validate_equation_solution

from .common import build_practice_quiz, require_positive_count, require_text


def generate_quadratic_factoring_worksheet(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate a deterministic worksheet of factorable quadratic equations."""
    require_text(topic, "topic")
    require_text(difficulty, "difficulty")
    require_text(start_id, "start_id")
    require_positive_count(count)

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


def generate_quadratic_factoring_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic quadratic factoring worksheet resource pack."""
    worksheet = generate_quadratic_factoring_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_quadratic_study_guide(topic, difficulty),
        common_mistakes=_build_quadratic_common_mistakes(topic, difficulty),
        tutor_notes=_build_quadratic_tutor_notes(topic, difficulty),
        practice_quiz=build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "quadratic_factoring_resource_pack",
        },
    )


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


def _build_quadratic_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing quadratic factoring guidance."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Factor the quadratic, use the zero product property, and check "
            "both solutions in the original equation."
        ),
        key_points=(
            "Learning objective: solve factorable quadratic equations.",
            "Key idea: rewrite x**2 + bx + c as two binomial factors.",
            "Key idea: if a product is zero, at least one factor must be zero.",
            "Key idea: quadratic equations can have two solutions.",
        ),
        practice_tips=(
            "Worked-example guidance: identify two integers whose product is c.",
            "Worked-example guidance: confirm those integers add to b.",
            "Worked-example guidance: set each factor equal to zero.",
            "Worked-example guidance: substitute both roots to check the equation.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_quadratic_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance for factoring quadratics."""
    return CommonMistakes(
        mistakes=(
            "Choosing factors whose product is correct but whose sum is not.",
            "Finding only one solution after factoring.",
            "Forgetting to set each factor equal to zero.",
            "Losing negative signs when writing binomial factors.",
        ),
        corrections=(
            "Check both the product and the sum before writing the factors.",
            "Use the zero product property to solve both linear factors.",
            "Write a separate equation for each factor.",
            "Substitute both answers into the original quadratic equation.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_quadratic_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts for factoring quadratics."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner to list factor pairs for c.",
            "Diagnostic question: which pair also adds to the x coefficient?",
            "Diagnostic question: did the learner find both roots?",
            "Intervention suggestion: use a product-sum table before factoring.",
            "Intervention suggestion: have the learner check each root by substitution.",
        ),
        discussion_prompts=(
            "Why does the zero product property create two equations?",
            "How do signs in the factors affect the roots?",
            "How can checking both roots reveal a factoring error?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )
