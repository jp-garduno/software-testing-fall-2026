from banking_system import BankAccount


class TestTransferValidationDecisionTable:

    def test_rule1_funds_within_limit_active_succeeds(self):
        """Rule 1: Sufficient funds, within limit, Active -> Transfer succeeds."""
        account = BankAccount("Checking", 1000)
        result = account.transfer(500)
        assert result["success"] is True

    def test_rule2_funds_within_limit_not_active_fails(self):
        """Rule 2: Sufficient funds, within limit, but Frozen -> Account not active."""
        account = BankAccount("Checking", 1000)
        account.freeze()
        result = account.transfer(500)
        assert result["success"] is False
        assert "Frozen" in result["error"]

    def test_rule3_funds_exceeds_limit_active_fails(self):
        """Rule 3: Sufficient funds, exceeds limit, Active -> Exceeds limit."""
        account = BankAccount("Checking", 10000)
        result = account.transfer(5000.01)
        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_rule5_insufficient_funds_within_limit_active_fails(self):
        """Rule 5: Insufficient funds (even if within limit, Active) -> Insufficient funds."""
        account = BankAccount("Checking", 100)
        result = account.transfer(500)
        assert result["success"] is False
        assert "Insufficient funds" in result["error"]


class TestBillPaymentValidationDecisionTable:

    def test_rule5_invalid_payee_dominates_other_conditions(self):
        """Rule 5: Invalid payee -> Invalid payee error, regardless of amount/funds."""
        account = BankAccount("Checking", 1000)
        result = account.pay_bill("Random LLC", 100)
        assert result["success"] is False
        assert "Invalid payee" in result["error"]