"""Budget-related data models and summary utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class ExpenseEntry:
    """Represents a single expense entry."""

    category: str
    amount: float
    description: str


@dataclass
class BudgetCategory:
    """Stores a category summary and remaining balance."""

    category: str
    planned: float
    spent: float = 0.0

    def remaining(self) -> float:
        """Return the remaining budget for the category."""
        return round(self.planned - self.spent, 2)


def calculate_total(entries: Iterable[ExpenseEntry]) -> float:
    """Compute the sum of all amounts in a collection of expenses."""
    return round(sum(entry.amount for entry in entries), 2)


def build_category_summary(
    entries: Iterable[ExpenseEntry],
    limits: Dict[str, float],
) -> List[BudgetCategory]:
    """Convert expenses into category summaries using the planned limits."""
    summary: Dict[str, BudgetCategory] = {
        category: BudgetCategory(category=category, planned=amount)
        for category, amount in limits.items()
    }

    for entry in entries:
        if entry.category in summary:
            summary[entry.category].spent += entry.amount

    return sorted(summary.values(), key=lambda item: item.category)


def budget_health(categories: Iterable[BudgetCategory]) -> Dict[str, float]:
    """Return remaining budget values for every category."""
    return {category.category: category.remaining() for category in categories}
