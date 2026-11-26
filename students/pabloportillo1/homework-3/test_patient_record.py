from src.patient_record import PatientRecord

HEALTHY = {
    "respiratory_rate": 16,
    "spo2": 98,
    "systolic_bp": 120,
    "heart_rate": 70,
    "temperature": 36.8,
}

CRITICAL = {
    "respiratory_rate": 26,
    "spo2": 90,
    "systolic_bp": 88,
    "heart_rate": 135,
    "temperature": 39.5,
    "consciousness": "V",
}


def test_new_record_has_no_observations():
    record = PatientRecord("P-001", "Ana Ruiz")
    assert record.latest() is None
    assert record.trend() == "INSUFFICIENT_DATA"
    assert record.escalation_required() is False


def test_add_reading_returns_scored_entry():
    record = PatientRecord("P-002", "Luis Mena")
    entry = record.add_reading(HEALTHY, taken_at="2026-09-14T10:00:00+00:00")
    assert entry["score"] == 0
    assert entry["risk"] == "LOW"
    assert entry["monitoring"] == "every 4-6 hours"


def test_trend_detects_deterioration():
    record = PatientRecord("P-003", "Sofia Lara")
    record.add_reading(HEALTHY)
    record.add_reading(CRITICAL)
    assert record.trend() == "DETERIORATING"


def test_escalation_required_for_high_risk():
    record = PatientRecord("P-004", "Mario Diaz")
    record.add_reading(CRITICAL)
    assert record.escalation_required() is True


def test_summary_mentions_patient_and_score():
    record = PatientRecord("P-005", "Elena Cruz")
    record.add_reading(HEALTHY)
    summary = record.summary()
    assert "Elena Cruz" in summary
    assert "P-005" in summary


def test_records_do_not_share_history():
    first = PatientRecord("P-006", "Jorge Paz")
    second = PatientRecord("P-007", "Nadia Sol")
    first.add_reading(HEALTHY)
    assert second.latest() is None
