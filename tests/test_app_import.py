"""Smoke tests for the Streamlit app module."""

from collections.abc import Callable

from streamlit.testing.v1 import AppTest

import app.main
from app.presets import generation_preset_labels
from topics.registry import supported_topic_labels


def test_app_main_imports_without_running_streamlit_app() -> None:
    assert isinstance(app.main.main, Callable)
    assert isinstance(app.main.generate_linear_equation_resource_pack, Callable)
    assert isinstance(app.main.generate_quadratic_factoring_resource_pack, Callable)
    assert isinstance(app.main.generate_systems_of_equations_resource_pack, Callable)
    assert isinstance(app.main.generate_factoring_techniques_resource_pack, Callable)
    assert isinstance(app.main.generate_functions_basics_resource_pack, Callable)
    assert isinstance(app.main.generate_resource_pack_from_learning_objective, Callable)
    assert isinstance(app.main.export_resource_pack_to_markdown, Callable)
    assert isinstance(app.main.export_resource_pack_to_html, Callable)
    assert isinstance(app.main.college_algebra_template, Callable)
    assert app.main.TOPIC_OPTIONS == supported_topic_labels()
    assert app.main.GENERATION_PRESET_OPTIONS == generation_preset_labels()


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

    test_app.selectbox[1].set_value("Quadratic equations by factoring").run()
    test_app.button[0].click().run()

    assert not test_app.exception
    assert test_app.text_input[0].value == "quadratic"
    assert "Quadratic equations by factoring Worksheet" in test_app.text_area[0].value
    assert "Solve by factoring" in test_app.text_area[0].value
    assert "Download Worksheet Markdown" in _download_labels(test_app)
    assert "Download Worksheet HTML" in _download_labels(test_app)


def test_topic_mode_generates_systems_of_equations_worksheet() -> None:
    test_app = _run_app()

    test_app.selectbox[1].set_value("Systems of linear equations").run()
    test_app.button[0].click().run()

    assert not test_app.exception
    assert test_app.text_input[0].value == "systems"
    assert "Systems of linear equations Worksheet" in test_app.text_area[0].value
    assert "Solve the system of equations" in test_app.text_area[0].value
    assert "Download Worksheet Markdown" in _download_labels(test_app)
    assert "Download Worksheet HTML" in _download_labels(test_app)


def test_topic_mode_generates_factoring_techniques_worksheet() -> None:
    test_app = _run_app()

    test_app.selectbox[1].set_value("Factoring techniques").run()
    test_app.button[0].click().run()

    assert not test_app.exception
    assert test_app.text_input[0].value == "factoring"
    assert "Factoring techniques Worksheet" in test_app.text_area[0].value
    assert "Factor completely" in test_app.text_area[0].value
    assert "Download Worksheet Markdown" in _download_labels(test_app)
    assert "Download Worksheet HTML" in _download_labels(test_app)


def test_topic_mode_generates_functions_basics_worksheet() -> None:
    test_app = _run_app()

    test_app.selectbox[1].set_value("Functions basics").run()
    test_app.button[0].click().run()

    assert not test_app.exception
    assert test_app.text_input[0].value == "functions"
    assert "Functions basics Worksheet" in test_app.text_area[0].value
    assert "evaluate f" in test_app.text_area[0].value
    assert "Download Worksheet Markdown" in _download_labels(test_app)
    assert "Download Worksheet HTML" in _download_labels(test_app)


def test_learning_objective_mode_exposes_college_algebra_objectives() -> None:
    test_app = _run_app()

    test_app.radio[1].set_value("Learning Objective mode").run()

    assert not test_app.exception
    assert test_app.selectbox[1].label == "Course"
    assert test_app.selectbox[1].value == "College Algebra"
    assert test_app.selectbox[2].label == "Module"
    assert "Linear Equations" in test_app.selectbox[2].options
    assert "Quadratic Equations" in test_app.selectbox[2].options
    assert "Systems of Equations" in test_app.selectbox[2].options
    assert "Factoring Techniques" in test_app.selectbox[2].options
    assert "Functions" in test_app.selectbox[2].options
    assert test_app.selectbox[3].label == "Learning Objective"
    assert "Solve linear equations in one variable" in test_app.selectbox[3].options
    assert any(
        "Selected learning objective: Solve linear equations in one variable"
        in caption.value
        for caption in test_app.caption
    )


