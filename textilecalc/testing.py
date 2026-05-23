from utils.validator import validate_positive


def tensile_strength(force, area):
    """
    Calculate tensile strength of yarn or fabric.

    Args:
        force (float): Breaking force in Newtons (N)
        area (float): Cross-sectional area in mm²

    Returns:
        float: Tensile strength in N/mm² (MPa)

    Example:
        >>> tensile_strength(500, 10)
        50.0
    """
    validate_positive(force, "Force")
    validate_positive(area, "Area")
    return force / area


def elongation_percent(final_length, original_length):
    """
    Calculate elongation at break percentage.

    Args:
        final_length (float): Extended/final length at break (mm or cm)
        original_length (float): Original gauge length (mm or cm)

    Returns:
        float: Elongation percentage

    Example:
        >>> elongation_percent(130, 100)
        30.0
    """
    validate_positive(final_length, "Final Length")
    validate_positive(original_length, "Original Length")
    return ((final_length - original_length) / original_length) * 100


def bursting_strength(force, fabric_area):
    """
    Calculate bursting strength of fabric.

    Args:
        force (float): Bursting force/pressure (kPa or psi)
        fabric_area (float): Test area in cm²

    Returns:
        float: Bursting strength per unit area

    Example:
        >>> bursting_strength(200, 10)
        20.0
    """
    validate_positive(force, "Force")
    validate_positive(fabric_area, "Fabric Area")
    return force / fabric_area


def abrasion_index(loss_weight, initial_weight):
    """
    Calculate abrasion resistance index — percentage of weight lost after abrasion test.

    Args:
        loss_weight (float): Weight lost after abrasion test in grams
        initial_weight (float): Initial fabric weight before test in grams

    Returns:
        float: Abrasion loss percentage (lower is better — more resistant)

    Example:
        >>> abrasion_index(2, 100)
        2.0
    """
    validate_positive(loss_weight, "Loss Weight")
    validate_positive(initial_weight, "Initial Weight")
    if loss_weight > initial_weight:
        raise ValueError("Loss weight cannot exceed initial weight.")
    return (loss_weight / initial_weight) * 100


def stiffness_index(bending_length_cm):
    """
    Calculate fabric flexural rigidity / stiffness from bending length (Cantilever method).
    Stiffness = (bending_length)³ × GSM × 9.807 × 10⁻⁶  (mN·m)

    Args:
        bending_length_cm (float): Bending length in cm (from cantilever test)

    Returns:
        float: Bending length cubed (indicator — multiply by GSM separately if needed)

    Example:
        >>> stiffness_index(3.5)
        42.875
    """
    validate_positive(bending_length_cm, "Bending Length")
    return round(bending_length_cm ** 3, 4)


def color_fastness_grade(rating):
    """
    Interpret color fastness test rating (1–5 grey scale).

    Args:
        rating (int/float): Rating from 1 to 5

    Returns:
        str: Grade description

    Example:
        >>> color_fastness_grade(4)
        'Good'
    """
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5.")
    grades = {1: "Very Poor", 2: "Poor", 3: "Moderate", 4: "Good", 5: "Excellent"}
    return grades[int(rating)]
