"""Pruebas del validador de clientes, guiadas por customer_validation.json.

Cada caso del archivo trae el cliente completo, si debe ser valido y la lista
exacta de errores esperados, en el orden que produce validate_customer.
"""

import pytest

from conftest import cargar_json
from customer_validator import (
    ERRORS,
    is_valid_card_number,
    is_valid_email,
    is_valid_expiry,
    is_valid_phone,
    passes_luhn,
    validate_customer,
)

DATOS = cargar_json("customer_validation.json")
CASOS = DATOS["test_cases"]
CATEGORIAS_MINIMAS = {
    "valid_customers": 3,
    "invalid_emails": 4,
    "invalid_phones": 4,
    "invalid_addresses": 5,
    "invalid_cards": 8,
    "multiple_errors": 6,
}


@pytest.mark.parametrize("caso", CASOS, ids=lambda caso: caso["test_name"])
def test_validacion_de_cliente(caso):
    """El veredicto y la lista completa de errores salen del archivo."""
    es_valido, errores = validate_customer(caso["customer"])

    assert es_valido == caso["expected_valid"], caso["reason"]
    assert errores == caso["expected_errors"], caso["reason"]


class TestCoberturaDelArchivo:
    """El archivo tiene que seguir cumpliendo lo que pide el enunciado."""

    def test_minimo_de_casos(self):
        assert len(CASOS) >= 30

    @pytest.mark.parametrize("categoria,minimo", sorted(CATEGORIAS_MINIMAS.items()))
    def test_minimo_por_categoria(self, categoria, minimo):
        assert len([c for c in CASOS if c["category"] == categoria]) >= minimo

    def test_cada_regla_aparece_fallando_sola(self):
        solos = {tuple(c["expected_errors"])[0] for c in CASOS if len(c["expected_errors"]) == 1}
        assert solos == set(ERRORS.values())


class TestLuhn:
    """El algoritmo por separado, sin pasar por el cliente completo."""

    @pytest.mark.parametrize(
        "numero",
        ["4532015112830366", "4111111111111111", "5425233430109903", "378282246310005", "6011111111111117"],
    )
    def test_numeros_que_pasan(self, numero):
        assert passes_luhn(numero) is True
        assert is_valid_card_number(numero) is True

    @pytest.mark.parametrize("numero", ["4532015112830367", "4111111111111112", "1234567890123"])
    def test_numeros_que_no_pasan(self, numero):
        assert is_valid_card_number(numero) is False

    @pytest.mark.parametrize("numero", ["4532 0151 1283 0366", "4532-0151-1283-0366"])
    def test_separadores_se_ignoran(self, numero):
        assert is_valid_card_number(numero) is True

    @pytest.mark.parametrize("largo,valido", [(12, False), (13, True), (19, True), (20, False)])
    def test_fronteras_de_longitud(self, largo, valido):
        """Se construye un numero del largo pedido y se le ajusta el digito final."""
        base = "4" + "0" * (largo - 2)
        for ultimo in "0123456789":
            if passes_luhn(base + ultimo):
                assert is_valid_card_number(base + ultimo) is valido
                return
        pytest.fail("no se encontro digito de control")

    @pytest.mark.parametrize("valor", [None, 4532015112830366, [], {}])
    def test_tipos_que_no_son_texto(self, valor):
        assert is_valid_card_number(valor) is False


class TestVencimiento:
    """La fecha de referencia es noviembre de 2026, fijada en el modulo."""

    @pytest.mark.parametrize(
        "valor,esperado",
        [("11/26", True), ("12/26", True), ("10/26", False), ("01/27", True), ("12/25", False)],
    )
    def test_frontera_del_mes(self, valor, esperado):
        assert is_valid_expiry(valor) is esperado

    @pytest.mark.parametrize("valor", ["13/27", "00/27", "2027-12", "12/2027", "1227", "", None])
    def test_formatos_invalidos(self, valor):
        assert is_valid_expiry(valor) is False


class TestCamposSueltos:
    """Email y telefono por separado."""

    @pytest.mark.parametrize(
        "valor,esperado",
        [("a@b.co", True), ("a@b", False), ("@b.co", False), ("a b@c.co", False), (None, False), (123, False)],
    )
    def test_email(self, valor, esperado):
        assert is_valid_email(valor) is esperado

    @pytest.mark.parametrize(
        "valor,esperado",
        [
            ("(555) 123-4567", True),
            ("(555)123-4567", False),
            ("555-123-4567", False),
            (None, False),
            (5551234567, False),
        ],
    )
    def test_telefono(self, valor, esperado):
        assert is_valid_phone(valor) is esperado

    def test_un_registro_que_no_es_objeto_reporta_todo(self):
        es_valido, errores = validate_customer("no soy un cliente")
        assert es_valido is False
        assert errores == list(ERRORS.values())
