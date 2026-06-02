"""Minimal Streamlit interface for MathForge instructional content generation."""

from __future__ import annotations

import logging
from typing import Any

from exporters.html_exporter import export_resource_pack_to_html, export_worksheet_to_html
from exporters.markdown_exporter import (
    export_resource_pack_to_markdown,
    export_worksheet_to_markdown,
)
from generator.curriculum_resource_pack_generator import (
    generate_resource_pack_from_learning_objective,
)
from generator.problem_generator import generate_linear_equation_worksheet
from generator.problem_generator import generate_quadratic_factoring_worksheet
from generator.resource_pack_generator import (
    generate_linear_equation_resource_pack,
    generate_quadratic_factoring_resource_pack,
)
from models.curriculum import CourseModule, CourseTemplate, LearningObjective
from models.content_models import ExportResult, Solution, Worksheet
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes
from templates.course_templates import college_algebra_template


LOGGER = logging.getLogger(__name__)

TOPIC_OPTIONS = (
    "Linear equations",
    "Quadratic equations by factoring",
)
DIFFICULTY_OPTIONS = ("Easy",)

_TOPIC_PREFIXES = {
    "Linear equations": "linear",
    "Quadratic equations by factoring": "quadratic",
}


def main() -> None:
    """Run the MathForge Streamlit application."""
    import streamlit as st

    st.set_page_config(page_title="MathForge", page_icon="M")
    st.title("MathForge")
    st.subheader(
        "Generate curriculum-aligned math worksheets and instructional resource packs."
    )
    st.caption(
        "MathForge currently supports deterministic generation for linear equations "
        "and quadratic equations by factoring."
    )

    output_type = st.radio(
        "Output type",
        options=("Worksheet only", "Full Resource Pack"),
        horizontal=True,
        help=(
            "Worksheet only = problems, solution key, Markdown export, HTML export. "
            "Full Resource Pack = worksheet, solution key, study guide, common "
            "mistakes, tutor notes, Markdown export, HTML export."
        ),
    )
    generation_mode = st.radio(
        "Generation mode",
        options=("Topic mode", "Learning Objective mode"),
        horizontal=True,
        help=(
            "Topic mode generates from a selected math topic. Learning Objective "
            "mode generates from the College Algebra course template."
        ),
    )

    learning_objective: LearningObjective | None = None
    if generation_mode == "Learning Objective mode":
        learning_objective = _select_learning_objective(st, college_algebra_template())
        topic = learning_objective.topic
    else:
        topic = st.selectbox("Topic", options=TOPIC_OPTIONS)

    difficulty_label = st.selectbox("Difficulty", options=DIFFICULTY_OPTIONS)
    st.caption("Additional difficulty levels are planned.")
    count = st.number_input(
        "Problem count",
        min_value=1,
        max_value=25,
        value=5,
        step=1,
        help="Number of practice problems to generate.",
    )

    with st.expander("Advanced options"):
        start_id = st.text_input(
            "Problem ID prefix",
            value=_default_problem_id_prefix(topic),
            help="Used internally to match problems with solutions.",
            key=f"problem_id_prefix_{_topic_key(topic)}",
        )

    if st.button("Generate", type="primary"):
        try:
            difficulty = _difficulty_value(difficulty_label)
            if output_type == "Full Resource Pack":
                if learning_objective is not None:
                    resource_pack = generate_resource_pack_from_learning_objective(
                        learning_objective=learning_objective,
                        difficulty=difficulty,
                        count=int(count),
                        start_id=start_id,
                    )
                else:
                    resource_pack = _generate_resource_pack_for_topic(
                        topic=topic,
                        difficulty=difficulty,
                        count=int(count),
                        start_id=start_id,
                    )
                _render_resource_pack(st, resource_pack)
                return

            worksheet = _generate_worksheet_for_topic(
                topic=topic,
                difficulty=difficulty,
                count=int(count),
                start_id=start_id,
            )
            _render_worksheet(st, worksheet)
        except (TypeError, ValueError) as exc:
            LOGGER.warning("MathForge generation failed: %s", exc)
            st.error(
                "MathForge could not generate this material. Please review the "
                "selected options and try again."
            )
            return


