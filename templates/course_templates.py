"""Deterministic course templates for MathForge."""

from __future__ import annotations

from models.curriculum import CourseModule, CourseTemplate, LearningObjective


def college_algebra_template() -> CourseTemplate:
    """Return the deterministic College Algebra sample course template."""
    linear_equations_objective = LearningObjective(
        objective_id="college-algebra-linear-equations-001",
        description="Solve linear equations in one variable",
        topic="Linear equations",
        standards=("College Algebra: Linear Equations",),
        metadata={
            "course": "College Algebra",
            "module": "Linear Equations",
        },
    )
    linear_equations_module = CourseModule(
        module_id="college-algebra-linear-equations",
        title="Linear Equations",
        learning_objectives=(linear_equations_objective,),
        metadata={"course": "College Algebra"},
    )
    return CourseTemplate(
        course_id="college-algebra",
        title="College Algebra",
        modules=(linear_equations_module,),
        metadata={"level": "community_college"},
    )
