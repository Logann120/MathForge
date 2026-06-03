"""Generation context view models for the MathForge Streamlit app."""

from __future__ import annotations

from dataclasses import dataclass

from models.content_models import ExportResult
from models.curriculum import LearningObjective


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


def generated_output_summary_lines(
    *,
    output_type: str,
    worksheet: WorksheetSummary,
    generation_context: GenerationContext,
    markdown_filename: str,
    html_filename: str,
    bundle_filename: str,
    canvas_filename: str = "",
) -> tuple[str, ...]:
    """Return Markdown lines for the generated output summary."""
    filename_lines = [
        "- **Generated export filenames:**",
        f"  - Markdown: `{markdown_filename}`",
        f"  - HTML: `{html_filename}`",
        f"  - ZIP bundle: `{bundle_filename}`",
    ]
    download_types = ["Markdown", "HTML", "ZIP bundle"]
    if canvas_filename:
        filename_lines.append(f"  - Canvas manual-entry CSV: `{canvas_filename}`")
        download_types.append("Canvas manual-entry CSV")

    lines = [
        f"- **Output type:** {output_type}",
        f"- **Generation mode:** {generation_context.mode}",
        *_generation_context_lines(generation_context, worksheet),
        f"- **Difficulty:** {worksheet.difficulty}",
        f"- **Problem count:** {worksheet.problem_count}",
        f"- **Problem ID prefix:** `{worksheet.problem_id_prefix}`",
        *filename_lines,
        f"- **Available downloads:** {', '.join(download_types)}",
    ]
    return tuple(lines)


def _generation_context_lines(
    generation_context: GenerationContext,
    worksheet: WorksheetSummary,
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


def _problem_count_from_export(export: ExportResult) -> int:
    """Return the problem count stored in export metadata."""
    raw_count = export.metadata.get("problem_count", "0")
    try:
        return int(raw_count)
    except ValueError:
        return 0
