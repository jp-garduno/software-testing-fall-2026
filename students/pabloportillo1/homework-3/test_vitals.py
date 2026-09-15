import pytest

from src.vitals import VitalsError, normalize, validate_reading

HEALTHY = {
    "respiratory_rate": 16,
    "spo2": 98,
    "systolic_bp": 120,
    "heart_rate": 70,
    "temperature": 36.8,
}


def test_validate_reading_accepts_healthy_reading():
    assert validate_reading(HEALTHY) == []


def test_validate_reading_raises_on_missing_field():
    incomplete = dict(HEALTHY)
    del incomplete["spo2"]
    with pytest.raises(VitalsError):
        validate_reading(incomplete)


def test_validate_reading_collects_errors_when_not_strict():
    broken = dict(HEALTHY, spo2=None, heart_rate="abc")
    errors = validate_reading(broken, strict=False)
    assert len(errors) == 2


def test_validate_reading_detects_out_of_range_value():
    out_of_range = dict(HEALTHY, temperature=60.0)
    errors = validate_reading(out_of_range, strict=False)
    assert "temperature" in errors[0]


def test_normalize_defaults_consciousness_and_oxygen():
    normalized = normalize(HEALTHY)
    assert normalized["consciousness"] == "A"
    assert normalized["on_oxygen"] is False


def test_normalize_uppercases_consciousness():
    normalized = normalize(dict(HEALTHY, consciousness="v"))
    assert normalized["consciousness"] == "V"
