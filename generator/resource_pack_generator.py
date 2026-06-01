"""Deterministic instructional resource pack generation for MathForge."""

from __future__ import annotations

from generator.problem_generator import generate_linear_equation_worksheet
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
