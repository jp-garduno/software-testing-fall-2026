from src.banking_system import BankAccount


class TestEquivalencePartitioning:

    def test_transfer_valid_amount(self, checking_account):
        """EP1: Transferir una cantidad válida dentro de los límites ($500) debe tener éxito."""
        result = checking_account.transfer(500)
        assert result["success"] is True
        assert checking_account.balance == 5500

    def test_transfer_zero_amount(self, checking_account):
        """EP2: Transferir cantidad cero ($0) debe fallar."""
        result = checking_account.transfer(0)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_transfer_negative_amount(self, checking_account):
        """EP3: Transferir cantidad negativa (-$100) debe fallar."""
        result = checking_account.transfer(-100)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_transfer_exceeds_daily_limit(self, checking_account):
        """EP4: Transferir una cantidad que exceda el límite diario ($10,000) debe fallar."""
        # El límite de checking es 5000
        checking_account.deposit(5000)  # Asegurar fondos suficientes
        result = checking_account.transfer(10000)
        assert result["success"] is False
        assert "Exceeds daily limit" in result["error"]

    def test_transfer_exceeds_balance(self, savings_account):
        """EP5: Transferir una cantidad mayor al saldo disponible debe fallar."""
        # Saldo es 1500
        result = savings_account.transfer(1501)
        assert result["success"] is False
        assert "Insufficient funds" in result["error"]
