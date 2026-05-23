from utils.validator import validate_positive


def moisture_regain(original_weight, dry_weight):
    """
    Calculate moisture regain percentage of textile material.
    Moisture Regain = ((Wet - Dry) / Dry) × 100

    Args:
        original_weight (float): Original (conditioned/wet) weight in grams
        dry_weight (float): Oven-dry weight in grams

    Returns:
        float: Moisture regain percentage

    Example:
        >>> moisture_regain(110, 100)
        10.0
    """
    validate_positive(original_weight, "Original Weight")
    validate_positive(dry_weight, "Dry Weight")
    return ((original_weight - dry_weight) / dry_weight) * 100


def moisture_content(original_weight, dry_weight):
    """
    Calculate moisture content percentage.
    Moisture Content = ((Wet - Dry) / Wet) × 100

    Note: Different from moisture regain — denominator is wet weight here.

    Args:
        original_weight (float): Original (wet) weight in grams
        dry_weight (float): Oven-dry weight in grams

    Returns:
        float: Moisture content percentage

    Example:
        >>> moisture_content(110, 100)
        9.09...
    """
    validate_positive(original_weight, "Original Weight")
    validate_positive(dry_weight, "Dry Weight")
    return ((original_weight - dry_weight) / original_weight) * 100


def shrinkage_percent(original, final):
    """
    Calculate dimensional shrinkage percentage after washing/finishing.

    Args:
        original (float): Original dimension (length or width) before wash
        final (float): Final dimension after wash

    Returns:
        float: Shrinkage percentage (positive = shrinkage, negative = growth)

    Example:
        >>> shrinkage_percent(100, 95)
        5.0
    """
    validate_positive(original, "Original")
    validate_positive(final, "Final")
    return ((original - final) / original) * 100


def absorbency_rate(water_absorbed, dry_weight):
    """
    Calculate water absorbency rate of fabric.

    Args:
        water_absorbed (float): Weight of water absorbed in grams
        dry_weight (float): Dry weight of fabric in grams

    Returns:
        float: Absorbency percentage

    Example:
        >>> absorbency_rate(300, 100)
        300.0
    """
    validate_positive(water_absorbed, "Water Absorbed")
    validate_positive(dry_weight, "Dry Weight")
    return (water_absorbed / dry_weight) * 100


def pilling_resistance_grade(pilling_score):
    """
    Interpret pilling resistance test grade (1–5 scale).

    Args:
        pilling_score (int/float): Test score from 1 to 5

    Returns:
        str: Grade description

    Example:
        >>> pilling_resistance_grade(4)
        'Good — Slight pilling'
    """
    if not (1 <= pilling_score <= 5):
        raise ValueError("Pilling score must be between 1 and 5.")
    grades = {
        1: "Very Poor — Very heavy pilling",
        2: "Poor — Heavy pilling",
        3: "Moderate — Moderate pilling",
        4: "Good — Slight pilling",
        5: "Excellent — No pilling"
    }
    return grades[int(pilling_score)]
