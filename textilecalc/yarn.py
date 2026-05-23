from utils.validator import validate_positive


def ne_to_tex(ne):
    """
    Convert yarn count from Ne (English Cotton Count) to Tex.

    Args:
        ne (float): Yarn count in Ne (must be positive)

    Returns:
        float: Yarn count in Tex

    Example:
        >>> ne_to_tex(30)
        19.683...
    """
    validate_positive(ne, "Ne")
    return 590.5 / ne


def tex_to_ne(tex):
    """
    Convert yarn count from Tex to Ne (English Cotton Count).

    Args:
        tex (float): Yarn count in Tex (must be positive)

    Returns:
        float: Yarn count in Ne

    Example:
        >>> tex_to_ne(20)
        29.525
    """
    validate_positive(tex, "Tex")
    return 590.5 / tex


def tex_to_denier(tex):
    """
    Convert yarn count from Tex to Denier.

    Args:
        tex (float): Yarn count in Tex (must be positive)

    Returns:
        float: Yarn count in Denier (1 Tex = 9 Denier)

    Example:
        >>> tex_to_denier(20)
        180
    """
    validate_positive(tex, "Tex")
    return tex * 9


def denier_to_tex(denier):
    """
    Convert yarn count from Denier to Tex.

    Args:
        denier (float): Yarn count in Denier (must be positive)

    Returns:
        float: Yarn count in Tex

    Example:
        >>> denier_to_tex(180)
        20.0
    """
    validate_positive(denier, "Denier")
    return denier / 9


def ne_to_denier(ne):
    """
    Convert yarn count from Ne to Denier directly.

    Args:
        ne (float): Yarn count in Ne (must be positive)

    Returns:
        float: Yarn count in Denier

    Example:
        >>> ne_to_denier(30)
        177.15
    """
    validate_positive(ne, "Ne")
    return (590.5 / ne) * 9


def cv_percentage(sd, mean):
    """
    Calculate Coefficient of Variation (CV%) — measures yarn evenness/unevenness.

    Args:
        sd (float): Standard deviation of yarn count
        mean (float): Mean yarn count value (must be positive)

    Returns:
        float: CV% value (lower is better quality)

    Example:
        >>> cv_percentage(1.5, 30)
        5.0
    """
    validate_positive(mean, "Mean")
    return (sd / mean) * 100


def csp(count, strength):
    """
    Calculate Count Strength Product (CSP) — indicates yarn quality.

    Args:
        count (float): Yarn count in Ne
        strength (float): Lea strength in lbs

    Returns:
        float: CSP value (higher is better quality)

    Example:
        >>> csp(30, 80)
        2400
    """
    validate_positive(count, "Count")
    validate_positive(strength, "Strength")
    return count * strength
