"""Tests for instructional resource pack models."""

import pytest

from generator.problem_generator import generate_linear_equation_worksheet
from models.resource_pack import (
    CommonMistakes,
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


def test_study_guide_requires_title() -> None:
    with pytest.raises(ValueError, match="title"):
        StudyGuide(title=" ", overview="Use inverse operations.")


def test_common_mistakes_requires_at_least_one_mistake() -> None:
    with pytest.raises(ValueError, match="mistakes"):
        CommonMistakes(mistakes=())


def test_tutor_notes_requires_at_least_one_note() -> None:
    with pytest.raises(ValueError, match="notes"):
        TutorNotes(notes=())


def test_resource_pack_requires_worksheet() -> None:
    resource_pack = _sample_resource_pack()

    with pytest.raises(TypeError, match="worksheet must be a Worksheet"):
        ResourcePack(
            worksheet="not a worksheet",
            study_guide=resource_pack.study_guide,
            common_mistakes=resource_pack.common_mistakes,
            tutor_notes=resource_pack.tutor_notes,
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
