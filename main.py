import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from textilecalc import *

# ============================================================
#   ABDUL MALEK — Textile Engineering Calculation Library
#   Version : 2.0.0
#   Developer: Abdul Malek
# ============================================================

VERSION = "2.0.0"

BANNER = r"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║        █████╗ ██████╗ ██████╗ ██╗   ██╗██╗                              ║
║       ██╔══██╗██╔══██╗██╔══██╗██║   ██║██║                              ║
║       ███████║██████╔╝██║  ██║██║   ██║██║                              ║
║       ██╔══██║██╔══██╗██║  ██║██║   ██║██║                              ║
║       ██║  ██║██████╔╝██████╔╝╚██████╔╝███████╗                         ║
║       ╚═╝  ╚═╝╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝                        ║
║                                                                          ║
║        ███╗   ███╗ █████╗ ██╗     ███████╗██╗  ██╗                      ║
║        ████╗ ████║██╔══██╗██║     ██╔════╝██║ ██╔╝                      ║
║        ██╔████╔██║███████║██║     █████╗  █████╔╝                       ║
║        ██║╚██╔╝██║██╔══██║██║     ██╔══╝  ██╔═██╗                       ║
║        ██║ ╚═╝ ██║██║  ██║███████╗███████╗██║  ██╗                      ║
║        ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝                     ║
║                                                                          ║
║      🧵  Python Library for Textile Engineering Calculations  🧵         ║
║                        Version 2.0.0                                     ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

TEXTILE_GLOSSARY = {
    "Ne":        "English Cotton Count — number of 840-yard lengths per pound",
    "Tex":       "Linear density — grams per 1000 meters of yarn",
    "Denier":    "Linear density — grams per 9000 meters of yarn",
    "Nm":        "Metric Count — number of 1000-meter lengths per kilogram",
    "CV%":       "Coefficient of Variation — measures yarn evenness/irregularity",
    "CSP":       "Count Strength Product — yarn quality indicator",
    "GSM":       "Grams per Square Meter — fabric weight per unit area",
    "EPI":       "Ends Per Inch — warp thread density",
    "PPI":       "Picks Per Inch — weft thread density",
    "TPI":       "Twist Per Inch — yarn twist density",
    "TPM":       "Twist Per Meter — metric twist density",
    "MLR":       "Material to Liquor Ratio — used in wet processing",
    "IPI":       "Imperfection Index — total yarn defects per km",
    "OWF":       "On Weight of Fabric — chemical dosing method",
    "TMC":       "Total Manufacturing Cost",
    "RPM":       "Revolutions Per Minute — machine speed",
    "CO2e":      "CO₂ Equivalent — greenhouse gas measurement unit",
    "LCA":       "Life Cycle Assessment — full environmental impact analysis",
    "Delta-E":   "ΔE* — colour difference in CIE Lab* space (lower = closer match)",
    "Lab*":      "CIE L*a*b* — perceptually uniform colour space used in dyeing",
}


# ============================================================
#   UTILITY FUNCTIONS
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line(char="─", width=72):
    print(char * width)


def header(title, subtitle=""):
    print()
    line("═")
    print(f"  🧵  ABDUL MALEK v{VERSION}  │  {title}")
    if subtitle:
        print(f"       {subtitle}")
    line("═")
    print()


def pause():
    input("\n  ↩  Press Enter to continue...")


def get_float(prompt, allow_zero=False):
    """Safely get a positive float from user input."""
    while True:
        try:
            val = float(input(f"  ➤  {prompt}: "))
            if not allow_zero and val <= 0:
                print("  ⚠  Value must be greater than 0. Try again.")
                continue
            if allow_zero and val < 0:
                print("  ⚠  Value cannot be negative. Try again.")
                continue
            return val
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number.")


def get_int(prompt, min_val=1, max_val=99):
    """Safely get an integer choice."""
    while True:
        try:
            val = int(input(f"\n  ➤  {prompt}: "))
            if min_val <= val <= max_val:
                return val
            print(f"  ⚠  Enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number.")


def get_choice_from_list(title, options):
    """Display a numbered list and return the chosen string value."""
    print(f"\n  {title}:")
    for i, opt in enumerate(options, 1):
        print(f"     {i:>2}.  {opt}")
    choice = get_int("Enter number", 1, len(options))
    return options[choice - 1]


def show_result(label, value, unit=""):
    """Display a calculation result in a styled box."""
    print()
    line("─")
    if isinstance(value, float):
        print(f"  ✅  {label} = {value:.4f} {unit}".rstrip())
    else:
        print(f"  ✅  {label} = {value} {unit}".rstrip())
    line("─")


def show_menu(title, options, back_label="Back to Previous Menu"):
    """Display a numbered menu and return user choice."""
    header(title)
    for i, opt in enumerate(options, 1):
        print(f"   {i:>2}.  {opt}")
    print(f"   {len(options)+1:>2}.  🔙 {back_label}")
    return get_int("Enter choice", 1, len(options) + 1)


# ============================================================
#   1. YARN MODULE
# ============================================================

def yarn_menu():
    options = [
        "Ne → Tex",
        "Tex → Ne",
        "Tex → Denier",
        "Denier → Tex",
        "Ne → Denier",
        "CV% (Coefficient of Variation)",
        "CSP (Count Strength Product)",
    ]
    while True:
        choice = show_menu("YARN CALCULATIONS", options)

        if choice == 1:
            ne = get_float("Enter Count (Ne)")
            show_result("Tex", ne_to_tex(ne), "Tex")

        elif choice == 2:
            tex = get_float("Enter Count (Tex)")
            show_result("Ne", tex_to_ne(tex), "Ne")

        elif choice == 3:
            tex = get_float("Enter Count (Tex)")
            show_result("Denier", tex_to_denier(tex), "den")

        elif choice == 4:
            den = get_float("Enter Count (Denier)")
            show_result("Tex", denier_to_tex(den), "Tex")

        elif choice == 5:
            ne = get_float("Enter Count (Ne)")
            show_result("Denier", ne_to_denier(ne), "den")

        elif choice == 6:
            print("\n  CV% measures how uneven/irregular your yarn is.")
            print("  Lower CV% = better quality yarn.\n")
            sd   = get_float("Enter Standard Deviation (SD)")
            mean = get_float("Enter Mean Value")
            show_result("CV%", cv_percentage(sd, mean), "%")

        elif choice == 7:
            print("\n  CSP = Count × Strength. Higher CSP = better yarn quality.\n")
            count    = get_float("Enter Yarn Count (Ne)")
            strength = get_float("Enter Lea Strength (lbs)")
            show_result("CSP", csp(count, strength), "")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   2. FABRIC MODULE
