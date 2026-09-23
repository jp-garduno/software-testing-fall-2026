from src.banking_system import BankAccount

class TestBoundaryValues:

    def test_transfer_below_minimum(self, checking_account):
        """BV1: Transferir $0.00 debe fallar por estar debajo del mínimo."""
        result = checking_account.transfer(0.00)
        assert result["success"] is False

    def test_transfer_at_minimum_valid_amount(self, checking_account):
        """BV2: Transferir exactamente $0.01 debe ser exitoso."""
        result = checking_account.transfer(0.01)
        assert result["success"] is True
        assert checking_account.balance == 5999.99

    def test_transfer_just_below_limit(self, checking_account):
        """BV3: Transferir justo por debajo del límite ($4,999.99) debe ser exitoso."""
        result = checking_account.transfer(4999.99)
        assert result["success"] is True
        assert checking_account.daily_transfer_total == 4999.99

    def test_transfer_at_limit(self, checking_account):
        """BV4: Transferir exactamente en el límite ($5,000.00) debe ser exitoso."""
        result = checking_account.transfer(5000.00)
        assert result["success"] is True
        assert checking_account.daily_transfer_total == 5000.00

    def test_transfer_just_above_limit(self, checking_account):
        """BV5: Transferir justo por encima del límite ($5,000.01) debe fallar."""
        result = checking_account.transfer(5000.01)
        assert result["success"] is False
        assert "Exceeds daily limit" in result["error"]

    def test_balance_drops_below_minimum_boundary(self):
        """BV6: Si el saldo cae exactamente debajo del mínimo ($100 en Savings), se suspende."""
        account = BankAccount("Savings", 100.00)
        result = account.transfer(0.01)
        assert result["success"] is True
        assert account.state == "Suspended" # El saldo quedó en 99.99