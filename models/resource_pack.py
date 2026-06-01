"""Instructional resource pack models for MathForge.

These models group a generated worksheet with supporting instructional
materials. They do not depend on Streamlit, AI integrations, Canvas, exporters,
or worksheet generation.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from models.content_models import Worksheet


Metadata = Mapping[str, str]


def _require_text(value: str, field_name: str) -> None:
    """Validate that a required text field is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty.")


def _normalize_text_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    """Validate a tuple of non-empty text items."""
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings.")

    for index, value in enumerate(values):
        if not isinstance(value, str):
            raise TypeError(f"{field_name}[{index}] must be a string.")
        if not value.strip():
            raise ValueError(f"{field_name}[{index}] must not be empty.")

    return values


def _normalize_metadata(metadata: Metadata) -> Metadata:
    """Validate metadata keys and values, then return an immutable mapping."""
    if not isinstance(metadata, Mapping):
        raise TypeError("metadata must be a mapping of string keys to string values.")

    normalized: dict[str, str] = {}
    for key, value in metadata.items():
        if not isinstance(key, str):
            raise TypeError("metadata keys must be strings.")
        if not isinstance(value, str):
            raise TypeError("metadata values must be strings.")
        if not key.strip():
            raise ValueError("metadata keys must not be empty.")
        normalized[key] = value

    return MappingProxyType(normalized)


@dataclass(frozen=True, slots=True)
class StudyGuide:
    """Student-facing study guidance for a worksheet."""

    title: str
    overview: str
    key_points: tuple[str, ...] = field(default_factory=tuple)
    practice_tips: tuple[str, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.title, "title")
        _require_text(self.overview, "overview")
        object.__setattr__(
            self,
            "key_points",
            _normalize_text_tuple(self.key_points, "key_points"),
        )
        object.__setattr__(
            self,
            "practice_tips",
            _normalize_text_tuple(self.practice_tips, "practice_tips"),
        )
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class CommonMistakes:
    """Common errors and correction guidance for a worksheet topic."""

    mistakes: tuple[str, ...]
    corrections: tuple[str, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "mistakes",
            _normalize_text_tuple(self.mistakes, "mistakes"),
        )
        if not self.mistakes:
            raise ValueError("mistakes must contain at least one item.")
        object.__setattr__(
            self,
            "corrections",
            _normalize_text_tuple(self.corrections, "corrections"),
        )
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class TutorNotes:
    """Instructor- or tutor-facing notes for supporting learners."""

    notes: tuple[str, ...]
    discussion_prompts: tuple[str, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "notes", _normalize_text_tuple(self.notes, "notes"))
        if not self.notes:
            raise ValueError("notes must contain at least one item.")
        object.__setattr__(
            self,
            "discussion_prompts",
            _normalize_text_tuple(self.discussion_prompts, "discussion_prompts"),
        )
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class ResourcePack:
    """A worksheet bundled with companion instructional resources."""

    worksheet: Worksheet
    study_guide: StudyGuide
    common_mistakes: CommonMistakes
    tutor_notes: TutorNotes
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.worksheet, Worksheet):
            raise TypeError("worksheet must be a Worksheet.")
        if not isinstance(self.study_guide, StudyGuide):
            raise TypeError("study_guide must be a StudyGuide.")
        if not isinstance(self.common_mistakes, CommonMistakes):
            raise TypeError("common_mistakes must be a CommonMistakes.")
        if not isinstance(self.tutor_notes, TutorNotes):
            raise TypeError("tutor_notes must be a TutorNotes.")
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))
