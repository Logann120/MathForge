"""Built-in generation presets for the MathForge Streamlit app."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GenerationPreset:
    """Default generation settings for a common instructor workflow."""

    label: str
    description: str
    output_type: str
    generation_mode: str
    topic_label: str
    difficulty_label: str
    problem_count: int


GENERATION_PRESETS: tuple[GenerationPreset, ...] = (
    GenerationPreset(
        label="Quick Worksheet",
        description="A short worksheet for warm-ups, exit tickets, or quick review.",
        output_type="Worksheet only",
        generation_mode="Topic mode",
        topic_label="Linear equations",
        difficulty_label="Easy",
        problem_count=3,
    ),
    GenerationPreset(
        label="Standard Practice Set",
        description="A moderate worksheet for routine classroom or tutoring practice.",
        output_type="Worksheet only",
        generation_mode="Topic mode",
        topic_label="Linear equations",
        difficulty_label="Easy",
        problem_count=10,
    ),
    GenerationPreset(
        label="Full Tutor Resource Pack",
        description="A complete resource pack with instructor-facing support materials.",
        output_type="Full Resource Pack",
        generation_mode="Topic mode",
        topic_label="Linear equations",
        difficulty_label="Easy",
        problem_count=5,
    ),
)


def generation_presets() -> tuple[GenerationPreset, ...]:
    """Return built-in generation presets in UI display order."""
    return GENERATION_PRESETS


def generation_preset_labels() -> tuple[str, ...]:
    """Return user-facing preset labels in UI display order."""
    return tuple(preset.label for preset in GENERATION_PRESETS)


def find_generation_preset(label: str) -> GenerationPreset:
    """Find a generation preset by exact display label."""
    for preset in GENERATION_PRESETS:
        if preset.label == label:
            return preset
    raise ValueError(f"unsupported generation preset: {label}")
