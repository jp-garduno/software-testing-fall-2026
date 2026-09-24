"""Pruebas de tabla de decisión para el proceso de inscripción."""

import pytest
from src.inscripcion import (
    EstadoInscripcion,
    SolicitudInscripcion,
    procesar_inscripcion,
)


@pytest.mark.parametrize(
    "datos_validos,cupo_disponible,pago_realizado,estado_esperado",
    [
        # Regla 1: datos válidos + cupo + pago = aceptada.
        (True, 1, True, EstadoInscripcion.ACEPTADA),
        # Regla 2: datos válidos + cupo + sin pago = pago pendiente.
        (True, 1, False, EstadoInscripcion.PAGO_PENDIENTE),
        # Regla 3: datos válidos + sin cupo + pago = lista de espera.
        (True, 0, True, EstadoInscripcion.LISTA_ESPERA),
        # Regla 4: datos válidos + sin cupo + sin pago = lista de espera.
        (True, 0, False, EstadoInscripcion.LISTA_ESPERA),
        # Regla 5: datos inválidos = rechazada, sin importar cupo o pago.
        (False, 1, True, EstadoInscripcion.RECHAZADA),
        # Regla 6: datos inválidos = rechazada, sin importar cupo o pago.
        (False, 0, False, EstadoInscripcion.RECHAZADA),
    ],
)
def test_tabla_decision(
    datos_validos,
    cupo_disponible,
    pago_realizado,
    estado_esperado,
):
    """Verifica las reglas de decisión para procesar una inscripción.

    Evalúa las combinaciones relevantes entre validez de los datos,
    disponibilidad de cupo y confirmación de pago, comprobando que
    cada combinación genere el estado de inscripción esperado.
    """
    edad = 25 if datos_validos else 17
    promedio = 85

    solicitud = SolicitudInscripcion(
        edad=edad,
        promedio=promedio,
        cupo_disponible=cupo_disponible,
        pago_realizado=pago_realizado,
    )

    resultado = procesar_inscripcion(solicitud)

    assert resultado == estado_esperado
    assert solicitud.estado == estado_esperado
