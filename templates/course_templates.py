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
    quadratic_factoring_objective = LearningObjective(
        objective_id="college-algebra-quadratic-factoring-001",
        description="Solve quadratic equations by factoring",
        topic="Quadratic equations by factoring",
        standards=("College Algebra: Quadratic Equations by Factoring",),
        metadata={
            "course": "College Algebra",
            "module": "Quadratic Equations",
        },
    )
    quadratic_equations_module = CourseModule(
        module_id="college-algebra-quadratic-equations",
        title="Quadratic Equations",
        learning_objectives=(quadratic_factoring_objective,),
        metadata={"course": "College Algebra"},
    )
    systems_objective = LearningObjective(
        objective_id="college-algebra-systems-equations-001",
        description="Solve systems of linear equations in two variables",
        topic="Systems of linear equations",
        standards=("College Algebra: Systems of Linear Equations",),
        metadata={
            "course": "College Algebra",
            "module": "Systems of Equations",
        },
    )
    systems_module = CourseModule(
        module_id="college-algebra-systems-equations",
        title="Systems of Equations",
        learning_objectives=(systems_objective,),
        metadata={"course": "College Algebra"},
    )
    return CourseTemplate(
        course_id="college-algebra",
        title="College Algebra",
        modules=(linear_equations_module, quadratic_equations_module, systems_module),
        metadata={"level": "community_college"},
    )
