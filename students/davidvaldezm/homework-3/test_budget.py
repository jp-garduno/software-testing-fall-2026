"""Behavioral tests for amounts, boundaries and persistence."""

import json
from decimal import Decimal

import pytest

from src.budget import Budget
from src.storage import load_budget, save_budget
from src.transactions import Transaction, normalize_category, parse_amount


@pytest.mark.parametrize("value", [True, "bad", "NaN", "Infinity", 0, -1, "1.001"])
def test_invalid_amount(value):
    """Reject malformed and unsupported monetary values."""
    with pytest.raises(ValueError):
        parse_amount(value)


@pytest.mark.parametrize("value", [None, "", "  ", 12])
def test_invalid_category(value):
    """Reject missing category names."""
    with pytest.raises(ValueError):
        normalize_category(value)


def test_exact_totals_and_boundaries():
    """Use exact decimal math and distinguish equal from over budget."""
    budget = Budget("0.30")
    assert budget.total() == 0
    budget.add(Transaction("0.10", " Food "))
    budget.add(Transaction("0.20", "food"))
    assert budget.total() == Decimal("0.30")
    assert budget.total("missing") == 0
    assert budget.remaining() == 0
    assert not budget.is_over_budget()
    assert budget.category_totals() == {"food": Decimal("0.30")}
    snapshot = budget.transactions
    budget.add(Transaction("0.01", "travel"))
    assert len(snapshot) == 2
    assert budget.is_over_budget()
    assert budget.remaining() == Decimal("-0.01")
    assert budget.remove(2).category == "travel"


@pytest.mark.parametrize(
    "index,error",
    [(-1, IndexError), (0, IndexError), (True, TypeError), ("0", TypeError)],
)
def test_invalid_removal(index, error):
    """Reject indexes that cannot identify an existing expense."""
    with pytest.raises(error):
        Budget(100).remove(index)


def test_invalid_transaction():
    """Only validated transaction objects enter a budget."""
    with pytest.raises(TypeError):
        Budget(100).add({})
    with pytest.raises(ValueError):
        Transaction(1, "food", None)


def test_storage_round_trip(tmp_path):
    """Preserve Unicode and decimal precision through JSON storage."""
    budget = Budget("100.00")
    budget.add(Transaction("12.30", "comida", "Café"))
    filename = tmp_path / "budget.json"
    save_budget(budget, filename)
    restored = load_budget(filename)
    assert restored.limit == budget.limit
    assert restored.transactions == budget.transactions


@pytest.mark.parametrize(
    "record",
    [[], {}, {"amount": "1", "category": "food", "description": "", "extra": 1}],
)
def test_invalid_transaction_schema(record):
    """Reject missing fields and unrecognized data."""
    with pytest.raises(ValueError):
        Transaction.from_dict(record)


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        {"version": 2, "limit": "10", "transactions": []},
        {"version": True, "limit": "10", "transactions": []},
        {"version": 1, "limit": "10", "transactions": {}},
    ],
)
def test_invalid_budget_schema(tmp_path, payload):
    """Reject invalid stored budget schemas."""
    filename = tmp_path / "invalid.json"
    filename.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        load_budget(filename)


def test_missing_and_malformed_file(tmp_path):
    """File and JSON parsing errors remain visible to callers."""
    filename = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_budget(filename)
    filename.write_text("{", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_budget(filename)
