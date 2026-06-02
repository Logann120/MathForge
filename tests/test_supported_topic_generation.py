"""Registry-backed regression tests for supported topic generation."""

import pytest

from models.content_models import Solution, Worksheet
from models.resource_pack import (
    CommonMistakes,
    PracticeQuiz,
    ResourcePack,
    StudyGuide,
    TutorNotes,
)
from topics.registry import SupportedTopic, supported_topics


def _topic_id(topic: SupportedTopic) -> str:
    """Return a readable pytest id for a supported topic."""
    return topic.slug


@pytest.mark.parametrize("topic", supported_topics(), ids=_topic_id)
def test_supported_topic_worksheet_generation_structure(
    topic: SupportedTopic,
) -> None:
    count = 3
    worksheet = topic.worksheet_generator(
        topic=topic.display_label,
        difficulty="easy",
        count=count,
        start_id=topic.default_problem_id_prefix,
    )

    assert isinstance(worksheet, Worksheet)
    assert worksheet.title == f"{topic.display_label} Worksheet"
    assert worksheet.worksheet_id == f"{topic.default_problem_id_prefix}-worksheet"
    assert worksheet.metadata["topic"] == topic.display_label
    assert worksheet.metadata["difficulty"] == "easy"
    assert len(worksheet.problems) == count
    assert len(worksheet.solutions) == count
    assert [problem.problem_id for problem in worksheet.problems] == [
        f"{topic.default_problem_id_prefix}-{index:03d}"
        for index in range(1, count + 1)
    ]

    solutions_by_problem_id = {
        solution.problem_id: solution for solution in worksheet.solutions
    }
    for problem in worksheet.problems:
        assert problem.topic == topic.display_label
        assert problem.difficulty == "easy"
        assert problem.prompt.strip()
        assert problem.answer.strip()
        assert problem.metadata

        solution = solutions_by_problem_id[problem.problem_id]
        assert isinstance(solution, Solution)
        assert solution.final_answer == problem.answer
        assert solution.steps
        assert all(step.strip() for step in solution.steps)


@pytest.mark.parametrize("topic", supported_topics(), ids=_topic_id)
def test_supported_topic_worksheet_generation_is_deterministic(
    topic: SupportedTopic,
) -> None:
    first = topic.worksheet_generator(
        topic=topic.display_label,
        difficulty="easy",
        count=3,
        start_id=topic.default_problem_id_prefix,
    )
    second = topic.worksheet_generator(
        topic=topic.display_label,
        difficulty="easy",
        count=3,
        start_id=topic.default_problem_id_prefix,
    )

    assert first == second


@pytest.mark.parametrize("topic", supported_topics(), ids=_topic_id)
def test_supported_topic_resource_pack_generation_structure(
    topic: SupportedTopic,
) -> None:
    count = 3
    resource_pack = topic.resource_pack_generator(
        topic=topic.display_label,
        difficulty="easy",
        count=count,
        start_id=topic.default_problem_id_prefix,
    )

    assert isinstance(resource_pack, ResourcePack)
    assert resource_pack.metadata["topic"] == topic.display_label
    assert resource_pack.metadata["difficulty"] == "easy"
    assert resource_pack.worksheet.title == f"{topic.display_label} Worksheet"
    assert len(resource_pack.worksheet.problems) == count

    assert isinstance(resource_pack.study_guide, StudyGuide)
    assert resource_pack.study_guide.title == f"{topic.display_label} Study Guide"
    assert resource_pack.study_guide.overview.strip()
    assert resource_pack.study_guide.key_points
    assert resource_pack.study_guide.practice_tips
    assert resource_pack.study_guide.metadata["topic"] == topic.display_label
    assert resource_pack.study_guide.metadata["resource_type"] == "study_guide"

    assert isinstance(resource_pack.common_mistakes, CommonMistakes)
    assert resource_pack.common_mistakes.mistakes
    assert resource_pack.common_mistakes.corrections
    assert resource_pack.common_mistakes.metadata["topic"] == topic.display_label
    assert (
        resource_pack.common_mistakes.metadata["resource_type"]
        == "common_mistakes"
    )

    assert isinstance(resource_pack.tutor_notes, TutorNotes)
    assert resource_pack.tutor_notes.notes
    assert resource_pack.tutor_notes.discussion_prompts
    assert resource_pack.tutor_notes.metadata["topic"] == topic.display_label
    assert resource_pack.tutor_notes.metadata["resource_type"] == "tutor_notes"

    assert isinstance(resource_pack.practice_quiz, PracticeQuiz)
    assert resource_pack.practice_quiz.title == f"{topic.display_label} Practice Quiz"
    assert len(resource_pack.practice_quiz.questions) == 4
    assert len(resource_pack.practice_quiz.answer_key) == 4
    assert resource_pack.practice_quiz.metadata["topic"] == topic.display_label
    assert resource_pack.practice_quiz.metadata["resource_type"] == "practice_quiz"
    assert (
        resource_pack.practice_quiz.metadata["source_worksheet_id"]
        == resource_pack.worksheet.worksheet_id
    )


@pytest.mark.parametrize("topic", supported_topics(), ids=_topic_id)
def test_supported_topic_resource_pack_generation_is_deterministic(
    topic: SupportedTopic,
) -> None:
    first = topic.resource_pack_generator(
        topic=topic.display_label,
        difficulty="easy",
        count=3,
        start_id=topic.default_problem_id_prefix,
    )
    second = topic.resource_pack_generator(
        topic=topic.display_label,
        difficulty="easy",
        count=3,
        start_id=topic.default_problem_id_prefix,
    )

    assert first == second
