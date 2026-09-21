"""Budget service that manages entries and generates financial summaries."""

from __future__ import annotations

from typing import Dict, List

from src.budget_models import BudgetCategory, ExpenseEntry, build_category_summary


class BudgetService:
    """Handle expense tracking and budget checks."""

    def __init__(self, limits: Dict[str, float]):
        self.limits = limits
        self.entries: List[ExpenseEntry] = []

    def add_entry(self, category: str, amount: float, description: str) -> None:
        """Add a new expense entry to the service."""
        if amount < 0:
            raise ValueError("Expense amount must be positive.")
        self.entries.append(
            ExpenseEntry(category=category, amount=amount, description=description)
        )

    def total_spent(self) -> float:
        """Return the total amount spent."""
        return round(sum(item.amount for item in self.entries), 2)

    def get_summary(self) -> List[BudgetCategory]:
        """Return a per-category summary for the active budget."""
        return build_category_summary(self.entries, self.limits)

    def over_budget_categories(self) -> List[str]:
        """Return category names that exceed their planned limit."""
        over_budget: List[str] = []
        for category in self.get_summary():
            if category.spent > category.planned:
                over_budget.append(category.category)
        return over_budget

    def remaining_budget(self) -> Dict[str, float]:
        """Return the remaining amount by category."""
        summary = self.get_summary()
        remaining: Dict[str, float] = {}
        for category in summary:
            remaining[category.category] = category.remaining()
        return remaining
