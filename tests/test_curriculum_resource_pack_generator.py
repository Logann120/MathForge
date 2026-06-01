"""Tests for curriculum-aligned resource pack generation."""

import pytest

from generator.curriculum_resource_pack_generator import (
    generate_resource_pack_from_learning_objective,
)
from models.curriculum import LearningObjective
from models.resource_pack import ResourcePack
from templates.course_templates import college_algebra_template


def test_generate_resource_pack_from_learning_objective() -> None:
    objective = college_algebra_template().modules[0].learning_objectives[0]

    resource_pack = generate_resource_pack_from_learning_objective(
        learning_objective=objective,
        difficulty="easy",
        count=2,
        start_id="linear-objective",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert resource_pack.worksheet.worksheet_id == "linear-objective-worksheet"
    assert len(resource_pack.worksheet.problems) == 2
    assert resource_pack.metadata["learning_objective_id"] == objective.objective_id
    assert resource_pack.metadata["learning_objective"] == objective.description


def test_generate_resource_pack_from_learning_objective_is_deterministic() -> None:
    objective = college_algebra_template().modules[0].learning_objectives[0]

    first = generate_resource_pack_from_learning_objective(
        objective,
        "easy",
        2,
        "linear-objective",
    )
    second = generate_resource_pack_from_learning_objective(
        objective,
        "easy",
        2,
        "linear-objective",
    )

    assert first == second


def test_generate_resource_pack_from_learning_objective_rejects_unsupported_topic() -> None:
    objective = LearningObjective(
        objective_id="quadratic-001",
        description="Solve quadratic equations",
        topic="Quadratic equations",
    )

    with pytest.raises(ValueError, match="only linear equations"):
        generate_resource_pack_from_learning_objective(
            learning_objective=objective,
            difficulty="easy",
            count=1,
            start_id="quadratic",
        )


def test_generate_resource_pack_from_learning_objective_requires_objective() -> None:
    with pytest.raises(TypeError, match="learning_objective"):
        generate_resource_pack_from_learning_objective(
            learning_objective="not an objective",
            difficulty="easy",
            count=1,
            start_id="linear",
        )
