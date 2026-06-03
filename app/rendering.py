"""Preview rendering helpers for the MathForge Streamlit app."""

from __future__ import annotations

from typing import Any

from app.downloads import render_resource_pack_exports, render_worksheet_exports
from app.generation_context import (
    GenerationContext,
    LearningObjectiveSelection,
    WorksheetSummary,
    generated_output_summary_lines,
)
from models.content_models import Solution, Worksheet
from models.resource_pack import (
    CommonMistakes,
    PracticeQuiz,
    ResourcePack,
    StudyGuide,
    TutorNotes,
)


def render_learning_objective_context_summary(
    st: Any,
    selection: LearningObjectiveSelection,
    output_type: str,
) -> None:
    """Render selected learning-objective context before generation."""
    st.subheader("Learning Objective Context")
    st.markdown(
        "\n".join(
            (
                f"- **Course:** {selection.course_title}",
                f"- **Module:** {selection.module_title}",
                (
                    "- **Learning objective:** "
                    f"{selection.learning_objective.description}"
                ),
                f"- **Mapped topic:** {selection.mapped_topic}",
                f"- **Planned output:** {output_type}",
            )
        )
    )


def render_worksheet(
    st: Any,
    worksheet: Worksheet,
    generation_context: GenerationContext,
) -> None:
    """Render previews and exports for a generated worksheet."""
    worksheet_tab, solution_tab, exports_tab = st.tabs(
        ("Worksheet", "Solution Key", "Exports")
    )

    with worksheet_tab:
        render_worksheet_preview(st, worksheet)
    with solution_tab:
        render_solution_key_preview(st, worksheet)
    with exports_tab:
        render_worksheet_exports(st, worksheet, generation_context)


def render_resource_pack(
    st: Any,
    resource_pack: ResourcePack,
    generation_context: GenerationContext,
) -> None:
    """Render previews and exports for a full resource pack."""
    (
        worksheet_tab,
        solution_tab,
        study_guide_tab,
        common_mistakes_tab,
        tutor_notes_tab,
        practice_quiz_tab,
        exports_tab,
    ) = st.tabs(
        (
            "Worksheet",
            "Solution Key",
            "Study Guide",
            "Common Mistakes",
            "Tutor Notes",
            "Practice Quiz",
            "Exports",
        )
    )

    with worksheet_tab:
        render_worksheet_preview(st, resource_pack.worksheet)
    with solution_tab:
        render_solution_key_preview(st, resource_pack.worksheet)
    with study_guide_tab:
        st.header("Study Guide")
        render_study_guide(st, resource_pack.study_guide)
    with common_mistakes_tab:
        st.header("Common Mistakes")
        render_common_mistakes(st, resource_pack.common_mistakes)
    with tutor_notes_tab:
        st.header("Tutor Notes")
        render_tutor_notes(st, resource_pack.tutor_notes)
    with practice_quiz_tab:
        st.header("Practice Quiz")
        if resource_pack.practice_quiz is None:
            st.write("No practice quiz provided.")
        else:
            render_practice_quiz(st, resource_pack.practice_quiz)
    with exports_tab:
        render_resource_pack_exports(st, resource_pack, generation_context)


def render_generated_output_summary(
    st: Any,
    *,
    output_type: str,
    worksheet: WorksheetSummary,
    generation_context: GenerationContext,
    markdown_filename: str,
    html_filename: str,
    bundle_filename: str,
    canvas_filename: str = "",
) -> None:
    """Render a compact summary of generated output and downloads."""
    st.subheader("Generated Output Summary")
    st.markdown(
        "\n".join(
            generated_output_summary_lines(
                output_type=output_type,
                worksheet=worksheet,
                generation_context=generation_context,
                markdown_filename=markdown_filename,
                html_filename=html_filename,
                bundle_filename=bundle_filename,
                canvas_filename=canvas_filename,
            )
        )
    )


def render_worksheet_preview(st: Any, worksheet: Worksheet) -> None:
    """Render the worksheet problem preview."""
    st.header("Worksheet")
    st.write(worksheet.instructions)

    for index, problem in enumerate(worksheet.problems, start=1):
        st.write(f"{index}. {problem.prompt}")


def render_solution_key_preview(st: Any, worksheet: Worksheet) -> None:
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


def render_study_guide(st: Any, study_guide: StudyGuide) -> None:
    """Render study guide content."""
    st.subheader(study_guide.title)
    st.write(study_guide.overview)
    _render_bullets(st, "Key Ideas", study_guide.key_points)
    _render_bullets(st, "Worked-Example Guidance", study_guide.practice_tips)


def render_common_mistakes(st: Any, common_mistakes: CommonMistakes) -> None:
    """Render common mistakes content."""
    _render_bullets(st, "Mistakes to Watch For", common_mistakes.mistakes)
    _render_bullets(
        st,
        "Corrections and Interventions",
        common_mistakes.corrections,
    )


def render_tutor_notes(st: Any, tutor_notes: TutorNotes) -> None:
    """Render tutor-facing notes."""
    _render_bullets(st, "Notes", tutor_notes.notes)
    _render_bullets(st, "Discussion Prompts", tutor_notes.discussion_prompts)


def render_practice_quiz(st: Any, practice_quiz: PracticeQuiz) -> None:
    """Render practice quiz content."""
    st.subheader(practice_quiz.title)
    _render_numbered_items(st, "Questions", practice_quiz.questions)
    _render_bullets(st, "Answer Key", practice_quiz.answer_key)


def _render_solution(st: Any, index: int, solution: Solution) -> None:
    """Render one solution preview entry."""
    st.write(f"{index}. Answer: {solution.final_answer}")
    for step in solution.steps:
        st.write(f"   - {step}")


def _render_bullets(st: Any, label: str, items: tuple[str, ...]) -> None:
    """Render a labeled list of text items."""
    if not items:
        return

    st.subheader(label)
    for item in items:
        st.write(f"- {item}")


def _render_numbered_items(st: Any, label: str, items: tuple[str, ...]) -> None:
    """Render a labeled numbered list of text items."""
    if not items:
        return

    st.subheader(label)
    for index, item in enumerate(items, start=1):
        st.write(f"{index}. {item}")
