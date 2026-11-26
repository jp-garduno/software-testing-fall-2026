"""NEWS2 early-warning score calculation."""

from src.vitals import normalize

RESP_BANDS = [(0, 8, 3), (9, 11, 1), (12, 20, 0), (21, 24, 2), (25, 999, 3)]
SPO2_BANDS = [(0, 91, 3), (92, 93, 2), (94, 95, 1), (96, 100, 0)]
SBP_BANDS = [(0, 90, 3), (91, 100, 2), (101, 110, 1), (111, 219, 0), (220, 999, 3)]
HR_BANDS = [(0, 40, 3), (41, 50, 1), (51, 90, 0), (91, 110, 1), (111, 130, 2), (131, 999, 3)]


def band_score(value, bands):
    """Return the NEWS2 points for a value using a table of (low, high, points) bands."""
    for low, high, points in bands:
        if low <= value <= high:
            return points
    return 3


def temperature_score(temperature):
    """Return the NEWS2 points for a temperature in degrees Celsius."""
    if temperature <= 35.0:
        return 3
    if temperature <= 36.0:
        return 1
    if temperature <= 38.0:
        return 0
    if temperature <= 39.0:
        return 1
    return 2


def consciousness_score(level):
    """Return 0 for an alert patient and 3 for any other AVPU level."""
    if level == "A":
        return 0
    return 3


def score_reading(reading):
    """Return the total NEWS2 score and the per-parameter breakdown for a reading."""
    values = normalize(reading)
    breakdown = {}
    breakdown["respiratory_rate"] = band_score(values["respiratory_rate"], RESP_BANDS)
    breakdown["spo2"] = band_score(values["spo2"], SPO2_BANDS)
    breakdown["systolic_bp"] = band_score(values["systolic_bp"], SBP_BANDS)
    breakdown["heart_rate"] = band_score(values["heart_rate"], HR_BANDS)
    breakdown["temperature"] = temperature_score(values["temperature"])
    breakdown["consciousness"] = consciousness_score(values["consciousness"])
    breakdown["on_oxygen"] = 2 if values["on_oxygen"] else 0
    total = sum(breakdown.values())
    return total, breakdown


def clinical_risk(total, breakdown):
    """Map a score and its breakdown to a clinical risk band."""
    if total >= 7:
        return "HIGH"
    if total >= 5:
        return "MEDIUM"
    if 3 in breakdown.values():
        return "LOW_MEDIUM"
    return "LOW"


def monitoring_frequency(risk):
    """Return the observation frequency recommended for a risk band."""
    table = {"HIGH": "continuous", "MEDIUM": "hourly", "LOW_MEDIUM": "hourly", "LOW": "every 4-6 hours"}
    return table[risk]
