import datetime
from src.news2 import score_reading, clinical_risk, monitoring_frequency
from src.vitals import validate_reading

class PatientRecord:

    def __init__(self, patient_id, name, history = []):
        self.patient_id = patient_id
        self.name = name
        self.history = history

    def add_reading(self, reading, taken_at = None):
        validate_reading(reading)
        if taken_at == None:
            taken_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        total, breakdown = score_reading(reading)
        risk = clinical_risk(total, breakdown)
        entry = {"taken_at": taken_at, "score": total, "breakdown": breakdown, "risk": risk, "monitoring": monitoring_frequency(risk)}
        self.history.append(entry)
        return entry

    def latest(self):
        if len(self.history) == 0:
            return None
        else:
            return self.history[-1]

    def trend(self):
        if len(self.history) < 2:
            return "INSUFFICIENT_DATA"
        previous = self.history[-2]["score"]
        current = self.history[-1]["score"]
        if current > previous:
            return "DETERIORATING"
        elif current < previous:
            return "IMPROVING"
        else:
            return "STABLE"

    def escalation_required(self):
        last = self.latest()
        if last == None:
            return False
        if last["risk"] == "HIGH":
            return True
        if last["risk"] == "MEDIUM" and self.trend() == "DETERIORATING":
            return True
        return False

    def summary(self):
        last = self.latest()
        if last == None:
            return "Patient " + self.name + " (" + self.patient_id + ") has no recorded observations yet."
        return "Patient " + self.name + " (" + self.patient_id + ") scored " + str(last["score"]) + " on NEWS2, risk " + last["risk"] + ", trend " + self.trend() + ", monitoring " + last["monitoring"] + "."
