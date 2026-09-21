import pytest

from banking_system import BankAccount


class TestBoundaryValues:
    def test_bv1_transferir_cero_falla(self):
        """BV1: Transferir $0.00 debe fallar"""
        cuenta = BankAccount("Estándar", 1000)
        resultado = cuenta.transfer(0.0)
        assert resultado["success"] is False
        assert resultado["error"] == "Error: el monto debe ser positivo"

    def test_bv2_transferir_minimo_valido(self):
        """BV2: Transferir exactamente $0.01 se realiza"""
        cuenta = BankAccount("Estándar", 1000)
        resultado = cuenta.transfer(0.01)
        assert resultado["success"] is True
        assert cuenta.balance == pytest.approx(999.99)

    def test_bv3_justo_bajo_el_limite(self, cuenta_estandar):
        """BV3: $4,999.99 (justo bajo el límite) se realiza"""
        assert cuenta_estandar.transfer(4999.99)["success"] is True

    def test_bv4_en_el_limite(self, cuenta_estandar):
        """BV4: Exactamente en el límite de $5,000 se realiza"""
        resultado = cuenta_estandar.transfer(5000)
        assert resultado["success"] is True
        assert cuenta_estandar.daily_transfer_total == 5000

    def test_bv5_justo_sobre_el_limite(self, cuenta_estandar):
        """BV5: $5,000.01 (justo sobre el límite) falla"""
        resultado = cuenta_estandar.transfer(5000.01)
        assert resultado["success"] is False
        assert resultado["error"] == "Error: supera el límite diario"

    def test_bv10_ahorro_en_el_limite(self, cuenta_ahorro):
        """BV10: Ahorro en su límite de $2,000 se realiza"""
        assert cuenta_ahorro.transfer(2000)["success"] is True

    def test_bv11_ahorro_sobre_el_limite(self, cuenta_ahorro):
        """BV11: Ahorro con $2,000.01 supera el límite"""
        resultado = cuenta_ahorro.transfer(2000.01)
        assert resultado["success"] is False
        assert resultado["error"] == "Error: supera el límite diario"
