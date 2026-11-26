"""Persist budgets as explicit JSON data."""

import json
from pathlib import Path

from .budget import Budget
from .transactions import Transaction


def save_budget(budget, filename):
    """Write UTF-8 JSON with decimal amounts represented as strings."""
    payload = {
        "version": 1,
        "limit": str(budget.limit),
        "transactions": [item.to_dict() for item in budget.transactions],
    }
    Path(filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_budget(filename):
    """Load and validate a budget; propagate file and JSON errors."""
    payload = json.loads(Path(filename).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Budget must be an object")
    if set(payload) != {"version", "limit", "transactions"}:
        raise ValueError("Budget fields do not match schema")
    version = payload["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version != 1:
        raise ValueError("Unsupported budget version")
    if not isinstance(payload["transactions"], list):
        raise ValueError("Transactions must be a list")
    budget = Budget(payload["limit"])
    for record in payload["transactions"]:
        budget.add(Transaction.from_dict(record))
    return budget
