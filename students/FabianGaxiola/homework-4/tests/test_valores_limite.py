import pytest
from src.inscripcion import (
    EstadoInscripcion,
    SolicitudInscripcion,
    procesar_inscripcion,
)


@pytest.mark.parametrize(
    "edad,promedio,estado_esperado",
    [
        # Límites de edad: mínimo - 1, mínimo, máximo, máximo + 1.
        (17, 85, EstadoInscripcion.RECHAZADA),
        (18, 85, EstadoInscripcion.ACEPTADA),
        (60, 85, EstadoInscripcion.ACEPTADA),
        (61, 85, EstadoInscripcion.RECHAZADA),
        # Límites de promedio: mínimo - 1, mínimo, máximo, máximo + 1.
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
    solicitud = SolicitudInscripcion(
        edad=edad,
        promedio=promedio,
        cupo_disponible=1,
        pago_realizado=True,
    )

    resultado = procesar_inscripcion(solicitud)

    assert resultado == estado_esperado


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
    solicitud = SolicitudInscripcion(
        edad=25,
        promedio=85,
        cupo_disponible=cupo,
        pago_realizado=True,
    )

    resultado = procesar_inscripcion(solicitud)

    assert resultado == estado_esperado
