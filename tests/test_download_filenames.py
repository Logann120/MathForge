"""Tests for instructor-friendly download filenames."""

from __future__ import annotations

import pytest

from exporters.download_filenames import (
    build_bundle_download_filename,
    build_export_download_filename,
    sanitize_filename_part,
    with_download_filename,
)
from models.content_models import ExportResult


def test_build_export_download_filename_includes_context_type_prefix_and_format() -> None:
    export = ExportResult(
        content="# Worksheet\n",
        format_name="markdown",
        filename="linear-worksheet.md",
        metadata={
            "topic": "Linear equations",
            "resource_type": "worksheet",
            "problem_id_prefix": "linear",
        },
    )

    assert (
        build_export_download_filename(export)
        == "mathforge-linear-equations-worksheet-linear-markdown.md"
    )


def test_build_resource_pack_download_filename_uses_learning_objective_context() -> None:
    export = ExportResult(
        content="<section>Resource Pack</section>\n",
        format_name="html",
        filename="linear-worksheet-resource-pack.html",
        metadata={
            "topic": "Linear equations",
            "learning_objective": "Solve linear equations in one variable",
            "resource_type": "resource_pack",
            "problem_id_prefix": "linear",
        },
    )

    assert (
        build_export_download_filename(export)
        == (
            "mathforge-solve-linear-equations-in-one-variable-resource-pack-"
            "linear-html.html"
        )
    )


def test_build_bundle_download_filename_includes_bundle_format() -> None:
    export = ExportResult(
        content="# Worksheet\n",
        format_name="markdown",
        filename="worksheet.md",
        metadata={
            "topic": "Factoring techniques",
            "resource_type": "worksheet",
            "problem_id_prefix": "Unit 1 / Week 2!",
        },
    )

    assert (
        build_bundle_download_filename(export)
        == "mathforge-factoring-techniques-worksheet-unit-1-week-2-bundle.zip"
    )


def test_build_canvas_csv_download_filename_uses_csv_extension() -> None:
    export = ExportResult(
        content="question_title,question_prompt\n",
        format_name="canvas_csv",
        filename="linear-worksheet-worksheet-canvas.csv",
        metadata={
            "topic": "Linear equations",
            "resource_type": "worksheet",
            "problem_id_prefix": "linear",
        },
    )

    assert (
        build_export_download_filename(export)
        == "mathforge-linear-equations-worksheet-linear-canvas-csv.csv"
    )


def test_sanitize_filename_part_handles_spaces_punctuation_case_and_paths() -> None:
    assert (
        sanitize_filename_part(
            "..\\Unit 1/Functions: Basics?!",
            default="fallback",
        )
        == "unit-1-functions-basics"
    )
    assert sanitize_filename_part("   ", default="fallback") == "fallback"


def test_build_download_filename_trims_overly_long_context() -> None:
    export = ExportResult(
        content="# Worksheet\n",
        format_name="markdown",
        filename="worksheet.md",
        metadata={
            "topic": "A very long topic name " * 8,
            "resource_type": "worksheet",
            "problem_id_prefix": "long-prefix",
        },
    )

    filename = build_export_download_filename(export)

    assert filename.endswith(".md")
    assert len(filename) <= 120


def test_with_download_filename_preserves_export_content_and_metadata() -> None:
    export = ExportResult(
        content="# Worksheet\n",
        format_name="markdown",
        filename="old-name.md",
        metadata={
            "topic": "Systems of linear equations",
            "resource_type": "worksheet",
            "problem_id_prefix": "systems",
        },
    )

    renamed_export = with_download_filename(export)

    assert renamed_export.content == export.content
    assert renamed_export.format_name == export.format_name
    assert renamed_export.metadata == export.metadata
    assert renamed_export.filename == (
        "mathforge-systems-of-linear-equations-worksheet-systems-markdown.md"
    )


def test_download_filename_helpers_reject_non_export_result() -> None:
    with pytest.raises(TypeError, match="ExportResult"):
        build_export_download_filename("not an export")

    with pytest.raises(TypeError, match="ExportResult"):
        build_bundle_download_filename("not an export")

    with pytest.raises(TypeError, match="ExportResult"):
        with_download_filename("not an export")
