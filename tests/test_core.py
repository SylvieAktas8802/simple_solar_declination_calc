import math
import unittest

from simple_solar_declination_calc import (
    solar_declination,
    solar_declination_degrees,
)
from simple_solar_declination_calc.core import (
    _COEFFICIENT_DEG,
    solar_declination as core_solar_declination,
)


class TestSolarDeclination(unittest.TestCase):
    # ----- Happy path, comparing radians to a hand-computed value. -----
    def test_january_1_is_negative(self):
        # Jan 1: argument = 1*0.9856 - 3.6 = -2.6144 deg -> sine negative
        result = solar_declination_degrees(1)
        self.assertLess(result, 0.0)

    def test_december_21_near_winter_solstice(self):
        # Dec 21 is around the minimum (-23.45 deg).
        result = solar_declination_degrees(355)
        self.assertLess(result, 0.0)
        self.assertGreaterEqual(result, -_COEFFICIENT_DEG - 1.0)

    def test_radians_and_degrees_agree(self):
        rad = solar_declination(200)
        deg = solar_declination_degrees(200)
        self.assertAlmostEqual(rad, math.radians(deg), places=9)

    # ----- Edge cases the implementation claims to handle. -----
    def test_day_of_year_366_accepted(self):
        # Leap years contain a Feb 29, so day 366 is valid.
        result = solar_declination_degrees(366)
        # day 366 is near Dec 31; declination should be a small negative value
        self.assertLess(result, 0.0)
        self.assertGreater(result, -24.0)

    def test_day_of_year_zero_rejected(self):
        with self.assertRaises(ValueError):
            solar_declination(0)

    def test_day_of_year_367_rejected(self):
        with self.assertRaises(ValueError):
            solar_declination(367)

    def test_negative_day_rejected(self):
        with self.assertRaises(ValueError):
            solar_declination(-1)

    def test_float_rejected(self):
        with self.assertRaises(TypeError):
            solar_declination(180.5)  # type: ignore[arg-type]

    def test_bool_rejected(self):
        # bool is a subclass of int but not a valid day index.
        with self.assertRaises(TypeError):
            solar_declination(True)  # type: ignore[arg-type]

    def test_string_rejected(self):
        with self.assertRaises(TypeError):
            solar_declination("172")  # type: ignore[arg-type]

    # ----- Consistency across the two export names. -----
    def test_both_exports_point_at_same_function(self):
        self.assertIs(solar_declination, core_solar_declination)


if __name__ == "__main__":
    unittest.main()
