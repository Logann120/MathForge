"""Deterministic instructional resource pack generation for MathForge."""

from __future__ import annotations

from generator.problem_generator import (
    generate_factoring_techniques_worksheet,
    generate_functions_basics_worksheet,
    generate_linear_equation_worksheet,
    generate_quadratic_factoring_worksheet,
    generate_systems_of_equations_worksheet,
)
from models.content_models import Worksheet
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes
from models.resource_pack import PracticeQuiz


def generate_linear_equation_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic linear equation worksheet resource pack."""
    worksheet = generate_linear_equation_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_study_guide(topic, difficulty),
        common_mistakes=_build_common_mistakes(topic, difficulty),
        tutor_notes=_build_tutor_notes(topic, difficulty),
        practice_quiz=_build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "linear_equation_resource_pack",
        },
    )


def generate_quadratic_factoring_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic quadratic factoring worksheet resource pack."""
    worksheet = generate_quadratic_factoring_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_quadratic_study_guide(topic, difficulty),
        common_mistakes=_build_quadratic_common_mistakes(topic, difficulty),
        tutor_notes=_build_quadratic_tutor_notes(topic, difficulty),
        practice_quiz=_build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "quadratic_factoring_resource_pack",
        },
    )


def generate_systems_of_equations_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic systems of equations worksheet resource pack."""
    worksheet = generate_systems_of_equations_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_systems_study_guide(topic, difficulty),
        common_mistakes=_build_systems_common_mistakes(topic, difficulty),
        tutor_notes=_build_systems_tutor_notes(topic, difficulty),
        practice_quiz=_build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "systems_of_equations_resource_pack",
        },
    )


def generate_factoring_techniques_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic factoring techniques worksheet resource pack."""
    worksheet = generate_factoring_techniques_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_factoring_study_guide(topic, difficulty),
        common_mistakes=_build_factoring_common_mistakes(topic, difficulty),
        tutor_notes=_build_factoring_tutor_notes(topic, difficulty),
        practice_quiz=_build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "factoring_techniques_resource_pack",
        },
    )


def generate_functions_basics_resource_pack(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> ResourcePack:
    """Generate a deterministic functions basics worksheet resource pack."""
    worksheet = generate_functions_basics_worksheet(
        topic=topic,
        difficulty=difficulty,
        count=count,
        start_id=start_id,
    )

    return ResourcePack(
        worksheet=worksheet,
        study_guide=_build_functions_study_guide(topic, difficulty),
        common_mistakes=_build_functions_common_mistakes(topic, difficulty),
        tutor_notes=_build_functions_tutor_notes(topic, difficulty),
        practice_quiz=_build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "functions_basics_resource_pack",
        },
    )


def _build_practice_quiz(topic: str, worksheet: Worksheet) -> PracticeQuiz:
    """Build a deterministic practice quiz from a generated worksheet."""
    questions = tuple(
        f"Quiz question {index}: {problem.prompt}"
        for index, problem in enumerate(worksheet.problems[:3], start=1)
    )
    answer_key = tuple(
        f"{index}. {problem.answer}"
        for index, problem in enumerate(worksheet.problems[:3], start=1)
    )

    return PracticeQuiz(
        title=f"{topic} Practice Quiz",
        questions=questions + (_topic_review_question(topic),),
        answer_key=answer_key + (_topic_review_answer(topic),),
        metadata={
            "topic": topic,
            "resource_type": "practice_quiz",
            "source_worksheet_id": worksheet.worksheet_id or "",
        },
    )


def _topic_review_question(topic: str) -> str:
    """Return a deterministic conceptual quiz question for a topic."""
    normalized_topic = topic.strip().lower()

    if "quadratic" in normalized_topic:
        return "Concept check: What property is used after factoring a quadratic equation?"
    if "systems" in normalized_topic:
        return "Concept check: What does the ordered pair solution represent?"
    if "factoring" in normalized_topic:
        return "Concept check: What should you check before using a special factoring pattern?"
    if "functions" in normalized_topic:
        return "Concept check: In f(a), what does a represent?"
    return "Concept check: How can you verify that a solution is correct?"


def _topic_review_answer(topic: str) -> str:
    """Return a deterministic conceptual quiz answer for a topic."""
    normalized_topic = topic.strip().lower()

    if "quadratic" in normalized_topic:
        return "4. The zero product property."
    if "systems" in normalized_topic:
        return "4. It is the point that satisfies both equations."
    if "factoring" in normalized_topic:
        return "4. Check for a greatest common factor first."
    if "functions" in normalized_topic:
        return "4. It represents the input value."
    return "4. Substitute the solution back into the original equation."


