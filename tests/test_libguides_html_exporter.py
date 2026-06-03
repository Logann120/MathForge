"""Tests for LibGuides-safe HTML exports."""

import re

import pytest

from exporters.html_exporter import export_worksheet_to_html
from exporters.libguides_html_exporter import (
    export_resource_pack_to_libguides_html,
    export_worksheet_to_libguides_html,
)
from generator.problem_generator import generate_linear_equation_worksheet
from generator.resource_pack_generator import generate_linear_equation_resource_pack
from models.content_models import ExportResult, MathProblem, Worksheet


def test_export_worksheet_to_libguides_html_returns_export_result() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_worksheet_to_libguides_html(worksheet)

    assert isinstance(result, ExportResult)
    assert result.format_name == "libguides_html"
    assert result.filename == "linear-worksheet-libguides.html"
    assert result.metadata["resource_type"] == "worksheet"
    assert result.metadata["topic"] == "Linear equations"
    assert result.metadata["problem_id_prefix"] == "linear"


def test_libguides_worksheet_uses_wrapper_and_no_h1_or_h2() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=2,
        start_id="linear",
    )

    result = export_worksheet_to_libguides_html(
        worksheet,
        include_solutions=True,
    )

    assert '<div class="mathforge-libguides-export"' in result.content
    assert 'data-mathforge-export="worksheet"' in result.content
    assert "<h1" not in result.content
    assert "<h2" not in result.content
    assert '<h3 class="mathforge-lg-title">Linear equations Worksheet</h3>' in (
        result.content
    )
    assert '<h4 class="mathforge-lg-heading">Instructions</h4>' in result.content
    assert '<h4 class="mathforge-lg-heading">Problems</h4>' in result.content
    assert '<h4 class="mathforge-lg-heading">Solution Key</h4>' in result.content
    assert "Solve for x: 2*x + 1 = 3" in result.content
    assert "<strong>Answer:</strong> 1" in result.content


def test_libguides_css_is_scoped_to_mathforge_wrapper() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_worksheet_to_libguides_html(worksheet)
    styles = _style_blocks(result.content)

    assert styles
    for selector in _css_selectors("\n".join(styles)):
        assert selector.startswith(".mathforge-libguides-export")
        assert selector not in {"body", "h1", "h2", "section", "p"}


def test_libguides_resource_pack_includes_expected_sections() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_resource_pack_to_libguides_html(resource_pack)

    assert result.format_name == "libguides_html"
    assert result.filename == "linear-worksheet-libguides-resource-pack.html"
    assert result.metadata["resource_type"] == "resource_pack"
    assert 'data-mathforge-export="resource-pack"' in result.content
    assert "<h1" not in result.content
    assert "<h2" not in result.content
    assert '<h3 class="mathforge-lg-title">Study Guide</h3>' in result.content
    assert '<h3 class="mathforge-lg-title">Common Mistakes</h3>' in result.content
    assert '<h3 class="mathforge-lg-title">Tutor Notes</h3>' in result.content
    assert '<h3 class="mathforge-lg-title">Practice Quiz</h3>' in result.content
    assert "Linear equations Practice Quiz" in result.content


def test_libguides_resource_pack_can_omit_solution_key() -> None:
    resource_pack = generate_linear_equation_resource_pack(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    result = export_resource_pack_to_libguides_html(
        resource_pack,
        include_solutions=False,
    )

    assert "Solution Key" not in result.content
    assert result.metadata["include_solutions"] == "False"


def test_libguides_html_escapes_html_sensitive_text() -> None:
    problem = MathProblem(
        problem_id="p1",
        prompt='Solve <x> & "show work".',
        answer="1",
    )
    worksheet = Worksheet(title="Practice <One>", problems=(problem,))

    result = export_worksheet_to_libguides_html(worksheet)

    assert "Practice &lt;One&gt;" in result.content
    assert "Solve &lt;x&gt; &amp; &quot;show work&quot;." in result.content


def test_libguides_exports_are_deterministic() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=2,
        start_id="linear",
    )

    first = export_worksheet_to_libguides_html(worksheet, include_solutions=True)
    second = export_worksheet_to_libguides_html(worksheet, include_solutions=True)

    assert first == second


def test_standard_html_export_remains_separate_from_libguides_export() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )

    standard_result = export_worksheet_to_html(worksheet, include_solutions=True)
    libguides_result = export_worksheet_to_libguides_html(
        worksheet,
        include_solutions=True,
    )

    assert standard_result.format_name == "html"
    assert standard_result.filename == "linear-worksheet.html"
    assert '<section class="mathforge-worksheet">' in standard_result.content
    assert "@media print" in standard_result.content
    assert '<div class="mathforge-libguides-export"' not in standard_result.content
    assert "@media print" not in libguides_result.content
    assert "page-break-before" not in libguides_result.content
    assert standard_result.content != libguides_result.content


def test_libguides_exporters_reject_invalid_inputs() -> None:
    with pytest.raises(TypeError, match="worksheet must be a Worksheet"):
        export_worksheet_to_libguides_html("not a worksheet")

    with pytest.raises(TypeError, match="resource_pack must be a ResourcePack"):
        export_resource_pack_to_libguides_html("not a resource pack")


def _style_blocks(content: str) -> list[str]:
    """Return style tag contents from an HTML fragment."""
    return re.findall(r"<style>(.*?)</style>", content, flags=re.DOTALL)


def _css_selectors(style_content: str) -> list[str]:
    """Return individual CSS selectors from simple style blocks."""
    selectors: list[str] = []
    for raw_selector in re.findall(r"([^{}]+)\{", style_content):
        selectors.extend(
            selector.strip()
            for selector in raw_selector.split(",")
            if selector.strip()
        )
    return selectors
