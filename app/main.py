"""Minimal Streamlit interface for MathForge instructional content generation."""

from __future__ import annotations

import logging

from app.controls import (
    GENERATION_MODE_OPTIONS,
    GENERATION_PRESET_OPTIONS,
    OUTPUT_TYPE_OPTIONS,
    TOPIC_OPTIONS,
    default_problem_id_prefix,
    difficulty_labels_for_topic,
    difficulty_value,
    generate_resource_pack_for_topic,
    generate_worksheet_for_topic,
    option_index,
    select_learning_objective,
    topic_key,
    widget_key,
)
from app.generation_context import GenerationContext
from app.presets import find_generation_preset
from app.rendering import render_resource_pack, render_worksheet
from exporters.canvas_exporter import (
    export_resource_pack_quiz_to_canvas_csv,
    export_worksheet_to_canvas_csv,
)
from exporters.html_exporter import export_resource_pack_to_html
from exporters.libguides_html_exporter import (
    export_resource_pack_to_libguides_html,
    export_worksheet_to_libguides_html,
)
from exporters.markdown_exporter import export_resource_pack_to_markdown
from generator.curriculum_resource_pack_generator import (
    generate_resource_pack_from_learning_objective,
)
from generator.resource_pack_generator import (
    generate_factoring_techniques_resource_pack,
    generate_functions_basics_resource_pack,
    generate_linear_equation_resource_pack,
    generate_quadratic_factoring_resource_pack,
    generate_systems_of_equations_resource_pack,
)
from models.curriculum import LearningObjective
from templates.course_templates import college_algebra_template


LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Run the MathForge Streamlit application."""
    import streamlit as st

    st.set_page_config(page_title="MathForge", page_icon="M")
    st.title("MathForge")
    st.subheader(
        "Generate curriculum-aligned math worksheets and instructional resource packs."
    )
    st.caption(
        "MathForge currently supports deterministic generation for linear equations, "
        "quadratic equations by factoring, systems of linear equations, and "
        "factoring techniques, and functions basics."
    )

    preset_label = st.selectbox(
        "Generation preset",
        options=GENERATION_PRESET_OPTIONS,
        help=(
            "Presets choose sensible starting defaults only. You can still edit "
            "the output type, generation mode, topic or objective, difficulty, "
            "problem count, and problem ID prefix before generating."
        ),
    )
    preset = find_generation_preset(preset_label)
    preset_key = widget_key(preset.label)
    st.caption(f"Preset: {preset.description}")

    output_type = st.radio(
        "Output type",
        options=OUTPUT_TYPE_OPTIONS,
        index=option_index(OUTPUT_TYPE_OPTIONS, preset.output_type),
        horizontal=True,
        help=(
            "Worksheet only = problems, solution key, Markdown export, HTML export. "
            "Full Resource Pack = worksheet, solution key, study guide, common "
            "mistakes, tutor notes, Markdown export, HTML export."
        ),
        key=f"output_type_{preset_key}",
    )
    generation_mode = st.radio(
        "Generation mode",
        options=GENERATION_MODE_OPTIONS,
        index=option_index(GENERATION_MODE_OPTIONS, preset.generation_mode),
        horizontal=True,
        help=(
            "Topic mode generates from a selected math topic. Learning Objective "
            "mode generates from the College Algebra course template."
        ),
        key=f"generation_mode_{preset_key}",
    )

    learning_objective: LearningObjective | None = None
    generation_context: GenerationContext
    difficulty_topic: str
    if generation_mode == "Learning Objective mode":
        learning_selection = select_learning_objective(
            st,
            college_algebra_template(),
            output_type=output_type,
        )
        learning_objective = learning_selection.learning_objective
        topic = learning_objective.topic
        difficulty_topic = learning_selection.mapped_topic
        generation_context = GenerationContext.from_learning_objective_selection(
            learning_selection
        )
    else:
        topic = st.selectbox(
            "Topic",
            options=TOPIC_OPTIONS,
            index=option_index(TOPIC_OPTIONS, preset.topic_label),
            key=f"topic_{preset_key}",
        )
        difficulty_topic = topic
        generation_context = GenerationContext.topic_mode(topic)

    difficulty_options = difficulty_labels_for_topic(difficulty_topic)
    difficulty_label = st.selectbox(
        "Difficulty",
        options=difficulty_options,
        index=option_index(difficulty_options, preset.difficulty_label),
        key=f"difficulty_{preset_key}_{topic_key(difficulty_topic)}",
    )
    st.caption("Additional difficulty levels are planned.")
    count = st.number_input(
        "Problem count",
        min_value=1,
        max_value=25,
        value=preset.problem_count,
        step=1,
        help="Number of practice problems to generate.",
        key=f"problem_count_{preset_key}",
    )

    with st.expander("Advanced options"):
        start_id = st.text_input(
            "Problem ID prefix",
            value=default_problem_id_prefix(topic),
            help="Used internally to match problems with solutions.",
            key=f"problem_id_prefix_{topic_key(topic)}",
        )

    if st.button("Generate", type="primary"):
        try:
            difficulty = difficulty_value(difficulty_label)
            if output_type == "Full Resource Pack":
                if learning_objective is not None:
                    resource_pack = generate_resource_pack_from_learning_objective(
                        learning_objective=learning_objective,
                        difficulty=difficulty,
                        count=int(count),
                        start_id=start_id,
                    )
                else:
                    resource_pack = generate_resource_pack_for_topic(
                        topic=topic,
                        difficulty=difficulty,
                        count=int(count),
                        start_id=start_id,
                    )
                render_resource_pack(st, resource_pack, generation_context)
                return

            worksheet = generate_worksheet_for_topic(
                topic=topic,
                difficulty=difficulty,
                count=int(count),
                start_id=start_id,
            )
            render_worksheet(st, worksheet, generation_context)
        except (TypeError, ValueError) as exc:
            LOGGER.warning("MathForge generation failed: %s", exc)
            st.error(
                "MathForge could not generate this material. Please review the "
                "selected options and try again."
            )
            return


if __name__ == "__main__":
    main()
