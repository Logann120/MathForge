"""Generate resource packs from curriculum-aligned learning objectives."""

from __future__ import annotations

from generator.resource_pack_generator import (
    generate_linear_equation_resource_pack,
    generate_quadratic_factoring_resource_pack,
    generate_systems_of_equations_resource_pack,
)
from models.curriculum import LearningObjective
from models.resource_pack import ResourcePack


def generate_resource_pack_from_learning_objective(
    learning_objective: LearningObjective,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a resource pack for a supported learning objective."""
    if not isinstance(learning_objective, LearningObjective):
        raise TypeError("learning_objective must be a LearningObjective.")

    if _is_linear_equations_topic(learning_objective.topic):
        resource_pack = generate_linear_equation_resource_pack(
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
            metadata={
                **dict(resource_pack.metadata),
                "learning_objective_id": learning_objective.objective_id,
                "learning_objective": learning_objective.description,
            },
        )

    if _is_quadratic_factoring_topic(learning_objective.topic):
        resource_pack = generate_quadratic_factoring_resource_pack(
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
            metadata={
                **dict(resource_pack.metadata),
                "learning_objective_id": learning_objective.objective_id,
                "learning_objective": learning_objective.description,
            },
        )

    if _is_systems_of_equations_topic(learning_objective.topic):
        resource_pack = generate_systems_of_equations_resource_pack(
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
            metadata={
                **dict(resource_pack.metadata),
                "learning_objective_id": learning_objective.objective_id,
                "learning_objective": learning_objective.description,
            },
        )

    raise ValueError(
        "resource pack generation currently supports only linear equations, "
        "quadratic factoring, and systems of equations learning objectives."
    )


def _is_linear_equations_topic(topic: str) -> bool:
    """Return whether a topic maps to the current linear equations generator."""
    return topic.strip().lower() in {
        "linear equation",
        "linear equations",
        "linear equations in one variable",
    }


def _is_quadratic_factoring_topic(topic: str) -> bool:
    """Return whether a topic maps to the current quadratic factoring generator."""
    return topic.strip().lower() in {
        "quadratic equation",
        "quadratic equations",
        "quadratic equations by factoring",
        "factoring quadratic equations",
    }


def _is_systems_of_equations_topic(topic: str) -> bool:
    """Return whether a topic maps to the current systems generator."""
    return topic.strip().lower() in {
        "systems of equations",
        "systems of linear equations",
        "systems of linear equations in two variables",
    }
