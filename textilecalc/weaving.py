from utils.validator import validate_positive


def loom_efficiency(actual, ideal):
    """
    Calculate loom efficiency percentage.

    Args:
        actual (float): Actual picks inserted or fabric produced
        ideal (float): Ideal/theoretical maximum picks or production

    Returns:
        float: Loom efficiency percentage

    Example:
        >>> loom_efficiency(850, 1000)
        85.0
    """
    validate_positive(actual, "Actual")
    validate_positive(ideal, "Ideal")
    return (actual / ideal) * 100


def warp_break_rate(breaks, total_ends):
    """
    Calculate warp break rate per 100 warp ends.

    Args:
        breaks (float): Total number of warp breaks observed
        total_ends (float): Total number of warp ends in loom

    Returns:
        float: Warp break rate percentage

    Example:
        >>> warp_break_rate(5, 2000)
        0.25
    """
    validate_positive(breaks, "Breaks")
    validate_positive(total_ends, "Total Ends")
    return (breaks / total_ends) * 100


def weft_break_rate(breaks, picks):
    """
    Calculate weft break rate per 100 picks.

    Args:
        breaks (float): Total number of weft breaks observed
        picks (float): Total number of picks inserted

    Returns:
        float: Weft break rate percentage

    Example:
        >>> weft_break_rate(3, 10000)
        0.03
    """
    validate_positive(breaks, "Breaks")
    validate_positive(picks, "Picks")
    return (breaks / picks) * 100


def fabric_defect_rate(defects, total_length):
    """
    Calculate fabric defect rate per meter/yard of fabric.

    Args:
        defects (float): Total number of defects found
        total_length (float): Total fabric length inspected (meters or yards)

    Returns:
        float: Defect rate (defects per unit length)

    Example:
        >>> fabric_defect_rate(10, 500)
        0.02
    """
    validate_positive(defects, "Defects")
    validate_positive(total_length, "Total Length")
    return defects / total_length


def production_per_loom(rpm, efficiency_percent, epi, width_inch):
    """
    Calculate fabric production per loom per hour in meters.

    Args:
        rpm (float): Loom speed in picks per minute (PPM)
        efficiency_percent (float): Loom efficiency (0-100)
        epi (float): Ends Per Inch (used for pick density reference)
        width_inch (float): Fabric width in inches

    Returns:
        float: Fabric production in meters per hour

    Example:
        >>> production_per_loom(600, 85, 60, 60)
        ~51 meters/hour
    """
    validate_positive(rpm, "RPM")
    validate_positive(efficiency_percent, "Efficiency")
    validate_positive(epi, "EPI")
    validate_positive(width_inch, "Width")
    picks_per_hour = rpm * 60 * (efficiency_percent / 100)
    meters_per_hour = (picks_per_hour / epi) * 0.0254 * width_inch
    return round(meters_per_hour, 2)
