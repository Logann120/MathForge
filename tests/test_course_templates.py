"""Tests for deterministic course templates."""

from templates.course_templates import college_algebra_template


def test_college_algebra_template_contains_linear_equations_module() -> None:
    course_template = college_algebra_template()

    assert course_template.course_id == "college-algebra"
    assert course_template.title == "College Algebra"
    assert len(course_template.modules) == 3
    assert course_template.modules[0].title == "Linear Equations"


def test_college_algebra_template_contains_linear_equations_objective() -> None:
    course_template = college_algebra_template()
    objective = course_template.modules[0].learning_objectives[0]

    assert objective.objective_id == "college-algebra-linear-equations-001"
    assert objective.description == "Solve linear equations in one variable"
    assert objective.topic == "Linear equations"
    assert objective.standards == ("College Algebra: Linear Equations",)


def test_college_algebra_template_contains_quadratic_factoring_objective() -> None:
    course_template = college_algebra_template()
    module = course_template.modules[1]
    objective = module.learning_objectives[0]

    assert module.title == "Quadratic Equations"
    assert objective.objective_id == "college-algebra-quadratic-factoring-001"
    assert objective.description == "Solve quadratic equations by factoring"
    assert objective.topic == "Quadratic equations by factoring"
    assert objective.standards == (
        "College Algebra: Quadratic Equations by Factoring",
    )


def test_college_algebra_template_contains_systems_objective() -> None:
    course_template = college_algebra_template()
    module = course_template.modules[2]
    objective = module.learning_objectives[0]

    assert module.title == "Systems of Equations"
    assert objective.objective_id == "college-algebra-systems-equations-001"
    assert objective.description == "Solve systems of linear equations in two variables"
    assert objective.topic == "Systems of linear equations"
    assert objective.standards == ("College Algebra: Systems of Linear Equations",)


def test_college_algebra_template_is_deterministic() -> None:
    first = college_algebra_template()
    second = college_algebra_template()

    assert first == second
