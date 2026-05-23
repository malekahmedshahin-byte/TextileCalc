from utils.validator import validate_positive


def yarn_cost(weight, rate):
    """
    Calculate total yarn cost.

    Args:
        weight (float): Yarn weight in kg or lbs
        rate (float): Rate per unit weight (cost per kg/lb)

    Returns:
        float: Total yarn cost

    Example:
        >>> yarn_cost(100, 3.5)
        350.0
    """
    validate_positive(weight, "Weight")
    validate_positive(rate, "Rate")
    return weight * rate


def process_cost(material_cost, labor_cost, overhead):
    """
    Calculate total process cost (material + labor + overhead).

    Args:
        material_cost (float): Total material/raw material cost
        labor_cost (float): Total labor/wages cost
        overhead (float): Overhead/indirect costs

    Returns:
        float: Total process cost

    Example:
        >>> process_cost(500, 200, 100)
        800
    """
    validate_positive(material_cost, "Material Cost")
    validate_positive(labor_cost, "Labor Cost")
    validate_positive(overhead, "Overhead")
    return material_cost + labor_cost + overhead


def profit_price(total_cost, profit_percent):
    """
    Calculate selling price based on desired profit percentage.

    Args:
        total_cost (float): Total production cost
        profit_percent (float): Desired profit percentage (e.g. 20 for 20%)

    Returns:
        float: Selling price including profit

    Example:
        >>> profit_price(1000, 20)
        1200.0
    """
    validate_positive(total_cost, "Total Cost")
    validate_positive(profit_percent, "Profit %")
    return total_cost + (total_cost * profit_percent / 100)


def break_even_units(fixed_cost, selling_price_per_unit, variable_cost_per_unit):
    """
    Calculate break-even point — how many units must be sold to cover all costs.

    Args:
        fixed_cost (float): Total fixed costs (rent, machines, etc.)
        selling_price_per_unit (float): Price per unit sold
        variable_cost_per_unit (float): Variable cost per unit produced

    Returns:
        float: Number of units needed to break even

    Example:
        >>> break_even_units(10000, 50, 30)
        500.0
    """
    validate_positive(fixed_cost, "Fixed Cost")
    validate_positive(selling_price_per_unit, "Selling Price")
    validate_positive(variable_cost_per_unit, "Variable Cost")
    contribution = selling_price_per_unit - variable_cost_per_unit
    if contribution <= 0:
        raise ValueError("Selling price must be greater than variable cost.")
    return fixed_cost / contribution
