# textilecalc/carbon_footprint.py
# Module: Textile Carbon Footprint & Sustainability Calculator
# Author: Abdul Malek | Version: 2.0.0
#
# Calculates CO₂ equivalent emissions across the full textile production
# lifecycle — from raw fiber to finished fabric — with process-level
# breakdowns, water footprint, and sustainability rating.
#
# Emission factors sourced from:
#   - Higg Materials Sustainability Index (Higg MSI)
#   - Textile Exchange Preferred Fiber Reports
#   - IPCC emission factor databases
#   - EU JRC Reference Document on Textile Industries (BREF)

import math
from utils.validator import validate_positive, validate_non_negative


# ─────────────────────────────────────────────────────────────────────────────
# Emission factor databases
# ─────────────────────────────────────────────────────────────────────────────

# Fiber production: kg CO₂e per kg of fiber produced
_FIBER_CO2_KG = {
    "cotton":             5.90,   # conventional cotton (pesticide + irrigation)
    "organic_cotton":     3.75,   # organic cotton (no synthetic pesticides)
    "recycled_cotton":    1.20,   # mechanically recycled
    "polyester":          9.52,   # virgin polyester (fossil-based)
    "recycled_polyester": 3.80,   # rPET from plastic bottles
    "viscose":            4.74,   # standard viscose/rayon
    "modal":              3.56,   # modal (closed-loop Lenzing process)
    "tencel":             1.97,   # TENCEL Lyocell (closed-loop, certified)
    "linen":              1.70,   # flax linen (low irrigation, no pesticide)
    "hemp":               1.10,   # hemp (no pesticide, rain-fed)
    "wool":              36.00,   # merino wool (methane from sheep)
    "recycled_wool":      4.30,   # mechanically recycled wool
    "silk":              19.50,   # conventional silk (sericulture)
    "nylon":             14.50,   # nylon 6/6 (fossil-based)
    "recycled_nylon":     5.90,   # recycled nylon (e.g. Econyl)
    "acrylic":           10.30,   # acrylic fiber
    "bamboo":             3.50,   # bamboo viscose (closed-loop)
    "lyocell":            1.97,   # same as tencel (generic lyocell)
}

# Water footprint: litres per kg of fiber
_FIBER_WATER_L_KG = {
    "cotton":             10000,
    "organic_cotton":      8000,
    "recycled_cotton":      700,
    "polyester":            125,
    "recycled_polyester":    60,
    "viscose":             3000,
    "modal":               1700,
    "tencel":               700,
    "linen":               2400,
    "hemp":                1100,
    "wool":               100000,
    "recycled_wool":        800,
    "silk":               26000,
    "nylon":                170,
    "recycled_nylon":        85,
    "acrylic":              200,
    "bamboo":              2700,
    "lyocell":              700,
}

# Process emission factors
# Spinning: kg CO₂e per kg of yarn (energy only; fiber already counted separately)
_SPINNING_CO2_KG_YARN = {
    "ring":         2.10,  # ring spinning (most common, high twist)
    "open_end":     1.20,  # OE/rotor spinning (lower energy, coarser yarn)
    "air_jet":      1.80,  # air-jet spinning
    "compact":      2.30,  # compact ring spinning
}

# Weaving/knitting: kg CO₂e per kg of fabric
_FABRIC_FORMATION_CO2 = {
    "weaving_rapier":     1.60,
    "weaving_airjet":     1.40,
    "weaving_waterjet":   1.20,
    "weaving_projectile": 1.80,
    "weaving_shuttle":    2.50,
    "knitting_circular":  0.90,
    "knitting_warp":      1.10,
    "knitting_flat":      1.30,
}

# Dyeing & finishing: kg CO₂e per kg of fabric
_DYEING_CO2_KG = {
    "reactive_exhaust":   4.50,  # reactive dyeing — standard exhaust
    "reactive_cold_pad":  2.20,  # cold pad-batch (lower energy)
    "disperse_hthp":      5.80,  # disperse HTHP (high temp)
    "disperse_thermosol": 4.80,  # thermosol continuous
    "acid_exhaust":       3.60,  # acid dyeing
    "vat_exhaust":        5.20,  # vat dyeing
    "direct_exhaust":     3.20,  # direct dyeing
    "pigment_padding":    1.80,  # pigment + binder (low water)
    "natural_dye":        2.10,  # natural dye (fermentation + mordant)
    "undyed":             0.10,  # bleach only / white
}

