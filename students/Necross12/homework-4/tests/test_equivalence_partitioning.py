from banking_system import BankAccount

class TestEquivalencePartitioning:
    def test_ep6_ahorro_valido(self):
        """EP6: Ahorro es un tipo válido"""
        r = BankAccount.validar_tipo_cuenta("Ahorro")
        assert r["valid"] is True
        assert r["message"] == "Se acepta: cuenta de ahorro"

    def test_ep7_estandar_valido(self):
        """EP7: Estándar es un tipo válido"""
        r = BankAccount.validar_tipo_cuenta("Estándar")
        assert r["valid"] is True
        assert r["message"] == "Se acepta: cuenta corriente"

    def test_ep8_premium_valido(self):
        """EP8: Premium es un tipo válido"""
        r = BankAccount.validar_tipo_cuenta("Premium")
        assert r["valid"] is True
        assert r["message"] == "Se acepta: cuenta premium"

    def test_ep9_otro_invalido(self):
        """EP9: 'Otro' es un tipo inválido"""
        r = BankAccount.validar_tipo_cuenta("Otro")
        assert r["valid"] is False
        assert r["error"] == "Error: tipo de cuenta no válido"

    def test_ep10_business_invalido(self):
        """EP10: 'Business' es un tipo inválido"""
        r = BankAccount.validar_tipo_cuenta("Business")
        assert r["valid"] is False
        assert r["error"] == "Error: tipo de cuenta no válido"

    def test_ep11_tipo_vacio_invalido(self):
        """EP11: tipo vacío es inválido"""
        r = BankAccount.validar_tipo_cuenta("")
        assert r["valid"] is False
        assert r["error"] == "Error: el tipo de cuenta es obligatorio"
