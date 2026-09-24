"""
Coverage completion tests — SecureBank Online Banking System.

Covers the remaining lines not exercised by EP, BVA, DT, or ST tests:
  - TransactionRecord.__repr__ and to_dict()
  - BankAccount.__repr__
  - BankAccount.export_transactions_csv()
  - BankAccount.get_transaction_history() — future end_date branch
  - BankingSystem.create_account() — invalid type and custom ID
  - BankingSystem.get_account()
  - BankingSystem.process_all_monthly_fees()
  - pay_bill() with past scheduled_date
  - unfreeze() when balance still below minimum → Suspended
"""

import pytest
from datetime import date, timedelta

from src.banking_system import (
    AccountState,
    AccountType,
    BankAccount,
    BankingSystem,
    TransactionRecord,
)


class TestTransactionRecord:
    """Coverage for TransactionRecord methods."""

    def test_repr_contains_type_and_amount(self):
        """TransactionRecord.__repr__ returns a meaningful string."""
        txn = TransactionRecord("DEPOSIT", 100.0, "Test deposit")
        result = repr(txn)
        assert "DEPOSIT" in result
        assert "100" in result

    def test_to_dict_returns_all_fields(self):
        """TransactionRecord.to_dict() returns a complete dictionary."""
        txn = TransactionRecord("TRANSFER_OUT", 50.0, "Wire transfer")
        d = txn.to_dict()
        assert d["type"] == "TRANSFER_OUT"
        assert d["amount"] == 50.0
        assert "description" in d
        assert "date" in d

    def test_custom_transaction_date_is_stored(self):
        """TransactionRecord accepts an explicit date."""
        custom_date = date(2026, 1, 15)
        txn = TransactionRecord("FEE", 5.0, "Monthly fee", custom_date)
        assert txn.date == custom_date


class TestBankAccountReprAndCsv:
    """Coverage for BankAccount.__repr__ and export_transactions_csv."""

    def test_repr_contains_account_info(self, checking_account):
        """BankAccount.__repr__ includes type, balance, and state."""
        result = repr(checking_account)
        assert "Checking" in result
        assert "1000" in result
        assert "Active" in result

    def test_export_csv_header_present(self, checking_account):
        """export_transactions_csv() returns CSV with header row."""
        csv = checking_account.export_transactions_csv()
        assert "date,type,amount,description" in csv

    def test_export_csv_includes_transactions(self, checking_account):
        """export_transactions_csv() includes transaction rows after a transfer."""
        checking_account.transfer(100.0)
        csv = checking_account.export_transactions_csv()
        lines = csv.strip().split("\n")
        assert len(lines) >= 2  # header + at least one transaction

    def test_export_csv_empty_history_only_header(self, premium_account):
        """export_transactions_csv() on a fresh account returns only the header."""
        csv = premium_account.export_transactions_csv()
        lines = csv.strip().split("\n")
        assert len(lines) == 1
        assert lines[0] == "date,type,amount,description"


class TestTransactionHistoryEdgeCases:
    """Coverage for remaining get_transaction_history branches."""

    def test_future_end_date_rejected(self, checking_account):
        """End date in the future is rejected."""
        future = date.today() + timedelta(days=30)
        result = checking_account.get_transaction_history(end_date=future)
        assert result["success"] is False
        assert "future" in result["error"].lower()

    def test_history_with_only_start_date(self, checking_account):
        """Filtering by start_date only works correctly."""
        checking_account.deposit(50.0)
        result = checking_account.get_transaction_history(start_date=date.today())
        assert result["success"] is True
        assert len(result["transactions"]) >= 1

    def test_history_with_only_end_date(self, checking_account):
        """Filtering by end_date only works correctly."""
        checking_account.deposit(50.0)
        result = checking_account.get_transaction_history(end_date=date.today())
        assert result["success"] is True


class TestBillPaymentEdgeCases:
    """Coverage for pay_bill() past-date branch."""

    def test_past_scheduled_date_rejected(self, checking_account):
        """Scheduling a bill payment in the past is rejected."""
        yesterday = date.today() - timedelta(days=1)
        result = checking_account.pay_bill("Electric Co", 50.0, yesterday)
        assert result["success"] is False
        assert "past" in result["error"].lower()


