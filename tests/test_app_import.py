"""Smoke tests for the Streamlit app module."""

from collections.abc import Callable

from streamlit.testing.v1 import AppTest

import app.main


def test_app_main_imports_without_running_streamlit_app() -> None:
    assert isinstance(app.main.main, Callable)
    assert isinstance(app.main.generate_linear_equation_resource_pack, Callable)
    assert isinstance(app.main.generate_quadratic_factoring_resource_pack, Callable)
    assert isinstance(app.main.generate_systems_of_equations_resource_pack, Callable)
    assert isinstance(app.main.generate_resource_pack_from_learning_objective, Callable)
    assert isinstance(app.main.export_resource_pack_to_markdown, Callable)
    assert isinstance(app.main.export_resource_pack_to_html, Callable)
    assert isinstance(app.main.college_algebra_template, Callable)
    assert "Quadratic equations by factoring" in app.main.TOPIC_OPTIONS
    assert "Systems of linear equations" in app.main.TOPIC_OPTIONS


def test_topic_mode_generates_linear_worksheet() -> None:
    test_app = _run_app()

    test_app.button[0].click().run()

    assert not test_app.exception
    assert "Worksheet" in _tab_labels(test_app)
    assert "Solution Key" in _tab_labels(test_app)
    assert "Exports" in _tab_labels(test_app)
    assert "Linear equations Worksheet" in test_app.text_area[0].value
    assert "Download Worksheet Markdown" in _download_labels(test_app)
    assert "Download Worksheet HTML" in _download_labels(test_app)


def test_topic_mode_generates_quadratic_factoring_worksheet() -> None:
    test_app = _run_app()

    test_app.selectbox[0].set_value("Quadratic equations by factoring").run()
    test_app.button[0].click().run()

    assert not test_app.exception
    assert test_app.text_input[0].value == "quadratic"
    assert "Quadratic equations by factoring Worksheet" in test_app.text_area[0].value
    assert "Solve by factoring" in test_app.text_area[0].value
    assert "Download Worksheet Markdown" in _download_labels(test_app)
    assert "Download Worksheet HTML" in _download_labels(test_app)


def test_topic_mode_generates_systems_of_equations_worksheet() -> None:
    test_app = _run_app()

    test_app.selectbox[0].set_value("Systems of linear equations").run()
    test_app.button[0].click().run()

    assert not test_app.exception
    assert test_app.text_input[0].value == "systems"
    assert "Systems of linear equations Worksheet" in test_app.text_area[0].value
    assert "Solve the system of equations" in test_app.text_area[0].value
    assert "Download Worksheet Markdown" in _download_labels(test_app)
    assert "Download Worksheet HTML" in _download_labels(test_app)


def test_learning_objective_mode_exposes_college_algebra_objectives() -> None:
    test_app = _run_app()

    test_app.radio[1].set_value("Learning Objective mode").run()

    assert not test_app.exception
    assert test_app.selectbox[0].label == "Course"
    assert test_app.selectbox[0].value == "College Algebra"
    assert test_app.selectbox[1].label == "Module"
    assert "Linear Equations" in test_app.selectbox[1].options
    assert "Quadratic Equations" in test_app.selectbox[1].options
    assert "Systems of Equations" in test_app.selectbox[1].options
    assert test_app.selectbox[2].label == "Learning Objective"
    assert "Solve linear equations in one variable" in test_app.selectbox[2].options
    assert any(
        "Selected learning objective: Solve linear equations in one variable"
        in caption.value
        for caption in test_app.caption
    )


def test_learning_objective_mode_exposes_quadratic_objective() -> None:
    test_app = _run_app()

    test_app.radio[1].set_value("Learning Objective mode").run()
    test_app.selectbox[1].set_value("Quadratic Equations").run()

    assert not test_app.exception
    assert test_app.selectbox[2].options == [
        "Solve quadratic equations by factoring",
    ]
    assert test_app.text_input[0].value == "quadratic"


def test_learning_objective_mode_exposes_systems_objective() -> None:
    test_app = _run_app()

    test_app.radio[1].set_value("Learning Objective mode").run()
    test_app.selectbox[1].set_value("Systems of Equations").run()

    assert not test_app.exception
    assert test_app.selectbox[2].options == [
        "Solve systems of linear equations in two variables",
    ]
    assert test_app.text_input[0].value == "systems"


def test_worksheet_only_ui_exposes_worksheet_exports() -> None:
    test_app = _run_app()

    test_app.button[0].click().run()

    assert not test_app.exception
    assert _download_labels(test_app) == [
        "Download Worksheet Markdown",
        "Download Worksheet HTML",
    ]
    assert test_app.text_area[0].label == "Markdown"
    assert test_app.text_area[1].label == "HTML"


def test_full_resource_pack_ui_exposes_resource_pack_exports() -> None:
    test_app = _run_app()

    test_app.radio[0].set_value("Full Resource Pack").run()
    test_app.button[0].click().run()

    assert not test_app.exception
    assert _tab_labels(test_app) == [
        "Worksheet",
        "Solution Key",
        "Study Guide",
        "Common Mistakes",
        "Tutor Notes",
        "Exports",
    ]
    assert _download_labels(test_app) == [
        "Download Resource Pack Markdown",
        "Download Resource Pack HTML",
    ]
    assert test_app.text_area[0].label == "Resource Pack Markdown"
    assert test_app.text_area[1].label == "Resource Pack HTML"
    assert "## Study Guide" in test_app.text_area[0].value
    assert "mathforge-resource-pack" in test_app.text_area[1].value


def _run_app() -> AppTest:
    """Return a freshly run Streamlit app test harness."""
    test_app = AppTest.from_file("app/main.py")
    test_app.run()
    assert not test_app.exception
    return test_app


def _tab_labels(test_app: AppTest) -> list[str]:
    """Return labels for rendered tabs."""
    return [tab.label for tab in test_app.tabs]


def _download_labels(test_app: AppTest) -> list[str]:
    """Return labels for rendered download buttons."""
    return [element.label for element in test_app.get("download_button")]
