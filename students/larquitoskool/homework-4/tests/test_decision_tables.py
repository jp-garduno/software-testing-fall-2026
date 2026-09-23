from src.banking_system import BankAccount

class TestDecisionTables:

    def test_dt_transfer_success(self, checking_account):
        """DT1: Fondos suficientes (Y), Dentro del límite (Y), Activa (Y) -> Éxito."""
        result = checking_account.transfer(1000)
        assert result["success"] is True

    def test_dt_transfer_insufficient_funds(self, checking_account):
        """DT2: Fondos suficientes (N), Dentro del límite (Y), Activa (Y) -> Error."""
        checking_account.balance = 500 # Forzar saldo bajo
        result = checking_account.transfer(1000)
        assert result["success"] is False
        assert "Insufficient funds" in result["error"]

    def test_dt_transfer_frozen_account(self, checking_account):
        """DT3: Fondos suficientes (Y), Dentro del límite (Y), Activa (N - Frozen) -> Error."""
        checking_account.freeze_account()
        result = checking_account.transfer(1000)
        assert result["success"] is False
        assert "Account is frozen" in result["error"]

    def test_dt_fee_waived(self, savings_account):
        """DT4: Procesamiento de comisión - Savings con balance > $1000 -> Comisión perdonada."""
        # Saldo es 1500
        result = savings_account.process_monthly_fee()
        assert result["success"] is True
        assert result["fee_charged"] == 0
        assert savings_account.balance == 1500

    def test_dt_fee_charged(self):
        """DT5: Procesamiento de comisión - Savings con balance < $1000 -> Comisión cobrada ($5)."""
        account = BankAccount("Savings", 500)
        result = account.process_monthly_fee()
        assert result["success"] is True
        assert result["fee_charged"] == 5
        assert account.balance == 495