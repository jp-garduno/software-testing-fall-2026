"""Pruebas de análisis de valores límite para el proceso de inscripción."""

import pytest
from src.inscripcion import (
    EstadoInscripcion,
    SolicitudInscripcion,
    procesar_inscripcion,
)


@pytest.mark.parametrize(
    "edad,promedio,estado_esperado",
    [
        # Límites de edad: mínimo - 1, mínimo, máximo y máximo + 1.
        (17, 85, EstadoInscripcion.RECHAZADA),
        (18, 85, EstadoInscripcion.ACEPTADA),
        (60, 85, EstadoInscripcion.ACEPTADA),
        (61, 85, EstadoInscripcion.RECHAZADA),
        # Límites de promedio: mínimo - 1, mínimo, máximo y máximo + 1.
        (25, 69, EstadoInscripcion.RECHAZADA),
        (25, 70, EstadoInscripcion.ACEPTADA),
        (25, 100, EstadoInscripcion.ACEPTADA),
        (25, 101, EstadoInscripcion.RECHAZADA),
    ],
)
def test_valores_limite_edad_y_promedio(
    edad,
    promedio,
    estado_esperado,
):
    """Verifica los límites permitidos para edad y promedio.

    Comprueba los valores inmediatamente inferiores, iguales y superiores
    a los límites de edad de 18 a 60 y promedio de 70 a 100.
    """
    solicitud = SolicitudInscripcion(
        edad=edad,
        promedio=promedio,
        cupo_disponible=1,
        pago_realizado=True,
    )

    resultado = procesar_inscripcion(solicitud)

    assert resultado == estado_esperado
    assert solicitud.estado == estado_esperado


@pytest.mark.parametrize(
    "cupo,estado_esperado",
    [
        # Límite para cupo: menor que cero, cero y uno.
        (-1, EstadoInscripcion.LISTA_ESPERA),
        (0, EstadoInscripcion.LISTA_ESPERA),
        (1, EstadoInscripcion.ACEPTADA),
    ],
)
def test_valores_limite_cupo(cupo, estado_esperado):
    """Verifica el comportamiento de inscripción según el cupo disponible.

    Comprueba que un cupo menor o igual a cero envíe la solicitud a lista
    de espera y que un cupo positivo permita aceptar la inscripción.
    """
    solicitud = SolicitudInscripcion(
        edad=25,
        promedio=85,
        cupo_disponible=cupo,
        pago_realizado=True,
    )

    resultado = procesar_inscripcion(solicitud)

    assert resultado == estado_esperado
    assert solicitud.estado == estado_esperado
