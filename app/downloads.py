"""Download and export controls for the MathForge Streamlit app."""

from __future__ import annotations

from typing import Any

from app.generation_context import (
    GenerationContext,
    WorksheetSummary,
    generated_output_summary_lines,
)
from exporters.bundle_exporter import create_export_bundle
from exporters.canvas_exporter import (
    export_resource_pack_quiz_to_canvas_csv,
    export_worksheet_to_canvas_csv,
)
from exporters.download_filenames import (
    build_bundle_download_filename,
    with_download_filename,
)
from exporters.html_exporter import export_resource_pack_to_html, export_worksheet_to_html
from exporters.libguides_html_exporter import (
    export_resource_pack_to_libguides_html,
    export_worksheet_to_libguides_html,
)
from exporters.markdown_exporter import (
    export_resource_pack_to_markdown,
    export_worksheet_to_markdown,
)
from models.content_models import Worksheet
from models.resource_pack import ResourcePack


def render_worksheet_exports(
    st: Any,
    worksheet: Worksheet,
    generation_context: GenerationContext,
) -> None:
    """Render worksheet export controls."""
    markdown_export = export_worksheet_to_markdown(worksheet, include_solutions=True)
    html_export = export_worksheet_to_html(worksheet, include_solutions=True)
    libguides_html_export = export_worksheet_to_libguides_html(
        worksheet,
        include_solutions=True,
    )
    canvas_export = export_worksheet_to_canvas_csv(worksheet)

    markdown_download = with_download_filename(markdown_export)
    html_download = with_download_filename(html_export)
    libguides_html_download = with_download_filename(libguides_html_export)
    canvas_download = with_download_filename(canvas_export)
    export_bundle = create_export_bundle(
        (markdown_download, html_download),
        bundle_filename=build_bundle_download_filename(markdown_download),
    )

    st.header("Exports")
    _render_generated_output_summary(
        st,
        output_type="Worksheet",
        worksheet=WorksheetSummary.from_export(markdown_download),
        generation_context=generation_context,
        markdown_filename=markdown_download.filename,
        html_filename=html_download.filename,
        libguides_html_filename=libguides_html_download.filename,
        bundle_filename=export_bundle.filename,
        canvas_filename=canvas_download.filename,
    )
    st.download_button(
        label="Download Worksheet Markdown",
        data=markdown_download.content,
        file_name=markdown_download.filename,
        mime="text/markdown",
    )
    st.download_button(
        label="Download Worksheet HTML",
        data=html_download.content,
        file_name=html_download.filename,
        mime="text/html",
    )
    st.download_button(
        label="Download Worksheet LibGuides-Safe HTML",
        data=libguides_html_download.content,
        file_name=libguides_html_download.filename,
        mime="text/html",
    )
    st.download_button(
        label="Download Worksheet Export Bundle",
        data=export_bundle.content,
        file_name=export_bundle.filename,
        mime=export_bundle.mime_type,
    )
    st.download_button(
        label="Download Worksheet Canvas Manual-Entry CSV",
        data=canvas_download.content,
        file_name=canvas_download.filename,
        mime="text/csv",
    )

    with st.expander("Markdown export text"):
        st.text_area(
            "Markdown",
            value=markdown_export.content,
            height=260,
            label_visibility="collapsed",
        )

    with st.expander("HTML export text"):
        st.text_area(
            "HTML",
            value=html_export.content,
            height=260,
            label_visibility="collapsed",
        )

    with st.expander("LibGuides-safe HTML export text"):
        st.text_area(
            "LibGuides-Safe HTML",
            value=libguides_html_export.content,
            height=260,
            label_visibility="collapsed",
        )

    with st.expander("Canvas manual-entry CSV text"):
        st.text_area(
            "Canvas Manual-Entry CSV",
            value=canvas_export.content,
            height=220,
            label_visibility="collapsed",
        )


