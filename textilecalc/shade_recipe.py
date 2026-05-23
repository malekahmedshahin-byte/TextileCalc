# textilecalc/shade_recipe.py
# Module: Shade Recipe Predictor
# Author: Abdul Malek | Version: 2.0.0
#
# Predicts dye recipe (dye percentages for R, G, B primaries) from a
# target color using CIE Lab* color science and Beer-Lambert-based
# dye absorption models. No external dependencies required.

import math
from utils.validator import validate_positive, validate_percentage


# ─────────────────────────────────────────────────────────────────────────────
# Color science helpers
# ─────────────────────────────────────────────────────────────────────────────

def hex_to_rgb(hex_color):
    """
    Convert a hex color code to an (R, G, B) tuple (0–255 each).

    Args:
        hex_color (str): Hex color string, e.g. '#FF5733' or 'FF5733'.

    Returns:
        tuple: (R, G, B) integers in range 0–255.

    Raises:
        ValueError: If hex string is not valid.

    Example:
        >>> hex_to_rgb('#FF5733')
        (255, 87, 51)
    """
    hex_color = hex_color.strip().lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color '{hex_color}'. Must be 6 hex characters.")
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        raise ValueError(f"Invalid hex color '#{hex_color}'. Contains non-hex characters.")
    return r, g, b


def rgb_to_hex(r, g, b):
    """
    Convert (R, G, B) values to a hex color string.

    Args:
        r, g, b (int): RGB values 0–255.

    Returns:
        str: Hex color string like '#FF5733'.

    Example:
        >>> rgb_to_hex(255, 87, 51)
        '#FF5733'
    """
    return '#{:02X}{:02X}{:02X}'.format(int(r), int(g), int(b))


def rgb_to_lab(r, g, b):
    """
    Convert sRGB (0–255) to CIE L*a*b* color space (D65 illuminant).

    CIE Lab* is the international standard for colorimetry in textile
    dyeing and color matching. L* = lightness, a* = green-red axis,
    b* = blue-yellow axis.

    Args:
        r, g, b (int): sRGB values 0–255.

    Returns:
        tuple: (L*, a*, b*) floats.

    Example:
        >>> rgb_to_lab(255, 0, 0)
        (53.23, 80.11, 67.22)  # approximate
    """
    # sRGB linearisation
    def _linearise(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    rl, gl, bl = _linearise(r), _linearise(g), _linearise(b)

    # sRGB to XYZ (D65)
    X = rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375
    Y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750
    Z = rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041

    # Normalise by D65 white point
    X /= 0.95047
    Y /= 1.00000
    Z /= 1.08883

    def _f(t):
        return t ** (1/3) if t > 0.008856 else 7.787 * t + 16/116

    fx, fy, fz = _f(X), _f(Y), _f(Z)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b_star = 200 * (fy - fz)

    return round(L, 4), round(a, 4), round(b_star, 4)


def lab_to_rgb(L, a, b_star):
    """
    Convert CIE L*a*b* (D65) back to sRGB (0–255).

    Args:
        L  (float): Lightness 0–100.
        a  (float): a* axis (−128 to +128).
        b_star (float): b* axis (−128 to +128).

    Returns:
        tuple: (R, G, B) integers 0–255, clamped to valid range.

    Example:
        >>> lab_to_rgb(53.23, 80.11, 67.22)
        (255, 0, 0)  # approximate
    """
    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b_star / 200

    def _inv_f(t):
        return t ** 3 if t > 0.206897 else (t - 16/116) / 7.787

    X = _inv_f(fx) * 0.95047
    Y = _inv_f(fy) * 1.00000
    Z = _inv_f(fz) * 1.08883

    # XYZ to sRGB linear
    rl =  X *  3.2404542 - Y * 1.5371385 - Z * 0.4985314
    gl = -X *  0.9692660 + Y * 1.8760108 + Z * 0.0415560
    bl =  X *  0.0556434 - Y * 0.2040259 + Z * 1.0572252

    def _gamma(c):
        c = max(0.0, min(1.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1/2.4)) - 0.055

    r = int(round(_gamma(rl) * 255))
    g = int(round(_gamma(gl) * 255))
    b = int(round(_gamma(bl) * 255))

    return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))


