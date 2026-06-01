"""Reusable dataclass models for MathForge instructional content.

The models in this module describe content shape only. They intentionally avoid
generation, symbolic validation, export rendering, Streamlit UI concerns, and
AI integration.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


Metadata = Mapping[str, str]


def _require_text(value: str, field_name: str) -> None:
    """Validate that a required field is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty.")


def _validate_optional_text(value: str | None, field_name: str) -> None:
    """Validate an optional string field when a value is provided."""
    if value is None:
        return
    _require_text(value, field_name)


def _normalize_text_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    """Validate and normalize a tuple of non-empty strings."""
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
class HintSet:
    """A reusable set of ordered hints for a math problem."""

    hints: tuple[str, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "hints", _normalize_text_tuple(self.hints, "hints"))
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class MathProblem:
    """A single math problem with prompt text and an expected answer."""

    problem_id: str
    prompt: str
    answer: str
    topic: str | None = None
    difficulty: str | None = None
    hints: HintSet | None = None
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.problem_id, "problem_id")
        _require_text(self.prompt, "prompt")
        _require_text(self.answer, "answer")
        _validate_optional_text(self.topic, "topic")
        _validate_optional_text(self.difficulty, "difficulty")

        if self.hints is not None and not isinstance(self.hints, HintSet):
            raise TypeError("hints must be a HintSet or None.")

        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class Solution:
    """A solution associated with a math problem."""

    problem_id: str
    final_answer: str
    steps: tuple[str, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.problem_id, "problem_id")
        _require_text(self.final_answer, "final_answer")
        object.__setattr__(self, "steps", _normalize_text_tuple(self.steps, "steps"))
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class Worksheet:
    """A collection of math problems and optional instructor solutions."""

    title: str
    problems: tuple[MathProblem, ...]
    worksheet_id: str | None = None
    instructions: str = ""
    solutions: tuple[Solution, ...] = field(default_factory=tuple)
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.title, "title")
        _validate_optional_text(self.worksheet_id, "worksheet_id")

        if not isinstance(self.instructions, str):
            raise TypeError("instructions must be a string.")
        if not isinstance(self.problems, tuple):
            raise TypeError("problems must be a tuple of MathProblem instances.")
        if not self.problems:
            raise ValueError("problems must contain at least one MathProblem.")
        if not isinstance(self.solutions, tuple):
            raise TypeError("solutions must be a tuple of Solution instances.")

        problem_ids: set[str] = set()
        for index, problem in enumerate(self.problems):
            if not isinstance(problem, MathProblem):
                raise TypeError(f"problems[{index}] must be a MathProblem.")
            if problem.problem_id in problem_ids:
                raise ValueError(f"duplicate problem_id: {problem.problem_id}.")
            problem_ids.add(problem.problem_id)

        for index, solution in enumerate(self.solutions):
            if not isinstance(solution, Solution):
                raise TypeError(f"solutions[{index}] must be a Solution.")
            if solution.problem_id not in problem_ids:
                raise ValueError(
                    f"solutions[{index}] references unknown problem_id: "
                    f"{solution.problem_id}."
                )

        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class ExportResult:
    """Rendered export content and related metadata.

    This model describes an export outcome but does not perform export
    rendering.
    """

    content: str
    format_name: str
    filename: str
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.content, "content")
        _require_text(self.format_name, "format_name")
        _require_text(self.filename, "filename")
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))