# ============================================================

def fabric_menu():
    options = [
        "GSM — Grams per Square Meter",
        "Fabric Weight (from GSM)",
        "Warp Cover Factor",
        "Weft Cover Factor",
        "Total Cover Factor (Peirce formula)",
        "Shrinkage %",
    ]
    while True:
        choice = show_menu("FABRIC CALCULATIONS", options)

        if choice == 1:
            print("\n  Sample size: measure a small piece of fabric.\n")
            w = get_float("Enter Sample Weight (g)")
            l = get_float("Enter Sample Length (m)")
            b = get_float("Enter Sample Width (m)")
            show_result("GSM", gsm(w, l, b), "g/m²")

        elif choice == 2:
            g = get_float("Enter Fabric GSM (g/m²)")
            w = get_float("Enter Fabric Width (m)")
            l = get_float("Enter Fabric Length (m)")
            show_result("Fabric Weight", fabric_weight(g, w, l), "grams")

        elif choice == 3:
            epi = get_float("Enter EPI (Ends Per Inch)")
            cnt = get_float("Enter Warp Yarn Count (Ne)")
            show_result("Warp Cover Factor", warp_cover_factor(epi, cnt), "")

        elif choice == 4:
            ppi = get_float("Enter PPI (Picks Per Inch)")
            cnt = get_float("Enter Weft Yarn Count (Ne)")
            show_result("Weft Cover Factor", weft_cover_factor(ppi, cnt), "")

        elif choice == 5:
            print("\n  Uses Peirce's formula: CF = Warp CF + Weft CF - (Warp×Weft / 28)\n")
            epi = get_float("Enter EPI (Ends Per Inch)")
            ppi = get_float("Enter PPI (Picks Per Inch)")
            cnt = get_float("Enter Yarn Count (Ne)")
            show_result("Total Cover Factor", cover_factor(epi, ppi, cnt), "")

        elif choice == 6:
            print("\n  Positive result = shrinkage. Negative = fabric growth.\n")
            orig = get_float("Enter Original Dimension (cm)")
            fin  = get_float("Enter Final Dimension after Wash (cm)")
            show_result("Shrinkage", shrinkage_percent(orig, fin), "%")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   3. DYEING MODULE
# ============================================================

def dyeing_menu():
    options = [
        "Dye Required (owf %)",
        "Liquor Volume Required (MLR)",
        "Chemical Required (owf %)",
        "Salt Required (Reactive Dyeing)",
        "Soda Ash Required (Reactive Dyeing)",
    ]
    while True:
        choice = show_menu("DYEING CALCULATIONS", options)

        if choice == 1:
            w = get_float("Enter Fabric/Yarn Weight (g)")
            s = get_float("Enter Shade % (e.g. 2 for 2%)")
            show_result("Dye Required", dye_required(w, s), "grams")

        elif choice == 2:
            w = get_float("Enter Material Weight (kg)")
            r = get_float("Enter MLR (e.g. 10 for 1:10)")
            show_result("Liquor Required", liquor_required(w, r), "Liters")

        elif choice == 3:
            w = get_float("Enter Material Weight (g)")
            p = get_float("Enter Chemical % owf")
            show_result("Chemical Required", chemical_required(w, p), "grams")

        elif choice == 4:
            print("\n  Based on shade depth:")
            print("  < 1%  →  40 g/L  |  1–3%  →  60 g/L  |  > 3%  →  80 g/L\n")
            w = get_float("Enter Fabric Weight (kg)")
            s = get_float("Enter Shade %")
            show_result("Recommended Salt", salt_required(w, s), "g/L")

        elif choice == 5:
            print("\n  Standard soda ash dose is 20% owf for reactive dyeing.\n")
            w = get_float("Enter Material Weight (g)")
            p = get_float("Enter Soda Ash % owf (default 20)")
            show_result("Soda Ash Required", soda_ash_required(w, p), "grams")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   4. ADVANCED DYEING MODULE
# ============================================================

def dyeing_advanced_menu():
    options = [
        "Dye Exhaustion %",
        "Dye Fixation %",
        "Liquor Ratio (MLR)",
        "Chemical Utilization %",
        "Wash Fastness Efficiency %",
    ]
    while True:
        choice = show_menu("ADVANCED DYEING", options)

        if choice == 1:
            print("\n  How much dye transferred from bath to fabric.\n")
            ini = get_float("Enter Initial Dye Concentration")
            rem = get_float("Enter Remaining Dye in Bath")
            show_result("Dye Exhaustion", dye_exhaustion(ini, rem), "%")

        elif choice == 2:
            print("\n  How much absorbed dye actually bonded to the fiber.\n")
            fix = get_float("Enter Fixed Dye Amount")
            app = get_float("Enter Total Applied Dye")
            show_result("Dye Fixation", dye_fixation(fix, app), "%")

        elif choice == 3:
            m = get_float("Enter Material Weight (g or kg)")
            l = get_float("Enter Liquor Volume (ml or L)")
            show_result("Liquor Ratio (1 : X)", liquor_ratio(m, l), "")

        elif choice == 4:
            a = get_float("Enter Actual Chemical Used")
            t = get_float("Enter Theoretical Chemical Required")
            show_result("Chemical Utilization", chemical_utilization(a, t), "%")

        elif choice == 5:
            print("\n  Color depth retained after washing.\n")
            ini = get_float("Enter Initial Color Depth")
            wsh = get_float("Enter Color Depth After Wash")
            show_result("Wash Fastness Efficiency", wash_fastness_efficiency(ini, wsh), "%")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   5. COSTING MODULE
# ============================================================

