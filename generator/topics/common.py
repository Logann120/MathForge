"""Shared helpers for topic-focused MathForge generators."""

from __future__ import annotations

from models.content_models import Worksheet
from models.resource_pack import PracticeQuiz


def require_text(value: str, field_name: str) -> None:
    """Validate that a generator input is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty.")


def require_positive_count(count: int) -> None:
    """Validate that a generator count is a positive integer."""
    if not isinstance(count, int):
        raise TypeError("count must be an integer.")
    if count <= 0:
        raise ValueError("count must be positive.")


def build_practice_quiz(topic: str, worksheet: Worksheet) -> PracticeQuiz:
    """Build a deterministic practice quiz from a generated worksheet."""
    questions = tuple(
        f"Quiz question {index}: {problem.prompt}"
        for index, problem in enumerate(worksheet.problems[:3], start=1)
    )
    answer_key = tuple(
        f"{index}. {problem.answer}"
        for index, problem in enumerate(worksheet.problems[:3], start=1)
    )

    return PracticeQuiz(
        title=f"{topic} Practice Quiz",
        questions=questions + (topic_review_question(topic),),
        answer_key=answer_key + (topic_review_answer(topic),),
        metadata={
            "topic": topic,
            "resource_type": "practice_quiz",
            "source_worksheet_id": worksheet.worksheet_id or "",
        },
    )


def topic_review_question(topic: str) -> str:
    """Return a deterministic conceptual quiz question for a topic."""
    normalized_topic = topic.strip().lower()

    if "quadratic" in normalized_topic:
        return "Concept check: What property is used after factoring a quadratic equation?"
    if "systems" in normalized_topic:
        return "Concept check: What does the ordered pair solution represent?"
    if "factoring" in normalized_topic:
        return "Concept check: What should you check before using a special factoring pattern?"
    if "functions" in normalized_topic:
        return "Concept check: In f(a), what does a represent?"
    return "Concept check: How can you verify that a solution is correct?"


def topic_review_answer(topic: str) -> str:
    """Return a deterministic conceptual quiz answer for a topic."""
    normalized_topic = topic.strip().lower()

    if "quadratic" in normalized_topic:
        return "4. The zero product property."
    if "systems" in normalized_topic:
        return "4. It is the point that satisfies both equations."
    if "factoring" in normalized_topic:
        return "4. Check for a greatest common factor first."
    if "functions" in normalized_topic:
        return "4. It represents the input value."
    return "4. Substitute the solution back into the original equation."
