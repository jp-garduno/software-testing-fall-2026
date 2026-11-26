"""Fresh account/clock fixtures and common assertions for the shared design IDs."""

import json
from pathlib import Path

import pytest

from src.banking_system import BankAccount

CASES = json.loads(
    (Path(__file__).parents[1] / "design" / "cases.json").read_text(encoding="utf-8")
)


def cases_for(technique):
    """Select the documented cases for one black box technique."""
    return [case for case in CASES if case["technique"] == technique]


def decode(value):
    """JSON cannot encode NaN/infinity; these explicit markers bridge both runners."""
    if isinstance(value, dict) and "$number" in value:
        return {
            "NaN": float("nan"),
            "Infinity": float("inf"),
            "-Infinity": -float("inf"),
        }[value["$number"]]
    return value


def checkpoint(account, expected):
    """Compare the requested public-state fields with their design oracle."""
    actual = account.snapshot()
    assert {key: actual[key] for key in expected} == expected


@pytest.fixture
def run_case():
    """Provide a runner that builds an independent account and clock per case."""

    def run(case):
        now = [case.get("date", "2026-09-22")]
        args = [decode(value) for value in case["account"]]
        if "constructor_error" in case:
            with pytest.raises(ValueError) as error:
                BankAccount(*args, clock=lambda: now[0])
            assert str(error.value) == case["constructor_error"]
            return
        account = BankAccount(*args, clock=lambda: now[0])
        checkpoint(account, case.get("initial", {}))
        for step in case.get("steps", []):
            if "date" in step:
                now[0] = step["date"]
            before = account.snapshot()
            args = [decode(value) for value in step.get("args", [])]
            result = getattr(account, step["call"])(*args)
            assert result == step["expect"], f'{case["id"]}: {step["call"]}'
            if not result["success"] and not step.get("allows_state_change", False):
                assert (
                    account.snapshot() == before
                ), "Rejected operation changed account"
            checkpoint(account, step.get("snapshot", {}))
            if step.get("mutate_return"):
                result["transactions"][0]["detail"] = "tampered"
                assert account.history(*args) == step["expect"]

    return run