class TestUnfreezeToSuspended:
    """Coverage for unfreeze() → Suspended branch when balance below minimum."""

    def test_unfreeze_with_low_balance_goes_to_suspended(self):
        """Unfreezing a Savings account with balance below $100 → Suspended."""
        account = BankAccount(AccountType.SAVINGS, 500.0)
        # Manually set balance below minimum then freeze
        account.balance = 50.0
        account.state = AccountState.FROZEN
        result = account.unfreeze()
        assert result["success"] is True
        assert account.state == AccountState.SUSPENDED


class TestBankingSystemFull:
    """Coverage for BankingSystem methods."""

    def test_create_account_success(self, banking_system):
        """BankingSystem.create_account() creates and registers an account."""
        result = banking_system.create_account(AccountType.CHECKING, 500.0, "ACC-001")
        assert result["success"] is True
        assert result["account"] is not None
        assert result["error"] is None

    def test_create_account_invalid_type_returns_error(self, banking_system):
        """BankingSystem.create_account() with invalid type returns error dict."""
        result = banking_system.create_account("Diamond", 500.0)
        assert result["success"] is False
        assert "Unknown account type" in result["error"]
        assert result["account"] is None

    def test_get_account_returns_registered_account(self, banking_system):
        """BankingSystem.get_account() retrieves an account by ID."""
        banking_system.create_account(AccountType.SAVINGS, 200.0, "ACC-SAVE")
        account = banking_system.get_account("ACC-SAVE")
        assert account is not None
        assert account.account_type == AccountType.SAVINGS

    def test_get_account_unknown_id_returns_none(self, banking_system):
        """BankingSystem.get_account() returns None for unknown ID."""
        assert banking_system.get_account("DOES-NOT-EXIST") is None

    def test_process_all_monthly_fees_charges_active_accounts(self, banking_system):
        """BankingSystem.process_all_monthly_fees() charges all non-closed accounts."""
        banking_system.create_account(AccountType.SAVINGS, 200.0, "S1")
        banking_system.create_account(AccountType.CHECKING, 1000.0, "C1")
        results = banking_system.process_all_monthly_fees()
        assert len(results) == 2
        # Each result has an account_id key
        for r in results:
            assert "account_id" in r

    def test_process_all_monthly_fees_skips_closed_accounts(self, banking_system):
        """BankingSystem.process_all_monthly_fees() skips Closed accounts."""
        banking_system.create_account(AccountType.CHECKING, 500.0, "C2")
        banking_system.get_account("C2").close()
        results = banking_system.process_all_monthly_fees()
        # Closed account is skipped
        assert len(results) == 0

    def test_process_all_fees_monthly_fee_closed_account_direct(self):
        """BankAccount.process_monthly_fee() on Closed account returns error."""
        account = BankAccount(AccountType.CHECKING, 500.0)
        account.close()
        result = account.process_monthly_fee()
        assert result["success"] is False
        assert "Closed" in result["error"]


class TestAdditionalEdgeCases:
    """Cover remaining 3 lines: deposit zero, freeze-already-frozen, unfreeze-non-frozen."""

    def test_deposit_zero_or_negative_rejected(self, checking_account):
        """deposit() with amount <= 0 is rejected."""
        result = checking_account.deposit(0.0)
        assert result["success"] is False
        assert "positive" in result["error"].lower()

    def test_deposit_negative_rejected(self, checking_account):
        """deposit() with negative amount is rejected."""
        result = checking_account.deposit(-50.0)
        assert result["success"] is False
        assert "positive" in result["error"].lower()

    def test_freeze_already_frozen_returns_error(self, frozen_account):
        """freeze() on an already Frozen account returns an error."""
        result = frozen_account.freeze()
        assert result["success"] is False
        assert "already" in result["error"].lower()

    def test_unfreeze_active_account_returns_error(self, checking_account):
        """unfreeze() on a non-Frozen (Active) account returns an error."""
        result = checking_account.unfreeze()
        assert result["success"] is False
        assert "not Frozen" in result["error"]

