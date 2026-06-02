"""Download filename helpers for rendered MathForge exports."""

from __future__ import annotations

from dataclasses import replace
import re

from models.content_models import ExportResult


MAX_FILENAME_LENGTH = 120
FORMAT_EXTENSIONS = {
    "canvas_csv": "csv",
    "html": "html",
    "markdown": "md",
}


def with_download_filename(export: ExportResult) -> ExportResult:
    """Return an export result with an instructor-friendly download filename."""
    if not isinstance(export, ExportResult):
        raise TypeError("export must be an ExportResult.")
    return replace(export, filename=build_export_download_filename(export))


def build_export_download_filename(export: ExportResult) -> str:
    """Build a deterministic download filename from export metadata."""
    if not isinstance(export, ExportResult):
        raise TypeError("export must be an ExportResult.")

    extension = _extension_for_export(export)
    base_name = _join_filename_parts(
        "mathforge",
        _context_part(export),
        _output_type_part(export),
        export.metadata.get("problem_id_prefix", ""),
        _format_part(export),
    )
    return _trim_filename(base_name, extension)


def build_bundle_download_filename(export: ExportResult) -> str:
    """Build a deterministic ZIP bundle filename from export metadata."""
    if not isinstance(export, ExportResult):
        raise TypeError("export must be an ExportResult.")

    base_name = _join_filename_parts(
        "mathforge",
        _context_part(export),
        _output_type_part(export),
        export.metadata.get("problem_id_prefix", ""),
        "bundle",
    )
    return _trim_filename(base_name, "zip")


def sanitize_filename_part(
    value: str | None,
    *,
    default: str,
    max_length: int = 48,
) -> str:
    """Sanitize one filename segment for deterministic downloads."""
    if value is None:
        return default

    normalized = str(value).strip().lower()
    safe_part = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    if not safe_part:
        return default

    return safe_part[:max_length].strip("-") or default


def _context_part(export: ExportResult) -> str:
    """Return the topic or learning-objective context segment."""
    return (
        export.metadata.get("learning_objective")
        or export.metadata.get("topic")
        or export.metadata.get("worksheet_id")
        or export.filename
    )


def _output_type_part(export: ExportResult) -> str:
    """Return the worksheet/resource-pack segment."""
    resource_type = export.metadata.get("resource_type", "worksheet")
    if resource_type == "resource_pack":
        return "resource-pack"
    return "worksheet"


def _format_part(export: ExportResult) -> str:
    """Return the format segment for a rendered export."""
    if export.format_name == "canvas_csv":
        return "canvas-csv"
    if export.format_name == "markdown":
        return "markdown"
    if export.format_name == "html":
        return "html"
    return export.format_name


def _extension_for_export(export: ExportResult) -> str:
    """Return the file extension for an export result."""
    if export.format_name in FORMAT_EXTENSIONS:
        return FORMAT_EXTENSIONS[export.format_name]

    if "." in export.filename:
        return sanitize_filename_part(
            export.filename.rsplit(".", maxsplit=1)[1],
            default="txt",
            max_length=12,
        )
    return "txt"


def _join_filename_parts(*parts: str) -> str:
    """Join non-empty filename segments with hyphens."""
    safe_parts = [
        sanitize_filename_part(part, default="", max_length=48)
        for part in parts
        if part
    ]
    return "-".join(part for part in safe_parts if part) or "mathforge-export"


def _trim_filename(base_name: str, extension: str) -> str:
    """Trim a filename while preserving its extension."""
    safe_extension = sanitize_filename_part(extension, default="txt", max_length=12)
    max_base_length = MAX_FILENAME_LENGTH - len(safe_extension) - 1
    safe_base_name = sanitize_filename_part(
        base_name,
        default="mathforge-export",
        max_length=max_base_length,
    )
    return f"{safe_base_name}.{safe_extension}"
