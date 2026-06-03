"""Supported College Algebra topic registry for MathForge.

The registry centralizes topic labels, default identifiers, generator routing,
and curriculum metadata. It is intentionally small and explicit; it is not a
plugin system.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from generator.problem_generator import (
    generate_factoring_techniques_worksheet,
    generate_functions_basics_worksheet,
    generate_linear_equation_worksheet,
    generate_quadratic_factoring_worksheet,
    generate_systems_of_equations_worksheet,
)
from generator.resource_pack_generator import (
    generate_factoring_techniques_resource_pack,
    generate_functions_basics_resource_pack,
    generate_linear_equation_resource_pack,
    generate_quadratic_factoring_resource_pack,
    generate_systems_of_equations_resource_pack,
)
from models.content_models import Worksheet
from models.resource_pack import ResourcePack

WorksheetGenerator = Callable[[str, str, int, str], Worksheet]
ResourcePackGenerator = Callable[[str, str, int, str], ResourcePack]


@dataclass(frozen=True)
class SupportedTopic:
    """Metadata and routing for one supported MathForge topic."""

    slug: str
    display_label: str
    default_problem_id_prefix: str
    supported_output_types: tuple[str, ...]
    worksheet_generator: WorksheetGenerator
    resource_pack_generator: ResourcePackGenerator
    supported_difficulty_levels: tuple[str, ...]
    curriculum_course: str
    curriculum_module_id: str
    curriculum_module_title: str
    curriculum_objective_id: str
    curriculum_objective_description: str
    curriculum_standards: tuple[str, ...]
    # Aliases are exact normalized matches for curriculum objective topics.
    # Avoid broad phrases that could accidentally route a future topic.
    topic_aliases: tuple[str, ...]


SUPPORTED_TOPICS: tuple[SupportedTopic, ...] = (
    SupportedTopic(
        slug="linear-equations",
        display_label="Linear equations",
        default_problem_id_prefix="linear",
        supported_output_types=("worksheet", "resource_pack"),
        worksheet_generator=generate_linear_equation_worksheet,
        resource_pack_generator=generate_linear_equation_resource_pack,
        supported_difficulty_levels=("easy", "medium", "hard"),
        curriculum_course="College Algebra",
        curriculum_module_id="college-algebra-linear-equations",
        curriculum_module_title="Linear Equations",
        curriculum_objective_id="college-algebra-linear-equations-001",
        curriculum_objective_description="Solve linear equations in one variable",
        curriculum_standards=("College Algebra: Linear Equations",),
        topic_aliases=(
            "linear equation",
            "linear equations",
            "linear equations in one variable",
        ),
    ),
    SupportedTopic(
        slug="quadratic-equations-by-factoring",
        display_label="Quadratic equations by factoring",
        default_problem_id_prefix="quadratic",
        supported_output_types=("worksheet", "resource_pack"),
        worksheet_generator=generate_quadratic_factoring_worksheet,
        resource_pack_generator=generate_quadratic_factoring_resource_pack,
        supported_difficulty_levels=("easy", "medium", "hard"),
        curriculum_course="College Algebra",
        curriculum_module_id="college-algebra-quadratic-equations",
        curriculum_module_title="Quadratic Equations",
        curriculum_objective_id="college-algebra-quadratic-factoring-001",
        curriculum_objective_description="Solve quadratic equations by factoring",
        curriculum_standards=("College Algebra: Quadratic Equations by Factoring",),
        topic_aliases=(
            "quadratic equation",
            "quadratic equations",
            "quadratic equations by factoring",
            "factoring quadratic equations",
        ),
    ),
    SupportedTopic(
        slug="systems-of-linear-equations",
        display_label="Systems of linear equations",
        default_problem_id_prefix="systems",
        supported_output_types=("worksheet", "resource_pack"),
        worksheet_generator=generate_systems_of_equations_worksheet,
        resource_pack_generator=generate_systems_of_equations_resource_pack,
        supported_difficulty_levels=("easy",),
        curriculum_course="College Algebra",
        curriculum_module_id="college-algebra-systems-equations",
        curriculum_module_title="Systems of Equations",
        curriculum_objective_id="college-algebra-systems-equations-001",
        curriculum_objective_description=(
            "Solve systems of linear equations in two variables"
        ),
        curriculum_standards=("College Algebra: Systems of Linear Equations",),
        topic_aliases=(
            "systems of equations",
            "systems of linear equations",
            "systems of linear equations in two variables",
        ),
    ),
    SupportedTopic(
        slug="factoring-techniques",
        display_label="Factoring techniques",
        default_problem_id_prefix="factoring",
        supported_output_types=("worksheet", "resource_pack"),
        worksheet_generator=generate_factoring_techniques_worksheet,
        resource_pack_generator=generate_factoring_techniques_resource_pack,
        supported_difficulty_levels=("easy",),
        curriculum_course="College Algebra",
        curriculum_module_id="college-algebra-factoring-techniques",
        curriculum_module_title="Factoring Techniques",
        curriculum_objective_id="college-algebra-factoring-techniques-001",
        curriculum_objective_description=(
            "Factor polynomial expressions using common factoring strategies"
        ),
        curriculum_standards=("College Algebra: Factoring Techniques",),
        topic_aliases=(
            "factoring",
            "factoring techniques",
            "factoring polynomial expressions",
        ),
    ),
    SupportedTopic(
        slug="functions-basics",
        display_label="Functions basics",
        default_problem_id_prefix="functions",
        supported_output_types=("worksheet", "resource_pack"),
        worksheet_generator=generate_functions_basics_worksheet,
        resource_pack_generator=generate_functions_basics_resource_pack,
        supported_difficulty_levels=("easy",),
        curriculum_course="College Algebra",
        curriculum_module_id="college-algebra-functions",
        curriculum_module_title="Functions",
        curriculum_objective_id="college-algebra-functions-001",
        curriculum_objective_description=(
            "Evaluate and interpret functions using function notation"
        ),
        curriculum_standards=("College Algebra: Functions",),
        topic_aliases=(
            "functions",
            "functions basics",
            "function notation",
            "introductory functions",
        ),
    ),
)


def supported_topics() -> tuple[SupportedTopic, ...]:
    """Return supported topics in UI display order."""
    return SUPPORTED_TOPICS


def supported_topic_labels() -> tuple[str, ...]:
    """Return user-facing topic labels in UI display order."""
    return tuple(topic.display_label for topic in SUPPORTED_TOPICS)


def find_topic_by_label(label: str) -> SupportedTopic:
    """Find a supported topic by its exact display label."""
    normalized_label = _normalize(label)
    for topic in SUPPORTED_TOPICS:
        if _normalize(topic.display_label) == normalized_label:
            return topic
    raise ValueError(f"unsupported topic: {label}")


def find_topic_by_slug(slug: str) -> SupportedTopic:
    """Find a supported topic by slug."""
    normalized_slug = _normalize(slug)
    for topic in SUPPORTED_TOPICS:
        if _normalize(topic.slug) == normalized_slug:
            return topic
    raise ValueError(f"unsupported topic slug: {slug}")


def find_topic_by_learning_objective_topic(topic_text: str) -> SupportedTopic:
    """Find a supported topic from curriculum learning-objective topic text."""
    normalized_topic = _normalize(topic_text)
    for topic in SUPPORTED_TOPICS:
        aliases = (topic.display_label, *topic.topic_aliases)
        if any(_normalize(alias) == normalized_topic for alias in aliases):
            return topic
    raise ValueError(f"unsupported learning objective topic: {topic_text}")


def _normalize(value: str) -> str:
    """Normalize topic lookup text."""
    return value.strip().lower()
