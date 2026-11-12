from dataclasses import dataclass
from datetime import date

BORROW = "borrow"
RETURN = "return"


@dataclass(frozen=True)
class HistoryEntry:
    member_id: str
    isbn: str
    action: str
    occurred_on: date