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
        prompt, answer, problem_type, metadata, steps = _function_problem_for_difficulty(
            difficulty,
            index,
        )

        if problem_type == "evaluate" and not _validate_function_evaluation(
            metadata
        ):
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


def _function_problem_for_difficulty(
    difficulty: str,
    index: int,
) -> tuple[str, str, str, dict[str, str], tuple[str, ...]]:
    """Return function basics content for a supported difficulty."""
    normalized_difficulty = difficulty.strip().lower()

    if normalized_difficulty == "medium":
        return _medium_function_problem(index)
    if normalized_difficulty == "hard":
        return _hard_function_problem(index)
    return _function_problem(index)


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


def _medium_function_problem(
    index: int,
) -> tuple[str, str, str, dict[str, str], tuple[str, ...]]:
    """Return deterministic medium function-notation practice."""
    problem_type_index = index % 3
    sequence = index // 3

    if problem_type_index == 0:
        coefficient = sequence + 1
        constant = sequence + 2
        input_value = sequence + 2
        if coefficient == 1:
            expression = f"x**2 + x + {constant}"
        else:
            expression = f"x**2 + {coefficient}*x + {constant}"
        answer = str((input_value**2) + (coefficient * input_value) + constant)
        prompt = f"Given f(x) = {expression}, evaluate f({input_value})."
        return (
            prompt,
            answer,
            "evaluate",
            {
                "difficulty_pattern": "quadratic_evaluation",
                "function_expression": expression,
                "function_rule": expression,
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
        input_value = sequence + 3
        output_value = (input_value**2) + 1
        prompt = (
            f"In the statement h({input_value}) = {output_value}, "
            "what ordered pair is represented?"
        )
        answer = f"({input_value}, {output_value})"
        return (
            prompt,
            answer,
            "notation",
            {
                "difficulty_pattern": "ordered_pair_interpretation",
                "input_value": str(input_value),
                "output_value": str(output_value),
                "ordered_pair": answer,
            },
            (
                f"Read h({input_value}) as the output when the input is {input_value}.",
                f"The input is {input_value} and the output is {output_value}.",
                f"The ordered pair is {answer}.",
            ),
        )

    minimum_value = sequence + 2
    expression = f"sqrt(x - {minimum_value})"
    answer = f"All real numbers x >= {minimum_value}"
    prompt = f"Determine the domain of f(x) = {expression}."
    return (
        prompt,
        answer,
        "domain",
        {
            "difficulty_pattern": "square_root_domain",
            "function_expression": expression,
            "function_rule": expression,
            "domain_minimum": str(minimum_value),
            "domain_restriction": f"x >= {minimum_value}",
        },
        (
            f"Start with f(x) = {expression}.",
            "The expression inside the square root must be nonnegative.",
            f"Solve x - {minimum_value} >= 0 to get x >= {minimum_value}.",
            f"The domain is {answer}.",
        ),
    )


def _hard_function_problem(
    index: int,
) -> tuple[str, str, str, dict[str, str], tuple[str, ...]]:
    """Return deterministic hard function-notation practice."""
    problem_type_index = index % 2
    sequence = index // 2

    if problem_type_index == 0:
        outer_coefficient = sequence + 2
        outer_constant = sequence + 1
        input_value = sequence + 2
        inner_expression = "x**2"
        outer_expression = f"{outer_coefficient}*x + {outer_constant}"
        inner_value = input_value**2
        answer = str((outer_coefficient * inner_value) + outer_constant)
        prompt = (
            f"Given f(x) = {outer_expression} and g(x) = {inner_expression}, "
            f"evaluate f(g({input_value}))."
        )
        return (
            prompt,
            answer,
            "evaluate",
            {
                "difficulty_pattern": "composition_evaluation",
                "function_expression": outer_expression,
                "function_rule": outer_expression,
                "inner_function_rule": inner_expression,
                "input_value": str(input_value),
                "composition_inner_value": str(inner_value),
                "expected_value": answer,
            },
            (
                f"Start by evaluating g({input_value}) using g(x) = {inner_expression}.",
                f"g({input_value}) = {inner_value}.",
                f"Now evaluate f({inner_value}) using f(x) = {outer_expression}.",
                f"f(g({input_value})) = {answer}.",
            ),
        )

    first_exclusion = sequence + 2
    second_exclusion = -(sequence + 3)
    positive_factor = abs(second_exclusion)
    expression = f"1/((x - {first_exclusion})*(x + {positive_factor}))"
    answer = (
        f"All real numbers except x = {second_exclusion} and x = {first_exclusion}"
    )
    prompt = f"Determine the domain of f(x) = {expression}."
    return (
        prompt,
        answer,
        "domain",
        {
            "difficulty_pattern": "two_factor_denominator_domain",
            "function_expression": expression,
            "function_rule": expression,
            "domain_exclusions": f"{second_exclusion},{first_exclusion}",
            "domain_restriction": (
                f"x != {second_exclusion} and x != {first_exclusion}"
            ),
        },
        (
            f"Start with f(x) = {expression}.",
            "The denominator cannot equal zero.",
            f"Set each factor equal to zero to find x = {first_exclusion} and x = {second_exclusion}.",
            f"The domain is {answer}.",
        ),
    )


def _validate_function_evaluation(metadata: dict[str, str]) -> bool:
    """Validate a generated function evaluation problem."""
    x_symbol = Symbol("x")
    expected_value = sympify(metadata["expected_value"])

    if metadata.get("difficulty_pattern") == "composition_evaluation":
        inner_expression = sympify(metadata["inner_function_rule"])
        outer_expression = sympify(metadata["function_expression"])
        input_value = sympify(metadata["input_value"])
        inner_value = inner_expression.subs(x_symbol, input_value)
        evaluated_value = outer_expression.subs(x_symbol, inner_value)
        return simplify(evaluated_value - expected_value) == 0

    expression = sympify(metadata["function_expression"])
    input_value = sympify(metadata["input_value"])
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