def costing_menu():
    options = [
        "Yarn Cost",
        "Process Cost (Material + Labour + Overhead)",
        "Selling Price (Cost + Profit %)",
        "Break-Even Units",
    ]
    while True:
        choice = show_menu("COSTING", options)

        if choice == 1:
            w = get_float("Enter Yarn Weight (kg or lb)")
            r = get_float("Enter Rate per Unit Weight")
            show_result("Yarn Cost", yarn_cost(w, r), "")

        elif choice == 2:
            m = get_float("Enter Material Cost")
            l = get_float("Enter Labour Cost")
            o = get_float("Enter Overhead Cost")
            show_result("Total Process Cost", process_cost(m, l, o), "")

        elif choice == 3:
            c = get_float("Enter Total Cost Price")
            p = get_float("Enter Desired Profit %")
            show_result("Selling Price", profit_price(c, p), "")

        elif choice == 4:
            print("\n  Units needed to cover all costs (profit = 0).\n")
            fc = get_float("Enter Total Fixed Cost")
            sp = get_float("Enter Selling Price per Unit")
            vc = get_float("Enter Variable Cost per Unit")
            try:
                show_result("Break-Even Units", break_even_units(fc, sp, vc), "units")
            except ValueError as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   6. ADVANCED COSTING MODULE
# ============================================================

def costing_advanced_menu():
    options = [
        "Cost per Meter",
        "Energy / Electricity Cost",
        "Machine Depreciation (per year)",
        "Profit Margin %",
        "Total Manufacturing Cost (TMC)",
    ]
    while True:
        choice = show_menu("ADVANCED COSTING", options)

        if choice == 1:
            c = get_float("Enter Total Production Cost")
            l = get_float("Enter Total Length Produced (meters)")
            show_result("Cost per Meter", cost_per_meter(c, l), "per meter")

        elif choice == 2:
            pw = get_float("Enter Power Consumption (kW)")
            hr = get_float("Enter Running Hours")
            rt = get_float("Enter Electricity Rate per kWh")
            show_result("Energy Cost", energy_cost(pw, hr, rt), "")

        elif choice == 3:
            mc = get_float("Enter Machine Purchase Cost")
            ly = get_float("Enter Machine Life (years)")
            show_result("Annual Depreciation", depreciation(mc, ly), "per year")

        elif choice == 4:
            sp = get_float("Enter Selling Price")
            cp = get_float("Enter Cost Price")
            show_result("Profit Margin", profit_margin(sp, cp), "%")

        elif choice == 5:
            rm = get_float("Enter Raw Material Cost")
            dl = get_float("Enter Direct Labour Cost")
            fo = get_float("Enter Factory Overhead Cost")
            show_result("Total Manufacturing Cost", total_manufacturing_cost(rm, dl, fo), "")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   7. PRODUCTION MODULE
# ============================================================

def production_menu():
    options = [
        "Production Efficiency %",
        "Production Rate (per hour)",
        "Machine Utilization %",
        "Daily Production Target (Spinning)",
    ]
    while True:
        choice = show_menu("PRODUCTION", options)

        if choice == 1:
            a = get_float("Enter Actual Production")
            t = get_float("Enter Target Production")
            show_result("Efficiency", efficiency(a, t), "%")

        elif choice == 2:
            o = get_float("Enter Total Output (kg / meters / pieces)")
            h = get_float("Enter Total Hours")
            show_result("Production Rate", production_rate(o, h), "per hour")

        elif choice == 3:
            r = get_float("Enter Machine Run Time (hours)")
            a = get_float("Enter Total Available Time (hours)")
            show_result("Machine Utilization", machine_utilization(r, a), "%")

        elif choice == 4:
            print("\n  Estimates yarn production per spindle per shift.\n")
            sh = get_float("Enter Shift Duration (hours)")
            ef = get_float("Enter Machine Efficiency %")
            ms = get_float("Enter Spindle Speed (RPM)")
            cn = get_float("Enter Yarn Count (Ne)")
            show_result("Daily Production Target", daily_production_target(sh, ef, ms, cn), "kg/spindle/shift")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   8. SPINNING MODULE
# ============================================================

def spinning_menu():
    options = [
        "Yarn Twist — TPI (Twist Per Inch)",
        "Convert TPI → TPM (Twist Per Meter)",
        "Imperfection Index (IPI)",
        "Spinning Efficiency %",
        "Draft Ratio",
    ]
    while True:
        choice = show_menu("SPINNING CALCULATIONS", options)

        if choice == 1:
            tw = get_float("Enter Total Number of Twists counted")
            ln = get_float("Enter Sample Length (inches)")
            show_result("TPI", yarn_twist_tpi(tw, ln), "Twist/inch")

        elif choice == 2:
            tpi = get_float("Enter TPI (Twist Per Inch)")
            show_result("TPM", yarn_tpm(tpi), "Twist/meter")

        elif choice == 3:
            print("\n  IPI = Thin places + Thick places + Neps (per km)")
            print("  Lower IPI = better quality yarn.\n")
            u   = get_float("Enter U% (Evenness, for reference)")
            th  = get_float("Enter Thin places per km  (-50% sensitivity)")
            tk  = get_float("Enter Thick places per km (+50% sensitivity)")
            nep = get_float("Enter Neps per km         (+200% sensitivity)")
            show_result("Imperfection Index (IPI)", yarn_imperfection(u, th, tk, nep), "per km")

        elif choice == 4:
            ao = get_float("Enter Actual Output")
            to = get_float("Enter Theoretical Output")
            show_result("Spinning Efficiency", spinning_efficiency(ao, to), "%")

        elif choice == 5:
            print("\n  Draft = how much the fiber strand is drawn out / attenuated.\n")
            feed = get_float("Enter Feed Count (Ne or Tex)")
            delv = get_float("Enter Delivery Count (Ne or Tex)")
            show_result("Draft Ratio", draft(feed, delv), "")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   9. WEAVING MODULE
# ============================================================

