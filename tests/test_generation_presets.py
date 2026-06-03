"""Tests for built-in generation presets."""

import pytest

from app.controls import DIFFICULTY_OPTIONS
from app.presets import (
    find_generation_preset,
    generation_preset_labels,
    generation_presets,
)
from topics.registry import supported_topic_labels


def test_generation_presets_are_small_and_ordered() -> None:
    labels = generation_preset_labels()

    assert labels == (
        "Quick Worksheet",
        "Standard Practice Set",
        "Full Tutor Resource Pack",
    )
    assert len(labels) == 3


def test_generation_presets_use_supported_defaults() -> None:
    supported_topics = supported_topic_labels()

    for preset in generation_presets():
        assert preset.output_type in {"Worksheet only", "Full Resource Pack"}
        assert preset.generation_mode in {"Topic mode", "Learning Objective mode"}
        assert preset.topic_label in supported_topics
        assert preset.difficulty_label == "Easy"
        assert preset.difficulty_label in DIFFICULTY_OPTIONS
        assert 1 <= preset.problem_count <= 25
        assert preset.description


def test_generation_preset_problem_counts_match_workflow_intent() -> None:
    quick = find_generation_preset("Quick Worksheet")
    standard = find_generation_preset("Standard Practice Set")
    tutor_pack = find_generation_preset("Full Tutor Resource Pack")

    assert quick.problem_count < standard.problem_count
    assert quick.output_type == "Worksheet only"
    assert standard.output_type == "Worksheet only"
    assert tutor_pack.output_type == "Full Resource Pack"


def test_find_generation_preset_rejects_unknown_label() -> None:
    with pytest.raises(ValueError, match="unsupported generation preset"):
        find_generation_preset("Custom Saved Preset")
