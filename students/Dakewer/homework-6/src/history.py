from collections import namedtuple

HistoryEvent = namedtuple("HistoryEvent", ["member_id", "isbn", "action", "date"])
