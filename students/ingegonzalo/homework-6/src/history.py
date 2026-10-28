from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HistoryEntry:
    member_id: str
    isbn: str
    action: str
    occurred_on: date