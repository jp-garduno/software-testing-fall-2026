from src.vitals import normalize
import sys

RESP_BANDS = [(0, 8, 3), (9, 11, 1), (12, 20, 0), (21, 24, 2), (25, 999, 3)]
SPO2_BANDS = [(0, 91, 3), (92, 93, 2), (94, 95, 1), (96, 100, 0)]
SBP_BANDS = [(0, 90, 3), (91, 100, 2), (101, 110, 1), (111, 219, 0), (220, 999, 3)]
HR_BANDS = [(0, 40, 3), (41, 50, 1), (51, 90, 0), (91, 110, 1), (111, 130, 2), (131, 999, 3)]

def band_score(value, bands):
    for low, high, points in bands:
        if value >= low and value <= high:
            return points
    return 3

def temperature_score(t):
    if t <= 35.0:
        return 3
    elif t <= 36.0:
        return 1
    elif t <= 38.0:
        return 0
    elif t <= 39.0:
        return 1
    else:
        return 2

def consciousness_score(level):
    if level == "A":
        return 0
    else:
        return 3

def score_reading(reading):
    r = normalize(reading)
    Total = 0
    breakdown = {}
    breakdown["respiratory_rate"] = band_score(r["respiratory_rate"], RESP_BANDS)
    breakdown["spo2"] = band_score(r["spo2"], SPO2_BANDS)
    breakdown["systolic_bp"] = band_score(r["systolic_bp"], SBP_BANDS)
    breakdown["heart_rate"] = band_score(r["heart_rate"], HR_BANDS)
    breakdown["temperature"] = temperature_score(r["temperature"])
    breakdown["consciousness"] = consciousness_score(r["consciousness"])
    breakdown["on_oxygen"] = 2 if r["on_oxygen"] else 0
    for k in breakdown:
        Total = Total + breakdown[k]
    return Total, breakdown

def clinical_risk(total, breakdown):
    if total >= 7:
        return "HIGH"
    if total >= 5:
        return "MEDIUM"
    for k in breakdown:
        if breakdown[k] == 3:
            return "LOW_MEDIUM"
    if total >= 1:
        return "LOW"
    return "LOW"

def monitoring_frequency(risk):
    table = {"HIGH": "continuous", "MEDIUM": "hourly", "LOW_MEDIUM": "hourly", "LOW": "every 4-6 hours"}
    return table[risk]
