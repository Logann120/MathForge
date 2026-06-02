"""Deterministic course templates for MathForge."""

from __future__ import annotations

from models.curriculum import CourseModule, CourseTemplate, LearningObjective
from topics.registry import SupportedTopic, supported_topics


def college_algebra_template() -> CourseTemplate:
    """Return the deterministic College Algebra sample course template."""
    return CourseTemplate(
        course_id="college-algebra",
        title="College Algebra",
        modules=tuple(_module_from_topic(topic) for topic in supported_topics()),
        metadata={"level": "community_college"},
    )


def _module_from_topic(topic: SupportedTopic) -> CourseModule:
    """Build a College Algebra course module from topic registry metadata."""
    objective = LearningObjective(
        objective_id=topic.curriculum_objective_id,
        description=topic.curriculum_objective_description,
        topic=topic.display_label,
        standards=topic.curriculum_standards,
        metadata={
            "course": topic.curriculum_course,
            "module": topic.curriculum_module_title,
        },
    )
    return CourseModule(
        module_id=topic.curriculum_module_id,
        title=topic.curriculum_module_title,
        learning_objectives=(objective,),
        metadata={"course": topic.curriculum_course},
    )
