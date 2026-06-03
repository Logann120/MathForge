"""Unit tests for pure Streamlit app helper behavior."""

import pytest

from app.controls import (
    DIFFICULTY_OPTIONS,
    GENERATION_MODE_OPTIONS,
    GENERATION_PRESET_OPTIONS,
    OUTPUT_TYPE_OPTIONS,
    TOPIC_OPTIONS,
    default_problem_id_prefix,
    difficulty_value,
    find_learning_objective,
    find_module,
    generate_resource_pack_for_topic,
    generate_worksheet_for_topic,
    mapped_topic_label,
    option_index,
    topic_key,
    widget_key,
)
from app.generation_context import (
    GenerationContext,
    LearningObjectiveSelection,
    WorksheetSummary,
    generated_output_summary_lines,
)
from app.presets import generation_preset_labels
from models.content_models import ExportResult, Worksheet
from models.curriculum import CourseModule, LearningObjective
from models.resource_pack import ResourcePack
from templates.course_templates import college_algebra_template
from topics.registry import supported_topic_labels


def test_app_option_constants_match_current_supported_metadata() -> None:
    assert OUTPUT_TYPE_OPTIONS == ("Worksheet only", "Full Resource Pack")
    assert GENERATION_MODE_OPTIONS == ("Topic mode", "Learning Objective mode")
    assert TOPIC_OPTIONS == supported_topic_labels()
    assert DIFFICULTY_OPTIONS == ("Easy",)
    assert GENERATION_PRESET_OPTIONS == generation_preset_labels()


def test_difficulty_value_maps_user_label_to_generator_value() -> None:
    assert difficulty_value("Easy") == "easy"

    with pytest.raises(ValueError, match="unsupported difficulty"):
        difficulty_value("Medium")


def test_option_index_returns_matching_index_or_first_option() -> None:
    options = ("First", "Second", "Third")

    assert option_index(options, "Second") == 1
    assert option_index(options, "Missing") == 0


def test_widget_key_normalizes_display_text_for_streamlit_keys() -> None:
    assert widget_key("Full Tutor Resource Pack") == "full_tutor_resource_pack"
    assert widget_key("  A/B: Test!  ") == "a_b__test"


def test_default_problem_id_prefix_uses_registry_with_fallback() -> None:
    assert default_problem_id_prefix("Quadratic equations by factoring") == "quadratic"
    assert default_problem_id_prefix("Not a supported topic") == "linear"
    assert topic_key("Systems of linear equations") == "systems"


def test_topic_generation_helpers_route_through_supported_topic_registry() -> None:
    worksheet = generate_worksheet_for_topic(
        topic="Functions basics",
        difficulty="easy",
        count=1,
        start_id="functions",
    )
    resource_pack = generate_resource_pack_for_topic(
        topic="Functions basics",
        difficulty="easy",
        count=1,
        start_id="functions",
    )

    assert isinstance(worksheet, Worksheet)
    assert worksheet.title == "Functions basics Worksheet"
    assert isinstance(resource_pack, ResourcePack)
    assert resource_pack.worksheet == worksheet


def test_curriculum_lookup_helpers_find_module_and_objective() -> None:
    course_template = college_algebra_template()

    module = find_module(course_template, "Factoring Techniques")
    objective = find_learning_objective(
        module,
        "Factor polynomial expressions using common factoring strategies",
    )

    assert isinstance(module, CourseModule)
    assert module.title == "Factoring Techniques"
    assert isinstance(objective, LearningObjective)
    assert objective.topic == "Factoring techniques"


def test_curriculum_lookup_helpers_reject_unknown_values() -> None:
    course_template = college_algebra_template()
    module = find_module(course_template, "Linear Equations")

    with pytest.raises(ValueError, match="unknown course module"):
        find_module(course_template, "Missing Module")

    with pytest.raises(ValueError, match="unknown learning objective"):
        find_learning_objective(module, "Missing objective")


def test_mapped_topic_label_uses_exact_registry_routing() -> None:
    objective = LearningObjective(
        objective_id="objective-1",
        description="Solve supported topic",
        topic="quadratic equations by factoring",
    )
    unsupported_objective = LearningObjective(
        objective_id="objective-2",
        description="Solve unsupported topic",
        topic="quadratic formula",
    )

    assert mapped_topic_label(objective) == "Quadratic equations by factoring"
    assert mapped_topic_label(unsupported_objective) == "Not mapped"


