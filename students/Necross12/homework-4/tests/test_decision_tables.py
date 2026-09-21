from banking_system import BankAccount


class TestDecisionTable1:
    def test_td1_todo_correcto(self):
        """TD1 (Regla 1): fondos OK, límite OK, cuenta activa -> éxito"""
        cuenta = BankAccount("Estándar", 10000)
        assert cuenta.transfer(100)["success"] is True
        assert cuenta.last_message == "La transferencia se realiza"

    def test_td2_cuenta_congelada(self):
        """TD2 (Regla 2): cuenta congelada -> error cuenta congelada"""
        cuenta = BankAccount("Estándar", 10000)
        cuenta.next_state("Congelado")
        resultado = cuenta.transfer(100)
        assert resultado["success"] is False
        assert resultado["error"] == "Error: Cuenta congelada"

    def test_td3_limite_excedido(self):
        """TD3 (Regla 3): límite excedido -> error de límite"""
        cuenta = BankAccount("Estándar", 10000)
        resultado = cuenta.transfer(5001)
        assert resultado["success"] is False
        assert resultado["error"] == "Error: supera el límite diario"

    def test_td4_fondos_insuficientes(self):
        """TD4 (Regla 5): fondos insuficientes -> error de fondos"""
        cuenta = BankAccount("Estándar", 100)
        resultado = cuenta.transfer(500)
        assert resultado["success"] is False
        assert resultado["error"] == "Error: fondos insuficientes"

    def test_td5_fondos_y_limite(self):
        """TD5 (Regla 7): prevalece fondos insuficientes"""
        cuenta = BankAccount("Estándar", 100)
        resultado = cuenta.transfer(6000)
        assert resultado["success"] is False
        assert resultado["error"] == "Error: fondos insuficientes"
