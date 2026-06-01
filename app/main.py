"""Minimal Streamlit interface for MathForge worksheet generation."""

from __future__ import annotations

from typing import Any

from exporters.html_exporter import export_worksheet_to_html
from exporters.markdown_exporter import export_worksheet_to_markdown
from generator.problem_generator import generate_linear_equation_worksheet
from models.content_models import Solution, Worksheet


def main() -> None:
    """Run the MathForge Streamlit application."""
    import streamlit as st

    st.set_page_config(page_title="MathForge", page_icon="M")
    st.title("MathForge")
    st.subheader("Linear equation worksheet generator")

    topic = st.text_input("Topic", value="Linear equations")
    difficulty = st.text_input("Difficulty", value="easy")
    count = st.number_input("Problem count", min_value=1, max_value=50, value=5, step=1)
    start_id = st.text_input("Start ID", value="linear")

    if st.button("Generate worksheet", type="primary"):
        try:
            worksheet = generate_linear_equation_worksheet(
                topic=topic,
                difficulty=difficulty,
                count=int(count),
                start_id=start_id,
            )
        except (TypeError, ValueError) as exc:
            st.error(str(exc))
            return

        _render_worksheet(st, worksheet)


def _render_worksheet(st: Any, worksheet: Worksheet) -> None:
    """Render previews and exports for a generated worksheet."""
    st.divider()
    st.header("Worksheet Preview")
    st.write(worksheet.instructions)

    for index, problem in enumerate(worksheet.problems, start=1):
        st.write(f"{index}. {problem.prompt}")

    st.header("Solution Key Preview")
    solutions_by_problem_id = {
        solution.problem_id: solution for solution in worksheet.solutions
    }

    for index, problem in enumerate(worksheet.problems, start=1):
        solution = solutions_by_problem_id.get(problem.problem_id)
        if solution is None:
            st.write(f"{index}. No solution provided.")
            continue
        _render_solution(st, index, solution)

    markdown_export = export_worksheet_to_markdown(worksheet, include_solutions=True)
    html_export = export_worksheet_to_html(worksheet, include_solutions=True)

    st.header("Exports")
    st.download_button(
        label="Download Markdown",
        data=markdown_export.content,
        file_name=markdown_export.filename,
        mime="text/markdown",
    )
    st.download_button(
        label="Download HTML",
        data=html_export.content,
        file_name=html_export.filename,
        mime="text/html",
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


def _render_solution(st: Any, index: int, solution: Solution) -> None:
    """Render one solution preview entry."""
    st.write(f"{index}. Answer: {solution.final_answer}")
    for step in solution.steps:
        st.write(f"   - {step}")


if __name__ == "__main__":
    main()
