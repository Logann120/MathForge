"""Canvas-friendly manual-entry quiz export helpers for MathForge."""

from __future__ import annotations

import csv
from io import StringIO

from models.content_models import ExportResult, Solution, Worksheet
from models.resource_pack import PracticeQuiz, ResourcePack


CANVAS_MANUAL_ENTRY_COLUMNS = (
    "question_title",
    "question_prompt",
    "correct_answer",
    "solution_explanation",
    "topic",
    "difficulty",
    "problem_id",
    "source_type",
    "source_id",
)


def export_worksheet_to_canvas_csv(worksheet: Worksheet) -> ExportResult:
    """Render worksheet problems as a Canvas manual-entry CSV.

    This is not a Canvas API integration. It produces deterministic CSV rows
    that instructors can inspect, copy, and adapt for manual Canvas quiz entry
    or institution-specific import workflows.
    """
    if not isinstance(worksheet, Worksheet):
        raise TypeError("worksheet must be a Worksheet.")

    solutions_by_problem_id = {
        solution.problem_id: solution for solution in worksheet.solutions
    }
    rows = [
        _worksheet_problem_row(
            worksheet=worksheet,
            problem_index=index,
            solution=solutions_by_problem_id.get(problem.problem_id),
        )
        for index, problem in enumerate(worksheet.problems, start=1)
    ]

    return ExportResult(
        content=_write_csv(rows),
        format_name="canvas_csv",
        filename=_canvas_csv_filename(worksheet.worksheet_id, "worksheet"),
        metadata={
            "worksheet_id": worksheet.worksheet_id or "",
            "resource_type": "worksheet",
            "topic": worksheet.metadata.get("topic", ""),
            "difficulty": worksheet.metadata.get("difficulty", ""),
            "problem_id_prefix": _problem_id_prefix(worksheet),
            "problem_count": str(len(worksheet.problems)),
            "canvas_export_type": "manual_entry_csv",
        },
    )


def export_resource_pack_quiz_to_canvas_csv(resource_pack: ResourcePack) -> ExportResult:
    """Render a resource-pack practice quiz as a Canvas manual-entry CSV."""
    if not isinstance(resource_pack, ResourcePack):
        raise TypeError("resource_pack must be a ResourcePack.")
    if resource_pack.practice_quiz is None:
        raise ValueError("resource_pack must include a PracticeQuiz.")

    rows = _practice_quiz_rows(
        practice_quiz=resource_pack.practice_quiz,
        resource_pack=resource_pack,
    )

    return ExportResult(
        content=_write_csv(rows),
        format_name="canvas_csv",
        filename=_canvas_csv_filename(
            resource_pack.worksheet.worksheet_id,
            "resource-pack-quiz",
        ),
        metadata={
            "worksheet_id": resource_pack.worksheet.worksheet_id or "",
            "resource_type": "resource_pack",
            "topic": resource_pack.metadata.get(
                "topic",
                resource_pack.worksheet.metadata.get("topic", ""),
            ),
            "difficulty": resource_pack.metadata.get(
                "difficulty",
                resource_pack.worksheet.metadata.get("difficulty", ""),
            ),
            "problem_id_prefix": _problem_id_prefix(resource_pack.worksheet),
            "problem_count": str(len(resource_pack.practice_quiz.questions)),
            "learning_objective": resource_pack.metadata.get(
                "learning_objective",
                "",
            ),
            "learning_objective_id": resource_pack.metadata.get(
                "learning_objective_id",
                "",
            ),
            "canvas_export_type": "manual_entry_csv",
        },
    )


def _worksheet_problem_row(
    worksheet: Worksheet,
    problem_index: int,
    solution: Solution | None,
) -> dict[str, str]:
    """Return one CSV row for a worksheet problem."""
    problem = worksheet.problems[problem_index - 1]
    correct_answer = solution.final_answer if solution is not None else problem.answer
    explanation = "\n".join(solution.steps) if solution is not None else ""
    return {
        "question_title": problem.problem_id,
        "question_prompt": problem.prompt,
        "correct_answer": correct_answer,
        "solution_explanation": explanation,
        "topic": problem.topic or worksheet.metadata.get("topic", ""),
        "difficulty": problem.difficulty or worksheet.metadata.get("difficulty", ""),
        "problem_id": problem.problem_id,
        "source_type": "worksheet",
        "source_id": worksheet.worksheet_id or "",
    }


def _practice_quiz_rows(
    practice_quiz: PracticeQuiz,
    resource_pack: ResourcePack,
) -> list[dict[str, str]]:
    """Return CSV rows for a resource-pack practice quiz."""
    topic = resource_pack.metadata.get(
        "topic",
        resource_pack.worksheet.metadata.get("topic", ""),
    )
    difficulty = resource_pack.metadata.get(
        "difficulty",
        resource_pack.worksheet.metadata.get("difficulty", ""),
    )
    source_id = resource_pack.worksheet.worksheet_id or practice_quiz.title

    return [
        {
            "question_title": f"{practice_quiz.title} - Question {index}",
            "question_prompt": question,
            "correct_answer": answer,
            "solution_explanation": "",
            "topic": topic,
            "difficulty": difficulty,
            "problem_id": f"{source_id}-quiz-{index:03d}",
            "source_type": "practice_quiz",
            "source_id": source_id,
        }
        for index, (question, answer) in enumerate(
            zip(practice_quiz.questions, practice_quiz.answer_key, strict=True),
            start=1,
        )
    ]


def _write_csv(rows: list[dict[str, str]]) -> str:
    """Write CSV rows with stable column ordering."""
    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CANVAS_MANUAL_ENTRY_COLUMNS)
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def _canvas_csv_filename(worksheet_id: str | None, suffix: str) -> str:
    """Create a simple Canvas CSV filename from worksheet metadata."""
    base_name = worksheet_id or "mathforge"
    safe_name = "".join(
        character.lower() if character.isalnum() else "-"
        for character in base_name.strip()
    ).strip("-")
    return f"{safe_name or 'mathforge'}-{suffix}-canvas.csv"


def _problem_id_prefix(worksheet: Worksheet) -> str:
    """Return the problem ID prefix used by a worksheet."""
    if worksheet.worksheet_id and worksheet.worksheet_id.endswith("-worksheet"):
        return worksheet.worksheet_id.removesuffix("-worksheet")
    if worksheet.problems:
        return worksheet.problems[0].problem_id.rsplit("-", maxsplit=1)[0]
    return ""
