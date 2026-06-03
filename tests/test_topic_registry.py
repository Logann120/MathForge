"""Tests for the supported topic registry."""

import pytest

from models.content_models import Worksheet
from models.resource_pack import ResourcePack
from topics.registry import (
    SupportedTopic,
    find_topic_by_label,
    find_topic_by_learning_objective_topic,
    find_topic_by_slug,
    supported_topic_labels,
    supported_topics,
)


EXPECTED_TOPIC_SNAPSHOT = (
    (
        "linear-equations",
        "Linear equations",
        "linear",
        "Linear Equations",
        "Solve linear equations in one variable",
    ),
    (
        "quadratic-equations-by-factoring",
        "Quadratic equations by factoring",
        "quadratic",
        "Quadratic Equations",
        "Solve quadratic equations by factoring",
    ),
    (
        "systems-of-linear-equations",
        "Systems of linear equations",
        "systems",
        "Systems of Equations",
        "Solve systems of linear equations in two variables",
    ),
    (
        "factoring-techniques",
        "Factoring techniques",
        "factoring",
        "Factoring Techniques",
        "Factor polynomial expressions using common factoring strategies",
    ),
    (
        "functions-basics",
        "Functions basics",
        "functions",
        "Functions",
        "Evaluate and interpret functions using function notation",
    ),
)


def test_supported_topics_are_in_ui_display_order() -> None:
    assert supported_topic_labels() == (
        "Linear equations",
        "Quadratic equations by factoring",
        "Systems of linear equations",
        "Factoring techniques",
        "Functions basics",
    )


def test_supported_topic_snapshot_preserves_labels_prefixes_and_objectives() -> None:
    snapshot = tuple(
        (
            topic.slug,
            topic.display_label,
            topic.default_problem_id_prefix,
            topic.curriculum_module_title,
            topic.curriculum_objective_description,
        )
        for topic in supported_topics()
    )

    assert snapshot == EXPECTED_TOPIC_SNAPSHOT


def test_supported_topics_use_current_output_types_and_difficulty() -> None:
    for topic in supported_topics():
        assert topic.supported_output_types == ("worksheet", "resource_pack")
        assert topic.supported_difficulty_levels == ("easy", "medium", "hard")


def test_supported_topics_include_expected_metadata() -> None:
    topic = find_topic_by_label("Quadratic equations by factoring")

    assert isinstance(topic, SupportedTopic)
    assert topic.slug == "quadratic-equations-by-factoring"
    assert topic.default_problem_id_prefix == "quadratic"
    assert topic.supported_output_types == ("worksheet", "resource_pack")
    assert topic.supported_difficulty_levels == ("easy", "medium", "hard")
    assert topic.curriculum_course == "College Algebra"
    assert topic.curriculum_module_title == "Quadratic Equations"
    assert topic.curriculum_objective_description == (
        "Solve quadratic equations by factoring"
    )


def test_linear_equations_registry_marks_expanded_difficulty_support() -> None:
    topic = find_topic_by_label("Linear equations")

    assert topic.supported_difficulty_levels == ("easy", "medium", "hard")


def test_quadratic_equations_registry_marks_expanded_difficulty_support() -> None:
    topic = find_topic_by_label("Quadratic equations by factoring")

    assert topic.supported_difficulty_levels == ("easy", "medium", "hard")


def test_systems_of_equations_registry_marks_expanded_difficulty_support() -> None:
    topic = find_topic_by_label("Systems of linear equations")

    assert topic.supported_difficulty_levels == ("easy", "medium", "hard")


def test_factoring_techniques_registry_marks_expanded_difficulty_support() -> None:
    topic = find_topic_by_label("Factoring techniques")

    assert topic.supported_difficulty_levels == ("easy", "medium", "hard")


def test_functions_basics_registry_marks_expanded_difficulty_support() -> None:
    topic = find_topic_by_label("Functions basics")

    assert topic.supported_difficulty_levels == ("easy", "medium", "hard")


def test_registry_difficulty_metadata_is_normalized_lowercase() -> None:
    for topic in supported_topics():
        for difficulty in topic.supported_difficulty_levels:
            assert difficulty == difficulty.lower()
            assert difficulty == difficulty.strip()


def test_all_current_topics_advertise_expanded_difficulty() -> None:
    expanded_topics = tuple(
        topic.slug
        for topic in supported_topics()
        if topic.supported_difficulty_levels != ("easy",)
    )
    easy_only_topics = tuple(
        topic.slug
        for topic in supported_topics()
        if topic.supported_difficulty_levels == ("easy",)
    )

    assert expanded_topics == (
        "linear-equations",
        "quadratic-equations-by-factoring",
        "systems-of-linear-equations",
        "factoring-techniques",
        "functions-basics",
    )
    assert easy_only_topics == ()


def test_find_topic_by_slug() -> None:
    topic = find_topic_by_slug("systems-of-linear-equations")

    assert topic.display_label == "Systems of linear equations"
    assert topic.default_problem_id_prefix == "systems"


def test_find_topic_by_learning_objective_topic_uses_aliases() -> None:
    topic = find_topic_by_learning_objective_topic(
        "systems of linear equations in two variables"
    )

    assert topic.display_label == "Systems of linear equations"


def test_learning_objective_topic_aliases_are_exact_not_fuzzy() -> None:
    unsupported_near_matches = (
        "linear equations and inequalities",
        "quadratic equations with the quadratic formula",
        "systems of nonlinear equations",
        "factoring rational expressions",
        "function transformations",
    )

    for topic_text in unsupported_near_matches:
        with pytest.raises(ValueError, match="unsupported learning objective topic"):
            find_topic_by_learning_objective_topic(topic_text)


def test_registry_generators_produce_current_model_types() -> None:
    topic = find_topic_by_label("Functions basics")

    worksheet = topic.worksheet_generator(
        topic=topic.display_label,
        difficulty="easy",
        count=1,
        start_id="registry-functions",
    )
    resource_pack = topic.resource_pack_generator(
        topic=topic.display_label,
        difficulty="easy",
        count=1,
        start_id="registry-functions-pack",
    )

    assert isinstance(worksheet, Worksheet)
    assert worksheet.title == "Functions basics Worksheet"
    assert isinstance(resource_pack, ResourcePack)
    assert resource_pack.practice_quiz is not None


def test_registry_rejects_unknown_topic_values() -> None:
    with pytest.raises(ValueError, match="unsupported topic"):
        find_topic_by_label("Exponential equations")

    with pytest.raises(ValueError, match="unsupported topic slug"):
        find_topic_by_slug("exponential-equations")

    with pytest.raises(ValueError, match="unsupported learning objective topic"):
        find_topic_by_learning_objective_topic("Solve exponential equations")


def test_supported_topics_are_immutable_tuple() -> None:
    topics = supported_topics()

    assert isinstance(topics, tuple)
    assert all(isinstance(topic, SupportedTopic) for topic in topics)
