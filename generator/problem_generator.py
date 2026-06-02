"""Public worksheet generator API for MathForge.

Topic-specific implementation lives in ``generator.topics``. This module keeps
the original public import paths stable for the app, registry, tests, examples,
and external callers.
"""

from __future__ import annotations

from generator.topics.factoring_techniques import (
    generate_factoring_techniques_worksheet,
)
from generator.topics.functions_basics import generate_functions_basics_worksheet
from generator.topics.linear_equations import generate_linear_equation_worksheet
from generator.topics.quadratic_equations import (
    generate_quadratic_factoring_worksheet,
)
from generator.topics.systems_of_equations import (
    generate_systems_of_equations_worksheet,
)

__all__ = [
    "generate_factoring_techniques_worksheet",
    "generate_functions_basics_worksheet",
    "generate_linear_equation_worksheet",
    "generate_quadratic_factoring_worksheet",
    "generate_systems_of_equations_worksheet",
]
