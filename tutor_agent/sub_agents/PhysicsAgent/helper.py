from pint import UnitRegistry

# Initialize the unit registry
ureg = UnitRegistry()
Q_ = ureg.Quantity

from typing import Literal

def convert_units(value: float, from_unit: Literal["m", "cm", "mm"], to_unit: Literal["m", "cm", "mm"]) -> dict:
    """
    Convert length units between meters, centimeters, and millimeters.

    Args:
        value (float): The numerical value to convert.
        from_unit (str): The unit to convert from ('m', 'cm', 'mm').
        to_unit (str): The unit to convert to ('m', 'cm', 'mm').

    Returns:
        float: The converted value.
    """
    conversion_factors = {
        "m": 1.0,
        "cm": 100.0,
        "mm": 1000.0,
    }


    value_in_meters = value / conversion_factors[from_unit]


    result = value_in_meters * conversion_factors[to_unit]

    return {"result":result}
