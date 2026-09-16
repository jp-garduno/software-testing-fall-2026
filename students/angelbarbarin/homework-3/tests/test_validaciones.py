"""Pruebas de las funciones de validacion."""
from src.validaciones import (
    normalizar_telefono,
    validar_cantidad,
    validar_descuento,
    validar_sku,
)


def test_validar_sku():
    assert validar_sku("CAM-001") is True
    assert validar_sku("CAM-1") is False
    assert validar_sku(None) is False


def test_validar_cantidad():
    assert validar_cantidad(3) is True
    assert validar_cantidad("3") is True
    assert validar_cantidad(0) is False
    assert validar_cantidad("tres") is False


def test_validar_descuento():
    assert validar_descuento(10) is True
    assert validar_descuento(-1) is False
    assert validar_descuento(31) is False


def test_normalizar_telefono():
    assert normalizar_telefono("+52 (33) 1234-5678") == "3312345678"
    assert normalizar_telefono("33 1234 5678") == "3312345678"
