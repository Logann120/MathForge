"""Deterministic functions-basics generators for MathForge."""

from __future__ import annotations

from sympy import Symbol, simplify, sympify

from models.content_models import MathProblem, Solution, Worksheet
from models.resource_pack import CommonMistakes, ResourcePack, StudyGuide, TutorNotes

from .common import build_practice_quiz, require_positive_count, require_text


def generate_functions_basics_worksheet(
    topic: str,
    difficulty: str,
    count: int,
    start_id: str,
) -> Worksheet:
    """Generate deterministic introductory function-notation practice."""
    require_text(topic, "topic")
    require_text(difficulty, "difficulty")
    require_text(start_id, "start_id")
    require_positive_count(count)

    problems: list[MathProblem] = []
    solutions: list[Solution] = []

    for index in range(count):
        problem_id = f"{start_id}-{index + 1:03d}"
        prompt, answer, problem_type, metadata, steps = _function_problem(index)

        if problem_type == "evaluate" and not _validate_function_evaluation(metadata):
            raise ValueError(
                f"generated function evaluation failed validation for {problem_id}."
            )

        problems.append(
            MathProblem(
                problem_id=problem_id,
                prompt=prompt,
                answer=answer,
                topic=topic,
                difficulty=difficulty,
                metadata={
                    **metadata,
                    "problem_type": problem_type,
                    "variable": "x",
                },
            )
        )
        solutions.append(
            Solution(
                problem_id=problem_id,
                final_answer=answer,
                steps=steps,
            )
        )

    return Worksheet(
        title=f"{topic} Worksheet",
        worksheet_id=f"{start_id}-worksheet",
        instructions="Evaluate and interpret each function notation problem.",
        problems=tuple(problems),
        solutions=tuple(solutions),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "functions_basics",
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
        practice_quiz=build_practice_quiz(topic, worksheet),
        metadata={
            "topic": topic,
            "difficulty": difficulty,
            "generator": "functions_basics_resource_pack",
        },
    )


def _function_problem(
    index: int,
) -> tuple[str, str, str, dict[str, str], tuple[str, ...]]:
    """Return a deterministic function basics problem."""
    problem_type_index = index % 3
    sequence = index // 3

    if problem_type_index == 0:
        coefficient = sequence + 2
        constant = sequence + 1
        input_value = sequence + 3
        expression = f"{coefficient}*x + {constant}"
        answer = str((coefficient * input_value) + constant)
        prompt = f"Given f(x) = {expression}, evaluate f({input_value})."
        return (
            prompt,
            answer,
            "evaluate",
            {
                "function_expression": expression,
                "input_value": str(input_value),
                "expected_value": answer,
            },
            (
                f"Start with f(x) = {expression}.",
                f"Substitute x = {input_value}.",
                f"Evaluate to get f({input_value}) = {answer}.",
            ),
        )

    if problem_type_index == 1:
        input_value = sequence + 4
        output_value = (2 * input_value) + 1
        prompt = (
            f"In the statement f({input_value}) = {output_value}, "
            f"what does {input_value} represent?"
        )
        answer = "The input value"
        return (
            prompt,
            answer,
            "notation",
            {
                "input_value": str(input_value),
                "output_value": str(output_value),
            },
            (
                f"Read f({input_value}) as the output of f when x = {input_value}.",
                f"The value {input_value} is the input.",
                f"The value {output_value} is the output.",
            ),
        )

    excluded_value = sequence + 2
    expression = f"1/(x - {excluded_value})"
    answer = f"All real numbers except x = {excluded_value}"
    prompt = f"Determine the domain of f(x) = {expression}."
    return (
        prompt,
        answer,
        "domain",
        {
            "function_expression": expression,
            "excluded_value": str(excluded_value),
        },
        (
            f"Start with f(x) = {expression}.",
            "The denominator cannot equal zero.",
            f"Exclude x = {excluded_value} from the domain.",
            f"The domain is {answer}.",
        ),
    )


def _validate_function_evaluation(metadata: dict[str, str]) -> bool:
    """Validate a generated function evaluation problem."""
    x_symbol = Symbol("x")
    expression = sympify(metadata["function_expression"])
    input_value = sympify(metadata["input_value"])
    expected_value = sympify(metadata["expected_value"])
    return simplify(expression.subs(x_symbol, input_value) - expected_value) == 0


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
