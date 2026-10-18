# simple_solar_declination_calc

Calculates the solar declination angle (in radians or degrees) for any day of the year, using Cooper's formula.

```python
from simple_solar_declination_calc import solar_declination, solar_declination_degrees

# Day 172 = ~June 21, near the Northern Hemisphere summer solstice
print(solar_declination_degrees(172))  # ~23.3
print(solar_declination(172))          # ~0.407 radians
```

## Why this exists

Many small solar-energy and daylighting calculations need a single, dependency-free
function that turns a day-of-year into a declination angle. Cooper's formula is the
most common textbook approximation:

```
delta = 23.45 * sin(0.9856 * N - 3.6)   degrees
```

where `N` is the day of the year (Jan 1 = 1).

The trade-off: accuracy is about ±1.5 degrees compared to high-precision astronomical
ephemerides. That is fine for panel-tilt sizing, rough shading studies, and teaching,
but not for work that needs arcminute-level precision.

## Interpretation chosen

- `N` is the calendar day-of-year, **not** a fractional day. Time-of-day is ignored.
- `N` ranges over `1..366` so leap years (which contain a Feb 29) are accepted. The
caller is responsible for knowing whether their year is leap; this library does not
take a year argument.
- The function returns a plain `float`; it does not round.

## Awkward edges

- Passing a float or a `bool` raises `TypeError` — the input must be a real `int`.
Day 0 and day 367 raise `ValueError`.
- Day 366 is accepted but, in a non-leap year, does not correspond to any real date.
This library intentionally does not take a year, so it cannot police that for you.
