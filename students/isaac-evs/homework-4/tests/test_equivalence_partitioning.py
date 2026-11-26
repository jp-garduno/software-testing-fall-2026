"""Equivalence Partitioning tests — see design/test-design-document.md, Section 1."""

from datetime import date

import pytest

from src.banking_system import (
    BankAccount,
    filter_transactions_by_date,
    validate_account_type,
    validate_bill_payment,
)


class TestTransferAmountPartitions:
    def test_ep1_valid_amount_within_limits(self, checking_account, today):
        """EP1: A valid amount within balance and daily limit succeeds."""
        result = checking_account.transfer(500, today=today)
        assert result["success"] is True

    def test_ep2_zero_amount(self, checking_account, today):
        """EP2: A zero transfer amount is rejected."""
        result = checking_account.transfer(0, today=today)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_ep3_negative_amount(self, checking_account, today):
        """EP3: A negative transfer amount is rejected."""
        result = checking_account.transfer(-100, today=today)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_ep4_amount_exceeds_daily_limit(self, today):
        """EP4: An amount exceeding the account type's daily limit is rejected."""
        account = BankAccount(
            "Checking", 200000, today=today
        )  # balance is not the limiting factor
        result = account.transfer(100000, today=today)
        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_ep5_amount_exceeds_balance(self, today):
        """EP5: An amount exceeding the current balance is rejected."""
        account = BankAccount("Checking", 100, today=today)
        result = account.transfer(101, today=today)
        assert result["success"] is False
        assert "Insufficient funds" in result["error"]


class TestAccountTypePartitions:
    def test_ep6_valid_type_savings(self):
        """EP6: 'Savings' is a recognized account type."""
        assert validate_account_type("Savings")["success"] is True

    def test_ep7_valid_type_checking(self):
        """EP7: 'Checking' is a recognized account type."""
        assert validate_account_type("Checking")["success"] is True

    def test_ep8_valid_type_premium(self):
        """EP8: 'Premium' is a recognized account type."""
        assert validate_account_type("Premium")["success"] is True

    def test_ep9_invalid_type(self):
        """EP9: An unrecognized account type is rejected."""
        result = validate_account_type("Crypto")
        assert result["success"] is False
        assert "Invalid account type" in result["error"]

    def test_ep10_blank_type(self):
        """EP10: An empty account type string is rejected."""
        result = validate_account_type("")
        assert result["success"] is False

    def test_ep9b_invalid_type_raises_on_account_creation(self):
        """EP9 (creation path): Creating a BankAccount with an unrecognized type raises."""
        with pytest.raises(ValueError):
            BankAccount("Crypto", 100)

    def test_ep2b_deposit_non_positive_amount_rejected(self, checking_account):
        """EP2 (deposit path): A zero or negative deposit amount is rejected."""
        result = checking_account.deposit(0)
        assert result["success"] is False
        assert "must be positive" in result["error"]


class TestAccountBalancePartitions:
    def test_ep11_balance_above_minimum_is_active(self):
        """EP11: A Savings account opened above its minimum balance starts Active."""
        account = BankAccount("Savings", 500)
        assert account.state == "Active"

    def test_ep12_balance_below_minimum_is_suspended(self):
        """EP12: A Savings account opened below its minimum balance starts Suspended."""
        account = BankAccount("Savings", 50)
        assert account.state == "Suspended"

    def test_ep13_balance_at_minimum_is_active(self):
        """EP13: A Savings account opened exactly at its minimum balance starts Active."""
        account = BankAccount("Savings", 100)
        assert account.state == "Active"


class TestPayeePartitions:
    def test_ep14_valid_payee(self, checking_account):
        """EP14: A non-empty payee name is accepted."""
        result = validate_bill_payment(checking_account, "City Water Utility", 50)
        assert result["success"] is True

    def test_ep15_empty_payee(self, checking_account):
        """EP15: An empty string payee is rejected."""
        result = validate_bill_payment(checking_account, "", 50)
        assert result["success"] is False
        assert "Invalid payee" in result["error"]

    def test_ep16_whitespace_payee(self, checking_account):
        """EP16: A whitespace-only payee is rejected."""
        result = validate_bill_payment(checking_account, "   ", 50)
        assert result["success"] is False
        assert "Invalid payee" in result["error"]

    def test_ep17_none_payee(self, checking_account):
        """EP17: A None payee is rejected."""
        result = validate_bill_payment(checking_account, None, 50)
        assert result["success"] is False
        assert "Invalid payee" in result["error"]


class TestDateRangePartitions:
    TRANSACTIONS = [
        (date(2026, 1, 5), "deposit", 100),
        (date(2026, 1, 15), "transfer", 50),
        (date(2026, 2, 1), "fee", 10),
    ]

    def test_ep18_valid_range_start_before_end(self):
        """EP18: A valid range with start before end returns matching transactions."""
        result = filter_transactions_by_date(
            self.TRANSACTIONS, date(2026, 1, 1), date(2026, 1, 31)
        )
        assert result["success"] is True
        assert len(result["transactions"]) == 2

    def test_ep19_valid_range_single_day(self):
        """EP19: A single-day range (start == end) returns only that day's transactions."""
        result = filter_transactions_by_date(
            self.TRANSACTIONS, date(2026, 1, 15), date(2026, 1, 15)
        )
        assert result["success"] is True
        assert len(result["transactions"]) == 1

    def test_ep20_invalid_range_start_after_end(self):
        """EP20: A range where start is after end is rejected."""
        result = filter_transactions_by_date(
            self.TRANSACTIONS, date(2026, 2, 1), date(2026, 1, 1)
        )
        assert result["success"] is False
        assert "start_date" in result["error"]

    def test_ep21_valid_range_no_matches(self):
        """EP21: A valid range with no matching transactions returns an empty list, not an error."""
        result = filter_transactions_by_date(
            self.TRANSACTIONS, date(2026, 6, 1), date(2026, 6, 30)
        )
        assert result["success"] is True
        assert result["transactions"] == []
