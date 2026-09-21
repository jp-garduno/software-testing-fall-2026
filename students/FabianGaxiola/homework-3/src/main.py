"""Entry point for the BudgetPulse demonstration application."""

from __future__ import annotations

from src.budget_service import BudgetService
from src.reporting import ConsoleReport


def main() -> int:
    """Generate a sample budget report for the current month."""
    service = BudgetService(
        {
            "Housing": 1500.0,
            "Food": 500.0,
            "Transport": 220.0,
            "Utilities": 280.0,
            "Entertainment": 180.0,
        }
    )

    service.add_entry("Housing", 1450.0, "Rent payment")
    service.add_entry("Food", 340.5, "Supermarket and groceries")
    service.add_entry("Transport", 90.0, "Fuel and bus rides")
    service.add_entry("Utilities", 175.25, "Electricity and internet")
    service.add_entry(
        "Entertainment",
        210.0,
        "Movie tickets and streaming subscriptions",
    )
    service.add_entry("Food", 95.0, "Coffee shop and lunch")

    print(ConsoleReport.render_summary(service))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