def weaving_menu():
    options = [
        "Loom Efficiency %",
        "Warp Break Rate",
        "Weft Break Rate",
        "Fabric Defect Rate",
        "Production per Loom (meters/hour)",
    ]
    while True:
        choice = show_menu("WEAVING CALCULATIONS", options)

        if choice == 1:
            ac = get_float("Enter Actual Picks/Output")
            id = get_float("Enter Ideal/Theoretical Picks/Output")
            show_result("Loom Efficiency", loom_efficiency(ac, id), "%")

        elif choice == 2:
            br = get_float("Enter Total Warp Breaks observed")
            en = get_float("Enter Total Warp Ends in loom")
            show_result("Warp Break Rate", warp_break_rate(br, en), "%")

        elif choice == 3:
            br = get_float("Enter Total Weft Breaks observed")
            pk = get_float("Enter Total Picks inserted")
            show_result("Weft Break Rate", weft_break_rate(br, pk), "%")

        elif choice == 4:
            df = get_float("Enter Total Defects found")
            ln = get_float("Enter Total Inspected Length (meters)")
            show_result("Defect Rate", fabric_defect_rate(df, ln), "defects/meter")

        elif choice == 5:
            print("\n  Calculates how many meters of fabric a loom produces per hour.\n")
            rpm = get_float("Enter Loom Speed (PPM — picks per minute)")
            ef  = get_float("Enter Loom Efficiency %")
            epi = get_float("Enter EPI (Ends Per Inch)")
            wi  = get_float("Enter Fabric Width (inches)")
            show_result("Production per Loom", production_per_loom(rpm, ef, epi, wi), "meters/hour")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   10. QUALITY CONTROL MODULE
# ============================================================

def qc_menu():
    options = [
        "Moisture Regain %",
        "Moisture Content %",
        "Shrinkage %",
        "Absorbency Rate %",
        "Pilling Resistance Grade (1–5)",
    ]
    while True:
        choice = show_menu("QUALITY CONTROL", options)

        if choice == 1:
            print("\n  Formula: ((Wet − Dry) / Dry) × 100\n")
            ow = get_float("Enter Original/Conditioned Weight (g)")
            dw = get_float("Enter Oven-Dry Weight (g)")
            show_result("Moisture Regain", moisture_regain(ow, dw), "%")

        elif choice == 2:
            print("\n  Formula: ((Wet − Dry) / Wet) × 100  (denominator differs from regain)\n")
            ow = get_float("Enter Original/Wet Weight (g)")
            dw = get_float("Enter Oven-Dry Weight (g)")
            show_result("Moisture Content", moisture_content(ow, dw), "%")

        elif choice == 3:
            orig = get_float("Enter Original Dimension (cm or inch)")
            fin  = get_float("Enter Final Dimension after Wash")
            show_result("Shrinkage", shrinkage_percent(orig, fin), "%")

        elif choice == 4:
            wa = get_float("Enter Water Absorbed (g)")
            dw = get_float("Enter Dry Fabric Weight (g)")
            show_result("Absorbency Rate", absorbency_rate(wa, dw), "%")

        elif choice == 5:
            print("\n  Grey scale: 1 = Very Poor   2 = Poor   3 = Moderate   4 = Good   5 = Excellent\n")
            sc = get_float("Enter Pilling Score (1–5)")
            try:
                grade = pilling_resistance_grade(sc)
                show_result("Grade", grade, "")
            except ValueError as e:
                print(f"\n  ❌  {e}")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   11. TEXTILE TESTING LAB
# ============================================================

def testing_menu():
    options = [
        "Tensile Strength (N/mm²)",
        "Elongation at Break %",
        "Bursting Strength",
        "Abrasion Index %",
        "Stiffness Index (Bending Length³)",
        "Color Fastness Grade (1–5)",
    ]
    while True:
        choice = show_menu("TEXTILE TESTING LAB", options)

        if choice == 1:
            f = get_float("Enter Breaking Force (N)")
            a = get_float("Enter Cross-sectional Area (mm²)")
            show_result("Tensile Strength", tensile_strength(f, a), "N/mm²")

        elif choice == 2:
            fl = get_float("Enter Final/Extended Length (mm or cm)")
            ol = get_float("Enter Original Gauge Length (mm or cm)")
            show_result("Elongation", elongation_percent(fl, ol), "%")

        elif choice == 3:
            f = get_float("Enter Pressure/Force (kPa or psi)")
            a = get_float("Enter Test Area (cm²)")
            show_result("Bursting Strength", bursting_strength(f, a), "per unit area")

        elif choice == 4:
            print("\n  Lower abrasion index = more durable/resistant fabric.\n")
            lw = get_float("Enter Weight Loss after test (g)")
            iw = get_float("Enter Initial Weight before test (g)")
            try:
                show_result("Abrasion Index", abrasion_index(lw, iw), "%")
            except ValueError as e:
                print(f"\n  ❌  {e}")

        elif choice == 5:
            print("\n  From Cantilever test — cube of bending length (cm³).\n")
            bl = get_float("Enter Bending Length (cm)")
            show_result("Stiffness Index (BL³)", stiffness_index(bl), "cm³")

        elif choice == 6:
            print("\n  Grey scale: 1 = Very Poor   2 = Poor   3 = Moderate   4 = Good   5 = Excellent\n")
            rt = get_float("Enter Rating (1–5)")
            try:
                grade = color_fastness_grade(rt)
                show_result("Color Fastness", grade, "")
            except ValueError as e:
                print(f"\n  ❌  {e}")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   12. WASTAGE MODULE
# ============================================================

def wastage_menu():
    options = [
        "Wastage / Loss %",
        "Raw Material Required (with expected wastage)",
    ]
    while True:
        choice = show_menu("WASTAGE CALCULATIONS", options)

        if choice == 1:
            inp = get_float("Enter Input Material Weight")
            out = get_float("Enter Output Material Weight")
            try:
                show_result("Wastage", wastage_percentage(inp, out), "%")
            except ValueError as e:
                print(f"\n  ❌  {e}")

        elif choice == 2:
            print("\n  How much raw material to order to get your required output.\n")
            req = get_float("Enter Required Final Output (kg or meters)")
            wp  = get_float("Enter Expected Wastage %")
            try:
                show_result("Raw Material Needed", material_required_with_wastage(req, wp), "")
            except ValueError as e:
                print(f"\n  ❌  {e}")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   13. UNIT CONVERSION MODULE
# ============================================================

