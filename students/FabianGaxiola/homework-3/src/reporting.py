"""Format a budget overview for terminal output."""

from __future__ import annotations

from typing import List

from src.budget_models import BudgetCategory
from src.budget_service import BudgetService


class ConsoleReport:
    """Display a readable summary of the current financial state."""

    @staticmethod
    def render_summary(service: BudgetService) -> str:
        """Build a text report with a clear breakdown of spending."""
        lines: List[str] = [
            "BudgetPulse Summary",
            "===================",
            f"Total spent: ${service.total_spent():,.2f}",
            "",
        ]

        for category in service.get_summary():
            status = "OK" if category.remaining() >= 0 else "OVER"
            lines.append(
                f"{category.category:<12} | planned: ${category.planned:,.2f} | "
                f"spent: ${category.spent:,.2f} | remaining: ${category.remaining():,.2f} | {status}"
            )

        if service.over_budget_categories():
            lines.extend(
                [
                    "",
                    "Categories over budget:",
                    *[f"- {name}" for name in service.over_budget_categories()],
                ]
            )

        return "\n".join(lines)


def render_category_table(categories: List[BudgetCategory]) -> str:
    """Create a compact category table for the CLI summary."""
    lines = [
        "Category      Planned      Spent      Remaining",
        "-----------------------------------------------",
    ]
    for category in categories:
        lines.append(
            f"{category.category:<12} ${category.planned:>9,.2f} ${category.spent:>9,.2f} "
            f"${category.remaining():>10,.2f}"
        )
    return "\n".join(lines)
