"""Tests for instructional resource pack models."""

import pytest

from generator.problem_generator import generate_linear_equation_worksheet
from models.resource_pack import (
    CommonMistakes,
    PracticeQuiz,
    ResourcePack,
    StudyGuide,
    TutorNotes,
)


def _sample_resource_pack() -> ResourcePack:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )
    return ResourcePack(
        worksheet=worksheet,
        study_guide=StudyGuide(
            title="Linear Equations Study Guide",
            overview="Practice isolating the variable in one-step equations.",
            key_points=("Undo addition or subtraction first.",),
            practice_tips=("Check by substituting your answer.",),
        ),
        common_mistakes=CommonMistakes(
            mistakes=("Forgetting to apply the same operation to both sides.",),
            corrections=("Write each operation on both sides of the equation.",),
        ),
        tutor_notes=TutorNotes(
            notes=("Ask learners to explain each inverse operation.",),
            discussion_prompts=("What keeps an equation balanced?",),
        ),
        metadata={"topic": "linear equations"},
    )


def test_resource_pack_creation() -> None:
    resource_pack = _sample_resource_pack()

    assert resource_pack.worksheet.title == "Linear equations Worksheet"
    assert resource_pack.study_guide.title == "Linear Equations Study Guide"
    assert resource_pack.common_mistakes.mistakes == (
        "Forgetting to apply the same operation to both sides.",
    )
    assert resource_pack.tutor_notes.notes == (
        "Ask learners to explain each inverse operation.",
    )
    assert resource_pack.metadata["topic"] == "linear equations"
    assert resource_pack.practice_quiz is None


def test_practice_quiz_creation() -> None:
    practice_quiz = PracticeQuiz(
        title="Linear Equations Practice Quiz",
        questions=("Solve x + 1 = 3.",),
        answer_key=("1. x = 2",),
        metadata={"topic": "linear equations"},
    )

    assert practice_quiz.title == "Linear Equations Practice Quiz"
    assert practice_quiz.questions == ("Solve x + 1 = 3.",)
    assert practice_quiz.answer_key == ("1. x = 2",)
    assert practice_quiz.metadata["topic"] == "linear equations"


def test_resource_pack_can_include_practice_quiz() -> None:
    resource_pack = _sample_resource_pack()
    practice_quiz = PracticeQuiz(
        title="Quiz",
        questions=("What is x?",),
        answer_key=("1. x = 1",),
    )

    resource_pack_with_quiz = ResourcePack(
        worksheet=resource_pack.worksheet,
        study_guide=resource_pack.study_guide,
        common_mistakes=resource_pack.common_mistakes,
        tutor_notes=resource_pack.tutor_notes,
        practice_quiz=practice_quiz,
    )

    assert resource_pack_with_quiz.practice_quiz == practice_quiz


def test_resource_pack_preserves_positional_metadata_compatibility() -> None:
    resource_pack = _sample_resource_pack()

    resource_pack_with_positional_metadata = ResourcePack(
        resource_pack.worksheet,
        resource_pack.study_guide,
        resource_pack.common_mistakes,
        resource_pack.tutor_notes,
        {"topic": "linear equations"},
    )

    assert resource_pack_with_positional_metadata.metadata["topic"] == (
        "linear equations"
    )
    assert resource_pack_with_positional_metadata.practice_quiz is None


def test_study_guide_requires_title() -> None:
    with pytest.raises(ValueError, match="title"):
        StudyGuide(title=" ", overview="Use inverse operations.")


def test_common_mistakes_requires_at_least_one_mistake() -> None:
    with pytest.raises(ValueError, match="mistakes"):
        CommonMistakes(mistakes=())


def test_tutor_notes_requires_at_least_one_note() -> None:
    with pytest.raises(ValueError, match="notes"):
        TutorNotes(notes=())


def test_practice_quiz_requires_title() -> None:
    with pytest.raises(ValueError, match="title"):
        PracticeQuiz(title=" ", questions=("Question",), answer_key=("Answer",))


def test_practice_quiz_requires_questions() -> None:
    with pytest.raises(ValueError, match="questions"):
        PracticeQuiz(title="Quiz", questions=(), answer_key=("Answer",))


def test_practice_quiz_requires_answer_key() -> None:
    with pytest.raises(ValueError, match="answer_key"):
        PracticeQuiz(title="Quiz", questions=("Question",), answer_key=())


def test_practice_quiz_requires_answer_key_for_each_question() -> None:
    with pytest.raises(ValueError, match="one entry per question"):
        PracticeQuiz(
            title="Quiz",
            questions=("Question 1", "Question 2"),
            answer_key=("1. Answer",),
        )


def test_resource_pack_requires_worksheet() -> None:
    resource_pack = _sample_resource_pack()

    with pytest.raises(TypeError, match="worksheet must be a Worksheet"):
        ResourcePack(
            worksheet="not a worksheet",
            study_guide=resource_pack.study_guide,
            common_mistakes=resource_pack.common_mistakes,
            tutor_notes=resource_pack.tutor_notes,
        )


def test_resource_pack_rejects_invalid_practice_quiz() -> None:
    resource_pack = _sample_resource_pack()

    with pytest.raises(TypeError, match="practice_quiz"):
        ResourcePack(
            worksheet=resource_pack.worksheet,
            study_guide=resource_pack.study_guide,
            common_mistakes=resource_pack.common_mistakes,
            tutor_notes=resource_pack.tutor_notes,
            practice_quiz="not a quiz",
        )


def test_resource_pack_metadata_requires_string_values() -> None:
    resource_pack = _sample_resource_pack()

    with pytest.raises(TypeError, match="metadata values"):
        ResourcePack(
            worksheet=resource_pack.worksheet,
            study_guide=resource_pack.study_guide,
            common_mistakes=resource_pack.common_mistakes,
            tutor_notes=resource_pack.tutor_notes,
            metadata={"version": 1},
        )


def test_resource_pack_is_frozen() -> None:
    resource_pack = _sample_resource_pack()

    with pytest.raises(AttributeError):
        resource_pack.metadata = {}
