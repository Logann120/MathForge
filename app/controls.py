"""Input controls and app routing helpers for the MathForge Streamlit app."""

from __future__ import annotations

from typing import Any

from app.generation_context import LearningObjectiveSelection
from app.presets import generation_preset_labels
from app.rendering import render_learning_objective_context_summary
from models.content_models import Worksheet
from models.curriculum import CourseModule, CourseTemplate, LearningObjective
from models.resource_pack import ResourcePack
from topics.registry import (
    find_topic_by_label,
    find_topic_by_learning_objective_topic,
    supported_topic_labels,
)

OUTPUT_TYPE_OPTIONS = ("Worksheet only", "Full Resource Pack")
GENERATION_MODE_OPTIONS = ("Topic mode", "Learning Objective mode")
TOPIC_OPTIONS = supported_topic_labels()
DIFFICULTY_OPTIONS = ("Easy",)
GENERATION_PRESET_OPTIONS = generation_preset_labels()


def generate_worksheet_for_topic(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate a worksheet for a supported topic."""
    topic_record = find_topic_by_label(topic)
    return topic_record.worksheet_generator(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )


def generate_resource_pack_for_topic(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a resource pack for a supported topic."""
    topic_record = find_topic_by_label(topic)
    return topic_record.resource_pack_generator(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )


def default_problem_id_prefix(topic: str) -> str:
    """Return a stable problem ID prefix for a supported topic."""
    try:
        return find_topic_by_label(topic).default_problem_id_prefix
    except ValueError:
        return "linear"


def topic_key(topic: str) -> str:
    """Return a widget-safe topic key."""
    return default_problem_id_prefix(topic)


def difficulty_value(label: str) -> str:
    """Map a user-facing difficulty label to the generator input value."""
    if label == "Easy":
        return "easy"
    raise ValueError(f"unsupported difficulty: {label}")


def option_index(options: tuple[str, ...], value: str) -> int:
    """Return the index for a default option value."""
    try:
        return options.index(value)
    except ValueError:
        return 0


def widget_key(value: str) -> str:
    """Return a stable widget-key fragment."""
    return "".join(
        character.lower() if character.isalnum() else "_"
        for character in value.strip()
    ).strip("_")


def select_learning_objective(
    st: Any,
    course_template: CourseTemplate,
    *,
    output_type: str,
) -> LearningObjectiveSelection:
    """Render curriculum selectors and return selected learning-objective context."""
    st.selectbox("Course", options=(course_template.title,))
    selected_module_title = st.selectbox(
        "Module",
        options=tuple(module.title for module in course_template.modules),
    )
    selected_module = find_module(course_template, selected_module_title)
    selected_objective_description = st.selectbox(
        "Learning Objective",
        options=tuple(
            objective.description
            for objective in selected_module.learning_objectives
        ),
    )
    learning_objective = find_learning_objective(
        selected_module,
        selected_objective_description,
    )
    selection = LearningObjectiveSelection(
        course_title=course_template.title,
        module_title=selected_module.title,
        learning_objective=learning_objective,
        mapped_topic=mapped_topic_label(learning_objective),
    )
    st.caption(f"Selected learning objective: {learning_objective.description}")
    render_learning_objective_context_summary(st, selection, output_type)
    return selection


def find_module(course_template: CourseTemplate, title: str) -> CourseModule:
    """Find a course module by title."""
    for module in course_template.modules:
        if module.title == title:
            return module
    raise ValueError(f"unknown course module: {title}")


def find_learning_objective(
    course_module: CourseModule,
    description: str,
) -> LearningObjective:
    """Find a learning objective by description."""
    for objective in course_module.learning_objectives:
        if objective.description == description:
            return objective
    raise ValueError(f"unknown learning objective: {description}")


def mapped_topic_label(learning_objective: LearningObjective) -> str:
    """Return the registry topic label mapped to a learning objective."""
    try:
        return find_topic_by_learning_objective_topic(
            learning_objective.topic
        ).display_label
    except ValueError:
        return "Not mapped"
