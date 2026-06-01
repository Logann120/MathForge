"""Minimal Streamlit interface for MathForge instructional content generation."""

from __future__ import annotations

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
from generator.resource_pack_generator import generate_linear_equation_resource_pack
from models.curriculum import CourseModule, CourseTemplate, LearningObjective
from models.content_models import Solution, Worksheet
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes
from templates.course_templates import college_algebra_template


def main() -> None:
    """Run the MathForge Streamlit application."""
    import streamlit as st

    st.set_page_config(page_title="MathForge", page_icon="M")
    st.title("MathForge")
    st.subheader("Linear equation worksheet generator")

    output_type = st.radio(
        "Output type",
        options=("Worksheet only", "Full Resource Pack"),
        horizontal=True,
    )
    generation_mode = st.radio(
        "Generation mode",
        options=("Topic mode", "Learning Objective mode"),
        horizontal=True,
    )

    learning_objective: LearningObjective | None = None
    if generation_mode == "Learning Objective mode":
        learning_objective = _select_learning_objective(st, college_algebra_template())
        topic = learning_objective.topic
    else:
        topic = st.text_input("Topic", value="Linear equations")

    difficulty = st.text_input("Difficulty", value="easy")
    count = st.number_input("Problem count", min_value=1, max_value=50, value=5, step=1)
    start_id = st.text_input("Start ID", value="linear")

    if st.button("Generate", type="primary"):
        try:
            if output_type == "Full Resource Pack":
                if learning_objective is not None:
                    resource_pack = generate_resource_pack_from_learning_objective(
                        learning_objective=learning_objective,
                        difficulty=difficulty,
                        count=int(count),
                        start_id=start_id,
                    )
                else:
                    resource_pack = generate_linear_equation_resource_pack(
                        topic=topic,
                        difficulty=difficulty,
                        count=int(count),
                        start_id=start_id,
                    )
                _render_resource_pack(st, resource_pack)
                return

            worksheet = generate_linear_equation_worksheet(
                topic=topic,
                difficulty=difficulty,
                count=int(count),
                start_id=start_id,
            )
            _render_worksheet(st, worksheet)
        except (TypeError, ValueError) as exc:
            st.error(str(exc))
            return


def _select_learning_objective(
    st: Any,
    course_template: CourseTemplate,
) -> LearningObjective:
    """Render curriculum selectors and return the selected learning objective."""
    st.write(f"Course template: {course_template.title}")
    selected_module_title = st.selectbox(
        "Course module",
        options=tuple(module.title for module in course_template.modules),
    )
    selected_module = _find_module(course_template, selected_module_title)
    selected_objective_description = st.selectbox(
        "Learning objective",
        options=tuple(
            objective.description
            for objective in selected_module.learning_objectives
        ),
    )
    return _find_learning_objective(selected_module, selected_objective_description)


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
    _render_worksheet_preview(st, worksheet)
    _render_solution_key_preview(st, worksheet)

    markdown_export = export_worksheet_to_markdown(worksheet, include_solutions=True)
    html_export = export_worksheet_to_html(worksheet, include_solutions=True)

    st.header("Exports")
    st.download_button(
        label="Download Markdown",
        data=markdown_export.content,
        file_name=markdown_export.filename,
        mime="text/markdown",
    )
    st.download_button(
        label="Download HTML",
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
    _render_worksheet_preview(st, resource_pack.worksheet)
    _render_solution_key_preview(st, resource_pack.worksheet)

    st.header("Study Guide")
    _render_study_guide(st, resource_pack.study_guide)

    st.header("Common Mistakes")
    _render_common_mistakes(st, resource_pack.common_mistakes)

    st.header("Tutor Notes")
    _render_tutor_notes(st, resource_pack.tutor_notes)

    markdown_export = export_resource_pack_to_markdown(
        resource_pack,
        include_solutions=True,
    )
    html_export = export_resource_pack_to_html(
        resource_pack,
        include_solutions=True,
    )

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
    st.divider()
    st.header("Worksheet Preview")
    st.write(worksheet.instructions)

    for index, problem in enumerate(worksheet.problems, start=1):
        st.write(f"{index}. {problem.prompt}")


def _render_solution_key_preview(st: Any, worksheet: Worksheet) -> None:
    """Render the solution key preview."""
    st.header("Solution Key Preview")
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
