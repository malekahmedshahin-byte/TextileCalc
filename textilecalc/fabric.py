from utils.validator import validate_positive
import math


def gsm(weight_g, length_m, width_m):
    """
    Calculate Fabric GSM (Grams per Square Meter).

    Args:
        weight_g (float): Sample fabric weight in grams
        length_m (float): Sample length in meters
        width_m (float): Sample width in meters

    Returns:
        float: GSM value (g/m²)

    Example:
        >>> gsm(50, 0.5, 0.5)
        200.0
    """
    validate_positive(weight_g, "Weight")
    validate_positive(length_m, "Length")
    validate_positive(width_m, "Width")
    return weight_g / (length_m * width_m)


def fabric_weight(gsm_val, width_m, length_m):
    """
    Calculate total fabric weight from GSM, width, and length.

    Args:
        gsm_val (float): Fabric GSM (g/m²)
        width_m (float): Fabric width in meters
        length_m (float): Fabric length in meters

    Returns:
        float: Total fabric weight in grams

    Example:
        >>> fabric_weight(200, 1.5, 100)
        30000.0
    """
    validate_positive(gsm_val, "GSM")
    validate_positive(width_m, "Width")
    validate_positive(length_m, "Length")
    return gsm_val * width_m * length_m


def warp_cover_factor(epi, count_ne):
    """
    Calculate Warp Cover Factor using standard textile formula.
    Warp CF = EPI / sqrt(count_Ne)

    Args:
        epi (float): Ends Per Inch
        count_ne (float): Warp yarn count in Ne

    Returns:
        float: Warp cover factor (max theoretical value ~28)

    Example:
        >>> warp_cover_factor(60, 40)
        9.487...
    """
    validate_positive(epi, "EPI")
    validate_positive(count_ne, "Count Ne")
    return epi / math.sqrt(count_ne)


def weft_cover_factor(ppi, count_ne):
    """
    Calculate Weft Cover Factor using standard textile formula.
    Weft CF = PPI / sqrt(count_Ne)

    Args:
        ppi (float): Picks Per Inch
        count_ne (float): Weft yarn count in Ne

    Returns:
        float: Weft cover factor (max theoretical value ~28)

    Example:
        >>> weft_cover_factor(50, 40)
        7.906...
    """
    validate_positive(ppi, "PPI")
    validate_positive(count_ne, "Count Ne")
    return ppi / math.sqrt(count_ne)


def cover_factor(epi, ppi, count_ne):
    """
    Calculate Total Fabric Cover Factor (Peirce's formula).
    Total CF = Warp CF + Weft CF - (Warp CF × Weft CF / 28)

    Args:
        epi (float): Ends Per Inch
        ppi (float): Picks Per Inch
        count_ne (float): Yarn count in Ne (assumes same count for both)

    Returns:
        float: Total cover factor (value between 0 and 1 scale, max ~1)

    Example:
        >>> cover_factor(60, 50, 40)
        ~1.2 (fabric is well-covered)
    """
    validate_positive(epi, "EPI")
    validate_positive(ppi, "PPI")
    validate_positive(count_ne, "Count Ne")
    warp_cf = epi / math.sqrt(count_ne)
    weft_cf = ppi / math.sqrt(count_ne)
    total_cf = warp_cf + weft_cf - (warp_cf * weft_cf / 28)
    return round(total_cf, 4)


def shrinkage_percent(original, final):
    """
    Calculate fabric shrinkage percentage after washing/finishing.

    Args:
        original (float): Original fabric length/width (cm or inches)
        final (float): Final fabric length/width after wash

    Returns:
        float: Shrinkage percentage (positive = shrinkage, negative = growth)

    Example:
        >>> shrinkage_percent(100, 96)
        4.0
    """
    validate_positive(original, "Original")
    validate_positive(final, "Final")
    return ((original - final) / original) * 100