def unit_menu():
    options = [
        "Weight  :  kg  ↔  lbs",
        "Length  :  inch  ↔  meter",
        "Length  :  inch  ↔  cm",
        "Fabric  :  GSM  ↔  oz/yd²",
        "Yarn    :  Ne   ↔  Nm",
        "Temp    :  °C   ↔  °F",
    ]
    while True:
        choice = show_menu("UNIT CONVERSIONS", options)

        if choice == 1:
            print("\n   1. kg → lbs     2. lbs → kg")
            d = get_int("Direction", 1, 2)
            if d == 1:
                v = get_float("Enter Weight (kg)")
                show_result("lbs", kg_to_lbs(v), "lbs")
            else:
                v = get_float("Enter Weight (lbs)")
                show_result("kg", lbs_to_kg(v), "kg")

        elif choice == 2:
            print("\n   1. inch → meter     2. meter → inch")
            d = get_int("Direction", 1, 2)
            if d == 1:
                v = get_float("Enter Length (inch)")
                show_result("Meters", inch_to_meter(v), "m")
            else:
                v = get_float("Enter Length (meter)")
                show_result("Inches", meter_to_inch(v), "inch")

        elif choice == 3:
            print("\n   1. inch → cm     2. cm → inch")
            d = get_int("Direction", 1, 2)
            if d == 1:
                v = get_float("Enter Length (inch)")
                show_result("cm", inch_to_cm(v), "cm")
            else:
                v = get_float("Enter Length (cm)")
                show_result("Inches", cm_to_inch(v), "inch")

        elif choice == 4:
            print("\n   1. GSM → oz/yd²     2. oz/yd² → GSM")
            d = get_int("Direction", 1, 2)
            if d == 1:
                v = get_float("Enter GSM (g/m²)")
                show_result("oz/yd²", gsm_to_oz_yd2(v), "oz/yd²")
            else:
                v = get_float("Enter oz/yd²")
                show_result("GSM", oz_yd2_to_gsm(v), "g/m²")

        elif choice == 5:
            print("\n   1. Ne → Nm     2. Nm → Ne")
            d = get_int("Direction", 1, 2)
            if d == 1:
                v = get_float("Enter Count (Ne)")
                show_result("Nm", ne_to_nm(v), "Nm")
            else:
                v = get_float("Enter Count (Nm)")
                show_result("Ne", nm_to_ne(v), "Ne")

        elif choice == 6:
            print("\n   1. °C → °F     2. °F → °C")
            d = get_int("Direction", 1, 2)
            if d == 1:
                v = get_float("Enter Temperature (°C)", allow_zero=True)
                show_result("°F", celsius_to_fahrenheit(v), "°F")
            else:
                v = get_float("Enter Temperature (°F)", allow_zero=True)
                show_result("°C", fahrenheit_to_celsius(v), "°C")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   14. AI YARN COUNT RECOMMENDER  (NEW v2.0)
# ============================================================

_END_USES    = ["shirt", "trouser", "denim", "bedsheet", "towel",
                "sportswear", "upholstery", "canvas", "voile", "suiting",
                "flannel", "medical_gauze"]
_FIBER_TYPES = ["cotton", "polyester", "viscose", "linen", "wool",
                "silk", "nylon", "acrylic", "modal", "tencel"]
_LOOM_TYPES  = ["rapier", "airjet", "waterjet", "projectile", "shuttle", "any"]


def yarn_recommender_menu():
    options = [
        "Recommend Yarn Count for a Fabric",
        "Compare Yarn Options Across Multiple Fibres",
        "View All Supported End-Uses",
        "View All Supported Fibre Types",
    ]
    while True:
        choice = show_menu("AI YARN COUNT RECOMMENDER  ✦ NEW v2.0", options)

        if choice == 1:
            print("\n  Enter your fabric requirements:\n")
            gsm_val   = get_float("Target GSM (g/m²)")
            end_use   = get_choice_from_list("End Use", _END_USES)
            fiber     = get_choice_from_list("Fibre Type", _FIBER_TYPES)
            loom      = get_choice_from_list("Loom Type", _LOOM_TYPES)
            width     = get_float("Fabric Width (inches)")

            try:
                rec = recommend_yarn_count(gsm_val, end_use, fiber, loom, width)
                print()
                line("─")
                print(f"  ✅  YARN RECOMMENDATION RESULT")
                line("─")
                print(f"  Recommended Ne       : {rec['recommended_ne']}")
                print(f"  EPI × PPI            : {rec['recommended_epi']} × {rec['recommended_ppi']}")
                print(f"  Weave Structure      : {rec['weave_structure']}")
                print(f"  Estimated GSM        : {rec['estimated_gsm']} g/m²")
                print(f"  Cover Factor         : {rec['cover_factor']}")
                print(f"  Total Warp Ends      : {rec['total_ends']:,}")
                print(f"  Confidence Score     : {rec['confidence_score']}%")
                print(f"  Weave Strength/Drape : {rec['weave_properties']['strength']} / {rec['weave_properties']['drape']}")
                print(f"  Fibre Note           : {rec['fiber_note']}")
                print(f"  End-Use Profile      : {rec['end_use_profile']}")
                if rec.get("warnings"):
                    print()
                    for w in rec["warnings"]:
                        print(f"  ⚠  {w}")
                line("─")
            except Exception as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == 2:
            print("\n  Compare same fabric across multiple fibres:\n")
            gsm_val  = get_float("Target GSM (g/m²)")
            end_use  = get_choice_from_list("End Use", _END_USES)
            loom     = get_choice_from_list("Loom Type", _LOOM_TYPES)
            width    = get_float("Fabric Width (inches)")
            print("\n  Select fibres to compare (enter numbers separated by commas, e.g. 1,3,5):")
            for i, f in enumerate(_FIBER_TYPES, 1):
                print(f"     {i:>2}.  {f}")
            raw = input("\n  ➤  Fibre numbers: ")
            try:
                indices  = [int(x.strip()) for x in raw.split(",")]
                selected = [_FIBER_TYPES[i - 1] for i in indices if 1 <= i <= len(_FIBER_TYPES)]
                if not selected:
                    print("  ⚠  No valid fibres selected.")
                else:
                    comps = compare_yarn_options(gsm_val, end_use, selected, loom, width)
                    print()
                    line("─")
                    print(f"  {'Fibre':<14} {'Ne':>5} {'EPI':>6} {'PPI':>6} {'GSM_est':>9} {'CF':>8} {'Conf%':>7}")
                    print(f"  {'-'*14} {'-'*5} {'-'*6} {'-'*6} {'-'*9} {'-'*8} {'-'*7}")
                    for c in comps:
                        print(f"  {c['fiber']:<14} {c['recommended_ne']:>5} {c['recommended_epi']:>6} "
                              f"{c['recommended_ppi']:>6} {c['estimated_gsm']:>9} {c['cover_factor']:>8} {c['confidence_score']:>7}%")
                    line("─")
            except Exception as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == 3:
            header("SUPPORTED END-USES")
            eus = list_end_uses()
            print(f"  {'End Use':<16} {'GSM Range':<18} {'Ne Range':<14} Description")
            line("─")
            for eu in eus:
                print(f"  {eu['end_use']:<16} {eu['gsm_range']:<18} {eu['ne_range']:<14} {eu['description']}")

        elif choice == 4:
            header("SUPPORTED FIBRE TYPES")
            fts = list_fiber_types()
            for ft in fts:
                print(f"  🧵  {ft['fiber']:<14} Ne mult: {ft['ne_multiplier']}   {ft['note']}")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   15. SHADE RECIPE PREDICTOR  (NEW v2.0)