def _build_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing guidance."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Use inverse operations to isolate x while keeping both sides of "
            "the equation balanced."
        ),
        key_points=(
            "Learning objective: solve equations of the form ax + b = c.",
            "Learning objective: explain each inverse operation used.",
            "Key idea: subtract the constant term before dividing by the coefficient.",
            "Key idea: check the answer by substituting it back into the equation.",
        ),
        practice_tips=(
            "Worked-example guidance: identify a, b, and c before solving.",
            "Worked-example guidance: subtract b from both sides.",
            "Worked-example guidance: divide both sides by a to find x.",
            "Worked-example guidance: substitute the result to verify both sides match.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_quadratic_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing quadratic factoring guidance."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Factor the quadratic, use the zero product property, and check "
            "both solutions in the original equation."
        ),
        key_points=(
            "Learning objective: solve factorable quadratic equations.",
            "Key idea: rewrite x**2 + bx + c as two binomial factors.",
            "Key idea: if a product is zero, at least one factor must be zero.",
            "Key idea: quadratic equations can have two solutions.",
        ),
        practice_tips=(
            "Worked-example guidance: identify two integers whose product is c.",
            "Worked-example guidance: confirm those integers add to b.",
            "Worked-example guidance: set each factor equal to zero.",
            "Worked-example guidance: substitute both roots to check the equation.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_functions_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing guidance for functions basics."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Function notation describes how an input value is paired with an "
            "output value according to a rule."
        ),
        key_points=(
            "Learning objective: evaluate and interpret functions using notation.",
            "Key idea: f(a) means the output when the input is a.",
            "Key idea: evaluating a function means substituting an input value.",
            "Key idea: domain restrictions come from values that make expressions undefined.",
        ),
        practice_tips=(
            "Worked-example guidance: replace every x with the given input.",
            "Worked-example guidance: read f(3) as f evaluated at 3.",
            "Worked-example guidance: check denominators for values that make zero.",
            "Worked-example guidance: state domain restrictions clearly in words.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_factoring_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing guidance for factoring techniques."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Factoring rewrites a polynomial as a product of simpler expressions "
            "without changing its value."
        ),
        key_points=(
            "Learning objective: factor polynomial expressions using common strategies.",
            "Key idea: always check for a greatest common factor first.",
            "Key idea: recognize a difference of squares as a**2 - b**2.",
            "Key idea: for x**2 + bx + c, find factors of c that add to b.",
        ),
        practice_tips=(
            "Worked-example guidance: scan for a shared numerical or variable factor.",
            "Worked-example guidance: identify perfect squares before factoring.",
            "Worked-example guidance: use a product-sum check for simple trinomials.",
            "Worked-example guidance: expand the answer to verify the factorization.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_systems_study_guide(topic: str, difficulty: str) -> StudyGuide:
    """Build deterministic student-facing guidance for systems of equations."""
    return StudyGuide(
        title=f"{topic} Study Guide",
        overview=(
            "Solve a system by finding the ordered pair that makes both "
            "linear equations true at the same time."
        ),
        key_points=(
            "Learning objective: solve systems of linear equations in two variables.",
            "Key idea: the solution is an ordered pair (x, y).",
            "Key idea: elimination can remove one variable by adding equations.",
            "Key idea: check the solution in both original equations.",
        ),
        practice_tips=(
            "Worked-example guidance: line up like variables before eliminating.",
            "Worked-example guidance: add or subtract equations to solve for one variable.",
            "Worked-example guidance: substitute the known value to find the other variable.",
            "Worked-example guidance: verify the ordered pair in both equations.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "study_guide",
        },
    )


def _build_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance."""
    return CommonMistakes(
        mistakes=(
            "Changing only one side of the equation during an inverse operation.",
            "Dividing before removing the constant term.",
            "Dropping the coefficient when rewriting ax.",
            "Not checking the final answer in the original equation.",
        ),
        corrections=(
            "Write the same operation on both sides before simplifying.",
            "Remove b first, then divide by a.",
            "Keep the coefficient attached to x until the division step.",
            "Substitute the proposed value of x into ax + b = c to confirm it works.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_quadratic_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance for factoring quadratics."""
    return CommonMistakes(
        mistakes=(
            "Choosing factors whose product is correct but whose sum is not.",
            "Finding only one solution after factoring.",
            "Forgetting to set each factor equal to zero.",
            "Losing negative signs when writing binomial factors.",
        ),
        corrections=(
            "Check both the product and the sum before writing the factors.",
            "Use the zero product property to solve both linear factors.",
            "Write a separate equation for each factor.",
            "Substitute both answers into the original quadratic equation.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_functions_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance for functions basics."""
    return CommonMistakes(
        mistakes=(
            "Treating f(x) as multiplication instead of function notation.",
            "Substituting the input into only part of the expression.",
            "Confusing the input value with the output value.",
            "Forgetting that a denominator cannot be zero.",
        ),
        corrections=(
            "Read f(x) as the value of the function at input x.",
            "Replace every occurrence of x with the input value.",
            "Identify the number inside parentheses as the input.",
            "Exclude input values that make any denominator equal zero.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_factoring_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance for factoring techniques."""
    return CommonMistakes(
        mistakes=(
            "Skipping the greatest common factor before using another strategy.",
            "Treating a sum of squares as a difference of squares.",
            "Choosing trinomial factors with the right product but wrong sum.",
            "Forgetting to check the answer by expanding.",
        ),
        corrections=(
            "Look for a shared factor before applying a special pattern.",
            "Use the difference of squares pattern only for subtraction.",
            "Check both the product and the sum for trinomial factors.",
            "Expand the factored form to confirm it matches the original expression.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_systems_common_mistakes(topic: str, difficulty: str) -> CommonMistakes:
    """Build deterministic common-mistake guidance for systems of equations."""
    return CommonMistakes(
        mistakes=(
            "Treating x and y values as separate answers instead of an ordered pair.",
            "Eliminating a variable but forgetting to solve for the second variable.",
            "Changing signs incorrectly when subtracting equations.",
            "Checking the ordered pair in only one equation.",
        ),
        corrections=(
            "Write the final answer as an ordered pair (x, y).",
            "After finding one variable, substitute it into either original equation.",
            "Keep columns aligned and distribute negative signs carefully.",
            "Substitute the ordered pair into both equations before finishing.",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "common_mistakes",
        },
    )


def _build_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts and interventions."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner to name the first inverse operation.",
            "Diagnostic question: what value is being added to or subtracted from ax?",
            "Diagnostic question: what coefficient is attached to x?",
            "Intervention suggestion: have the learner rewrite each equation as two "
            "balanced columns before simplifying.",
            "Intervention suggestion: ask the learner to verify the answer by substitution.",
        ),
        discussion_prompts=(
            "How do you know which operation to undo first?",
            "What does it mean for both sides of an equation to stay balanced?",
            "How can substitution help you catch arithmetic mistakes?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )


def _build_functions_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts for functions basics."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner to identify the input and output.",
            "Diagnostic question: what does the number inside f( ) represent?",
            "Diagnostic question: did the learner substitute into every x?",
            "Intervention suggestion: use an input-output table for notation practice.",
            "Intervention suggestion: ask what value would make a denominator zero.",
        ),
        discussion_prompts=(
            "How is f(3) different from f times 3?",
            "Why does evaluating a function require substitution?",
            "How can an expression tell you a value is outside the domain?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )


def _build_factoring_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts for factoring techniques."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner which factoring strategy fits first.",
            "Diagnostic question: is there a greatest common factor?",
            "Diagnostic question: does the expression match a special product pattern?",
            "Intervention suggestion: have the learner expand the proposed factors.",
            "Intervention suggestion: use a product-sum table for simple trinomials.",
        ),
        discussion_prompts=(
            "Why is checking for a greatest common factor a useful first step?",
            "How can expanding help verify a factorization?",
            "What clues distinguish a difference of squares from a trinomial?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )


def _build_systems_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts for systems of equations."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner what an ordered pair represents.",
            "Diagnostic question: which variable is easiest to eliminate first?",
            "Diagnostic question: did the learner check both equations?",
            "Intervention suggestion: have the learner stack equations in columns.",
            "Intervention suggestion: graph the intersection concept verbally before solving.",
        ),
        discussion_prompts=(
            "Why must the same ordered pair satisfy both equations?",
            "How does elimination reduce two equations to one variable?",
            "What can checking both equations reveal about arithmetic mistakes?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )


def _build_quadratic_tutor_notes(topic: str, difficulty: str) -> TutorNotes:
    """Build deterministic tutor-facing prompts for factoring quadratics."""
    return TutorNotes(
        notes=(
            "Tutoring prompt: ask the learner to list factor pairs for c.",
            "Diagnostic question: which pair also adds to the x coefficient?",
            "Diagnostic question: did the learner find both roots?",
            "Intervention suggestion: use a product-sum table before factoring.",
            "Intervention suggestion: have the learner check each root by substitution.",
        ),
        discussion_prompts=(
            "Why does the zero product property create two equations?",
            "How do signs in the factors affect the roots?",
            "How can checking both roots reveal a factoring error?",
        ),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "resource_type": "tutor_notes",
        },
    )
