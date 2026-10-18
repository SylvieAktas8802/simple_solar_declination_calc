"""Solar declination angle using Cooper's formula.

Cooper (1969) gives the declination of the sun as

    delta = 23.45 * sin(0.9856 * N - 3.6)  degrees

where N is the day-of-year (1 for Jan 1, 365 or 366 for Dec 31). The
approximation is accurate to roughly 1.5 degrees, which is adequate for
solar-panel orientation, simple shading studies, and educational use —
but not for astronomical work.

This module deliberately pins N to the *day of the calendar year* (Jan 1 = 1).
It does not fold in time-of-day or orbit perturbations.
"""

import math


_SEASONAL_OFFSET_RAD = math.radians(3.6)
_COEFFICIENT_DEG = 23.45
_COEFFICIENT_RAD = math.radians(_COEFFICIENT_DEG)
# 0.9856 degrees per day in the Cooper formula; convert to radians per day
# so the argument to math.sin is dimensionless and the result is in radians.
_DEGREES_PER_DAY_TO_RAD = math.radians(0.9856)


def solar_declination(day_of_year: int) -> float:
    """Return solar declination in radians for ``day_of_year`` (1-based).

    Raises ValueError if the value is not a valid day of a (non-leap) or
    leap year. We accept 1-366 because leap years contain a Feb 29; the
    caller is responsible for knowing whether their year is leap.
    """
    if not isinstance(day_of_year, int) or isinstance(day_of_year, bool):
        raise TypeError("day_of_year must be a non-boolean int")
    if day_of_year < 1 or day_of_year > 366:
        raise ValueError("day_of_year must be in [1, 366]")
    argument = day_of_year * _DEGREES_PER_DAY_TO_RAD - _SEASONAL_OFFSET_RAD
    return _COEFFICIENT_RAD * math.sin(argument)


def solar_declination_degrees(day_of_year: int) -> float:
    """Return solar declination in degrees for ``day_of_year`` (1-based)."""
    return math.degrees(solar_declination(day_of_year))