# ============================================================

_FIBER_TYPES_DYE = ["cotton", "viscose", "modal", "tencel", "wool",
                     "silk", "polyester", "nylon", "acrylic", "linen"]


def shade_recipe_menu():
    options = [
        "Predict Dye Recipe from Hex Colour (#RRGGBB)",
        "Predict Dye Recipe from L*a*b* Values",
        "Shade QC — Compare Produced vs Target Colour",
        "Colour Utilities  (hex↔RGB↔Lab*, ΔE*)",
        "View Supported Dye Classes",
    ]
    while True:
        choice = show_menu("SHADE RECIPE PREDICTOR  ✦ NEW v2.0", options)

        if choice == 1:
            print("\n  Enter target colour and fabric details:\n")
            hex_col = input("  ➤  Hex colour (e.g. #1B3A6B): ").strip()
            fiber   = get_choice_from_list("Fibre Type", _FIBER_TYPES_DYE)
            weight  = get_float("Fabric Weight (grams)")
            mlr     = get_float("MLR — Material to Liquor Ratio (e.g. 10 for 1:10)")

            try:
                rec = predict_shade_recipe(hex_col, weight, fiber, dye_class=None, mlr=mlr)
                print()
                line("─")
                print(f"  ✅  SHADE RECIPE RESULT")
                line("─")
                print(f"  Colour Hex        : {rec['color_hex']}")
                print(f"  Colour L*a*b*     : {rec['color_lab']}")
                print(f"  Shade Description : {rec['shade_description']}")
                print(f"  Dye Class         : {rec['dye_class']}")
                print(f"  ΔE* Accuracy Est. : {rec['delta_e_estimate']}")
                print(f"  Fixation Rate     : {rec['fixation_rate_%']}%")
                print(f"  Liquor Volume     : {rec['liquor_volume_L']} L  (MLR {rec['mlr']}:1)")
                print(f"\n  Recipe (% owf):")
                for dye, pct in rec["recipe_percent"].items():
                    print(f"    {dye:<28}: {pct}%")
                print(f"\n  Recipe (grams):")
                for dye, g in rec["recipe_grams"].items():
                    print(f"    {dye:<28}: {g} g")
                print(f"\n  Auxiliaries (grams):")
                for chem, g in rec["auxiliaries_g"].items():
                    print(f"    {chem:<28}: {g} g")
                print(f"\n  Process Note: {rec['process_note']}")
                if rec.get("warnings"):
                    for w in rec["warnings"]:
                        print(f"  ⚠  {w}")
                line("─")
            except Exception as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == 2:
            print("\n  Enter CIE L*a*b* values:\n")
            L = get_float("L* (Lightness, 0–100)", allow_zero=True)
            a = get_float("a* (green–red axis)", allow_zero=True)
            b = get_float("b* (blue–yellow axis)", allow_zero=True)
            fiber  = get_choice_from_list("Fibre Type", _FIBER_TYPES_DYE)
            weight = get_float("Fabric Weight (grams)")
            mlr    = get_float("MLR (e.g. 10)")

            try:
                rec = predict_shade_recipe((L, a, b), weight, fiber, dye_class=None, mlr=mlr, input_format="lab")
                print()
                line("─")
                print(f"  ✅  SHADE RECIPE RESULT  (from L*a*b* input)")
                line("─")
                print(f"  Hex Equivalent    : {rec['color_hex']}")
                print(f"  Shade Description : {rec['shade_description']}")
                print(f"  Dye Class         : {rec['dye_class']}")
                print(f"  ΔE* Accuracy Est. : {rec['delta_e_estimate']}")
                print(f"  Fixation Rate     : {rec['fixation_rate_%']}%")
                print(f"\n  Recipe (% owf):")
                for dye, pct in rec["recipe_percent"].items():
                    print(f"    {dye:<28}: {pct}%")
                print(f"\n  Auxiliaries (grams):")
                for chem, g in rec["auxiliaries_g"].items():
                    print(f"    {chem:<28}: {g} g")
                line("─")
            except Exception as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == 3:
            print("\n  QC — Compare produced shade against target:\n")
            prod = input("  ➤  Produced colour hex (e.g. #1C3B6C): ").strip()
            tgt  = input("  ➤  Target colour hex   (e.g. #1B3A6B): ").strip()

            try:
                qc = compare_shade_accuracy(prod, tgt)
                print()
                line("─")
                print(f"  ✅  SHADE QC RESULT")
                line("─")
                print(f"  Produced Hex      : {qc['produced_hex']}")
                print(f"  Target Hex        : {qc['target_hex']}")
                print(f"  ΔE*               : {qc['delta_e']}  (< 1.0 = excellent match)")
                print(f"  ΔL*               : {qc['delta_L']}  (+ = too light, − = too dark)")
                print(f"  Δa*               : {qc['delta_a']}  (+ = too red, − = too green)")
                print(f"  Δb*               : {qc['delta_b']}  (+ = too yellow, − = too blue)")
                print(f"  Verdict           : {qc['verdict']}")
                print(f"  Recommendation    : {qc['recommendation']}")
                line("─")
            except Exception as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == 4:
            sub_opts = [
                "Hex → RGB",
                "RGB → Hex",
                "RGB → L*a*b*",
                "Calculate ΔE* between two hex colours",
            ]
            sub = show_menu("COLOUR UTILITIES", sub_opts)

            if sub == 1:
                hx = input("  ➤  Hex colour: ").strip()
                try:
                    r, g, b = hex_to_rgb(hx)
                    print(f"\n  ✅  RGB = ({r}, {g}, {b})")
                except Exception as e:
                    print(f"\n  ❌  {e}")

            elif sub == 2:
                r = int(get_float("R (0–255)"))
                g = int(get_float("G (0–255)"))
                b = int(get_float("B (0–255)"))
                print(f"\n  ✅  Hex = {rgb_to_hex(r, g, b)}")

            elif sub == 3:
                r = int(get_float("R (0–255)"))
                g = int(get_float("G (0–255)"))
                b = int(get_float("B (0–255)"))
                L, a, bv = rgb_to_lab(r, g, b)
                print(f"\n  ✅  L* = {L:.2f}   a* = {a:.2f}   b* = {bv:.2f}")

            elif sub == 4:
                h1 = input("  ➤  Colour 1 hex: ").strip()
                h2 = input("  ➤  Colour 2 hex: ").strip()
                try:
                    r1, g1, b1 = hex_to_rgb(h1)
                    r2, g2, b2 = hex_to_rgb(h2)
                    lab1 = rgb_to_lab(r1, g1, b1)
                    lab2 = rgb_to_lab(r2, g2, b2)
                    de = delta_e(lab1, lab2)
                    print(f"\n  ✅  ΔE* = {de:.4f}")
                    if   de < 1.0:  print("       Excellent match — imperceptible difference")
                    elif de < 2.0:  print("       Good match — slight difference")
                    elif de < 3.5:  print("       Acceptable — noticeable to trained eye")
                    else:           print("       Poor match — clear visible difference")
                except Exception as e:
                    print(f"\n  ❌  {e}")

            if sub != len(sub_opts) + 1:
                pause()

        elif choice == 5:
            header("SUPPORTED DYE CLASSES")
            dcs = list_dye_classes()
            print(f"  {'Dye Class':<14} {'Fix Rate':>9}  {'Max %owf':>9}  Compatible Fibres")
            line("─")
            for dc in dcs:
                fibers = ", ".join(dc["compatible_fibers"])
                print(f"  {dc['dye_class']:<14} {dc['typical_fix_rate_%']:>8}%  {dc['shade_limit_%_owf']:>8}%owf  {fibers}")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   16. CARBON FOOTPRINT CALCULATOR  (NEW v2.0)
