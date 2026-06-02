"""Minimal Streamlit interface for MathForge instructional content generation."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from app.presets import find_generation_preset, generation_preset_labels
from exporters.bundle_exporter import create_export_bundle
from exporters.download_filenames import (
    build_bundle_download_filename,
    with_download_filename,
)
from exporters.html_exporter import export_resource_pack_to_html, export_worksheet_to_html
from exporters.markdown_exporter import (
    export_resource_pack_to_markdown,
    export_worksheet_to_markdown,
)
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
from models.curriculum import CourseModule, CourseTemplate, LearningObjective
from models.content_models import ExportResult, Solution, Worksheet
from models.resource_pack import (
    CommonMistakes,
    PracticeQuiz,
    ResourcePack,
    StudyGuide,
    TutorNotes,
)
from templates.course_templates import college_algebra_template
from topics.registry import (
    find_topic_by_label,
    find_topic_by_learning_objective_topic,
    supported_topic_labels,
)


LOGGER = logging.getLogger(__name__)

OUTPUT_TYPE_OPTIONS = ("Worksheet only", "Full Resource Pack")
GENERATION_MODE_OPTIONS = ("Topic mode", "Learning Objective mode")
TOPIC_OPTIONS = supported_topic_labels()
DIFFICULTY_OPTIONS = ("Easy",)
GENERATION_PRESET_OPTIONS = generation_preset_labels()


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
    preset_key = _widget_key(preset.label)
    st.caption(f"Preset: {preset.description}")

    output_type = st.radio(
        "Output type",
        options=OUTPUT_TYPE_OPTIONS,
        index=_option_index(OUTPUT_TYPE_OPTIONS, preset.output_type),
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
        index=_option_index(GENERATION_MODE_OPTIONS, preset.generation_mode),
        horizontal=True,
        help=(
            "Topic mode generates from a selected math topic. Learning Objective "
            "mode generates from the College Algebra course template."
        ),
        key=f"generation_mode_{preset_key}",
    )

    learning_objective: LearningObjective | None = None
    generation_context: GenerationContext
    if generation_mode == "Learning Objective mode":
        learning_selection = _select_learning_objective(
            st,
            college_algebra_template(),
            output_type=output_type,
        )
        learning_objective = learning_selection.learning_objective
        topic = learning_objective.topic
        generation_context = GenerationContext.from_learning_objective_selection(
            learning_selection
        )
    else:
        topic = st.selectbox(
            "Topic",
            options=TOPIC_OPTIONS,
            index=_option_index(TOPIC_OPTIONS, preset.topic_label),
            key=f"topic_{preset_key}",
        )
        generation_context = GenerationContext.topic_mode(topic)

    difficulty_label = st.selectbox(
        "Difficulty",
        options=DIFFICULTY_OPTIONS,
        index=_option_index(DIFFICULTY_OPTIONS, preset.difficulty_label),
        key=f"difficulty_{preset_key}",
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
                _render_resource_pack(st, resource_pack, generation_context)
                return

            worksheet = _generate_worksheet_for_topic(
                topic=topic,
                difficulty=difficulty,
                count=int(count),
                start_id=start_id,
            )
            _render_worksheet(st, worksheet, generation_context)
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
    topic_record = find_topic_by_label(topic)
    return topic_record.worksheet_generator(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )


def _generate_resource_pack_for_topic(
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


def _default_problem_id_prefix(topic: str) -> str:
    """Return a stable problem ID prefix for a supported topic."""
    try:
        return find_topic_by_label(topic).default_problem_id_prefix
    except ValueError:
        return "linear"


def _topic_key(topic: str) -> str:
    """Return a widget-safe topic key."""
    return _default_problem_id_prefix(topic)


def _difficulty_value(label: str) -> str:
    """Map a user-facing difficulty label to the generator input value."""
    if label == "Easy":
        return "easy"
    raise ValueError(f"unsupported difficulty: {label}")


def _option_index(options: tuple[str, ...], value: str) -> int:
    """Return the index for a default option value."""
    try:
        return options.index(value)
    except ValueError:
        return 0


def _widget_key(value: str) -> str:
    """Return a stable widget-key fragment."""
    return "".join(
        character.lower() if character.isalnum() else "_"
        for character in value.strip()
    ).strip("_")


def _select_learning_objective(
    st: Any,
    course_template: CourseTemplate,
    *,
    output_type: str,
) -> "LearningObjectiveSelection":
    """Render curriculum selectors and return selected learning-objective context."""
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
    selection = LearningObjectiveSelection(
        course_title=course_template.title,
        module_title=selected_module.title,
        learning_objective=learning_objective,
        mapped_topic=_mapped_topic_label(learning_objective),
    )
    st.caption(f"Selected learning objective: {learning_objective.description}")
    _render_learning_objective_context_summary(st, selection, output_type)
    return selection


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


def _mapped_topic_label(learning_objective: LearningObjective) -> str:
    """Return the registry topic label mapped to a learning objective."""
    try:
        return find_topic_by_learning_objective_topic(
            learning_objective.topic
        ).display_label
    except ValueError:
        return "Not mapped"


def _render_learning_objective_context_summary(
    st: Any,
    selection: "LearningObjectiveSelection",
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


@dataclass(frozen=True, slots=True)
class LearningObjectiveSelection:
    """Selected curriculum context for Learning Objective mode."""

    course_title: str
    module_title: str
    learning_objective: LearningObjective
    mapped_topic: str


@dataclass(frozen=True, slots=True)
class GenerationContext:
    """Generation mode context for preview summaries."""

    mode: str
    topic: str = ""
    course_title: str = ""
    module_title: str = ""
    learning_objective: str = ""
    mapped_topic: str = ""

    @classmethod
    def topic_mode(cls, topic: str) -> "GenerationContext":
        """Return context for Topic mode generation."""
        return cls(mode="Topic mode", topic=topic)

    @classmethod
    def from_learning_objective_selection(
        cls,
        selection: LearningObjectiveSelection,
    ) -> "GenerationContext":
        """Return context for Learning Objective mode generation."""
        return cls(
            mode="Learning Objective mode",
            course_title=selection.course_title,
            module_title=selection.module_title,
            learning_objective=selection.learning_objective.description,
            mapped_topic=selection.mapped_topic,
        )


def _render_worksheet(
    st: Any,
    worksheet: Worksheet,
    generation_context: GenerationContext,
) -> None:
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
        _render_worksheet_exports(st, markdown_export, html_export, generation_context)


def _render_worksheet_exports(
    st: Any,
    markdown_export: ExportResult,
    html_export: ExportResult,
    generation_context: GenerationContext,
) -> None:
    """Render worksheet export controls."""
    markdown_download = with_download_filename(markdown_export)
    html_download = with_download_filename(html_export)
    export_bundle = create_export_bundle(
        (markdown_download, html_download),
        bundle_filename=build_bundle_download_filename(markdown_download),
    )

    st.header("Exports")
    _render_generated_output_summary(
        st,
        output_type="Worksheet",
        worksheet=WorksheetSummary.from_export(markdown_download),
        generation_context=generation_context,
        markdown_filename=markdown_download.filename,
        html_filename=html_download.filename,
        bundle_filename=export_bundle.filename,
    )
    st.download_button(
        label="Download Worksheet Markdown",
        data=markdown_download.content,
        file_name=markdown_download.filename,
        mime="text/markdown",
    )
    st.download_button(
        label="Download Worksheet HTML",
        data=html_download.content,
        file_name=html_download.filename,
        mime="text/html",
    )
    st.download_button(
        label="Download Worksheet Export Bundle",
        data=export_bundle.content,
        file_name=export_bundle.filename,
        mime=export_bundle.mime_type,
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


def _render_resource_pack(
    st: Any,
    resource_pack: ResourcePack,
    generation_context: GenerationContext,
) -> None:
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
    with practice_quiz_tab:
        st.header("Practice Quiz")
        if resource_pack.practice_quiz is None:
            st.write("No practice quiz provided.")
        else:
            _render_practice_quiz(st, resource_pack.practice_quiz)
    with exports_tab:
        _render_resource_pack_exports(
            st,
            markdown_export,
            html_export,
            generation_context,
        )


def _render_resource_pack_exports(
    st: Any,
    markdown_export: ExportResult,
    html_export: ExportResult,
    generation_context: GenerationContext,
) -> None:
    """Render resource pack export controls."""
    markdown_download = with_download_filename(markdown_export)
    html_download = with_download_filename(html_export)
    export_bundle = create_export_bundle(
        (markdown_download, html_download),
        bundle_filename=build_bundle_download_filename(markdown_download),
    )

    st.header("Resource Pack Export")
    _render_generated_output_summary(
        st,
        output_type="Full Resource Pack",
        worksheet=WorksheetSummary.from_export(markdown_download),
        generation_context=generation_context,
        markdown_filename=markdown_download.filename,
        html_filename=html_download.filename,
        bundle_filename=export_bundle.filename,
    )
    st.download_button(
        label="Download Resource Pack Markdown",
        data=markdown_download.content,
        file_name=markdown_download.filename,
        mime="text/markdown",
    )
    st.download_button(
        label="Download Resource Pack HTML",
        data=html_download.content,
        file_name=html_download.filename,
        mime="text/html",
    )
    st.download_button(
        label="Download Resource Pack Export Bundle",
        data=export_bundle.content,
        file_name=export_bundle.filename,
        mime=export_bundle.mime_type,
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


def _render_generated_output_summary(
    st: Any,
    *,
    output_type: str,
    worksheet: "WorksheetSummary",
    generation_context: GenerationContext,
    markdown_filename: str,
    html_filename: str,
    bundle_filename: str,
) -> None:
    """Render a compact summary of generated output and downloads."""
    st.subheader("Generated Output Summary")
    st.markdown(
        "\n".join(
            _generated_output_summary_lines(
                output_type=output_type,
                worksheet=worksheet,
                generation_context=generation_context,
                markdown_filename=markdown_filename,
                html_filename=html_filename,
                bundle_filename=bundle_filename,
            )
        )
    )


def _generated_output_summary_lines(
    *,
    output_type: str,
    worksheet: "WorksheetSummary",
    generation_context: GenerationContext,
    markdown_filename: str,
    html_filename: str,
    bundle_filename: str,
) -> tuple[str, ...]:
    """Return Markdown lines for the generated output summary."""
    lines = [
        f"- **Output type:** {output_type}",
        f"- **Generation mode:** {generation_context.mode}",
        *_generation_context_lines(generation_context, worksheet),
        f"- **Difficulty:** {worksheet.difficulty}",
        f"- **Problem count:** {worksheet.problem_count}",
        f"- **Problem ID prefix:** `{worksheet.problem_id_prefix}`",
        "- **Generated export filenames:**",
        f"  - Markdown: `{markdown_filename}`",
        f"  - HTML: `{html_filename}`",
        f"  - ZIP bundle: `{bundle_filename}`",
        "- **Available downloads:** Markdown, HTML, ZIP bundle",
    ]
    return tuple(lines)


def _generation_context_lines(
    generation_context: GenerationContext,
    worksheet: "WorksheetSummary",
) -> tuple[str, ...]:
    """Return summary lines for Topic mode or Learning Objective mode."""
    if generation_context.mode == "Learning Objective mode":
        return (
            f"- **Course:** {generation_context.course_title}",
            f"- **Module:** {generation_context.module_title}",
            f"- **Learning objective:** {generation_context.learning_objective}",
            f"- **Mapped topic:** {generation_context.mapped_topic}",
        )

    topic = generation_context.topic or worksheet.context
    return (f"- **Topic:** {topic}",)


@dataclass(frozen=True, slots=True)
class WorksheetSummary:
    """Small view model for generated-output summary metadata."""

    context: str
    difficulty: str
    problem_count: int
    problem_id_prefix: str

    @classmethod
    def from_export(cls, export: ExportResult) -> "WorksheetSummary":
        """Build summary metadata from a rendered export."""
        return cls(
            context=(
                export.metadata.get("learning_objective")
                or export.metadata.get("topic")
                or export.metadata.get("worksheet_id")
                or "Generated material"
            ),
            difficulty=export.metadata.get("difficulty") or "Not specified",
            problem_count=_problem_count_from_export(export),
            problem_id_prefix=(
                export.metadata.get("problem_id_prefix")
                or export.metadata.get("worksheet_id")
                or "Not specified"
            ),
        )


def _problem_count_from_export(export: ExportResult) -> int:
    """Return the problem count stored in export metadata."""
    raw_count = export.metadata.get("problem_count", "0")
    try:
        return int(raw_count)
    except ValueError:
        return 0


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


def _render_practice_quiz(st: Any, practice_quiz: PracticeQuiz) -> None:
    """Render practice quiz content."""
    st.subheader(practice_quiz.title)
    _render_numbered_items(st, "Questions", practice_quiz.questions)
    _render_bullets(st, "Answer Key", practice_quiz.answer_key)


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


if __name__ == "__main__":
    main()
