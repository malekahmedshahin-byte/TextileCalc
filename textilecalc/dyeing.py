from utils.validator import validate_positive


def dye_required(fabric_weight, shade_percent):
    """
    Calculate amount of dye required for a given fabric weight and shade.

    Args:
        fabric_weight (float): Weight of fabric/yarn in grams
        shade_percent (float): Required shade percentage (e.g. 2 for 2%)

    Returns:
        float: Dye required in grams

    Example:
        >>> dye_required(1000, 2)
        20.0
    """
    validate_positive(fabric_weight, "Fabric Weight")
    validate_positive(shade_percent, "Shade %")
    return (fabric_weight * shade_percent) / 100


def liquor_required(material_weight, mlr):
    """
    Calculate total liquor (water) required based on Material-to-Liquor Ratio (MLR).

    Args:
        material_weight (float): Weight of material in kg
        mlr (float): Material to Liquor Ratio (e.g. 10 for 1:10)

    Returns:
        float: Total liquor required in Liters

    Example:
        >>> liquor_required(5, 10)
        50.0
    """
    validate_positive(material_weight, "Material Weight")
    validate_positive(mlr, "MLR")
    return material_weight * mlr


def chemical_required(material_weight, percent):
    """
    Calculate chemical required based on percentage on weight of fabric (owf).

    Args:
        material_weight (float): Weight of material in grams
        percent (float): Chemical percentage on weight of fabric (owf)

    Returns:
        float: Chemical required in grams

    Example:
        >>> chemical_required(1000, 5)
        50.0
    """
    validate_positive(material_weight, "Material Weight")
    validate_positive(percent, "Percent")
    return (material_weight * percent) / 100


def salt_required(fabric_weight, shade_percent):
    """
    Estimate salt required for reactive dyeing based on shade depth.
    Standard guideline: light shade (<1%) = 40 g/L, medium (1-3%) = 60 g/L,
    dark (>3%) = 80 g/L.

    Args:
        fabric_weight (float): Weight of fabric in kg
        shade_percent (float): Shade percentage

    Returns:
        float: Recommended salt in grams per liter (g/L)

    Example:
        >>> salt_required(10, 2)
        60
    """
    validate_positive(fabric_weight, "Fabric Weight")
    validate_positive(shade_percent, "Shade %")
    if shade_percent < 1:
        return 40
    elif shade_percent <= 3:
        return 60
    else:
        return 80


def soda_ash_required(material_weight, percent=20):
    """
    Calculate soda ash (Na2CO3) required for reactive dyeing fixation.
    Default is 20% owf — industry standard.

    Args:
        material_weight (float): Weight of fabric in grams
        percent (float): Soda ash percentage owf (default: 20)

    Returns:
        float: Soda ash required in grams

    Example:
        >>> soda_ash_required(1000)
        200.0
    """
    validate_positive(material_weight, "Material Weight")
    return (material_weight * percent) / 100