# ============================================================

_CARBON_FIBERS     = ["cotton", "organic_cotton", "recycled_cotton", "polyester",
                       "recycled_polyester", "viscose", "modal", "tencel", "linen",
                       "hemp", "wool", "recycled_wool", "silk", "nylon",
                       "recycled_nylon", "acrylic", "bamboo", "lyocell"]
_SPINNING_METHODS  = ["ring", "open_end", "air_jet", "compact"]
_FORMATIONS        = ["weaving_rapier", "weaving_airjet", "weaving_waterjet",
                       "weaving_projectile", "weaving_shuttle",
                       "knitting_circular", "knitting_warp", "knitting_flat"]
_DYE_PROCESSES     = ["undyed", "pigment_padding", "natural_dye",
                       "reactive_cold_pad", "reactive_exhaust",
                       "direct_exhaust", "acid_exhaust",
                       "disperse_thermosol", "disperse_hthp", "vat_exhaust"]
_FINISHING         = ["none", "softener_only", "calendering", "sanforizing",
                       "raising_napping", "water_repellent", "mercerizing",
                       "coating", "flame_retardant"]
_COUNTRIES         = ["bangladesh", "india", "china", "pakistan", "vietnam",
                       "indonesia", "turkey", "uk", "eu_average", "usa", "global_avg"]
_TRANSPORT_MODES   = ["sea_freight", "air_freight", "road_truck", "rail"]


