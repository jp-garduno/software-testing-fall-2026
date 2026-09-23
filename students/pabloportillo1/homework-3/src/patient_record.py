"""Patient observation history built on top of the NEWS2 scorer."""

import datetime

from src.news2 import clinical_risk, monitoring_frequency, score_reading
from src.vitals import validate_reading


class PatientRecord:
    """A patient and the ordered history of their scored observations."""

    def __init__(self, patient_id, name, history=None):
        """Create a record, optionally seeded with an existing history."""
        self.patient_id = patient_id
        self.name = name
        self.history = list(history) if history else []

    def add_reading(self, reading, taken_at=None):
        """Validate, score and store a reading, returning the stored entry."""
        validate_reading(reading)
        if taken_at is None:
            taken_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        total, breakdown = score_reading(reading)
        risk = clinical_risk(total, breakdown)
        entry = {
            "taken_at": taken_at,
            "score": total,
            "breakdown": breakdown,
            "risk": risk,
            "monitoring": monitoring_frequency(risk),
        }
        self.history.append(entry)
        return entry

    def latest(self):
        """Return the most recent entry, or None when nothing is recorded yet."""
        if not self.history:
            return None
        return self.history[-1]

    def trend(self):
        """Compare the last two scores and report the direction of travel."""
        if len(self.history) < 2:
            return "INSUFFICIENT_DATA"
        previous = self.history[-2]["score"]
        current = self.history[-1]["score"]
        if current > previous:
            return "DETERIORATING"
        if current < previous:
            return "IMPROVING"
        return "STABLE"

    def escalation_required(self):
        """True when the latest observation warrants calling the clinical team."""
        last = self.latest()
        if last is None:
            return False
        if last["risk"] == "HIGH":
            return True
        if last["risk"] == "MEDIUM" and self.trend() == "DETERIORATING":
            return True
        return False

    def summary(self):
        """Return a one-line, human readable status line for the patient."""
        last = self.latest()
        who = f"Patient {self.name} ({self.patient_id})"
        if last is None:
            return f"{who} has no recorded observations yet."
        return (
            f"{who} scored {last['score']} on NEWS2, risk {last['risk']}, "
            f"trend {self.trend()}, monitoring {last['monitoring']}."
        )
