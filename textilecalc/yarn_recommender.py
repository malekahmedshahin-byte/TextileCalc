# textilecalc/yarn_recommender.py
# Module: AI-Powered Yarn Count & Fabric Structure Recommender
# Author: Abdul Malek | Version: 2.0.0
#
# Uses rule-based expert knowledge + weighted scoring to recommend
# optimal yarn count, EPI/PPI, and weave structure from target specs.

import math
from utils.validator import validate_positive


# ─────────────────────────────────────────────────────────────────────────────
# Internal knowledge bases
# ─────────────────────────────────────────────────────────────────────────────

# End-use profiles: (gsm_min, gsm_max, ne_min, ne_max, label)
_END_USE_PROFILES = {
    "shirt":         {"gsm": (80,  140), "ne": (40, 80),  "epi": (80, 120), "ppi": (70, 100), "weave": "plain",   "description": "Lightweight, smooth, breathable"},
    "trouser":       {"gsm": (160, 260), "ne": (20, 40),  "epi": (60, 90),  "ppi": (55, 80),  "weave": "twill",   "description": "Medium-heavy, durable, structured"},
    "denim":         {"gsm": (280, 450), "ne": (6,  16),  "epi": (55, 75),  "ppi": (40, 55),  "weave": "3/1 twill","description": "Heavy, rigid, very durable"},
    "bedsheet":      {"gsm": (90,  160), "ne": (40, 80),  "epi": (90, 140), "ppi": (80, 130), "weave": "plain",   "description": "Fine, smooth, high thread count"},
    "towel":         {"gsm": (300, 600), "ne": (10, 20),  "epi": (16, 28),  "ppi": (16, 24),  "weave": "terry",   "description": "Thick, absorbent, pile structure"},
    "sportswear":    {"gsm": (130, 220), "ne": (20, 40),  "epi": (70, 100), "ppi": (60, 90),  "weave": "plain",   "description": "Elastic, moisture-wicking, lightweight"},
    "upholstery":    {"gsm": (300, 600), "ne": (8,  20),  "epi": (40, 70),  "ppi": (35, 60),  "weave": "satin",   "description": "Heavy, tight, abrasion-resistant"},
    "canvas":        {"gsm": (200, 400), "ne": (6,  16),  "epi": (30, 55),  "ppi": (28, 50),  "weave": "plain",   "description": "Very tight, stiff, industrial"},
    "voile":         {"gsm": (40,  80),  "ne": (60, 120), "epi": (70, 100), "ppi": (60, 90),  "weave": "plain",   "description": "Ultra-sheer, fine, delicate"},
    "suiting":       {"gsm": (180, 280), "ne": (30, 60),  "epi": (70, 110), "ppi": (65, 100), "weave": "twill",   "description": "Structured, drapeable, formal"},
    "flannel":       {"gsm": (150, 250), "ne": (16, 30),  "epi": (50, 75),  "ppi": (45, 70),  "weave": "plain",   "description": "Soft, napped, warm, winter fabric"},
    "medical_gauze": {"gsm": (20,  50),  "ne": (16, 30),  "epi": (18, 28),  "ppi": (14, 22),  "weave": "plain",   "description": "Open weave, absorbent, medical grade"},
}

# Fiber type adjustments to Ne (multiplier) and EPI/PPI (multiplier)
_FIBER_ADJUSTMENTS = {
    "cotton":    {"ne_mult": 1.00, "density_mult": 1.00, "note": "Standard reference fiber"},
    "polyester": {"ne_mult": 0.90, "density_mult": 1.05, "note": "Slightly finer, denser packing"},
    "viscose":   {"ne_mult": 1.05, "density_mult": 0.95, "note": "Softer, slightly looser structure"},
    "linen":     {"ne_mult": 0.80, "density_mult": 0.90, "note": "Coarser hand, lower thread density"},
    "wool":      {"ne_mult": 0.75, "density_mult": 0.85, "note": "Bulkier, springy, lower density"},
    "silk":      {"ne_mult": 1.30, "density_mult": 1.10, "note": "Ultra-fine, high density possible"},
    "nylon":     {"ne_mult": 0.95, "density_mult": 1.05, "note": "Strong, slightly denser weave"},
    "acrylic":   {"ne_mult": 0.85, "density_mult": 0.95, "note": "Bulky, lower density"},
    "modal":     {"ne_mult": 1.10, "density_mult": 1.00, "note": "Smooth, fine, similar to cotton"},
    "tencel":    {"ne_mult": 1.10, "density_mult": 1.00, "note": "Fine, silky, eco-friendly"},
}