def carbon_footprint_menu():
    options = [
        "Calculate Full Lifecycle Carbon Footprint",
        "Compare Carbon Footprint Across Fibre Types",
        "Calculate Carbon Offset Cost",
        "View Emission Factors (Fibres & Processes)",
    ]
    while True:
        choice = show_menu("CARBON FOOTPRINT CALCULATOR  ✦ NEW v2.0", options)

        if choice == 1:
            print("\n  Enter fabric production details:\n")
            fiber    = get_choice_from_list("Fibre Type", _CARBON_FIBERS)
            weight   = get_float("Fabric Weight (kg)")
            spin     = get_choice_from_list("Spinning Method", _SPINNING_METHODS)
            form     = get_choice_from_list("Fabric Formation", _FORMATIONS)
            dye_proc = get_choice_from_list("Dyeing Process", _DYE_PROCESSES)
            finish   = get_choice_from_list("Finishing Process", _FINISHING)
            country  = get_choice_from_list("Manufacturing Country", _COUNTRIES)
            transport= get_choice_from_list("Transport Mode", _TRANSPORT_MODES)
            dist     = get_float("Transport Distance (km)")

            try:
                cf = calculate_carbon_footprint(
                    fiber_type=fiber,
                    fabric_weight_kg=weight,
                    spinning_method=spin,
                    fabric_formation=form,
                    dyeing_process=dye_proc,
                    finishing=finish,
                    country=country,
                    transport_mode=transport,
                    transport_distance_km=dist,
                )
                print()
                line("─")
                print(f"  ✅  CARBON FOOTPRINT RESULT")
                line("─")
                print(f"  Total CO₂e per kg    : {cf['total_co2e_kg_per_kg']} kg CO₂e / kg fabric")
                print(f"  Total batch CO₂e     : {cf['total_co2e_kg']} kg CO₂e  ({cf['fabric_weight_kg']} kg fabric)")
                print(f"  Water footprint      : {cf['water_footprint_L']:,} L  ({cf['water_footprint_L_per_kg']:,} L/kg)")
                print(f"  Sustainability       : {cf['sustainability_rating']} — {cf['rating_description']}")
                print(f"\n  Stage Breakdown (kg CO₂e per kg fabric):")
                for stage, val in cf["breakdown_kg_per_kg"].items():
                    bar = "█" * max(1, int(val * 3))
                    print(f"    {stage:<42}: {val:>6}  {bar}")
                print(f"\n  vs Industry Average  : {cf['comparison'].get('industry_avg_cotton_reactive', 'N/A')} kg CO₂e/kg")
                print(f"  vs Avg (difference)  : {cf['comparison'].get('vs_industry_avg_pct', 'N/A'):+.1f}%"
                      if isinstance(cf['comparison'].get('vs_industry_avg_pct'), (int, float)) else "")
                print(f"\n  Reduction Tips:")
                for tip in cf["reduction_tips"]:
                    print(f"    → {tip}")
                line("─")
            except Exception as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == 2:
            weight = get_float("Batch Weight to Compare (kg)")
            try:
                fibres = compare_fiber_footprints(weight)
                print()
                line("─")
                print(f"  {'Fibre':<24} {'CO₂e/kg':>9} {'CO₂e Total':>12} {'Water L/kg':>12} {'Rating':>7}")
                line("─")
                for f in fibres:
                    print(
                        f"  {f['fiber']:<24} {f['co2e_kg_per_kg']:>9.2f} "
                        f"{f['co2e_kg_total']:>12.0f} {f['water_L_per_kg']:>12,} {f['fiber_stage_rating']:>7}"
                    )
                line("─")
            except Exception as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == 3:
            print("\n  Calculate the cost to offset your carbon emissions:\n")
            co2e_kg = get_float("Total CO₂e to offset (kg)")
            price   = get_float("Carbon credit price per tonne USD (e.g. 20)")
            try:
                offset = carbon_offset_cost(co2e_kg, price_per_tonne_usd=price)
                print()
                line("─")
                print(f"  ✅  CARBON OFFSET COST")
                line("─")
                print(f"  CO₂e to offset       : {offset['tonnes_co2e']} tonnes")
                print(f"  Price per tonne      : ${price} USD")
                print(f"  Total offset cost    : ${offset['offset_cost_usd']} USD")
                line("─")
            except Exception as e:
                print(f"\n  ❌  Error: {e}")

        elif choice == 4:
            header("EMISSION FACTORS — FIBRES")
            fts = list_fiber_types_carbon()
            print(f"  {'Fibre':<24} {'CO₂e/kg':>9}  {'Water L/kg':>12}  Rating")
            line("─")
            for f in fts:
                print(f"  {f['fiber']:<24} {f['co2e_kg_per_kg']:>9.2f}  {f['water_L_per_kg']:>12,}  {f['rating']}")

            print()
            header("EMISSION FACTORS — DYEING PROCESSES")
            dps = list_dyeing_processes_carbon()
            print(f"  {'Process':<28} {'CO₂e/kg':>9}  {'Water L/kg':>12}")
            line("─")
            for dp in dps:
                print(f"  {dp['process']:<28} {dp['co2e_kg_per_kg']:>9.2f}  {dp['water_L_per_kg']:>12,}")

        elif choice == len(options) + 1:
            break

        pause()


# ============================================================
#   17. GLOSSARY
# ============================================================

def glossary_menu():
    header("TEXTILE GLOSSARY", "Common terms and abbreviations")
    print()
    for term, definition in TEXTILE_GLOSSARY.items():
        print(f"  📘  {term:<12} —  {definition}")
    pause()


# ============================================================
#   MAIN MENU
# ============================================================

MAIN_MENU_OPTIONS = [
    "🧵  Yarn Calculations",
    "🧶  Fabric Calculations",
    "🎨  Dyeing",
    "🔬  Advanced Dyeing",
    "💰  Costing",
    "📊  Advanced Costing",
    "🏭  Production",
    "🌀  Spinning",
    "🪡  Weaving",
    "✅  Quality Control (QC)",
    "🧪  Textile Testing Lab",
    "♻️   Wastage",
    "🔄  Unit Conversions",
    "🤖  AI Yarn Count Recommender     ✦ NEW v2.0",
    "🎨  Shade Recipe Predictor        ✦ NEW v2.0",
    "🌿  Carbon Footprint Calculator   ✦ NEW v2.0",
    "📘  Textile Glossary",
]

MODULE_MAP = {
    1:  yarn_menu,
    2:  fabric_menu,
    3:  dyeing_menu,
    4:  dyeing_advanced_menu,
    5:  costing_menu,
    6:  costing_advanced_menu,
    7:  production_menu,
    8:  spinning_menu,
    9:  weaving_menu,
    10: qc_menu,
    11: testing_menu,
    12: wastage_menu,
    13: unit_menu,
    14: yarn_recommender_menu,
    15: shade_recipe_menu,
    16: carbon_footprint_menu,
    17: glossary_menu,
}


def main():
    clear()
    print(BANNER)
    print(f"  Welcome! {len(MODULE_MAP)} modules loaded.")
    print(f"  Type the module number and press Enter.\n")
    pause()

    while True:
        clear()
        header("MAIN MENU", f"Version {VERSION}  |  Developer: Abdul Malek")

        for i, opt in enumerate(MAIN_MENU_OPTIONS, 1):
            print(f"   {i:>2}.  {opt}")
        print(f"\n   {len(MAIN_MENU_OPTIONS)+1:>2}.  ❌  Exit")

        choice = get_int("Enter choice", 1, len(MAIN_MENU_OPTIONS) + 1)

        if choice == len(MAIN_MENU_OPTIONS) + 1:
            print("\n  Thank you for using Abdul Malek Textile Library!")
            print("  — Every meaningful innovation starts with Version 1.00 —\n")
            sys.exit(0)

        try:
            MODULE_MAP[choice]()
        except Exception as e:
            print(f"\n  ❌  Unexpected error: {e}")
            pause()


if __name__ == "__main__":
    main()
