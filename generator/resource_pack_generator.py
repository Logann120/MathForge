"""Public resource-pack generator API for MathForge.

Topic-specific implementation lives in ``generator.topics``. This module keeps
the original public import paths stable for the app, registry, tests, examples,
and external callers.
"""

from __future__ import annotations

from generator.topics.factoring_techniques import (
    generate_factoring_techniques_resource_pack,
)
from generator.topics.functions_basics import generate_functions_basics_resource_pack
from generator.topics.linear_equations import generate_linear_equation_resource_pack
from generator.topics.quadratic_equations import (
    generate_quadratic_factoring_resource_pack,
)
from generator.topics.systems_of_equations import (
    generate_systems_of_equations_resource_pack,
)

__all__ = [
    "generate_factoring_techniques_resource_pack",
    "generate_functions_basics_resource_pack",
    "generate_linear_equation_resource_pack",
    "generate_quadratic_factoring_resource_pack",
    "generate_systems_of_equations_resource_pack",
]
