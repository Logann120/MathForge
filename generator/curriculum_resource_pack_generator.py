"""Generate resource packs from curriculum-aligned learning objectives."""

from __future__ import annotations

from models.curriculum import LearningObjective
from models.resource_pack import ResourcePack
from topics.registry import find_topic_by_learning_objective_topic


def generate_resource_pack_from_learning_objective(
    learning_objective: LearningObjective,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a resource pack for a supported learning objective."""
    if not isinstance(learning_objective, LearningObjective):
        raise TypeError("learning_objective must be a LearningObjective.")

    try:
        topic = find_topic_by_learning_objective_topic(learning_objective.topic)
    except ValueError as exc:
        raise ValueError(
            "resource pack generation currently supports only linear equations, "
            "quadratic factoring, systems of equations, factoring techniques, "
            "and functions basics learning objectives."
        ) from exc

    resource_pack = topic.resource_pack_generator(
        topic=learning_objective.topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )
    return ResourcePack(
        worksheet=resource_pack.worksheet,
        study_guide=resource_pack.study_guide,
        common_mistakes=resource_pack.common_mistakes,
        tutor_notes=resource_pack.tutor_notes,
        practice_quiz=resource_pack.practice_quiz,
        metadata={
            **dict(resource_pack.metadata),
            "learning_objective_id": learning_objective.objective_id,
            "learning_objective": learning_objective.description,
        },
    )
