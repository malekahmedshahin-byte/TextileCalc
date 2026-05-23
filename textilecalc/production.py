from utils.validator import validate_positive


def efficiency(actual, target):
    """
    Calculate production efficiency percentage.

    Args:
        actual (float): Actual production output
        target (float): Target/planned production output

    Returns:
        float: Efficiency percentage

    Example:
        >>> efficiency(900, 1000)
        90.0
    """
    validate_positive(actual, "Actual")
    validate_positive(target, "Target")
    return (actual / target) * 100


def production_rate(output, hours):
    """
    Calculate production rate per hour.

    Args:
        output (float): Total output produced (kg, meters, pieces)
        hours (float): Total time in hours

    Returns:
        float: Production rate per hour

    Example:
        >>> production_rate(500, 8)
        62.5
    """
    validate_positive(output, "Output")
    validate_positive(hours, "Hours")
    return output / hours


def machine_utilization(run_time, available_time):
    """
    Calculate machine utilization percentage.

    Args:
        run_time (float): Actual machine running time in hours
        available_time (float): Total available time in hours

    Returns:
        float: Utilization percentage

    Example:
        >>> machine_utilization(7, 8)
        87.5
    """
    validate_positive(run_time, "Run Time")
    validate_positive(available_time, "Available Time")
    return (run_time / available_time) * 100


def daily_production_target(shift_hours, efficiency_percent, machine_speed, count_ne):
    """
    Estimate daily yarn production target for a spinning frame.

    Args:
        shift_hours (float): Hours per shift
        efficiency_percent (float): Machine efficiency (e.g. 85)
        machine_speed (float): Spindle speed in RPM
        count_ne (float): Yarn count in Ne

    Returns:
        float: Estimated production in kg per spindle per shift

    Example:
        >>> daily_production_target(8, 85, 14000, 30)
        ~1.2 kg approx
    """
    validate_positive(shift_hours, "Shift Hours")
    validate_positive(efficiency_percent, "Efficiency %")
    validate_positive(machine_speed, "Machine Speed")
    validate_positive(count_ne, "Count Ne")
    tpi = 4.5  # approximate twist multiplier for standard carded cotton
    delivery_rate = machine_speed / (tpi * 39.37)  # meters per minute
    grams_per_min = (delivery_rate * 1000) / (count_ne * 1.693)
    kg_per_shift = (grams_per_min * 60 * shift_hours * (efficiency_percent / 100)) / 1000
    return round(kg_per_shift, 3)
