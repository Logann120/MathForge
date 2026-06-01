"""Tests for curriculum alignment models."""

import pytest

from models.curriculum import CourseModule, CourseTemplate, LearningObjective


def test_learning_objective_creation() -> None:
    objective = LearningObjective(
        objective_id="obj-001",
        description="Solve linear equations in one variable",
        topic="Linear equations",
        standards=("College Algebra",),
        metadata={"module": "Linear Equations"},
    )

    assert objective.objective_id == "obj-001"
    assert objective.topic == "Linear equations"
    assert objective.standards == ("College Algebra",)
    assert objective.metadata["module"] == "Linear Equations"


def test_learning_objective_requires_description() -> None:
    with pytest.raises(ValueError, match="description"):
        LearningObjective(
            objective_id="obj-001",
            description=" ",
            topic="Linear equations",
        )


def test_course_module_requires_objectives() -> None:
    with pytest.raises(ValueError, match="learning_objectives"):
        CourseModule(
            module_id="module-001",
            title="Linear Equations",
            learning_objectives=(),
        )


def test_course_module_rejects_duplicate_objective_ids() -> None:
    objective = LearningObjective(
        objective_id="obj-001",
        description="Solve linear equations in one variable",
        topic="Linear equations",
    )

    with pytest.raises(ValueError, match="duplicate objective_id"):
        CourseModule(
            module_id="module-001",
            title="Linear Equations",
            learning_objectives=(objective, objective),
        )


def test_course_template_creation() -> None:
    objective = LearningObjective(
        objective_id="obj-001",
        description="Solve linear equations in one variable",
        topic="Linear equations",
    )
    module = CourseModule(
        module_id="module-001",
        title="Linear Equations",
        learning_objectives=(objective,),
    )
    course = CourseTemplate(
        course_id="college-algebra",
        title="College Algebra",
        modules=(module,),
    )

    assert course.course_id == "college-algebra"
    assert course.modules == (module,)


def test_course_template_rejects_duplicate_module_ids() -> None:
    objective = LearningObjective(
        objective_id="obj-001",
        description="Solve linear equations in one variable",
        topic="Linear equations",
    )
    module = CourseModule(
        module_id="module-001",
        title="Linear Equations",
        learning_objectives=(objective,),
    )

    with pytest.raises(ValueError, match="duplicate module_id"):
        CourseTemplate(
            course_id="college-algebra",
            title="College Algebra",
            modules=(module, module),
        )


def test_curriculum_metadata_requires_string_values() -> None:
    with pytest.raises(TypeError, match="metadata values"):
        LearningObjective(
            objective_id="obj-001",
            description="Solve linear equations in one variable",
            topic="Linear equations",
            metadata={"order": 1},
        )