def _generate_worksheet_for_topic(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate a worksheet for a supported topic."""
    if topic == "Linear equations":
        return generate_linear_equation_worksheet(
            topic=topic,
            difficulty=difficulty,
            count=count,
            start_id=start_id,
        )

    if _is_quadratic_factoring_topic(topic):
        return generate_quadratic_factoring_worksheet(
            topic=topic,
            difficulty=difficulty,
            count=count,
            start_id=start_id,
        )

    raise ValueError(f"unsupported topic: {topic}")


def _generate_resource_pack_for_topic(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a resource pack for a supported topic."""
    if topic == "Linear equations":
        return generate_linear_equation_resource_pack(
            topic=topic,
            difficulty=difficulty,
            count=count,
            start_id=start_id,
        )

    if _is_quadratic_factoring_topic(topic):
        return generate_quadratic_factoring_resource_pack(
            topic=topic,
            difficulty=difficulty,
            count=count,
            start_id=start_id,
        )

    raise ValueError(f"unsupported topic: {topic}")


def _is_quadratic_factoring_topic(topic: str) -> bool:
    """Return whether the selected topic is quadratic factoring."""
    return topic.strip().lower() == "quadratic equations by factoring"


def _default_problem_id_prefix(topic: str) -> str:
    """Return a stable problem ID prefix for a supported topic."""
    return _TOPIC_PREFIXES.get(topic, "linear")


def _topic_key(topic: str) -> str:
    """Return a widget-safe topic key."""
    return _default_problem_id_prefix(topic)


def _difficulty_value(label: str) -> str:
    """Map a user-facing difficulty label to the generator input value."""
    if label == "Easy":
        return "easy"
    raise ValueError(f"unsupported difficulty: {label}")


def _select_learning_objective(
    st: Any,
    course_template: CourseTemplate,
) -> LearningObjective:
    """Render curriculum selectors and return the selected learning objective."""
    st.selectbox("Course", options=(course_template.title,))
    selected_module_title = st.selectbox(
        "Module",
        options=tuple(module.title for module in course_template.modules),
    )
    selected_module = _find_module(course_template, selected_module_title)
    selected_objective_description = st.selectbox(
        "Learning Objective",
        options=tuple(
            objective.description
            for objective in selected_module.learning_objectives
        ),
    )
    learning_objective = _find_learning_objective(
        selected_module,
        selected_objective_description,
    )
    st.caption(f"Selected learning objective: {learning_objective.description}")
    return learning_objective


def _find_module(course_template: CourseTemplate, title: str) -> CourseModule:
    """Find a course module by title."""
    for module in course_template.modules:
        if module.title == title:
            return module
    raise ValueError(f"unknown course module: {title}")


def _find_learning_objective(
    course_module: CourseModule,
    description: str,
) -> LearningObjective:
    """Find a learning objective by description."""
    for objective in course_module.learning_objectives:
        if objective.description == description:
            return objective
    raise ValueError(f"unknown learning objective: {description}")


def _render_worksheet(st: Any, worksheet: Worksheet) -> None:
    """Render previews and exports for a generated worksheet."""
    markdown_export = export_worksheet_to_markdown(worksheet, include_solutions=True)
    html_export = export_worksheet_to_html(worksheet, include_solutions=True)

    worksheet_tab, solution_tab, exports_tab = st.tabs(
        ("Worksheet", "Solution Key", "Exports")
    )

    with worksheet_tab:
        _render_worksheet_preview(st, worksheet)
    with solution_tab:
        _render_solution_key_preview(st, worksheet)
    with exports_tab:
        _render_worksheet_exports(st, markdown_export, html_export)


def _render_worksheet_exports(
    st: Any,
    markdown_export: ExportResult,
    html_export: ExportResult,
) -> None:
    """Render worksheet export controls."""
    st.header("Exports")
    st.download_button(
        label="Download Worksheet Markdown",
        data=markdown_export.content,
        file_name=markdown_export.filename,
        mime="text/markdown",
    )
    st.download_button(
        label="Download Worksheet HTML",
        data=html_export.content,
        file_name=html_export.filename,
        mime="text/html",
    )

    with st.expander("Markdown export text"):
        st.text_area(
            "Markdown",
            value=markdown_export.content,
            height=260,
            label_visibility="collapsed",
        )

    with st.expander("HTML export text"):
        st.text_area(
            "HTML",
            value=html_export.content,
            height=260,
            label_visibility="collapsed",
        )


def _render_resource_pack(st: Any, resource_pack: ResourcePack) -> None:
    """Render previews and Markdown export for a full resource pack."""
    markdown_export = export_resource_pack_to_markdown(
        resource_pack,
        include_solutions=True,
    )
    html_export = export_resource_pack_to_html(
        resource_pack,
        include_solutions=True,
    )

    (
        worksheet_tab,
        solution_tab,
        study_guide_tab,
        common_mistakes_tab,
        tutor_notes_tab,
        exports_tab,
    ) = st.tabs(
        (
            "Worksheet",
            "Solution Key",
            "Study Guide",
            "Common Mistakes",
            "Tutor Notes",
            "Exports",
        )
    )

    with worksheet_tab:
        _render_worksheet_preview(st, resource_pack.worksheet)
    with solution_tab:
        _render_solution_key_preview(st, resource_pack.worksheet)
    with study_guide_tab:
        st.header("Study Guide")
        _render_study_guide(st, resource_pack.study_guide)
    with common_mistakes_tab:
        st.header("Common Mistakes")
        _render_common_mistakes(st, resource_pack.common_mistakes)
    with tutor_notes_tab:
        st.header("Tutor Notes")
        _render_tutor_notes(st, resource_pack.tutor_notes)
    with exports_tab:
        _render_resource_pack_exports(st, markdown_export, html_export)


def _render_resource_pack_exports(
    st: Any,
    markdown_export: ExportResult,
    html_export: ExportResult,
) -> None:
    """Render resource pack export controls."""
    st.header("Resource Pack Export")
    st.download_button(
        label="Download Resource Pack Markdown",
        data=markdown_export.content,
        file_name=markdown_export.filename,
        mime="text/markdown",
    )
    st.download_button(
        label="Download Resource Pack HTML",
        data=html_export.content,
        file_name=html_export.filename,
        mime="text/html",
    )

    with st.expander("Resource pack Markdown export text"):
        st.text_area(
            "Resource Pack Markdown",
            value=markdown_export.content,
            height=320,
            label_visibility="collapsed",
        )

    with st.expander("Resource pack HTML export text"):
        st.text_area(
            "Resource Pack HTML",
            value=html_export.content,
            height=320,
            label_visibility="collapsed",
        )


def _render_worksheet_preview(st: Any, worksheet: Worksheet) -> None:
    """Render the worksheet problem preview."""
    st.header("Worksheet")
    st.write(worksheet.instructions)

    for index, problem in enumerate(worksheet.problems, start=1):
        st.write(f"{index}. {problem.prompt}")


def _render_solution_key_preview(st: Any, worksheet: Worksheet) -> None:
    """Render the solution key preview."""
    st.header("Solution Key")
    solutions_by_problem_id = {
        solution.problem_id: solution for solution in worksheet.solutions
    }

    for index, problem in enumerate(worksheet.problems, start=1):
        solution = solutions_by_problem_id.get(problem.problem_id)
        if solution is None:
            st.write(f"{index}. No solution provided.")
            continue
        _render_solution(st, index, solution)


def _render_solution(st: Any, index: int, solution: Solution) -> None:
    """Render one solution preview entry."""
    st.write(f"{index}. Answer: {solution.final_answer}")
    for step in solution.steps:
        st.write(f"   - {step}")


def _render_study_guide(st: Any, study_guide: StudyGuide) -> None:
    """Render study guide content."""
    st.subheader(study_guide.title)
    st.write(study_guide.overview)
    _render_bullets(st, "Key Ideas", study_guide.key_points)
    _render_bullets(st, "Worked-Example Guidance", study_guide.practice_tips)


def _render_common_mistakes(st: Any, common_mistakes: CommonMistakes) -> None:
    """Render common mistakes content."""
    _render_bullets(st, "Mistakes to Watch For", common_mistakes.mistakes)
    _render_bullets(
        st,
        "Corrections and Interventions",
        common_mistakes.corrections,
    )


def _render_tutor_notes(st: Any, tutor_notes: TutorNotes) -> None:
    """Render tutor-facing notes."""
    _render_bullets(st, "Notes", tutor_notes.notes)
    _render_bullets(st, "Discussion Prompts", tutor_notes.discussion_prompts)


def _render_bullets(st: Any, label: str, items: tuple[str, ...]) -> None:
    """Render a labeled list of text items."""
    if not items:
        return

    st.subheader(label)
    for item in items:
        st.write(f"- {item}")


if __name__ == "__main__":
    main()