# Loom type constraints: max EPI supported
_LOOM_EPI_LIMITS = {
    "rapier":       180,
    "airjet":       160,
    "waterjet":     140,
    "projectile":   200,
    "shuttle":      120,
    "any":          200,
}

# Weave structure properties
_WEAVE_PROPERTIES = {
    "plain":    {"crimp_factor": 1.08, "cover_efficiency": 1.00, "strength": "High",   "drape": "Low"},
    "twill":    {"crimp_factor": 1.05, "cover_efficiency": 1.05, "strength": "Medium", "drape": "Medium"},
    "3/1 twill":{"crimp_factor": 1.04, "cover_efficiency": 1.06, "strength": "High",   "drape": "Low"},
    "satin":    {"crimp_factor": 1.02, "cover_efficiency": 1.10, "strength": "Low",    "drape": "High"},
    "terry":    {"crimp_factor": 1.20, "cover_efficiency": 0.80, "strength": "Medium", "drape": "Low"},
}


# ─────────────────────────────────────────────────────────────────────────────
# Core recommendation engine
# ─────────────────────────────────────────────────────────────────────────────

def recommend_yarn_count(
    target_gsm,
    end_use,
    fiber_type="cotton",
    loom_type="any",
    width_inch=60.0
):
    """
    AI-powered yarn count and fabric structure recommender.

    Given a target GSM, end-use, fiber type, and loom constraints, this
    function recommends the optimal yarn count (Ne), EPI, PPI, weave
    structure, and estimated cover factor — using expert textile knowledge
    encoded as a weighted scoring engine.

    Args:
        target_gsm  (float): Target fabric GSM (g/m²). Must be positive.
        end_use     (str):   Fabric end-use. One of:
                             'shirt', 'trouser', 'denim', 'bedsheet', 'towel',
                             'sportswear', 'upholstery', 'canvas', 'voile',
                             'suiting', 'flannel', 'medical_gauze'
        fiber_type  (str):   Fiber type (default: 'cotton'). One of:
                             'cotton', 'polyester', 'viscose', 'linen', 'wool',
                             'silk', 'nylon', 'acrylic', 'modal', 'tencel'
        loom_type   (str):   Loom type (default: 'any'). One of:
                             'rapier', 'airjet', 'waterjet', 'projectile',
                             'shuttle', 'any'
        width_inch  (float): Fabric width in inches (default: 60.0)

    Returns:
        dict: Recommendation report containing:
            - recommended_ne     (float): Optimal warp/weft yarn count in Ne
            - recommended_epi    (int):   Ends per inch
            - recommended_ppi    (int):   Picks per inch
            - weave_structure    (str):   Recommended weave (plain/twill/satin/etc.)
            - estimated_gsm      (float): Estimated GSM from recommendation
            - cover_factor       (float): Calculated fabric cover factor
            - total_ends         (int):   Total warp ends for given width
            - confidence_score   (float): How well inputs match the profile (0–100)
            - warnings           (list):  Any constraint violations or alerts
            - fiber_note         (str):   Fiber-specific advice
            - end_use_profile    (str):   Description of end-use requirements

    Raises:
        ValueError: If end_use or fiber_type is unrecognized, or GSM is invalid.

    Example:
        >>> rec = recommend_yarn_count(160, 'trouser', 'polyester', 'rapier', 63)
        >>> print(rec['recommended_ne'])
        32
        >>> print(rec['weave_structure'])
        'twill'
    """
    validate_positive(target_gsm, "Target GSM")
    validate_positive(width_inch, "Width (inch)")

    end_use = end_use.lower().strip()
    fiber_type = fiber_type.lower().strip()
    loom_type = loom_type.lower().strip()

    if end_use not in _END_USE_PROFILES:
        valid = ", ".join(sorted(_END_USE_PROFILES.keys()))
        raise ValueError(f"Unknown end_use '{end_use}'. Valid options: {valid}")
    if fiber_type not in _FIBER_ADJUSTMENTS:
        valid = ", ".join(sorted(_FIBER_ADJUSTMENTS.keys()))
        raise ValueError(f"Unknown fiber_type '{fiber_type}'. Valid options: {valid}")
    if loom_type not in _LOOM_EPI_LIMITS:
        valid = ", ".join(sorted(_LOOM_EPI_LIMITS.keys()))
        raise ValueError(f"Unknown loom_type '{loom_type}'. Valid options: {valid}")

    profile = _END_USE_PROFILES[end_use]
    fiber   = _FIBER_ADJUSTMENTS[fiber_type]
    max_epi = _LOOM_EPI_LIMITS[loom_type]
    warnings = []

    # ── Step 1: Derive base Ne from GSM using Peirce's fabric weight equation
    # GSM ≈ (EPI/Ne_warp + PPI/Ne_weft) × 25.6  (simplified cotton plain)
    # Rearranged: Ne_base ≈ 51.2 × avg_thread_density / GSM
    ne_min, ne_max = profile["ne"]
    epi_min, epi_max = profile["epi"]
    ppi_min, ppi_max = profile["ppi"]

    # Midpoint of the profile range as anchor
    ne_mid  = (ne_min + ne_max) / 2
    epi_mid = (epi_min + epi_max) / 2
    ppi_mid = (ppi_min + ppi_max) / 2

    # GSM-based correction: scale Ne proportionally to how far GSM is from profile centre
    gsm_min, gsm_max = profile["gsm"]
    gsm_mid  = (gsm_min + gsm_max) / 2
    gsm_ratio = target_gsm / gsm_mid  # >1 means heavier than centre → coarser yarn

    # Heavier fabric → lower Ne (coarser); lighter → higher Ne (finer)
    ne_raw = ne_mid / gsm_ratio

    # Apply fiber adjustment
    ne_adjusted = ne_raw * fiber["ne_mult"]

    # Clamp to profile range (±25% tolerance for edge targets)
    ne_lo = ne_min * 0.75
    ne_hi = ne_max * 1.25
    ne_final = max(ne_lo, min(ne_hi, ne_adjusted))
    ne_final = round(ne_final / 2) * 2   # round to nearest even count (industry standard)
    ne_final = max(2, ne_final)

    # ── Step 2: Derive EPI / PPI from Ne and target GSM
    # GSM = (EPI/Ne_w + PPI/Ne_f) × 25.6  → EPI+PPI = GSM × Ne / 25.6
    thread_density_total = (target_gsm * ne_final) / 25.6
    # Standard warp:weft density ratio from profile
    warp_fraction = epi_mid / (epi_mid + ppi_mid)
    epi_raw = thread_density_total * warp_fraction * fiber["density_mult"]
    ppi_raw = thread_density_total * (1 - warp_fraction) * fiber["density_mult"]

    epi_final = int(round(max(epi_min * 0.75, min(epi_max * 1.25, epi_raw))))
    ppi_final = int(round(max(ppi_min * 0.75, min(ppi_max * 1.25, ppi_raw))))

    # ── Step 3: Loom EPI constraint check
    if epi_final > max_epi:
        warnings.append(
            f"Recommended EPI ({epi_final}) exceeds {loom_type} loom capacity "
            f"({max_epi}). Clamped to {max_epi}. Consider a finer yarn or different loom."
        )
        epi_final = max_epi

    # ── Step 4: Weave structure
    weave = profile["weave"]
    weave_props = _WEAVE_PROPERTIES.get(weave, _WEAVE_PROPERTIES["plain"])

    # ── Step 5: Cover factor (Peirce's formula)
    warp_cf = epi_final / math.sqrt(ne_final)
    weft_cf = ppi_final / math.sqrt(ne_final)
    total_cf = round(warp_cf + weft_cf - (warp_cf * weft_cf / 28), 3)

    # ── Step 6: Estimated GSM from final parameters
    estimated_gsm = round(
        ((epi_final / ne_final) + (ppi_final / ne_final)) * 25.6 / fiber["density_mult"],
        1
    )

    # GSM mismatch warning
    gsm_error_pct = abs(estimated_gsm - target_gsm) / target_gsm * 100
    if gsm_error_pct > 15:
        warnings.append(
            f"Estimated GSM ({estimated_gsm}) deviates {gsm_error_pct:.1f}% from "
            f"target ({target_gsm}). Adjust yarn count or density manually."
        )

    # ── Step 7: Total warp ends
    total_ends = int(epi_final * width_inch)

    # ── Step 8: GSM range check
    if not (gsm_min * 0.75 <= target_gsm <= gsm_max * 1.25):
        warnings.append(
            f"Target GSM ({target_gsm}) is outside the typical range for "
            f"'{end_use}' ({gsm_min}–{gsm_max} g/m²). Results may be unconventional."
        )

    # ── Step 9: Confidence score (0–100)
    gsm_score   = max(0, 100 - gsm_error_pct * 2)
    range_score = 100 if (ne_min <= ne_final <= ne_max) else 60
    loom_score  = 100 if epi_final <= max_epi else 40
    confidence  = round((gsm_score * 0.5 + range_score * 0.3 + loom_score * 0.2), 1)

    return {
        "recommended_ne":   ne_final,
        "recommended_epi":  epi_final,
        "recommended_ppi":  ppi_final,
        "weave_structure":  weave,
        "weave_properties": {
            "crimp_factor":     weave_props["crimp_factor"],
            "strength":         weave_props["strength"],
            "drape":            weave_props["drape"],
        },
        "estimated_gsm":    estimated_gsm,
        "cover_factor":     total_cf,
        "total_ends":       total_ends,
        "confidence_score": confidence,
        "warnings":         warnings,
        "fiber_note":       fiber["note"],
        "end_use_profile":  profile["description"],
    }


