"""Tests for deterministic resource pack generation."""

import pytest

from generator.resource_pack_generator import (
    generate_factoring_techniques_resource_pack,
    generate_functions_basics_resource_pack,
    generate_linear_equation_resource_pack,
    generate_quadratic_factoring_resource_pack,
    generate_systems_of_equations_resource_pack,
)
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes


def test_generate_linear_equation_resource_pack_returns_resource_pack() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=2,
        start_id="linear",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert isinstance(resource_pack.study_guide, StudyGuide)
    assert isinstance(resource_pack.common_mistakes, CommonMistakes)
    assert isinstance(resource_pack.tutor_notes, TutorNotes)
    assert resource_pack.worksheet.worksheet_id == "linear-worksheet"
    assert len(resource_pack.worksheet.problems) == 2


def test_generate_linear_equation_resource_pack_is_deterministic() -> None:
    first = generate_linear_equation_resource_pack(
        "Linear equations",
        "easy",
        3,
        "linear",
    )
    second = generate_linear_equation_resource_pack(
        "Linear equations",
        "easy",
        3,
        "linear",
    )

    assert first == second


def test_resource_pack_includes_study_guide_content() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    assert resource_pack.study_guide.title == "Linear equations Study Guide"
    assert "inverse operations" in resource_pack.study_guide.overview
    assert any(
        "Learning objective" in point for point in resource_pack.study_guide.key_points
    )
    assert any(
        "Worked-example guidance" in tip
        for tip in resource_pack.study_guide.practice_tips
    )


def test_resource_pack_includes_common_mistakes_content() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    assert any(
        "one side" in mistake
        for mistake in resource_pack.common_mistakes.mistakes
    )
    assert any(
        "Remove b first" in correction
        for correction in resource_pack.common_mistakes.corrections
    )


def test_resource_pack_includes_tutor_notes_content() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    assert any("Tutoring prompt" in note for note in resource_pack.tutor_notes.notes)
    assert any("Diagnostic question" in note for note in resource_pack.tutor_notes.notes)
    assert any(
        "Intervention suggestion" in note for note in resource_pack.tutor_notes.notes
    )
    assert any(
        "balanced" in prompt
        for prompt in resource_pack.tutor_notes.discussion_prompts
    )


def test_resource_pack_metadata_describes_generator() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="advanced",
        count=1,
        start_id="linear",
    )

    assert resource_pack.metadata["topic"] == "Linear equations"
    assert resource_pack.metadata["difficulty"] == "advanced"
    assert resource_pack.metadata["generator"] == "linear_equation_resource_pack"
    assert resource_pack.study_guide.metadata["resource_type"] == "study_guide"
    assert resource_pack.common_mistakes.metadata["resource_type"] == "common_mistakes"
    assert resource_pack.tutor_notes.metadata["resource_type"] == "tutor_notes"
    assert resource_pack.practice_quiz is not None
    assert resource_pack.practice_quiz.metadata["resource_type"] == "practice_quiz"


def test_generate_linear_equation_resource_pack_rejects_invalid_count() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        generate_linear_equation_resource_pack(
            topic="Linear equations",
            difficulty="easy",
            count=0,
            start_id="linear",
        )


