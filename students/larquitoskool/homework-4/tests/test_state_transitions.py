from src.banking_system import BankAccount


class TestStateTransitions:

    def test_st_active_to_suspended(self):
        """ST1: Active -> Suspended cuando el saldo cae por debajo del mínimo."""
        account = BankAccount("Checking", 0)  # Mínimo es 0
        # Forzar el saldo a negativo extrayendo la comisión (simulando un cargo)
        account.balance = -10
        account._update_state()
        assert account.state == "Suspended"

    def test_st_suspended_to_active(self):
        """ST2: Suspended -> Active cuando un depósito restaura el saldo mínimo."""
        # Crear cuenta directamente por debajo del mínimo para que nazca suspendida
        account = BankAccount("Savings", 50)
        assert account.state == "Suspended"

        # Depositar para restaurar el saldo por encima de 100
        account.deposit(100)
        assert account.state == "Active"

    def test_st_active_to_frozen(self, premium_account):
        """ST3: Active -> Frozen por petición."""
        premium_account.freeze_account()
        assert premium_account.state == "Frozen"

    def test_st_frozen_to_closed(self, premium_account):
        """ST4: Frozen -> Closed por petición, sin posibilidad de reapertura."""
        premium_account.freeze_account()
        premium_account.close_account()
        assert premium_account.state == "Closed"

        # Intentar interactuar con la cuenta cerrada
        result = premium_account.deposit(100)
        assert result["success"] is False
        assert "Account closed" in result["error"]
