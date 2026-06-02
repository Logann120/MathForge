"""Deterministic factoring-techniques generators for MathForge."""

from __future__ import annotations

from sympy import expand, simplify, sympify

from models.content_models import MathProblem, Solution, Worksheet
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes

from .common import build_practice_quiz, require_positive_count, require_text


def generate_factoring_techniques_worksheet(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate deterministic factoring practice across common strategies."""
    require_text(topic, "topic")
    require_text(difficulty, "difficulty")
    require_text(start_id, "start_id")
    require_positive_count(count)

    problems: list[MathProblem] = []
    solutions: list[Solution] = []

    for index in range(count):
        problem_id = f"{start_id}-{index + 1:03d}"
        expression, factored_form, strategy = _factoring_problem(index)

        if not _validate_factored_expression(expression, factored_form):
            raise ValueError(
                f"generated factorization failed validation for {problem_id}."
            )

        problems.append(
            MathProblem(
                problem_id=problem_id,
                prompt=f"Factor completely: {expression}",
                answer=factored_form,
                topic=topic,
                difficulty=difficulty,
                metadata={
                    "expression": expression,
                    "factored_form": factored_form,
                    "strategy": strategy,
                    "variable": "x",
                },
            )
        )
        solutions.append(
            Solution(
                problem_id=problem_id,
                final_answer=factored_form,
                steps=(
                    f"Start with {expression}.",
                    f"Identify the strategy: {strategy}.",
                    f"Rewrite the expression as {factored_form}.",
                    "Check by expanding the factored form.",
                ),
            )
        )

    return Worksheet(
        title=f"{topic} Worksheet",
        worksheet_id=f"{start_id}-worksheet",
        instructions="Factor each polynomial expression completely.",
        problems=tuple(problems),
        solutions=tuple(solutions),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "factoring_techniques",
        },
    )


def generate_factoring_techniques_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic factoring techniques worksheet resource pack."""
    worksheet = generate_factoring_techniques_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_factoring_study_guide(topic, difficulty),
        common_mistakes=_build_factoring_common_mistakes(topic, difficulty),
        tutor_notes=_build_factoring_tutor_notes(topic, difficulty),
        practice_quiz=build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "factoring_techniques_resource_pack",
        },
    )


def _factoring_problem(index: int) -> tuple[str, str, str]:
    """Return expression, factored form, and strategy for factoring practice."""
    strategy_index = index % 3
    sequence = index // 3

    if strategy_index == 0:
        factor = sequence + 2
        coefficient = sequence + 3
        constant = sequence + 4
        expression = f"{factor * coefficient}*x + {factor * constant}"
        factored_form = f"{factor}*({coefficient}*x + {constant})"
        return expression, factored_form, "greatest common factor"

    if strategy_index == 1:
        root = sequence + 2
        expression = f"x**2 - {root * root}"
        factored_form = f"(x - {root})*(x + {root})"
        return expression, factored_form, "difference of squares"

    first_root = sequence + 2
    second_root = sequence + 3
    linear_coefficient = first_root + second_root
    constant = first_root * second_root
    expression = f"x**2 + {linear_coefficient}*x + {constant}"
    factored_form = f"(x + {first_root})*(x + {second_root})"
    return expression, factored_form, "simple trinomial"


def _validate_factored_expression(expression: str, factored_form: str) -> bool:
    """Validate that a factored form expands to the original expression."""
    return simplify(sympify(expression) - expand(sympify(factored_form))) == 0


def _build_factoring_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing guidance for factoring techniques."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Factoring rewrites a polynomial as a product of simpler expressions "
            "without changing its value."
        ),
        key_points=(
            "Learning objective: factor polynomial expressions using common strategies.",
            "Key idea: always check for a greatest common factor first.",
            "Key idea: recognize a difference of squares as a**2 - b**2.",
            "Key idea: for x**2 + bx + c, find factors of c that add to b.",
        ),
        practice_tips=(
            "Worked-example guidance: scan for a shared numerical or variable factor.",
            "Worked-example guidance: identify perfect squares before factoring.",
            "Worked-example guidance: use a product-sum check for simple trinomials.",
            "Worked-example guidance: expand the answer to verify the factorization.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_factoring_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance for factoring techniques."""
    return CommonMistakes(
        mistakes=(
            "Skipping the greatest common factor before using another strategy.",
            "Treating a sum of squares as a difference of squares.",
            "Choosing trinomial factors with the right product but wrong sum.",
            "Forgetting to check the answer by expanding.",
        ),
        corrections=(
            "Look for a shared factor before applying a special pattern.",
            "Use the difference of squares pattern only for subtraction.",
            "Check both the product and the sum for trinomial factors.",
            "Expand the factored form to confirm it matches the original expression.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_factoring_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts for factoring techniques."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner which factoring strategy fits first.",
            "Diagnostic question: is there a greatest common factor?",
            "Diagnostic question: does the expression match a special product pattern?",
            "Intervention suggestion: have the learner expand the proposed factors.",
            "Intervention suggestion: use a product-sum table for simple trinomials.",
        ),
        discussion_prompts=(
            "Why is checking for a greatest common factor a useful first step?",
            "How can expanding help verify a factorization?",
            "What clues distinguish a difference of squares from a trinomial?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )
