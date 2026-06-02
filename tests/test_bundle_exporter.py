"""Tests for ZIP export bundle helpers."""

from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile

import pytest

from exporters.bundle_exporter import ExportBundle, create_export_bundle
from exporters.html_exporter import export_worksheet_to_html
from exporters.markdown_exporter import export_worksheet_to_markdown
from generator.problem_generator import generate_linear_equation_worksheet
from models.content_models import ExportResult


def test_create_export_bundle_includes_export_files() -> None:
    worksheet = generate_linear_equation_worksheet(
        topic="Linear equations",
        difficulty="easy",
        count=1,
        start_id="linear",
    )
    markdown_export = export_worksheet_to_markdown(worksheet, include_solutions=True)
    html_export = export_worksheet_to_html(worksheet, include_solutions=True)

    bundle = create_export_bundle((markdown_export, html_export))
    zip_contents = _read_zip_text(bundle.content)

    assert isinstance(bundle, ExportBundle)
    assert bundle.filename == "linear-worksheet-bundle.zip"
    assert bundle.mime_type == "application/zip"
    assert set(zip_contents) == {
        "linear-worksheet.md",
        "linear-worksheet.html",
    }
    assert zip_contents["linear-worksheet.md"] == markdown_export.content
    assert zip_contents["linear-worksheet.html"] == html_export.content


def test_create_export_bundle_sanitizes_bundle_and_entry_filenames() -> None:
    markdown_export = ExportResult(
        content="# Example\n",
        format_name="markdown",
        filename="../Unsafe Prefix/Worksheet Export.md",
    )
    html_export = ExportResult(
        content="<section>Example</section>\n",
        format_name="html",
        filename="..\\Unsafe Prefix\\Worksheet Export.html",
    )

    bundle = create_export_bundle(
        (markdown_export, html_export),
        bundle_filename="../Unsafe Prefix/Instructor Bundle!.zip",
    )
    zip_contents = _read_zip_text(bundle.content)

    assert bundle.filename == "instructor-bundle-.zip"
    assert set(zip_contents) == {
        "worksheet-export.md",
        "worksheet-export.html",
    }


def test_create_export_bundle_deduplicates_entry_filenames() -> None:
    first_export = ExportResult(
        content="first",
        format_name="markdown",
        filename="worksheet.md",
    )
    second_export = ExportResult(
        content="second",
        format_name="markdown",
        filename="worksheet.md",
    )

    bundle = create_export_bundle((first_export, second_export))
    zip_contents = _read_zip_text(bundle.content)

    assert zip_contents == {
        "worksheet.md": "first",
        "worksheet-2.md": "second",
    }


def test_create_export_bundle_rejects_empty_exports() -> None:
    with pytest.raises(ValueError, match="exports"):
        create_export_bundle(())


def test_create_export_bundle_rejects_non_export_result() -> None:
    with pytest.raises(TypeError, match="ExportResult"):
        create_export_bundle(("not an export",))


def _read_zip_text(content: bytes) -> dict[str, str]:
    """Read ZIP archive entries as UTF-8 text."""
    with ZipFile(BytesIO(content)) as zip_file:
        return {
            name: zip_file.read(name).decode("utf-8")
            for name in zip_file.namelist()
        }