def test_learning_objective_mode_exposes_quadratic_objective() -> None:
    test_app = _run_app()

    test_app.radio[1].set_value("Learning Objective mode").run()
    test_app.selectbox[2].set_value("Quadratic Equations").run()

    assert not test_app.exception
    assert test_app.selectbox[3].options == [
        "Solve quadratic equations by factoring",
    ]
    assert test_app.text_input[0].value == "quadratic"


def test_learning_objective_mode_exposes_systems_objective() -> None:
    test_app = _run_app()

    test_app.radio[1].set_value("Learning Objective mode").run()
    test_app.selectbox[2].set_value("Systems of Equations").run()

    assert not test_app.exception
    assert test_app.selectbox[3].options == [
        "Solve systems of linear equations in two variables",
    ]
    assert test_app.text_input[0].value == "systems"


def test_learning_objective_mode_exposes_factoring_objective() -> None:
    test_app = _run_app()

    test_app.radio[1].set_value("Learning Objective mode").run()
    test_app.selectbox[2].set_value("Factoring Techniques").run()

    assert not test_app.exception
    assert test_app.selectbox[3].options == [
        "Factor polynomial expressions using common factoring strategies",
    ]
    assert test_app.text_input[0].value == "factoring"


def test_learning_objective_mode_exposes_functions_objective() -> None:
    test_app = _run_app()

    test_app.radio[1].set_value("Learning Objective mode").run()
    test_app.selectbox[2].set_value("Functions").run()

    assert not test_app.exception
    assert test_app.selectbox[3].options == [
        "Evaluate and interpret functions using function notation",
    ]
    assert test_app.text_input[0].value == "functions"


def test_worksheet_only_ui_exposes_worksheet_exports() -> None:
    test_app = _run_app()

    test_app.button[0].click().run()

    assert not test_app.exception
    assert _download_labels(test_app) == [
        "Download Worksheet Markdown",
        "Download Worksheet HTML",
        "Download Worksheet Export Bundle",
    ]
    assert test_app.text_area[0].label == "Markdown"
    assert test_app.text_area[1].label == "HTML"


def test_generation_preset_selector_exposes_built_in_presets() -> None:
    test_app = _run_app()

    assert test_app.selectbox[0].label == "Generation preset"
    assert test_app.selectbox[0].options == [
        "Quick Worksheet",
        "Standard Practice Set",
        "Full Tutor Resource Pack",
    ]
    assert test_app.selectbox[0].value == "Quick Worksheet"
    assert any(
        "Presets choose sensible starting defaults only" in selectbox.help
        for selectbox in test_app.selectbox
        if selectbox.label == "Generation preset"
    )


def test_standard_practice_set_preset_applies_editable_defaults() -> None:
    test_app = _run_app()

    test_app.selectbox[0].set_value("Standard Practice Set").run()

    assert not test_app.exception
    assert test_app.radio[0].value == "Worksheet only"
    assert test_app.radio[1].value == "Topic mode"
    assert test_app.selectbox[1].value == "Linear equations"
    assert test_app.selectbox[2].value == "Easy"
    assert test_app.number_input[0].value == 10

    test_app.number_input[0].set_value(7).run()

    assert not test_app.exception
    assert test_app.number_input[0].value == 7


def test_full_tutor_resource_pack_preset_generates_resource_pack() -> None:
    test_app = _run_app()

    test_app.selectbox[0].set_value("Full Tutor Resource Pack").run()
    test_app.button[0].click().run()

    assert not test_app.exception
    assert test_app.radio[0].value == "Full Resource Pack"
    assert test_app.number_input[0].value == 5
    assert "Study Guide" in _tab_labels(test_app)
    assert "Download Resource Pack Export Bundle" in _download_labels(test_app)


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
        "Practice Quiz",
        "Exports",
    ]
    assert _download_labels(test_app) == [
        "Download Resource Pack Markdown",
        "Download Resource Pack HTML",
        "Download Resource Pack Export Bundle",
    ]
    assert test_app.text_area[0].label == "Resource Pack Markdown"
    assert test_app.text_area[1].label == "Resource Pack HTML"
    assert "## Study Guide" in test_app.text_area[0].value
    assert "## Practice Quiz" in test_app.text_area[0].value
    assert "mathforge-resource-pack" in test_app.text_area[1].value
    assert "mathforge-practice-quiz" in test_app.text_area[1].value


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
