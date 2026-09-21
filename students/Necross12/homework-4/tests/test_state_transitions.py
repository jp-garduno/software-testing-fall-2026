from banking_system import BankAccount


class TestStateTransitions:
    def test_st1_activo_a_suspendido(self):
        """ST1: Activo -> Suspendido"""
        cuenta = BankAccount("Ahorro", 500)
        assert cuenta.next_state("Suspendido") is True
        assert cuenta.state == "Suspendido"
        assert cuenta.last_message == "Enviar notificación de advertencia"

    def test_st2_activo_a_congelado(self):
        """ST2: Activo -> Congelado"""
        cuenta = BankAccount("Ahorro", 500)
        assert cuenta.next_state("Congelado") is True
        assert cuenta.state == "Congelado"
        assert cuenta.last_message == "Bloquear todas las transacciones"

    def test_st3_activo_a_cerrado(self):
        """ST3: Activo -> Cerrado"""
        cuenta = BankAccount("Ahorro", 500)
        assert cuenta.next_state("Cerrado") is True
        assert cuenta.state == "Cerrado"
        assert cuenta.last_message == "Declaración final generada"

    def test_st4_suspendido_a_activo(self):
        """ST4: Suspendido -> Activo al restablecer el saldo"""
        cuenta = BankAccount("Ahorro", 500)
        cuenta.next_state("Suspendido")
        assert cuenta.next_state("Activo") is True
        assert cuenta.state == "Activo"

    def test_st5_saldo_bajo_minimo_suspende(self):
        """ST5: transferir dejando el saldo bajo el mínimo suspende la cuenta"""
        cuenta = BankAccount("Ahorro", 1000)
        cuenta.transfer(950)  # saldo 50 < 100
        assert cuenta.state == "Suspendido"

    def test_st8_cerrado_a_activo_rechazado(self):
        """ST8: Cerrado -> Activo se rechaza"""
        cuenta = BankAccount("Ahorro", 500)
        cuenta.next_state("Cerrado")
        assert cuenta.next_state("Activo") is False
        assert cuenta.state == "Cerrado"
        assert cuenta.last_message == "Error: Cuenta cerrada"
