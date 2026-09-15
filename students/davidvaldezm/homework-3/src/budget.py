"""Summarize expenses against a monthly budget."""

from decimal import Decimal

from .transactions import Transaction, normalize_category, parse_amount


class Budget:
    """Hold expenses and calculate exact monetary totals."""

    def __init__(self, limit):
        """Start an empty budget with a positive spending limit."""
        self.limit = parse_amount(limit)
        self._transactions = []

    @property
    def transactions(self):
        """Expose an immutable snapshot of the transaction list."""
        return tuple(self._transactions)

    def add(self, transaction):
        """Record a validated transaction."""
        if not isinstance(transaction, Transaction):
            raise TypeError("Expected a Transaction")
        self._transactions.append(transaction)

    def remove(self, index):
        """Remove by nonnegative index and return the removed expense."""
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError("Index must be an integer")
        if index < 0 or index >= len(self._transactions):
            raise IndexError("Transaction index out of range")
        return self._transactions.pop(index)

    def total(self, category=None):
        """Sum all expenses, optionally restricted to one category."""
        category = normalize_category(category) if category is not None else None
        return sum(
            (
                item.amount
                for item in self._transactions
                if category is None or item.category == category
            ),
            Decimal("0"),
        )

    def remaining(self):
        """Return available funds; negative values indicate overspending."""
        return self.limit - self.total()

    def is_over_budget(self):
        """An expense total equal to the limit is still within budget."""
        return self.total() > self.limit

    def category_totals(self):
        """Return sorted category totals."""
        return {
            category: self.total(category)
            for category in sorted({item.category for item in self._transactions})
        }
