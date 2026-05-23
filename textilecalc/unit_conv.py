def kg_to_lbs(kg):
    """Convert kilograms to pounds. 1 kg = 2.20462 lbs"""
    return kg * 2.20462


def lbs_to_kg(lbs):
    """Convert pounds to kilograms. 1 lb = 0.453592 kg"""
    return lbs / 2.20462


def inch_to_meter(inch):
    """Convert inches to meters. 1 inch = 0.0254 m"""
    return inch * 0.0254


def meter_to_inch(meter):
    """Convert meters to inches. 1 m = 39.3701 inches"""
    return meter / 0.0254


def cm_to_inch(cm):
    """Convert centimeters to inches. 1 cm = 0.3937 inches"""
    return cm / 2.54


def inch_to_cm(inch):
    """Convert inches to centimeters. 1 inch = 2.54 cm"""
    return inch * 2.54


def gsm_to_oz_yd2(gsm):
    """
    Convert fabric weight from GSM (g/m²) to oz/yd².
    1 g/m² = 0.02949 oz/yd²
    """
    return gsm * 0.02949


def oz_yd2_to_gsm(oz):
    """
    Convert fabric weight from oz/yd² to GSM (g/m²).
    1 oz/yd² = 33.906 g/m²
    """
    return oz / 0.02949


def ne_to_nm(ne):
    """
    Convert yarn count from Ne (English Cotton Count) to Nm (Metric Count).
    Nm = Ne × 1.693
    """
    return ne * 1.693


def nm_to_ne(nm):
    """
    Convert yarn count from Nm (Metric Count) to Ne.
    Ne = Nm / 1.693
    """
    return nm / 1.693


def celsius_to_fahrenheit(c):
    """Convert temperature from Celsius to Fahrenheit."""
    return (c * 9/5) + 32


def fahrenheit_to_celsius(f):
    """Convert temperature from Fahrenheit to Celsius."""
    return (f - 32) * 5/9