# Finishing processes: kg CO₂e per kg of fabric (additive)
_FINISHING_CO2_KG = {
    "none":              0.00,
    "mercerizing":       0.80,
    "sanforizing":       0.40,
    "calendering":       0.30,
    "raising_napping":   0.50,
    "coating":           1.20,
    "water_repellent":   0.70,
    "flame_retardant":   1.50,
    "softener_only":     0.20,
}

# Electricity CO₂e: kg CO₂e per kWh (by country/region grid mix)
_GRID_EMISSION_KG_KWH = {
    "bangladesh":  0.622,
    "india":       0.708,
    "china":       0.555,
    "vietnam":     0.464,
    "turkey":      0.400,
    "pakistan":    0.455,
    "indonesia":   0.761,
    "eu_average":  0.231,
    "uk":          0.193,
    "usa":         0.386,
    "global_avg":  0.475,
}

# Transport: kg CO₂e per tonne·km
_TRANSPORT_CO2_TONNE_KM = {
    "sea_freight":    0.010,
    "air_freight":    0.602,
    "road_hgv":       0.085,
    "rail":           0.027,
}

# Rating thresholds: kg CO₂e per kg of finished fabric
_RATING_THRESHOLDS = [
    (8,   "A+", "Exceptional — Industry-leading sustainability"),
    (12,  "A",  "Excellent — Well above industry average"),
    (18,  "B",  "Good — Above average sustainability"),
    (25,  "C",  "Average — Meets basic industry standard"),
    (35,  "D",  "Below average — Significant improvement recommended"),
    (float("inf"), "E", "Poor — High carbon intensity, major redesign needed"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Core calculator
# ─────────────────────────────────────────────────────────────────────────────

def calculate_carbon_footprint(
    fiber_type,
    fabric_weight_kg,
    spinning_method="ring",
    fabric_formation="weaving_rapier",
    dyeing_process="reactive_exhaust",
    finishing="softener_only",
    country="global_avg",
    electricity_kwh_per_kg_extra=0.0,
    transport_mode="sea_freight",
    transport_distance_km=5000.0,
    include_breakdown=True,
):
    """
    Calculate the full lifecycle carbon footprint of textile production.

    Covers: fiber production → spinning → fabric formation → dyeing &
    finishing → transport. Returns CO₂e in kg per kg of finished fabric,
    a water footprint, and a sustainability rating (A+ to E).

    Args:
        fiber_type            (str):   Fiber type. See list_fiber_types_carbon().
        fabric_weight_kg      (float): Weight of finished fabric in kg.
        spinning_method       (str):   'ring', 'open_end', 'air_jet', 'compact'.
        fabric_formation      (str):   Weaving/knitting process. See list_fabric_formations().
        dyeing_process        (str):   Dyeing method. See list_dyeing_processes_carbon().
        finishing             (str):   Finishing treatment. See list_finishing_processes().
        country               (str):   Production country (determines grid emission factor).
                                       See list_countries_carbon().
        electricity_kwh_per_kg_extra (float):
                                       Any additional electricity consumption (kWh/kg)
                                       not captured by process factors (default: 0).
        transport_mode        (str):   'sea_freight', 'air_freight', 'road_hgv', 'rail'.
        transport_distance_km (float): Distance from factory to buyer in km.
        include_breakdown     (bool):  Include per-stage breakdown in output.

    Returns:
        dict: Carbon footprint report containing:
            - total_co2e_kg_per_kg   (float): Total kg CO₂e per kg of fabric
            - total_co2e_kg          (float): Total kg CO₂e for the batch
            - water_footprint_L      (float): Water used (litres) for the batch
            - sustainability_rating  (str):   'A+' to 'E'
            - rating_description     (str):   Human-readable rating note
            - breakdown_kg_per_kg    (dict):  Stage-by-stage CO₂e (if requested)
            - reduction_tips         (list):  Actionable recommendations
            - comparison             (dict):  vs industry avg and best-in-class

    Raises:
        ValueError: If unknown fiber, process, or country is provided.

    Example:
        >>> result = calculate_carbon_footprint(
        ...     'cotton', 500,
        ...     spinning_method='open_end',
        ...     dyeing_process='reactive_cold_pad',
        ...     country='bangladesh'
        ... )
        >>> print(result['total_co2e_kg_per_kg'])
        15.3
        >>> print(result['sustainability_rating'])
        'B'
    """
    validate_positive(fabric_weight_kg, "Fabric Weight (kg)")
    validate_non_negative(electricity_kwh_per_kg_extra, "Extra Electricity (kWh/kg)")
    validate_positive(transport_distance_km, "Transport Distance (km)")

    fiber_type      = fiber_type.lower().strip()
    spinning_method = spinning_method.lower().strip()
    country         = country.lower().strip()
    transport_mode  = transport_mode.lower().strip()
    finishing       = finishing.lower().strip()

    # Validation
    def _check(value, table, name):
        if value not in table:
            raise ValueError(
                f"Unknown {name} '{value}'. Valid options: {', '.join(sorted(table))}"
            )
    _check(fiber_type,      _FIBER_CO2_KG,            "fiber_type")
    _check(spinning_method, _SPINNING_CO2_KG_YARN,     "spinning_method")
    _check(fabric_formation,_FABRIC_FORMATION_CO2,     "fabric_formation")
    _check(dyeing_process,  _DYEING_CO2_KG,            "dyeing_process")
    _check(finishing,       _FINISHING_CO2_KG,         "finishing")
    _check(country,         _GRID_EMISSION_KG_KWH,     "country")
    _check(transport_mode,  _TRANSPORT_CO2_TONNE_KM,   "transport_mode")

    grid = _GRID_EMISSION_KG_KWH[country]

    # ── Stage emissions (kg CO₂e per kg finished fabric) ──
    fiber_co2      = _FIBER_CO2_KG[fiber_type]
    spinning_co2   = _SPINNING_CO2_KG_YARN[spinning_method]
    formation_co2  = _FABRIC_FORMATION_CO2[fabric_formation]
    dyeing_co2     = _DYEING_CO2_KG[dyeing_process]
    finishing_co2  = _FINISHING_CO2_KG[finishing]

    # Extra electricity (e.g. air conditioning, compressed air, lighting)
    extra_co2      = electricity_kwh_per_kg_extra * grid

    # Transport: convert kg to tonnes, calculate tonne·km
    transport_co2  = round(
        (_TRANSPORT_CO2_TONNE_KM[transport_mode] * transport_distance_km * fabric_weight_kg) / 1000,
        4
    )  # total kg CO₂e (not per-kg)
    transport_co2_per_kg = transport_co2 / fabric_weight_kg

    total_per_kg = round(
        fiber_co2 + spinning_co2 + formation_co2 +
        dyeing_co2 + finishing_co2 + extra_co2 + transport_co2_per_kg,
        3
    )
    total_batch  = round(total_per_kg * fabric_weight_kg, 2)

    # ── Water footprint ──
    water_L = round(_FIBER_WATER_L_KG[fiber_type] * fabric_weight_kg, 0)

    # ── Sustainability rating ──
    rating_label = "E"
    rating_desc  = ""
    for threshold, label, desc in _RATING_THRESHOLDS:
        if total_per_kg <= threshold:
            rating_label = label
            rating_desc  = desc
            break

    # ── Breakdown ──
    breakdown = None
    if include_breakdown:
        breakdown = {
            "1_fiber_production_kg_CO2e_per_kg":    round(fiber_co2, 3),
            "2_spinning_kg_CO2e_per_kg":            round(spinning_co2, 3),
            "3_fabric_formation_kg_CO2e_per_kg":    round(formation_co2, 3),
            "4_dyeing_kg_CO2e_per_kg":              round(dyeing_co2, 3),
            "5_finishing_kg_CO2e_per_kg":           round(finishing_co2, 3),
            "6_extra_electricity_kg_CO2e_per_kg":   round(extra_co2, 3),
            "7_transport_kg_CO2e_per_kg":           round(transport_co2_per_kg, 4),
        }

    # ── Reduction tips ──
    tips = []
    if fiber_co2 > 10:
        recycled = f"recycled_{fiber_type}" if f"recycled_{fiber_type}" in _FIBER_CO2_KG else None
        if recycled:
            saving = round(fiber_co2 - _FIBER_CO2_KG[recycled], 2)
            tips.append(
                f"Switch to {recycled.replace('_',' ')} — saves ~{saving} kg CO₂e/kg "
                f"({round(saving/fiber_co2*100)}% less from fiber stage)."
            )
        elif fiber_type == "wool":
            tips.append("Wool has a very high footprint (methane). Consider blending with recycled wool or alternative fibers.")
    if dyeing_co2 > 4.0:
        tips.append(
            "Switch to cold pad-batch reactive dyeing or pigment dyeing to reduce "
            "dyeing stage CO₂e by 40–60%."
        )
    if grid > 0.5:
        tips.append(
            f"The {country} grid emits {grid} kg CO₂e/kWh. Installing solar or purchasing "
            "renewable energy certificates (RECs) can cut process energy emissions by up to 80%."
        )
    if transport_mode == "air_freight":
        saving_sea = round(
            (transport_co2 - (_TRANSPORT_CO2_TONNE_KM["sea_freight"] * transport_distance_km * fabric_weight_kg / 1000)),
            1
        )
        tips.append(
            f"Air freight emits 60× more than sea freight. Switching saves ~{saving_sea} kg CO₂e for this batch."
        )
    if spinning_method in ("ring", "compact"):
        tips.append("Open-end spinning uses ~40% less energy than ring spinning for coarser yarn counts.")
    if not tips:
        tips.append("Excellent choices across all stages. Consider third-party certification (GOTS, bluesign, Higg).")

    # ── Industry comparison ──
    cotton_reactive_avg = (
        _FIBER_CO2_KG["cotton"] +
        _SPINNING_CO2_KG_YARN["ring"] +
        _FABRIC_FORMATION_CO2["weaving_rapier"] +
        _DYEING_CO2_KG["reactive_exhaust"] +
        _FINISHING_CO2_KG["softener_only"] +
        _TRANSPORT_CO2_TONNE_KM["sea_freight"] * 5000 * 1 / 1000
    )
    best_class = (
        _FIBER_CO2_KG["tencel"] +
        _SPINNING_CO2_KG_YARN["open_end"] +
        _FABRIC_FORMATION_CO2["knitting_circular"] +
        _DYEING_CO2_KG["pigment_padding"] +
        _FINISHING_CO2_KG["none"] +
        _TRANSPORT_CO2_TONNE_KM["rail"] * 1000 * 1 / 1000
    )

    return {
        "fiber_type":              fiber_type,
        "fabric_weight_kg":        fabric_weight_kg,
        "total_co2e_kg_per_kg":    total_per_kg,
        "total_co2e_kg":           total_batch,
        "water_footprint_L":       int(water_L),
        "water_footprint_L_per_kg": int(water_L / fabric_weight_kg),
        "sustainability_rating":   rating_label,
        "rating_description":      rating_desc,
        "breakdown_kg_per_kg":     breakdown,
        "reduction_tips":          tips,
        "comparison": {
            "your_footprint_kg_per_kg":        total_per_kg,
            "industry_avg_cotton_reactive":    round(cotton_reactive_avg, 2),
            "best_in_class_estimate":          round(best_class, 2),
            "vs_industry_avg_pct":             round((total_per_kg - cotton_reactive_avg) / cotton_reactive_avg * 100, 1),
            "vs_best_class_pct":               round((total_per_kg - best_class) / best_class * 100, 1),
        }
    }


def compare_fiber_footprints(fabric_weight_kg=100.0):
    """
    Compare carbon and water footprints of all supported fibers
    at the fiber production stage only.

    Useful for fiber selection decisions early in product development.

    Args:
        fabric_weight_kg (float): Batch weight in kg for absolute values.

    Returns:
        list of dict: Sorted by CO₂e ascending (lowest first), containing
                      'fiber', 'co2e_kg_per_kg', 'co2e_kg_total',
                      'water_L_per_kg', 'water_L_total', 'rating'.

    Example:
        >>> fibers = compare_fiber_footprints(500)
        >>> for f in fibers[:3]:
        ...     print(f['fiber'], f['co2e_kg_per_kg'])
    """
    validate_positive(fabric_weight_kg, "Fabric Weight (kg)")
    results = []
    for fiber, co2 in sorted(_FIBER_CO2_KG.items(), key=lambda x: x[1]):
        water = _FIBER_WATER_L_KG.get(fiber, 0)
        rating = "E"
        for t, lbl, _ in _RATING_THRESHOLDS:
            if co2 <= t:
                rating = lbl
                break
        results.append({
            "fiber":            fiber,
            "co2e_kg_per_kg":   co2,
            "co2e_kg_total":    round(co2 * fabric_weight_kg, 1),
            "water_L_per_kg":   water,
            "water_L_total":    water * fabric_weight_kg,
            "fiber_stage_rating": rating,
        })
    return results


def carbon_offset_cost(total_co2e_kg, price_per_tonne_usd=15.0):
    """
    Calculate the cost to offset a batch's carbon emissions via carbon credits.

    Args:
        total_co2e_kg       (float): Total CO₂ equivalent in kg.
        price_per_tonne_usd (float): Carbon credit price per tonne CO₂e
                                     (default: $15 USD — voluntary market avg).

    Returns:
        dict: Containing 'offset_cost_usd', 'tonnes_co2e', 'price_per_tonne_usd'.

    Example:
        >>> carbon_offset_cost(2500, 20)
        {'tonnes_co2e': 2.5, 'offset_cost_usd': 50.0, ...}
    """
    validate_positive(total_co2e_kg, "CO₂e (kg)")
    validate_positive(price_per_tonne_usd, "Price per tonne USD")
    tonnes = round(total_co2e_kg / 1000, 4)
    cost   = round(tonnes * price_per_tonne_usd, 2)
    return {
        "tonnes_co2e":          tonnes,
        "offset_cost_usd":      cost,
        "price_per_tonne_usd":  price_per_tonne_usd,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Discovery helpers
# ─────────────────────────────────────────────────────────────────────────────

def list_fiber_types_carbon():
    """Return all supported fibers with their CO₂e and water factors."""
    return [
        {"fiber": k, "co2e_kg_per_kg": v, "water_L_per_kg": _FIBER_WATER_L_KG.get(k, "N/A")}
        for k, v in sorted(_FIBER_CO2_KG.items(), key=lambda x: x[1])
    ]

def list_dyeing_processes_carbon():
    """Return all supported dyeing processes with their CO₂e factors."""
    return [{"process": k, "co2e_kg_per_kg": v} for k, v in sorted(_DYEING_CO2_KG.items(), key=lambda x: x[1])]

def list_fabric_formations():
    """Return all supported fabric formation processes with their CO₂e factors."""
    return [{"process": k, "co2e_kg_per_kg": v} for k, v in sorted(_FABRIC_FORMATION_CO2.items(), key=lambda x: x[1])]

def list_finishing_processes():
    """Return all supported finishing processes with their CO₂e factors."""
    return [{"process": k, "co2e_kg_per_kg": v} for k, v in sorted(_FINISHING_CO2_KG.items(), key=lambda x: x[1])]

def list_countries_carbon():
    """Return all supported countries with their electricity grid emission factors."""
    return [{"country": k, "kg_co2e_per_kwh": v} for k, v in sorted(_GRID_EMISSION_KG_KWH.items(), key=lambda x: x[1])]
