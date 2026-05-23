from utils.validator import validate_positive


def cost_per_meter(total_cost, length):
    """
    Calculate production cost per meter of fabric.

    Args:
        total_cost (float): Total production cost
        length (float): Total fabric length produced in meters

    Returns:
        float: Cost per meter

    Example:
        >>> cost_per_meter(5000, 200)
        25.0
    """
    validate_positive(total_cost, "Total Cost")
    validate_positive(length, "Length")
    return total_cost / length


def energy_cost(power_kw, hours, rate):
    """
    Calculate total electricity/energy cost.

    Args:
        power_kw (float): Machine power consumption in kilowatts (kW)
        hours (float): Total running hours
        rate (float): Electricity rate per kWh (cost per unit)

    Returns:
        float: Total energy cost

    Example:
        >>> energy_cost(5, 8, 0.15)
        6.0
    """
    validate_positive(power_kw, "Power (kW)")
    validate_positive(hours, "Hours")
    validate_positive(rate, "Rate")
    return power_kw * hours * rate


def depreciation(machine_cost, life_years):
    """
    Calculate annual straight-line depreciation of a machine.

    Args:
        machine_cost (float): Total purchase cost of machine
        life_years (float): Expected useful life in years

    Returns:
        float: Annual depreciation amount

    Example:
        >>> depreciation(100000, 10)
        10000.0
    """
    validate_positive(machine_cost, "Machine Cost")
    validate_positive(life_years, "Life Years")
    return machine_cost / life_years


def profit_margin(selling_price, cost_price):
    """
    Calculate profit margin percentage.

    Args:
        selling_price (float): Total selling price
        cost_price (float): Total cost price

    Returns:
        float: Profit margin percentage

    Example:
        >>> profit_margin(1200, 1000)
        20.0
    """
    validate_positive(selling_price, "Selling Price")
    validate_positive(cost_price, "Cost Price")
    return ((selling_price - cost_price) / cost_price) * 100


def total_manufacturing_cost(raw_material, direct_labor, factory_overhead):
    """
    Calculate total manufacturing cost (TMC) — standard accounting formula.

    Args:
        raw_material (float): Raw material cost
        direct_labor (float): Direct labor cost
        factory_overhead (float): Factory overhead cost

    Returns:
        float: Total manufacturing cost

    Example:
        >>> total_manufacturing_cost(5000, 2000, 1500)
        8500
    """
    validate_positive(raw_material, "Raw Material")
    validate_positive(direct_labor, "Direct Labor")
    validate_positive(factory_overhead, "Factory Overhead")
    return raw_material + direct_labor + factory_overhead
