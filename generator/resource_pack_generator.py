"""Deterministic instructional resource pack generation for MathForge."""

from __future__ import annotations

from generator.problem_generator import (
    generate_linear_equation_worksheet,
    generate_quadratic_factoring_worksheet,
    generate_systems_of_equations_worksheet,
)
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes


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
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "linear_equation_resource_pack",
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
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "quadratic_factoring_resource_pack",
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
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "systems_of_equations_resource_pack",
        },
    )


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
