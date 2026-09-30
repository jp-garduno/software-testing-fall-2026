"""History tracking utilities for calculator operations."""

import datetime
import json


class HistoryManager:
    """Manages a persistent log of calculator operations."""

    def __init__(self):
        self.entries = []

    def log(self, operation, operands, result):
        """Record one operation into the history log."""
        entry = {
            "operation": operation,
            "operands": operands,
            "result": result,
            "timestamp": str(datetime.datetime.now()),
        }
        self.entries.append(entry)
        return entry

    def to_json(self):
        """Serialize the current history to a JSON string."""
        return json.dumps(self.entries)

    def most_common_operation(self):
        """Return the operation type that occurs most frequently."""
        counts = {}
        for entry in self.entries:
            op = entry["operation"]
            if op in counts:
                counts[op] = counts[op] + 1
            else:
                counts[op] = 1
        if not counts:
            return None
        return max(counts, key=counts.get)

    def filter_by_operation(self, operation):
        """Return all history entries matching a given operation type."""
        return [e for e in self.entries if e["operation"] == operation]

    def clear(self):
        """Remove all entries from the history."""
        self.entries = []

    def count(self):
        """Return the total number of recorded entries."""
        return len(self.entries)

    def save_to_file(self, path):
        """Save the history log to a file at the given path."""
        try:
            with open(path, "w", encoding="utf-8") as file_handle:
                file_handle.write(self.to_json())
        except OSError as error:
            print(f"Could not save history: {error}")
