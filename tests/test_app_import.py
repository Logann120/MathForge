"""Smoke tests for the Streamlit app module."""

from collections.abc import Callable

import app.main


def test_app_main_imports_without_running_streamlit_app() -> None:
    assert isinstance(app.main.main, Callable)
    assert isinstance(app.main.generate_linear_equation_resource_pack, Callable)
    assert isinstance(app.main.export_resource_pack_to_markdown, Callable)
