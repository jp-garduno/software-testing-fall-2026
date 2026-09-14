import pytest

from src.news2 import RESP_BANDS, band_score, clinical_risk, monitoring_frequency, score_reading, temperature_score

HEALTHY = {
    "respiratory_rate": 16,
    "spo2": 98,
    "systolic_bp": 120,
    "heart_rate": 70,
    "temperature": 36.8,
}


def test_healthy_reading_scores_zero():
    total, breakdown = score_reading(HEALTHY)
    assert total == 0
    assert set(breakdown) == {
        "respiratory_rate",
        "spo2",
        "systolic_bp",
        "heart_rate",
        "temperature",
        "consciousness",
        "on_oxygen",
    }


def test_oxygen_therapy_adds_two_points():
    total, _ = score_reading(dict(HEALTHY, on_oxygen=True))
    assert total == 2


def test_deteriorating_patient_scores_high():
    total, _ = score_reading(
        {
            "respiratory_rate": 26,
            "spo2": 90,
            "systolic_bp": 88,
            "heart_rate": 135,
            "temperature": 39.5,
            "consciousness": "V",
        }
    )
    assert total >= 7


@pytest.mark.parametrize(
    "rate,expected",
    [(7, 3), (10, 1), (16, 0), (22, 2), (30, 3)],
)
def test_respiratory_rate_bands(rate, expected):
    assert band_score(rate, RESP_BANDS) == expected


@pytest.mark.parametrize(
    "temperature,expected",
    [(34.0, 3), (35.5, 1), (37.0, 0), (38.5, 1), (39.5, 2)],
)
def test_temperature_bands(temperature, expected):
    assert temperature_score(temperature) == expected


def test_single_three_point_parameter_raises_risk_level():
    assert clinical_risk(3, {"spo2": 3}) == "LOW_MEDIUM"


def test_clinical_risk_thresholds():
    assert clinical_risk(7, {}) == "HIGH"
    assert clinical_risk(5, {}) == "MEDIUM"
    assert clinical_risk(0, {}) == "LOW"


def test_monitoring_frequency_for_high_risk():
    assert monitoring_frequency("HIGH") == "continuous"
