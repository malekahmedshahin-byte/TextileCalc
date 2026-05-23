from utils.validator import validate_positive


def wastage_percentage(input_weight, output_weight):
    """
    Calculate wastage/loss percentage during textile processing.

    Args:
        input_weight (float): Input material weight (before processing)
        output_weight (float): Output material weight (after processing)

    Returns:
        float: Wastage percentage

    Example:
        >>> wastage_percentage(100, 92)
        8.0
    """
    validate_positive(input_weight, "Input Weight")
    validate_positive(output_weight, "Output Weight")
    if output_weight > input_weight:
        raise ValueError("Output weight cannot be greater than input weight.")
    return ((input_weight - output_weight) / input_weight) * 100


def material_required_with_wastage(required_output, wastage_percent):
    """
    Calculate how much raw material to order/use considering expected wastage.

    Args:
        required_output (float): Final output quantity needed (kg/meters)
        wastage_percent (float): Expected wastage percentage (e.g. 5 for 5%)

    Returns:
        float: Raw material input needed

    Example:
        >>> material_required_with_wastage(950, 5)
        1000.0
    """
    validate_positive(required_output, "Required Output")
    validate_positive(wastage_percent, "Wastage %")
    if wastage_percent >= 100:
        raise ValueError("Wastage cannot be 100% or more.")
    return required_output / (1 - wastage_percent / 100)
