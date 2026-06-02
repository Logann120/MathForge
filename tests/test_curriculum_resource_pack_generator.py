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


def test_generate_quadratic_resource_pack_from_learning_objective() -> None:
    objective = college_algebra_template().modules[1].learning_objectives[0]

    resource_pack = generate_resource_pack_from_learning_objective(
        learning_objective=objective,
        difficulty="easy",
        count=2,
        start_id="quadratic-objective",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert resource_pack.worksheet.worksheet_id == "quadratic-objective-worksheet"
    assert len(resource_pack.worksheet.problems) == 2
    assert resource_pack.worksheet.metadata["generator"] == "quadratic_factoring"
    assert resource_pack.metadata["learning_objective_id"] == objective.objective_id
    assert resource_pack.metadata["learning_objective"] == objective.description


def test_generate_systems_resource_pack_from_learning_objective() -> None:
    objective = college_algebra_template().modules[2].learning_objectives[0]

    resource_pack = generate_resource_pack_from_learning_objective(
        learning_objective=objective,
        difficulty="easy",
        count=2,
        start_id="systems-objective",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert resource_pack.worksheet.worksheet_id == "systems-objective-worksheet"
    assert len(resource_pack.worksheet.problems) == 2
    assert resource_pack.worksheet.metadata["generator"] == "systems_of_equations"
    assert resource_pack.metadata["learning_objective_id"] == objective.objective_id
    assert resource_pack.metadata["learning_objective"] == objective.description


def test_generate_factoring_resource_pack_from_learning_objective() -> None:
    objective = college_algebra_template().modules[3].learning_objectives[0]

    resource_pack = generate_resource_pack_from_learning_objective(
        learning_objective=objective,
        difficulty="easy",
        count=3,
        start_id="factoring-objective",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert resource_pack.worksheet.worksheet_id == "factoring-objective-worksheet"
    assert len(resource_pack.worksheet.problems) == 3
    assert resource_pack.worksheet.metadata["generator"] == "factoring_techniques"
    assert resource_pack.metadata["learning_objective_id"] == objective.objective_id
    assert resource_pack.metadata["learning_objective"] == objective.description


def test_generate_functions_resource_pack_from_learning_objective() -> None:
    objective = college_algebra_template().modules[4].learning_objectives[0]

    resource_pack = generate_resource_pack_from_learning_objective(
        learning_objective=objective,
        difficulty="easy",
        count=3,
        start_id="functions-objective",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert resource_pack.worksheet.worksheet_id == "functions-objective-worksheet"
    assert len(resource_pack.worksheet.problems) == 3
    assert resource_pack.worksheet.metadata["generator"] == "functions_basics"
    assert resource_pack.metadata["learning_objective_id"] == objective.objective_id
    assert resource_pack.metadata["learning_objective"] == objective.description


def test_generate_resource_pack_from_learning_objective_rejects_unsupported_topic() -> None:
    objective = LearningObjective(
        objective_id="exponential-001",
        description="Solve exponential equations",
        topic="Exponential equations",
    )

    with pytest.raises(ValueError, match="functions basics"):
        generate_resource_pack_from_learning_objective(
            learning_objective=objective,
            difficulty="easy",
            count=1,
            start_id="exponential",
        )


def test_generate_resource_pack_from_learning_objective_requires_objective() -> None:
    with pytest.raises(TypeError, match="learning_objective"):
        generate_resource_pack_from_learning_objective(
            learning_objective="not an objective",
            difficulty="easy",
            count=1,
            start_id="linear",
        )
