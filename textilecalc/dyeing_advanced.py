from utils.validator import validate_positive


def dye_exhaustion(initial_dye, remaining_dye):
    """
    Calculate dye exhaustion percentage — how much dye was absorbed from bath.

    Args:
        initial_dye (float): Initial dye concentration in dyebath
        remaining_dye (float): Remaining dye concentration after dyeing

    Returns:
        float: Exhaustion percentage (higher is better)

    Example:
        >>> dye_exhaustion(100, 20)
        80.0
    """
    validate_positive(initial_dye, "Initial Dye")
    validate_positive(remaining_dye, "Remaining Dye")
    if remaining_dye > initial_dye:
        raise ValueError("Remaining dye cannot be greater than initial dye.")
    return ((initial_dye - remaining_dye) / initial_dye) * 100


def dye_fixation(fixed_dye, applied_dye):
    """
    Calculate dye fixation percentage — how much absorbed dye actually bonded to fiber.

    Args:
        fixed_dye (float): Amount of dye fixed on fabric
        applied_dye (float): Total dye applied

    Returns:
        float: Fixation percentage

    Example:
        >>> dye_fixation(75, 100)
        75.0
    """
    validate_positive(fixed_dye, "Fixed Dye")
    validate_positive(applied_dye, "Applied Dye")
    if fixed_dye > applied_dye:
        raise ValueError("Fixed dye cannot be greater than applied dye.")
    return (fixed_dye / applied_dye) * 100


def liquor_ratio(material, liquor):
    """
    Calculate Material to Liquor Ratio (MLR).

    Args:
        material (float): Weight of material (g or kg)
        liquor (float): Volume of liquor (ml or L, same unit as material)

    Returns:
        float: Liquor ratio value (e.g. 10 means 1:10)

    Example:
        >>> liquor_ratio(5, 50)
        10.0
    """
    validate_positive(material, "Material")
    validate_positive(liquor, "Liquor")
    return liquor / material


def chemical_utilization(actual, theoretical):
    """
    Calculate chemical utilization efficiency.

    Args:
        actual (float): Actual amount of chemical used
        theoretical (float): Theoretically required amount

    Returns:
        float: Utilization percentage

    Example:
        >>> chemical_utilization(90, 100)
        90.0
    """
    validate_positive(actual, "Actual")
    validate_positive(theoretical, "Theoretical")
    return (actual / theoretical) * 100


def wash_fastness_efficiency(initial_depth, washed_depth):
    """
    Estimate wash fastness loss — how much color depth remained after washing.

    Args:
        initial_depth (float): Initial color depth value
        washed_depth (float): Color depth after washing

    Returns:
        float: Color retention percentage (higher means better wash fastness)

    Example:
        >>> wash_fastness_efficiency(100, 92)
        92.0
    """
    validate_positive(initial_depth, "Initial Depth")
    validate_positive(washed_depth, "Washed Depth")
    return (washed_depth / initial_depth) * 100
