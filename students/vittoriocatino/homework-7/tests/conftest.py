"""Validate all required external datasets before the test session starts."""

from pathlib import Path

from data_loader import load_customers, load_orders, load_workflows


def pytest_sessionstart(session):
    """Reject malformed fixtures early with file/line diagnostics."""
    root = Path(session.config.rootpath) / "test_data"
    load_orders(root / "order_calculations.csv")
    load_customers(root / "customer_validation.json")
    load_workflows(root / "order_workflows.json")
