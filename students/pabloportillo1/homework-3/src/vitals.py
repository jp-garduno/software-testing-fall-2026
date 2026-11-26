"""Validation and normalization of patient vital-sign readings."""

import json

RANGES = {
    "respiratory_rate": (4, 60),
    "spo2": (50, 100),
    "systolic_bp": (40, 300),
    "heart_rate": (20, 250),
    "temperature": (25.0, 45.0),
}


class VitalsError(Exception):
    """Raised when a reading cannot be trusted for clinical scoring."""


def validate_reading(reading, strict=True):
    """Check a reading against physiological ranges.

    Returns the list of problems found. When ``strict`` is set, a non-empty
    list is raised as a :class:`VitalsError` instead of being returned.
    """
    errors = []
    for field, bounds in RANGES.items():
        if field not in reading:
            errors.append("missing field: " + field)
            continue
        value = reading[field]
        if value is None:
            errors.append("null value for field: " + field)
            continue
        try:
            value = float(value)
        except (TypeError, ValueError):
            errors.append("non numeric value for field: " + field)
            continue
        low, high = bounds
        if value < low or value > high:
            errors.append(
                f"field {field} out of physiological range, got {value} " f"expected between {low} and {high}"
            )
    if strict and errors:
        raise VitalsError("; ".join(errors))
    return errors


def normalize(reading):
    """Return a reading with defaults filled in and values coerced to floats."""
    out = {}
    for k in RANGES:
        if k in reading and reading[k] is not None:
            out[k] = float(reading[k])
    if "consciousness" in reading:
        out["consciousness"] = str(reading["consciousness"]).upper()
    else:
        out["consciousness"] = "A"
    out["on_oxygen"] = bool(reading.get("on_oxygen", False))
    return out


def load_readings(path):
    """Load a JSON file containing a list of readings."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)