def test_generation_context_for_topic_mode() -> None:
    context = GenerationContext.topic_mode("Linear equations")

    assert context.mode == "Topic mode"
    assert context.topic == "Linear equations"
    assert context.course_title == ""


def test_generation_context_from_learning_objective_selection() -> None:
    objective = LearningObjective(
        objective_id="linear-001",
        description="Solve linear equations in one variable",
        topic="Linear equations",
    )
    selection = LearningObjectiveSelection(
        course_title="College Algebra",
        module_title="Linear Equations",
        learning_objective=objective,
        mapped_topic="Linear equations",
    )

    context = GenerationContext.from_learning_objective_selection(selection)

    assert context.mode == "Learning Objective mode"
    assert context.course_title == "College Algebra"
    assert context.module_title == "Linear Equations"
    assert context.learning_objective == "Solve linear equations in one variable"
    assert context.mapped_topic == "Linear equations"


def test_worksheet_summary_from_export_uses_metadata() -> None:
    export = ExportResult(
        content="export content",
        format_name="markdown",
        filename="worksheet.md",
        metadata={
            "topic": "Linear equations",
            "difficulty": "easy",
            "problem_count": "5",
            "problem_id_prefix": "linear",
        },
    )

    summary = WorksheetSummary.from_export(export)

    assert summary.context == "Linear equations"
    assert summary.difficulty == "easy"
    assert summary.problem_count == 5
    assert summary.problem_id_prefix == "linear"


def test_worksheet_summary_from_export_handles_missing_or_invalid_metadata() -> None:
    export = ExportResult(
        content="export content",
        format_name="html",
        filename="worksheet.html",
        metadata={
            "worksheet_id": "fallback-worksheet",
            "problem_count": "not-a-number",
        },
    )

    summary = WorksheetSummary.from_export(export)

    assert summary.context == "fallback-worksheet"
    assert summary.difficulty == "Not specified"
    assert summary.problem_count == 0
    assert summary.problem_id_prefix == "fallback-worksheet"


def test_generated_output_summary_lines_for_topic_mode_include_downloads() -> None:
    lines = generated_output_summary_lines(
        output_type="Worksheet",
        worksheet=WorksheetSummary(
            context="Linear equations",
            difficulty="easy",
            problem_count=3,
            problem_id_prefix="linear",
        ),
        generation_context=GenerationContext.topic_mode("Linear equations"),
        markdown_filename="worksheet.md",
        html_filename="worksheet.html",
        libguides_html_filename="worksheet-libguides.html",
        bundle_filename="worksheet.zip",
        canvas_filename="worksheet.csv",
    )

    assert "- **Output type:** Worksheet" in lines
    assert "- **Generation mode:** Topic mode" in lines
    assert "- **Topic:** Linear equations" in lines
    assert "  - LibGuides-safe HTML: `worksheet-libguides.html`" in lines
    assert "  - Canvas manual-entry CSV: `worksheet.csv`" in lines
    assert (
        "- **Available downloads:** Markdown, HTML, LibGuides-safe HTML, "
        "ZIP bundle, Canvas manual-entry CSV"
        in lines
    )


def test_generated_output_summary_lines_for_learning_objective_mode() -> None:
    context = GenerationContext(
        mode="Learning Objective mode",
        course_title="College Algebra",
        module_title="Linear Equations",
        learning_objective="Solve linear equations in one variable",
        mapped_topic="Linear equations",
    )

    lines = generated_output_summary_lines(
        output_type="Full Resource Pack",
        worksheet=WorksheetSummary(
            context="Solve linear equations in one variable",
            difficulty="easy",
            problem_count=5,
            problem_id_prefix="linear",
        ),
        generation_context=context,
        markdown_filename="resource-pack.md",
        html_filename="resource-pack.html",
        bundle_filename="resource-pack.zip",
    )

    assert "- **Output type:** Full Resource Pack" in lines
    assert "- **Generation mode:** Learning Objective mode" in lines
    assert "- **Course:** College Algebra" in lines
    assert "- **Module:** Linear Equations" in lines
    assert "- **Learning objective:** Solve linear equations in one variable" in lines
    assert "- **Mapped topic:** Linear equations" in lines
    assert "- **Available downloads:** Markdown, HTML, ZIP bundle" in lines