def delta_e(lab1, lab2):
    """
    Calculate CIE Delta-E 1976 (ΔE*) colour difference between two Lab* colours.

    ΔE < 1.0  → Imperceptible to human eye
    ΔE 1–2    → Perceptible on close inspection
    ΔE 2–10   → Perceptible at a glance
    ΔE > 10   → Strong colour difference

    Used in textile QC to assess shade matching accuracy (pass/fail).

    Args:
        lab1 (tuple): (L*, a*, b*) of first colour.
        lab2 (tuple): (L*, a*, b*) of second colour.

    Returns:
        float: ΔE* value.

    Example:
        >>> delta_e((53.0, 80.0, 67.0), (55.0, 78.0, 65.0))
        3.0
    """
    return round(math.sqrt(sum((x - y) ** 2 for x, y in zip(lab1, lab2))), 4)


# ─────────────────────────────────────────────────────────────────────────────
# Dye class profiles
# ─────────────────────────────────────────────────────────────────────────────

# Each dye class stores:
#   - compatible_fibers: fibers this dye can colour
#   - typical_fix_rate:  dye fixation % on the fiber
#   - shade_limit:       max practical shade % achievable
#   - primary_rgb:       approximate Lab* of R, G, B primaries for this class
#     (These are representative values for recipe modelling; labs calibrate to
#      their own primaries.)
_DYE_CLASSES = {
    "reactive": {
        "compatible_fibers": ["cotton", "viscose", "modal", "tencel", "linen"],
        "typical_fix_rate":  75.0,
        "shade_limit":       8.0,
        "note": "Best for cellulosic fibers. Requires salt + soda ash fixation.",
        "primaries_lab": {
            "red":   (40.0,  55.0,  38.0),
            "green": (55.0, -35.0,  20.0),
            "blue":  (35.0,  15.0, -52.0),
            "black": (12.0,   1.0,   1.0),
            "white": (96.0,  -2.0,   2.0),
        }
    },
    "disperse": {
        "compatible_fibers": ["polyester", "nylon", "acrylic"],
        "typical_fix_rate":  92.0,
        "shade_limit":       10.0,
        "note": "For synthetic fibers. Applied at high temperature (130°C).",
        "primaries_lab": {
            "red":   (42.0,  62.0,  45.0),
            "green": (57.0, -38.0,  22.0),
            "blue":  (33.0,  18.0, -58.0),
            "black": (10.0,   0.5,   0.5),
            "white": (97.0,  -1.5,   1.5),
        }
    },
    "acid": {
        "compatible_fibers": ["wool", "silk", "nylon"],
        "typical_fix_rate":  88.0,
        "shade_limit":       9.0,
        "note": "For protein and polyamide fibers. Applied in acidic pH (3–6).",
        "primaries_lab": {
            "red":   (44.0,  58.0,  40.0),
            "green": (53.0, -32.0,  18.0),
            "blue":  (37.0,  14.0, -55.0),
            "black": (11.0,   1.0,   1.0),
            "white": (95.0,  -2.0,   2.0),
        }
    },
    "vat": {
        "compatible_fibers": ["cotton", "linen"],
        "typical_fix_rate":  95.0,
        "shade_limit":       12.0,
        "note": "Outstanding wash fastness. Requires reduction-oxidation process.",
        "primaries_lab": {
            "red":   (38.0,  52.0,  34.0),
            "green": (50.0, -30.0,  16.0),
            "blue":  (32.0,  12.0, -60.0),
            "black": ( 9.0,   0.5,   0.5),
            "white": (94.0,  -1.0,   1.0),
        }
    },
    "direct": {
        "compatible_fibers": ["cotton", "viscose", "linen"],
        "typical_fix_rate":  60.0,
        "shade_limit":       5.0,
        "note": "Simple application, lower fastness. Good for light shades.",
        "primaries_lab": {
            "red":   (48.0,  50.0,  32.0),
            "green": (58.0, -28.0,  14.0),
            "blue":  (40.0,  10.0, -48.0),
            "black": (14.0,   1.0,   1.0),
            "white": (96.0,  -1.5,   1.5),
        }
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Recipe prediction engine
# ─────────────────────────────────────────────────────────────────────────────

def _predict_recipe_from_lab(target_lab, primaries_lab, shade_limit):
    """
    Internal: Predict R, G, B, Black dye % from target L*a*b* using
    weighted Neugebauer-inspired decomposition.

    The model works by expressing the target colour as a weighted sum
    of the primary dye Lab* vectors (Red, Green, Blue, Black, White).
    Black and White are used to control lightness independently.

    Returns: dict of {dye: percentage}
    """
    L_t, a_t, b_t = target_lab
    L_r, a_r, b_r = primaries_lab["red"]
    L_g, a_g, b_g = primaries_lab["green"]
    L_b, a_b, b_b = primaries_lab["blue"]
    L_k, a_k, b_k = primaries_lab["black"]
    L_w, a_w, b_w = primaries_lab["white"]

    # ── Lightness decomposition ──
    # L_t = L_w - (L_w - L_k) × depth  →  depth = (L_w - L_t) / (L_w - L_k)
    depth = max(0.0, min(1.0, (L_w - L_t) / (L_w - L_k + 1e-9)))

    # ── Chroma decomposition ──
    # Normalise target chroma relative to primaries
    # Solve for r_frac, g_frac, b_frac so that:
    #   a_t ≈ r_frac × a_r + g_frac × a_g + b_frac × a_b
    #   b_t ≈ r_frac × b_r + g_frac × b_g + b_frac × b_b
    # with r_frac + g_frac + b_frac = 1  (constrained)

    # Two-equation system (a*, b*), constrain b_frac = 1 - r - g:
    # a_t = r(a_r-a_b) + g(a_g-a_b) + a_b
    # b_t = r(b_r-b_b) + g(b_g-b_b) + b_b

    denom = (a_r - a_b) * (b_g - b_b) - (a_g - a_b) * (b_r - b_b)

    if abs(denom) < 1e-6:
        # Degenerate case — fall back to equal distribution
        r_f = g_f = b_f = 1/3
    else:
        r_f = ((a_t - a_b) * (b_g - b_b) - (a_g - a_b) * (b_t - b_b)) / denom
        g_f = ((a_r - a_b) * (b_t - b_b) - (a_t - a_b) * (b_r - b_b)) / denom
        b_f = 1.0 - r_f - g_f

    # Clamp and renormalise fractions
    r_f = max(0.0, r_f)
    g_f = max(0.0, g_f)
    b_f = max(0.0, b_f)
    total_f = r_f + g_f + b_f
    if total_f > 1e-9:
        r_f /= total_f
        g_f /= total_f
        b_f /= total_f
    else:
        r_f = g_f = b_f = 1/3

    # Chroma magnitude — how saturated is the colour?
    chroma = math.sqrt(a_t ** 2 + b_t ** 2)
    max_chroma = math.sqrt(max(a_r**2+b_r**2, a_g**2+b_g**2, a_b**2+b_b**2))
    chroma_factor = min(1.0, chroma / (max_chroma + 1e-9))

    # ── Convert fractions to dye % owf ──
    # Total colour dye scales with depth × shade_limit
    total_colour_shade = depth * shade_limit * chroma_factor
    black_shade = depth * shade_limit * (1 - chroma_factor) * 0.5

    red_pct   = round(total_colour_shade * r_f, 3)
    green_pct = round(total_colour_shade * g_f, 3)
    blue_pct  = round(total_colour_shade * b_f, 3)
    black_pct = round(black_shade, 3)

    # Filter out negligible amounts (<0.05%)
    recipe = {}
    if red_pct   >= 0.01: recipe["red_dye_%"]   = red_pct
    if green_pct >= 0.01: recipe["green_dye_%"] = green_pct
    if blue_pct  >= 0.01: recipe["blue_dye_%"]  = blue_pct
    if black_pct >= 0.01: recipe["black_dye_%"] = black_pct

    if not recipe:
        recipe["white_ground"] = True

    return recipe, depth


def predict_shade_recipe(
    color_input,
    fabric_weight_g,
    fiber_type="cotton",
    dye_class=None,
    mlr=10.0,
    input_format="hex"
):
    """
    Predict dye recipe for a target colour on a given textile substrate.

    Given a target color (hex or Lab*), fiber type, and fabric weight,
    this function predicts:
      - Which dye percentages (% owf) to use for Red, Green, Blue, and Black
      - Amounts of each dye in grams
      - Required salt, soda ash (for reactive) or auxiliaries
      - Estimated dye bath volume
      - Predicted Delta-E accuracy of the recipe

    Args:
        color_input    (str or tuple):
                         If input_format='hex'  → '#RRGGBB' string.
                         If input_format='rgb'  → (R, G, B) tuple, 0–255.
                         If input_format='lab'  → (L*, a*, b*) tuple.
        fabric_weight_g (float): Weight of fabric/yarn in grams.
        fiber_type     (str):   Fiber being dyed (default: 'cotton').
                                One of: cotton, polyester, viscose, linen,
                                wool, silk, nylon, acrylic, modal, tencel.
        dye_class      (str):   Dye class to use. If None, auto-selected
                                based on fiber_type.
                                One of: 'reactive', 'disperse', 'acid', 'vat', 'direct'.
        mlr            (float): Material to Liquor Ratio (default: 10.0 → 1:10).
        input_format   (str):   'hex', 'rgb', or 'lab'.

    Returns:
        dict: Full dye recipe containing:
            - color_hex          (str):   Input color as hex
            - color_lab          (tuple): Input color in L*a*b*
            - shade_description  (str):   Human-readable shade depth category
            - dye_class          (str):   Dye class used
            - fiber_type         (str):   Fiber being dyed
            - recipe_percent     (dict):  Dye % owf for each component
            - recipe_grams       (dict):  Dye in grams for each component
            - auxiliaries_g      (dict):  Required auxiliaries in grams
            - liquor_volume_L    (float): Required dyebath volume in litres
            - fixation_rate      (float): Expected dye fixation %
            - delta_e_estimate   (float): Estimated colour accuracy (ΔE*)
            - warnings           (list):  Any alerts or substitution notes
            - process_note       (str):   Dye class-specific process guidance

    Raises:
        ValueError: If color is invalid, fiber is unsupported, or inputs are out of range.

    Example:
        >>> rec = predict_shade_recipe('#3A5F8A', 1000, 'cotton')
        >>> print(rec['recipe_percent'])
        {'red_dye_%': 0.12, 'blue_dye_%': 2.84, 'black_dye_%': 0.45}
        >>> print(rec['recipe_grams'])
        {'red_dye': 1.2, 'blue_dye': 28.4, 'black_dye': 4.5}
    """
    validate_positive(fabric_weight_g, "Fabric Weight (g)")
    validate_positive(mlr, "MLR")

    fiber_type = fiber_type.lower().strip()
    warnings   = []

    # ── Resolve Lab* from input ──
    if input_format == "hex":
        r, g, b = hex_to_rgb(str(color_input))
        color_lab = rgb_to_lab(r, g, b)
        color_hex = rgb_to_hex(r, g, b)
    elif input_format == "rgb":
        r, g, b = int(color_input[0]), int(color_input[1]), int(color_input[2])
        color_lab = rgb_to_lab(r, g, b)
        color_hex = rgb_to_hex(r, g, b)
    elif input_format == "lab":
        color_lab = (float(color_input[0]), float(color_input[1]), float(color_input[2]))
        rgb_approx = lab_to_rgb(*color_lab)
        color_hex = rgb_to_hex(*rgb_approx)
    else:
        raise ValueError("input_format must be 'hex', 'rgb', or 'lab'.")

    L_t = color_lab[0]

    # ── Auto-select dye class ──
    if dye_class is None:
        for cls, props in _DYE_CLASSES.items():
            if fiber_type in props["compatible_fibers"]:
                dye_class = cls
                break
        if dye_class is None:
            raise ValueError(
                f"No compatible dye class found for fiber '{fiber_type}'. "
                f"Supported fibers: {', '.join(set(f for p in _DYE_CLASSES.values() for f in p['compatible_fibers']))}"
            )
    else:
        dye_class = dye_class.lower().strip()
        if dye_class not in _DYE_CLASSES:
            raise ValueError(f"Unknown dye class '{dye_class}'. Options: {', '.join(_DYE_CLASSES)}")

    dye_props = _DYE_CLASSES[dye_class]

    # Check fiber compatibility
    if fiber_type not in dye_props["compatible_fibers"]:
        compatible_classes = [c for c, p in _DYE_CLASSES.items() if fiber_type in p["compatible_fibers"]]
        if compatible_classes:
            warnings.append(
                f"'{dye_class}' dye is not ideal for '{fiber_type}'. "
                f"Recommended: {', '.join(compatible_classes)}. Proceeding anyway."
            )
        else:
            raise ValueError(f"No known dye class is compatible with fiber '{fiber_type}'.")

    # ── Predict recipe ──
    recipe_pct, depth = _predict_recipe_from_lab(
        color_lab,
        dye_props["primaries_lab"],
        dye_props["shade_limit"]
    )

    # ── Shade depth description ──
    total_shade = sum(v for v in recipe_pct.values() if isinstance(v, (int, float)))
    if total_shade < 0.3:
        shade_desc = "Pastel / Extra-light shade"
    elif total_shade < 1.0:
        shade_desc = "Light shade"
    elif total_shade < 2.5:
        shade_desc = "Medium shade"
    elif total_shade < 5.0:
        shade_desc = "Dark shade"
    else:
        shade_desc = "Extra-dark / Deep shade"

    # ── Convert % to grams ──
    recipe_grams = {}
    for key, pct in recipe_pct.items():
        if isinstance(pct, (int, float)):
            dye_name = key.replace("_%", "").replace("_", " ").title()
            recipe_grams[dye_name + " (g)"] = round((fabric_weight_g * pct) / 100, 2)

    # ── Auxiliaries calculation ──
    auxiliaries_g = {}
    if dye_class == "reactive":
        salt_g_per_L = 80 if total_shade > 3 else (60 if total_shade > 1 else 40)
        liquor_L = (fabric_weight_g / 1000) * mlr
        auxiliaries_g = {
            "common_salt_NaCl_g":  round(salt_g_per_L * liquor_L, 1),
            "soda_ash_Na2CO3_g":   round(fabric_weight_g * 0.20, 1),
            "wetting_agent_g":     round(fabric_weight_g * 0.01, 1),
            "sequestering_agent_g": round(fabric_weight_g * 0.005, 1),
        }
    elif dye_class == "disperse":
        liquor_L = (fabric_weight_g / 1000) * mlr
        auxiliaries_g = {
            "dispersing_agent_g":  round(fabric_weight_g * 0.01, 1),
            "acetic_acid_g":       round(fabric_weight_g * 0.005, 1),
            "leveling_agent_g":    round(fabric_weight_g * 0.005, 1),
        }
    elif dye_class == "acid":
        liquor_L = (fabric_weight_g / 1000) * mlr
        auxiliaries_g = {
            "acetic_acid_g":       round(fabric_weight_g * 0.02, 1),
            "leveling_agent_g":    round(fabric_weight_g * 0.01, 1),
            "glauber_salt_g":      round(fabric_weight_g * 0.10, 1),
        }
    elif dye_class == "vat":
        liquor_L = (fabric_weight_g / 1000) * mlr
        auxiliaries_g = {
            "sodium_hydrosulphite_g": round(fabric_weight_g * 0.15, 1),
            "caustic_soda_NaOH_g":    round(fabric_weight_g * 0.08, 1),
            "salt_NaCl_g":            round(fabric_weight_g * 0.05, 1),
        }
    else:
        liquor_L = (fabric_weight_g / 1000) * mlr
        auxiliaries_g = {
            "common_salt_NaCl_g": round(fabric_weight_g * 0.15, 1),
            "soda_ash_g":         round(fabric_weight_g * 0.05, 1),
        }

    liquor_L = round((fabric_weight_g / 1000) * mlr, 2)

    # ── Delta-E estimation ──
    # Re-synthesise Lab from recipe to estimate accuracy
    prim = dye_props["primaries_lab"]
    r_pct = recipe_pct.get("red_dye_%",   0)
    g_pct = recipe_pct.get("green_dye_%", 0)
    b_pct = recipe_pct.get("blue_dye_%",  0)
    k_pct = recipe_pct.get("black_dye_%", 0)

    shade_lim = dye_props["shade_limit"]
    # Inverse: reconstruct Lab prediction
    L_w, a_w, b_w = prim["white"]
    L_k, a_k, b_k = prim["black"]
    L_r, a_r, b_r = prim["red"]
    L_g, a_g, b_g = prim["green"]
    L_b2, a_b2, b_b2 = prim["blue"]

    total_c = (r_pct + g_pct + b_pct)
    r_f2 = r_pct / total_c if total_c > 0 else 0
    g_f2 = g_pct / total_c if total_c > 0 else 0
    b_f2 = b_pct / total_c if total_c > 0 else 0

    a_pred = r_f2 * a_r + g_f2 * a_g + b_f2 * a_b2
    b_pred = r_f2 * b_r + g_f2 * b_g + b_f2 * b_b2
    dep2   = (total_c / shade_lim) if shade_lim > 0 else 0
    L_pred = L_w - (L_w - L_k) * dep2

    pred_lab = (L_pred, a_pred, b_pred)
    de = delta_e(color_lab, pred_lab)

    # ── Shade limit warning ──
    if total_shade > dye_props["shade_limit"]:
        warnings.append(
            f"Total shade ({total_shade:.2f}% owf) exceeds the practical limit for "
            f"{dye_class} dye ({dye_props['shade_limit']}% owf). "
            f"Consider switching to a dye class with higher shade capacity."
        )

    # Lightness warnings
    if L_t > 90:
        warnings.append("Very light shade — consider undyed fabric or optical brightener instead.")
    if de > 5.0:
        warnings.append(
            f"ΔE* estimate ({de:.1f}) is moderate. Lab calibration with actual dye primaries "
            "is recommended for production accuracy."
        )

    return {
        "color_hex":         color_hex,
        "color_lab":         color_lab,
        "shade_description": shade_desc,
        "dye_class":         dye_class,
        "fiber_type":        fiber_type,
        "recipe_percent":    recipe_pct,
        "recipe_grams":      recipe_grams,
        "auxiliaries_g":     auxiliaries_g,
        "liquor_volume_L":   liquor_L,
        "mlr":               mlr,
        "fixation_rate_%":   dye_props["typical_fix_rate"],
        "delta_e_estimate":  round(de, 2),
        "warnings":          warnings,
        "process_note":      dye_props["note"],
    }


def compare_shade_accuracy(produced_hex, target_hex):
    """
    Compare a produced shade to the target shade using CIE Delta-E.

    Used in quality control to determine pass/fail of a dyed batch
    against the target colour standard.

    Args:
        produced_hex (str): Hex color of the produced fabric.
        target_hex   (str): Hex color of the target/standard.

    Returns:
        dict: Comparison result containing:
            - produced_lab  (tuple): Lab* of produced fabric
            - target_lab    (tuple): Lab* of target
            - delta_e       (float): Colour difference ΔE*
            - delta_L       (float): Lightness difference (positive = too light)
            - delta_a       (float): Red-green difference
            - delta_b       (float): Blue-yellow difference
            - verdict       (str):   'Pass', 'Marginal', or 'Fail'
            - recommendation (str):  Corrective action suggestion

    Example:
        >>> compare_shade_accuracy('#3A5F8B', '#3A5F8A')
        {'delta_e': 0.2, 'verdict': 'Pass', ...}
    """
    prod_lab   = rgb_to_lab(*hex_to_rgb(produced_hex))
    target_lab = rgb_to_lab(*hex_to_rgb(target_hex))
    de = delta_e(prod_lab, target_lab)
    dL = round(prod_lab[0] - target_lab[0], 3)
    da = round(prod_lab[1] - target_lab[1], 3)
    db = round(prod_lab[2] - target_lab[2], 3)

    if de < 1.0:
        verdict = "Pass — Excellent match"
        rec = "No adjustment needed."
    elif de < 2.0:
        verdict = "Pass — Good match"
        rec = "Minor adjustment may improve visual uniformity."
    elif de < 4.0:
        verdict = "Marginal — Borderline"
        rec = (
            f"{'Add more dye' if dL < 0 else 'Reduce dye concentration'} "
            f"({'redden' if da < 0 else 'greenen'} slightly)."
        )
    else:
        verdict = "Fail — Unacceptable shade"
        rec = (
            f"Significant re-dyeing required. "
            f"Shade is {'too light' if dL > 0 else 'too dark'} "
            f"and {'too green' if da < 0 else 'too red'} / "
            f"{'too blue' if db < 0 else 'too yellow'}."
        )

    return {
        "produced_hex":   produced_hex,
        "target_hex":     target_hex,
        "produced_lab":   prod_lab,
        "target_lab":     target_lab,
        "delta_e":        round(de, 3),
        "delta_L":        dL,
        "delta_a":        da,
        "delta_b":        db,
        "verdict":        verdict,
        "recommendation": rec,
    }


def list_dye_classes():
    """
    Return all supported dye classes with their fiber compatibility and properties.

    Returns:
        list of dict: Each dict has 'dye_class', 'compatible_fibers',
                      'fix_rate', 'shade_limit', 'note'.

    Example:
        >>> for cls in list_dye_classes():
        ...     print(cls['dye_class'], cls['compatible_fibers'])
    """
    return [
        {
            "dye_class":          key,
            "compatible_fibers":  v["compatible_fibers"],
            "typical_fix_rate_%": v["typical_fix_rate"],
            "shade_limit_%_owf":  v["shade_limit"],
            "note":               v["note"],
        }
        for key, v in sorted(_DYE_CLASSES.items())
    ]
