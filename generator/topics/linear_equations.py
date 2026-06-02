"""Deterministic linear-equation generators for MathForge."""

from __future__ import annotations

from models.content_models import MathProblem, Solution, Worksheet
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes
from validators.sympy_validator import validate_equation_solution

from .common import build_practice_quiz, require_positive_count, require_text


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
    require_text(topic, "topic")
    require_text(difficulty, "difficulty")
    require_text(start_id, "start_id")
    require_positive_count(count)

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


def generate_linear_equation_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic linear equation worksheet resource pack."""
    worksheet = generate_linear_equation_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_study_guide(topic, difficulty),
        common_mistakes=_build_common_mistakes(topic, difficulty),
        tutor_notes=_build_tutor_notes(topic, difficulty),
        practice_quiz=build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "linear_equation_resource_pack",
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


def _build_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing guidance."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Use inverse operations to isolate x while keeping both sides of "
            "the equation balanced."
        ),
        key_points=(
            "Learning objective: solve equations of the form ax + b = c.",
            "Learning objective: explain each inverse operation used.",
            "Key idea: subtract the constant term before dividing by the coefficient.",
            "Key idea: check the answer by substituting it back into the equation.",
        ),
        practice_tips=(
            "Worked-example guidance: identify a, b, and c before solving.",
            "Worked-example guidance: subtract b from both sides.",
            "Worked-example guidance: divide both sides by a to find x.",
            "Worked-example guidance: substitute the result to verify both sides match.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance."""
    return CommonMistakes(
        mistakes=(
            "Changing only one side of the equation during an inverse operation.",
            "Dividing before removing the constant term.",
            "Dropping the coefficient when rewriting ax.",
            "Not checking the final answer in the original equation.",
        ),
        corrections=(
            "Write the same operation on both sides before simplifying.",
            "Remove b first, then divide by a.",
            "Keep the coefficient attached to x until the division step.",
            "Substitute the proposed value of x into ax + b = c to confirm it works.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts and interventions."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner to name the first inverse operation.",
            "Diagnostic question: what value is being added to or subtracted from ax?",
            "Diagnostic question: what coefficient is attached to x?",
            "Intervention suggestion: have the learner rewrite each equation as two "
            "balanced columns before simplifying.",
            "Intervention suggestion: ask the learner to verify the answer by substitution.",
        ),
        discussion_prompts=(
            "How do you know which operation to undo first?",
            "What does it mean for both sides of an equation to stay balanced?",
            "How can substitution help you catch arithmetic mistakes?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )
