"""Pruebas de particiones de equivalencia para el proceso de inscripción."""

import pytest
from src.inscripcion import (
    EstadoInscripcion,
    SolicitudInscripcion,
    procesar_inscripcion,
)


@pytest.mark.parametrize(
    "edad,promedio,cupo,pago,estado_esperado",
    [
        # Partición válida: edad y promedio válidos, cupo y pago correctos.
        (25, 85, 10, True, EstadoInscripcion.ACEPTADA),
        # Partición inválida: edad menor al mínimo.
        (17, 85, 10, True, EstadoInscripcion.RECHAZADA),
        # Partición inválida: edad mayor al máximo.
        (61, 85, 10, True, EstadoInscripcion.RECHAZADA),
        # Partición inválida: promedio menor al mínimo.
        (25, 69, 10, True, EstadoInscripcion.RECHAZADA),
        # Partición inválida: promedio mayor al máximo.
        (25, 101, 10, True, EstadoInscripcion.RECHAZADA),
        # Partición válida de datos, pero sin cupo.
        (25, 85, 0, True, EstadoInscripcion.LISTA_ESPERA),
        # Partición válida de datos y cupo, pero sin pago.
        (25, 85, 10, False, EstadoInscripcion.PAGO_PENDIENTE),
    ],
)
def test_particiones_equivalencia(
    edad,
    promedio,
    cupo,
    pago,
    estado_esperado,
):
    """Verifica que cada partición produzca el estado esperado.

    Evalúa solicitudes con datos válidos e inválidos, así como
    escenarios sin cupo disponible o con pago pendiente.
    """
    solicitud = SolicitudInscripcion(
        edad=edad,
        promedio=promedio,
        cupo_disponible=cupo,
        pago_realizado=pago,
    )

    resultado = procesar_inscripcion(solicitud)

    assert resultado == estado_esperado
    assert solicitud.estado == estado_esperado
