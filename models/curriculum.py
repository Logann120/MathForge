"""Curriculum alignment models for MathForge."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


Metadata = Mapping[str, str]


def _require_text(value: str, field_name: str) -> None:
    """Validate that a required text field is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty.")


def _normalize_text_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    """Validate a tuple of non-empty text values."""
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
class LearningObjective:
    """A single curriculum-aligned learning objective."""

    objective_id: str
    description: str
    topic: str
    standards: tuple[str, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.objective_id, "objective_id")
        _require_text(self.description, "description")
        _require_text(self.topic, "topic")
        object.__setattr__(
            self,
            "standards",
            _normalize_text_tuple(self.standards, "standards"),
        )
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class CourseModule:
    """A course module containing one or more learning objectives."""

    module_id: str
    title: str
    learning_objectives: tuple[LearningObjective, ...]
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.module_id, "module_id")
        _require_text(self.title, "title")

        if not isinstance(self.learning_objectives, tuple):
            raise TypeError(
                "learning_objectives must be a tuple of LearningObjective instances."
            )
        if not self.learning_objectives:
            raise ValueError("learning_objectives must contain at least one item.")

        objective_ids: set[str] = set()
        for index, objective in enumerate(self.learning_objectives):
            if not isinstance(objective, LearningObjective):
                raise TypeError(
                    f"learning_objectives[{index}] must be a LearningObjective."
                )
            if objective.objective_id in objective_ids:
                raise ValueError(f"duplicate objective_id: {objective.objective_id}.")
            objective_ids.add(objective.objective_id)

        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class CourseTemplate:
    """A reusable course template composed of curriculum modules."""

    course_id: str
    title: str
    modules: tuple[CourseModule, ...]
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.course_id, "course_id")
        _require_text(self.title, "title")

        if not isinstance(self.modules, tuple):
            raise TypeError("modules must be a tuple of CourseModule instances.")
        if not self.modules:
            raise ValueError("modules must contain at least one CourseModule.")

        module_ids: set[str] = set()
        for index, module in enumerate(self.modules):
            if not isinstance(module, CourseModule):
                raise TypeError(f"modules[{index}] must be a CourseModule.")
            if module.module_id in module_ids:
                raise ValueError(f"duplicate module_id: {module.module_id}.")
            module_ids.add(module.module_id)

        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))
