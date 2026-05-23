# textilecalc — Python Library for Textile Engineering Calculations
# Version: 2.0.0
# Developer: Abdul Malek

# ── v1.1 core modules ──────────────────────────────────────────────────────
from .yarn import *
from .fabric import *
from .dyeing import *
from .dyeing_advanced import *
from .costing import *
from .costing_advanced import *
from .production import *
from .wastage import *
from .unit_conv import *
from .qc import *
from .spinning import *
from .weaving import *
from .testing import *

# ── v2.0 revolutionary modules ─────────────────────────────────────────────
from .yarn_recommender import (
    recommend_yarn_count,
    compare_yarn_options,
    list_end_uses,
    list_fiber_types,
)

from .shade_recipe import (
    predict_shade_recipe,
    compare_shade_accuracy,
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_lab,
    lab_to_rgb,
    delta_e,
    list_dye_classes,
)

from .carbon_footprint import (
    calculate_carbon_footprint,
    compare_fiber_footprints,
    carbon_offset_cost,
    list_fiber_types_carbon,
    list_dyeing_processes_carbon,
    list_fabric_formations,
    list_finishing_processes,
    list_countries_carbon,
)

__version__     = "2.0.0"
__author__      = "Abdul Malek"
__description__ = (
    "A complete Python library for textile engineering calculations — "
    "v2.0 adds AI-powered yarn count recommendation, shade recipe prediction, "
    "and full lifecycle carbon footprint calculation."
)
