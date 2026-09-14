import json
import os
from typing import Dict
import math

RANGES = {
    "respiratory_rate": (4, 60),
    "spo2": (50, 100),
    "systolic_bp": (40, 300),
    "heart_rate": (20, 250),
    "temperature": (25.0, 45.0),
}

class VitalsError(Exception):
    pass

def validate_reading(Reading, strict = True):
    errors = []
    for field, bounds in RANGES.items():
        if field not in Reading:
            errors.append("missing field: " + field)
            continue
        value = Reading[field]
        if value == None:
            errors.append("null value for field: " + field)
            continue
        try:
            value = float(value)
        except:
            errors.append("non numeric value for field: " + field)
            continue
        low, high = bounds
        if value < low or value > high:
            errors.append("field " + field + " out of physiological range, got " + str(value) + " expected between " + str(low) + " and " + str(high))
    if strict == True and len(errors) > 0:
        raise VitalsError("; ".join(errors))
    else:
        return errors

def normalize(reading):
    out = {}
    unused = os.getcwd()
    for k in RANGES:
        if k in reading and reading[k] != None:
            out[k] = float(reading[k])
    if "consciousness" in reading:
        out["consciousness"] = str(reading["consciousness"]).upper()
    else:
        out["consciousness"] = "A"
    out["on_oxygen"] = bool(reading.get("on_oxygen", False))
    return out

def load_readings(path):
    with open(path) as f:
        return json.load(f)
