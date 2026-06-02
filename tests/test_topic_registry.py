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


def test_supported_topics_are_in_ui_display_order() -> None:
    assert supported_topic_labels() == (
        "Linear equations",
        "Quadratic equations by factoring",
        "Systems of linear equations",
        "Factoring techniques",
        "Functions basics",
    )


def test_supported_topics_include_expected_metadata() -> None:
    topic = find_topic_by_label("Quadratic equations by factoring")

    assert isinstance(topic, SupportedTopic)
    assert topic.slug == "quadratic-equations-by-factoring"
    assert topic.default_problem_id_prefix == "quadratic"
    assert topic.supported_output_types == ("worksheet", "resource_pack")
    assert topic.supported_difficulty_levels == ("easy",)
    assert topic.curriculum_course == "College Algebra"
    assert topic.curriculum_module_title == "Quadratic Equations"
    assert topic.curriculum_objective_description == (
        "Solve quadratic equations by factoring"
    )


def test_find_topic_by_slug() -> None:
    topic = find_topic_by_slug("systems-of-linear-equations")

    assert topic.display_label == "Systems of linear equations"
    assert topic.default_problem_id_prefix == "systems"


def test_find_topic_by_learning_objective_topic_uses_aliases() -> None:
    topic = find_topic_by_learning_objective_topic(
        "systems of linear equations in two variables"
    )

    assert topic.display_label == "Systems of linear equations"


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