def list_end_uses():
    """
    Return a list of all supported end-use categories with their GSM ranges.

    Returns:
        list of dict: Each dict has 'end_use', 'gsm_range', 'description'.

    Example:
        >>> for item in list_end_uses():
        ...     print(item['end_use'], item['gsm_range'])
    """
    return [
        {
            "end_use":     key,
            "gsm_range":   f"{v['gsm'][0]}–{v['gsm'][1]} g/m²",
            "ne_range":    f"Ne {v['ne'][0]}–{v['ne'][1]}",
            "description": v["description"],
        }
        for key, v in sorted(_END_USE_PROFILES.items())
    ]


def list_fiber_types():
    """
    Return all supported fiber types with their adjustment notes.

    Returns:
        list of dict: Each dict has 'fiber', 'ne_multiplier', 'note'.

    Example:
        >>> for f in list_fiber_types():
        ...     print(f['fiber'], f['note'])
    """
    return [
        {
            "fiber":         key,
            "ne_multiplier": v["ne_mult"],
            "density_multiplier": v["density_mult"],
            "note":          v["note"],
        }
        for key, v in sorted(_FIBER_ADJUSTMENTS.items())
    ]


def compare_yarn_options(target_gsm, end_use, fiber_types=None, loom_type="any", width_inch=60.0):
    """
    Compare yarn count recommendations across multiple fiber types side by side.

    Args:
        target_gsm  (float): Target GSM.
        end_use     (str):   Fabric end-use.
        fiber_types (list):  List of fiber type strings to compare.
                             Defaults to ['cotton', 'polyester', 'viscose'].
        loom_type   (str):   Loom type constraint.
        width_inch  (float): Fabric width in inches.

    Returns:
        list of dict: One recommendation dict per fiber type, with 'fiber' key added.

    Example:
        >>> results = compare_yarn_options(160, 'trouser', ['cotton', 'polyester', 'wool'])
        >>> for r in results:
        ...     print(r['fiber'], r['recommended_ne'], r['estimated_gsm'])
    """
    if fiber_types is None:
        fiber_types = ["cotton", "polyester", "viscose"]

    results = []
    for fiber in fiber_types:
        rec = recommend_yarn_count(target_gsm, end_use, fiber, loom_type, width_inch)
        rec["fiber"] = fiber
        results.append(rec)
    return results