def render_resource_pack_exports(
    st: Any,
    resource_pack: ResourcePack,
    generation_context: GenerationContext,
) -> None:
    """Render resource pack export controls."""
    markdown_export = export_resource_pack_to_markdown(
        resource_pack,
        include_solutions=True,
    )
    html_export = export_resource_pack_to_html(
        resource_pack,
        include_solutions=True,
    )
    libguides_html_export = export_resource_pack_to_libguides_html(
        resource_pack,
        include_solutions=True,
    )
    canvas_export = (
        export_resource_pack_quiz_to_canvas_csv(resource_pack)
        if resource_pack.practice_quiz is not None
        else None
    )

    markdown_download = with_download_filename(markdown_export)
    html_download = with_download_filename(html_export)
    libguides_html_download = with_download_filename(libguides_html_export)
    canvas_download = (
        with_download_filename(canvas_export)
        if canvas_export is not None
        else None
    )
    export_bundle = create_export_bundle(
        (markdown_download, html_download),
        bundle_filename=build_bundle_download_filename(markdown_download),
    )

    st.header("Resource Pack Export")
    _render_generated_output_summary(
        st,
        output_type="Full Resource Pack",
        worksheet=WorksheetSummary.from_export(markdown_download),
        generation_context=generation_context,
        markdown_filename=markdown_download.filename,
        html_filename=html_download.filename,
        libguides_html_filename=libguides_html_download.filename,
        bundle_filename=export_bundle.filename,
        canvas_filename=canvas_download.filename if canvas_download else "",
    )
    st.download_button(
        label="Download Resource Pack Markdown",
        data=markdown_download.content,
        file_name=markdown_download.filename,
        mime="text/markdown",
    )
    st.download_button(
        label="Download Resource Pack HTML",
        data=html_download.content,
        file_name=html_download.filename,
        mime="text/html",
    )
    st.download_button(
        label="Download Resource Pack LibGuides-Safe HTML",
        data=libguides_html_download.content,
        file_name=libguides_html_download.filename,
        mime="text/html",
    )
    st.download_button(
        label="Download Resource Pack Export Bundle",
        data=export_bundle.content,
        file_name=export_bundle.filename,
        mime=export_bundle.mime_type,
    )
    if canvas_download is not None:
        st.download_button(
            label="Download Resource Pack Canvas Manual-Entry Quiz CSV",
            data=canvas_download.content,
            file_name=canvas_download.filename,
            mime="text/csv",
        )

    with st.expander("Resource pack Markdown export text"):
        st.text_area(
            "Resource Pack Markdown",
            value=markdown_export.content,
            height=320,
            label_visibility="collapsed",
        )

    with st.expander("Resource pack HTML export text"):
        st.text_area(
            "Resource Pack HTML",
            value=html_export.content,
            height=320,
            label_visibility="collapsed",
        )

    with st.expander("Resource pack LibGuides-safe HTML export text"):
        st.text_area(
            "Resource Pack LibGuides-Safe HTML",
            value=libguides_html_export.content,
            height=320,
            label_visibility="collapsed",
        )

    if canvas_export is not None:
        with st.expander("Resource pack Canvas manual-entry quiz CSV text"):
            st.text_area(
                "Resource Pack Canvas Manual-Entry Quiz CSV",
                value=canvas_export.content,
                height=220,
                label_visibility="collapsed",
            )


def _render_generated_output_summary(
    st: Any,
    *,
    output_type: str,
    worksheet: WorksheetSummary,
    generation_context: GenerationContext,
    markdown_filename: str,
    html_filename: str,
    bundle_filename: str,
    libguides_html_filename: str = "",
    canvas_filename: str = "",
) -> None:
    """Render a compact summary of generated output and downloads."""
    st.subheader("Generated Output Summary")
    st.markdown(
        "\n".join(
            generated_output_summary_lines(
                output_type=output_type,
                worksheet=worksheet,
                generation_context=generation_context,
                markdown_filename=markdown_filename,
                html_filename=html_filename,
                libguides_html_filename=libguides_html_filename,
                bundle_filename=bundle_filename,
                canvas_filename=canvas_filename,
            )
        )
    )
