"""Snapshot-style regression tests for representative exports."""

from __future__ import annotations

import re
from textwrap import dedent

from exporters.html_exporter import (
    export_resource_pack_to_html,
    export_worksheet_to_html,
)
from exporters.markdown_exporter import (
    export_resource_pack_to_markdown,
    export_worksheet_to_markdown,
)
from generator.problem_generator import generate_linear_equation_worksheet
from generator.resource_pack_generator import generate_linear_equation_resource_pack


def test_linear_worksheet_markdown_export_snapshot() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="snapshot-linear",
    )

    result = export_worksheet_to_markdown(worksheet, include_solutions=True)

    assert result.filename == "snapshot-linear-worksheet.md"
    assert result.metadata["worksheet_id"] == "snapshot-linear-worksheet"
    assert worksheet.problems[0].problem_id == "snapshot-linear-001"
    assert result.content == dedent(
        """\
        # Linear equations Worksheet

        ## Instructions

        Solve each equation for x.

        ## Problems

        1. Solve for x: 2\\*x + 1 = 3

        ## Solution Key

        1. Answer: 1

           - Start with 2\\*x + 1 = 3.
           - Subtract 1 from both sides.
           - Divide both sides by 2.
           - x = 1.
        """
    )


def test_linear_worksheet_html_export_snapshot() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="snapshot-linear",
    )

    result = export_worksheet_to_html(worksheet, include_solutions=True)

    assert result.filename == "snapshot-linear-worksheet.html"
    assert result.metadata["worksheet_id"] == "snapshot-linear-worksheet"
    assert worksheet.problems[0].problem_id == "snapshot-linear-001"
    assert "<h1" not in result.content
    assert result.content == dedent(
        """\
        <section class="mathforge-worksheet">
          <h2>Linear equations Worksheet</h2>
          <section class="mathforge-instructions">
            <h3>Instructions</h3>
            <p>Solve each equation for x.</p>
          </section>
          <section class="mathforge-problems">
            <h3>Problems</h3>
            <ol>
              <li>Solve for x: 2*x + 1 = 3</li>
            </ol>
          </section>
          <section class="mathforge-solution-key">
            <h3>Solution Key</h3>
            <ol>
              <li>
                <p><strong>Answer:</strong> 1</p>
                <ol>
                  <li>Start with 2*x + 1 = 3.</li>
                  <li>Subtract 1 from both sides.</li>
                  <li>Divide both sides by 2.</li>
                  <li>x = 1.</li>
                </ol>
              </li>
            </ol>
          </section>
        </section>
        """
    )


def test_linear_resource_pack_markdown_export_structural_snapshot() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="snapshot-linear-pack",
    )

    result = export_resource_pack_to_markdown(resource_pack, include_solutions=True)

    assert result.filename == "snapshot-linear-pack-worksheet-resource-pack.md"
    assert result.metadata["worksheet_id"] == "snapshot-linear-pack-worksheet"
    assert resource_pack.worksheet.problems[0].problem_id == "snapshot-linear-pack-001"
    assert _markdown_headings(result.content) == (
        "# Linear equations Worksheet",
        "## Instructions",
        "## Problems",
        "## Solution Key",
        "## Study Guide",
        "### Linear equations Study Guide",
        "#### Key Ideas",
        "#### Worked-Example Guidance",
        "## Common Mistakes",
        "### Mistakes to Watch For",
        "### Corrections and Interventions",
        "## Tutor Notes",
        "### Notes",
        "### Discussion Prompts",
        "## Practice Quiz",
        "### Linear equations Practice Quiz",
        "#### Questions",
        "#### Answer Key",
    )
    assert "1. Solve for x: 2\\*x + 1 = 3" in result.content
    assert "1. Answer: 1" in result.content
    assert "- Learning objective: solve equations of the form ax + b = c." in result.content
    assert "- Changing only one side of the equation" in result.content
    assert "- Tutoring prompt: ask the learner" in result.content
    assert "1. Quiz question 1: Solve for x: 2\\*x + 1 = 3" in result.content
    assert "- 4. Substitute the solution back into the original equation." in result.content


def test_linear_resource_pack_html_export_structural_snapshot() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="snapshot-linear-pack",
    )

    result = export_resource_pack_to_html(resource_pack, include_solutions=True)

    assert result.filename == "snapshot-linear-pack-worksheet-resource-pack.html"
    assert result.metadata["worksheet_id"] == "snapshot-linear-pack-worksheet"
    assert resource_pack.worksheet.problems[0].problem_id == "snapshot-linear-pack-001"
    assert "<h1" not in result.content
    assert _html_section_classes(result.content) == (
        "mathforge-resource-pack",
        "mathforge-worksheet",
        "mathforge-instructions",
        "mathforge-problems",
        "mathforge-solution-key",
        "mathforge-study-guide",
        "mathforge-common-mistakes",
        "mathforge-tutor-notes",
        "mathforge-practice-quiz",
    )
    assert _html_headings(result.content) == (
        "Linear equations Worksheet",
        "Instructions",
        "Problems",
        "Solution Key",
        "Study Guide",
        "Linear equations Study Guide",
        "Key Ideas",
        "Worked-Example Guidance",
        "Common Mistakes",
        "Mistakes to Watch For",
        "Corrections and Interventions",
        "Tutor Notes",
        "Notes",
        "Discussion Prompts",
        "Practice Quiz",
        "Linear equations Practice Quiz",
        "Questions",
        "Answer Key",
    )
    assert "<li>Solve for x: 2*x + 1 = 3</li>" in result.content
    assert "<strong>Answer:</strong> 1" in result.content
    assert "<li>Learning objective: solve equations of the form ax + b = c.</li>" in result.content
    assert "<li>Changing only one side of the equation" in result.content
    assert "<li>Tutoring prompt: ask the learner" in result.content
    assert "<li>Quiz question 1: Solve for x: 2*x + 1 = 3</li>" in result.content
    assert (
        "<li>4. Substitute the solution back into the original equation.</li>"
        in result.content
    )


def _markdown_headings(content: str) -> tuple[str, ...]:
    """Return Markdown headings in exported order."""
    return tuple(line for line in content.splitlines() if line.startswith("#"))


def _html_section_classes(content: str) -> tuple[str, ...]:
    """Return semantic section classes in exported order."""
    return tuple(re.findall(r'<section class="([^"]+)">', content))


def _html_headings(content: str) -> tuple[str, ...]:
    """Return h2/h3 headings in exported order."""
    return tuple(re.findall(r"<h[23]>(.*?)</h[23]>", content))
