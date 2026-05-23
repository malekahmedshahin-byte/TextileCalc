from utils.validator import validate_positive


def yarn_twist_tpi(twist, length_inches):
    """
    Calculate Twist Per Inch (TPI) of yarn.

    Args:
        twist (float): Total number of twists counted
        length_inches (float): Sample length in inches

    Returns:
        float: Twist Per Inch (TPI)

    Example:
        >>> yarn_twist_tpi(200, 10)
        20.0
    """
    validate_positive(twist, "Twist")
    validate_positive(length_inches, "Length")
    return twist / length_inches


def yarn_tpm(tpi):
    """
    Convert Twist Per Inch (TPI) to Twist Per Meter (TPM).
    1 inch = 39.37 mm, so TPM = TPI × 39.37

    Args:
        tpi (float): Twist Per Inch

    Returns:
        float: Twist Per Meter (TPM)

    Example:
        >>> yarn_tpm(20)
        787.4
    """
    validate_positive(tpi, "TPI")
    return tpi * 39.37


def yarn_imperfection(u_percent, thin, thick, neps):
    """
    Calculate Imperfection Index (IPI) — total yarn defects per km.
    IPI = Thin places + Thick places + Neps (per km)

    Args:
        u_percent (float): Yarn unevenness U% (not included in IPI count but noted)
        thin (float): Thin places per km (-50% sensitivity)
        thick (float): Thick places per km (+50% sensitivity)
        neps (float): Neps per km (+200% sensitivity)

    Returns:
        float: Total Imperfection Index (IPI) — lower is better

    Example:
        >>> yarn_imperfection(12, 10, 30, 50)
        90
    """
    validate_positive(u_percent, "U%")
    return thin + thick + neps


def spinning_efficiency(actual_output, theoretical_output):
    """
    Calculate spinning machine efficiency.

    Args:
        actual_output (float): Actual production output (kg/hour)
        theoretical_output (float): Theoretical/calculated max output (kg/hour)

    Returns:
        float: Efficiency percentage

    Example:
        >>> spinning_efficiency(80, 100)
        80.0
    """
    validate_positive(actual_output, "Actual Output")
    validate_positive(theoretical_output, "Theoretical Output")
    return (actual_output / theoretical_output) * 100


def draft(feed_count, delivery_count):
    """
    Calculate draft ratio in spinning — how much the fiber is attenuated.

    Args:
        feed_count (float): Input sliver/roving count (Ne or tex)
        delivery_count (float): Output yarn count (Ne or tex)

    Returns:
        float: Draft ratio

    Example:
        >>> draft(0.5, 30)
        60.0
    """
    validate_positive(feed_count, "Feed Count")
    validate_positive(delivery_count, "Delivery Count")
    return delivery_count / feed_count