def test_generate_quadratic_factoring_resource_pack_returns_resource_pack() -> None:
    resource_pack = generate_quadratic_factoring_resource_pack(
        topic="Quadratic equations by factoring",
        difficulty="easy",
        count=2,
        start_id="quadratic",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert isinstance(resource_pack.study_guide, StudyGuide)
    assert isinstance(resource_pack.common_mistakes, CommonMistakes)
    assert isinstance(resource_pack.tutor_notes, TutorNotes)
    assert resource_pack.worksheet.worksheet_id == "quadratic-worksheet"
    assert len(resource_pack.worksheet.problems) == 2
    assert resource_pack.metadata["generator"] == "quadratic_factoring_resource_pack"


def test_generate_quadratic_factoring_resource_pack_is_deterministic() -> None:
    first = generate_quadratic_factoring_resource_pack(
        "Quadratic equations by factoring",
        "easy",
        2,
        "quadratic",
    )
    second = generate_quadratic_factoring_resource_pack(
        "Quadratic equations by factoring",
        "easy",
        2,
        "quadratic",
    )

    assert first == second


@pytest.mark.parametrize("difficulty", ("medium", "hard"))
def test_generate_quadratic_factoring_resource_pack_passes_through_difficulty(
    difficulty: str,
) -> None:
    resource_pack = generate_quadratic_factoring_resource_pack(
        topic="Quadratic equations by factoring",
        difficulty=difficulty,
        count=2,
        start_id=f"{difficulty}-quadratic",
    )

    assert resource_pack.metadata["difficulty"] == difficulty
    assert resource_pack.worksheet.metadata["difficulty"] == difficulty
    assert resource_pack.study_guide.metadata["difficulty"] == difficulty
    assert resource_pack.common_mistakes.metadata["difficulty"] == difficulty
    assert resource_pack.tutor_notes.metadata["difficulty"] == difficulty
    assert resource_pack.practice_quiz is not None
    assert len(resource_pack.practice_quiz.questions) >= 2
    assert len(resource_pack.practice_quiz.answer_key) == len(
        resource_pack.practice_quiz.questions
    )


def test_quadratic_resource_pack_includes_factoring_guidance() -> None:
    resource_pack = generate_quadratic_factoring_resource_pack(
        topic="Quadratic equations by factoring",
        difficulty="easy",
        count=1,
        start_id="quadratic",
    )

    assert "zero product property" in resource_pack.study_guide.overview
    assert any("factorable" in point for point in resource_pack.study_guide.key_points)
    assert any(
        "product-sum table" in note for note in resource_pack.tutor_notes.notes
    )
    assert any(
        "only one solution" in mistake
        for mistake in resource_pack.common_mistakes.mistakes
    )


def test_generate_systems_of_equations_resource_pack_returns_resource_pack() -> None:
    resource_pack = generate_systems_of_equations_resource_pack(
        topic="Systems of linear equations",
        difficulty="easy",
        count=2,
        start_id="systems",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert isinstance(resource_pack.study_guide, StudyGuide)
    assert isinstance(resource_pack.common_mistakes, CommonMistakes)
    assert isinstance(resource_pack.tutor_notes, TutorNotes)
    assert resource_pack.worksheet.worksheet_id == "systems-worksheet"
    assert len(resource_pack.worksheet.problems) == 2
    assert resource_pack.metadata["generator"] == "systems_of_equations_resource_pack"


def test_generate_systems_of_equations_resource_pack_is_deterministic() -> None:
    first = generate_systems_of_equations_resource_pack(
        "Systems of linear equations",
        "easy",
        2,
        "systems",
    )
    second = generate_systems_of_equations_resource_pack(
        "Systems of linear equations",
        "easy",
        2,
        "systems",
    )

    assert first == second


def test_systems_resource_pack_includes_systems_guidance() -> None:
    resource_pack = generate_systems_of_equations_resource_pack(
        topic="Systems of linear equations",
        difficulty="easy",
        count=1,
        start_id="systems",
    )

    assert "ordered pair" in resource_pack.study_guide.overview
    assert any("elimination" in point for point in resource_pack.study_guide.key_points)
    assert any("both equations" in note for note in resource_pack.tutor_notes.notes)
    assert any(
        "only one equation" in mistake
        for mistake in resource_pack.common_mistakes.mistakes
    )


def test_generate_factoring_techniques_resource_pack_returns_resource_pack() -> None:
    resource_pack = generate_factoring_techniques_resource_pack(
        topic="Factoring techniques",
        difficulty="easy",
        count=3,
        start_id="factoring",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert isinstance(resource_pack.study_guide, StudyGuide)
    assert isinstance(resource_pack.common_mistakes, CommonMistakes)
    assert isinstance(resource_pack.tutor_notes, TutorNotes)
    assert resource_pack.worksheet.worksheet_id == "factoring-worksheet"
    assert len(resource_pack.worksheet.problems) == 3
    assert resource_pack.metadata["generator"] == "factoring_techniques_resource_pack"


def test_generate_factoring_techniques_resource_pack_is_deterministic() -> None:
    first = generate_factoring_techniques_resource_pack(
        "Factoring techniques",
        "easy",
        3,
        "factoring",
    )
    second = generate_factoring_techniques_resource_pack(
        "Factoring techniques",
        "easy",
        3,
        "factoring",
    )

    assert first == second


def test_factoring_resource_pack_includes_factoring_guidance() -> None:
    resource_pack = generate_factoring_techniques_resource_pack(
        topic="Factoring techniques",
        difficulty="easy",
        count=3,
        start_id="factoring",
    )

    assert "product of simpler expressions" in resource_pack.study_guide.overview
    assert any(
        "greatest common factor" in point
        for point in resource_pack.study_guide.key_points
    )
    assert any("product-sum table" in note for note in resource_pack.tutor_notes.notes)
    assert any(
        "sum of squares" in mistake
        for mistake in resource_pack.common_mistakes.mistakes
    )


def test_generate_functions_basics_resource_pack_returns_resource_pack() -> None:
    resource_pack = generate_functions_basics_resource_pack(
        topic="Functions basics",
        difficulty="easy",
        count=3,
        start_id="functions",
    )

    assert isinstance(resource_pack, ResourcePack)
    assert isinstance(resource_pack.study_guide, StudyGuide)
    assert isinstance(resource_pack.common_mistakes, CommonMistakes)
    assert isinstance(resource_pack.tutor_notes, TutorNotes)
    assert resource_pack.worksheet.worksheet_id == "functions-worksheet"
    assert len(resource_pack.worksheet.problems) == 3
    assert resource_pack.metadata["generator"] == "functions_basics_resource_pack"


def test_generate_functions_basics_resource_pack_is_deterministic() -> None:
    first = generate_functions_basics_resource_pack(
        "Functions basics",
        "easy",
        3,
        "functions",
    )
    second = generate_functions_basics_resource_pack(
        "Functions basics",
        "easy",
        3,
        "functions",
    )

    assert first == second


def test_functions_resource_pack_includes_function_notation_guidance() -> None:
    resource_pack = generate_functions_basics_resource_pack(
        topic="Functions basics",
        difficulty="easy",
        count=3,
        start_id="functions",
    )

    assert "input value" in resource_pack.study_guide.overview
    assert any("f(a)" in point for point in resource_pack.study_guide.key_points)
    assert any("input-output table" in note for note in resource_pack.tutor_notes.notes)
    assert any(
        "multiplication" in mistake
        for mistake in resource_pack.common_mistakes.mistakes
    )


def test_supported_resource_packs_include_practice_quizzes() -> None:
    resource_packs = (
        generate_linear_equation_resource_pack(
            "Linear equations",
            "easy",
            1,
            "linear",
        ),
        generate_quadratic_factoring_resource_pack(
            "Quadratic equations by factoring",
            "easy",
            1,
            "quadratic",
        ),
        generate_systems_of_equations_resource_pack(
            "Systems of linear equations",
            "easy",
            1,
            "systems",
        ),
        generate_factoring_techniques_resource_pack(
            "Factoring techniques",
            "easy",
            1,
            "factoring",
        ),
        generate_functions_basics_resource_pack(
            "Functions basics",
            "easy",
            1,
            "functions",
        ),
    )

    for resource_pack in resource_packs:
        assert resource_pack.practice_quiz is not None
        assert resource_pack.practice_quiz.title.endswith("Practice Quiz")
        assert len(resource_pack.practice_quiz.questions) == 2
        assert len(resource_pack.practice_quiz.answer_key) == 2
        assert resource_pack.practice_quiz.metadata["resource_type"] == "practice_quiz"
