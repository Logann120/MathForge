"""ZIP bundle helpers for MathForge exports."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePath
from zipfile import ZIP_DEFLATED, ZipFile

from models.content_models import ExportResult


@dataclass(frozen=True, slots=True)
class ExportBundle:
    """A downloadable ZIP archive of related export files."""

    content: bytes
    filename: str
    mime_type: str = "application/zip"


def create_export_bundle(
    exports: Sequence[ExportResult],
    *,
    bundle_filename: str | None = None,
) -> ExportBundle:
    """Create a deterministic ZIP bundle from rendered export results."""
    if not exports:
        raise ValueError("exports must contain at least one ExportResult.")

    archive = BytesIO()
    used_filenames: set[str] = set()

    with ZipFile(archive, mode="w", compression=ZIP_DEFLATED) as zip_file:
        for export in exports:
            if not isinstance(export, ExportResult):
                raise TypeError("exports must contain only ExportResult instances.")

            entry_filename = _unique_filename(
                _safe_filename(export.filename, default_name="export.txt"),
                used_filenames,
            )
            zip_file.writestr(entry_filename, export.content.encode("utf-8"))

    filename = (
        _safe_filename(bundle_filename, default_name="mathforge-export-bundle.zip")
        if bundle_filename is not None
        else _default_bundle_filename(exports[0])
    )
    if not filename.endswith(".zip"):
        filename = f"{filename}.zip"

    return ExportBundle(content=archive.getvalue(), filename=filename)


def _default_bundle_filename(export: ExportResult) -> str:
    """Return a safe bundle filename based on the first export filename."""
    base_name = _safe_filename(export.filename, default_name="mathforge-export")
    stem = base_name.rsplit(".", maxsplit=1)[0] if "." in base_name else base_name
    return f"{stem}-bundle.zip"


def _safe_filename(filename: str | None, *, default_name: str) -> str:
    """Normalize a filename so it is safe for ZIP entries and downloads."""
    if filename is None:
        return default_name

    basename = PurePath(str(filename).replace("\\", "/")).name
    safe_name = "".join(
        character.lower()
        if character.isalnum() or character in {".", "-", "_"}
        else "-"
        for character in basename.strip()
    ).strip(".-_")
    return safe_name or default_name


def _unique_filename(filename: str, used_filenames: set[str]) -> str:
    """Return a deterministic unique filename for a ZIP entry."""
    if filename not in used_filenames:
        used_filenames.add(filename)
        return filename

    stem, extension = _split_extension(filename)
    suffix = 2
    while True:
        candidate = f"{stem}-{suffix}{extension}"
        if candidate not in used_filenames:
            used_filenames.add(candidate)
            return candidate
        suffix += 1


def _split_extension(filename: str) -> tuple[str, str]:
    """Split a filename into stem and extension."""
    if "." not in filename:
        return filename, ""
    stem, extension = filename.rsplit(".", maxsplit=1)
    return stem, f".{extension}"
