"""Pruebas de transiciones de estado para solicitudes de inscripción."""

import pytest
from src.inscripcion import (
    EstadoInscripcion,
    SolicitudInscripcion,
    cancelar_inscripcion,
    confirmar_pago,
    liberar_cupo,
    procesar_inscripcion,
)


def test_transicion_pendiente_a_aceptada():
    """Verifica la transición de pendiente a aceptada con pago y cupo."""
    solicitud = SolicitudInscripcion(25, 85, 1, True)

    estado = procesar_inscripcion(solicitud)

    assert estado == EstadoInscripcion.ACEPTADA
    assert solicitud.estado == EstadoInscripcion.ACEPTADA


def test_transicion_pendiente_a_pago_pendiente():
    """Verifica la transición de pendiente a pago pendiente sin pago."""
    solicitud = SolicitudInscripcion(25, 85, 1, False)

    estado = procesar_inscripcion(solicitud)

    assert estado == EstadoInscripcion.PAGO_PENDIENTE
    assert solicitud.estado == EstadoInscripcion.PAGO_PENDIENTE


def test_transicion_pago_pendiente_a_aceptada():
    """Verifica que confirmar el pago acepte una solicitud con cupo."""
    solicitud = SolicitudInscripcion(25, 85, 1, False)

    procesar_inscripcion(solicitud)
    estado = confirmar_pago(solicitud)

    assert estado == EstadoInscripcion.ACEPTADA
    assert solicitud.estado == EstadoInscripcion.ACEPTADA
    assert solicitud.pago_realizado is True


def test_transicion_pago_pendiente_a_lista_espera_sin_cupo():
    """Verifica que confirmar el pago sin cupo envíe a lista de espera."""
    solicitud = SolicitudInscripcion(25, 85, 1, False)

    procesar_inscripcion(solicitud)
    solicitud.cupo_disponible = 0

    estado = confirmar_pago(solicitud)

    assert estado == EstadoInscripcion.LISTA_ESPERA
    assert solicitud.estado == EstadoInscripcion.LISTA_ESPERA
    assert solicitud.pago_realizado is True


def test_transicion_pendiente_a_lista_espera():
    """Verifica la transición de pendiente a lista de espera sin cupo."""
    solicitud = SolicitudInscripcion(25, 85, 0, True)

    estado = procesar_inscripcion(solicitud)

    assert estado == EstadoInscripcion.LISTA_ESPERA
    assert solicitud.estado == EstadoInscripcion.LISTA_ESPERA


def test_transicion_lista_espera_a_aceptada():
    """Verifica que liberar cupo acepte una solicitud pagada en espera."""
    solicitud = SolicitudInscripcion(25, 85, 0, True)

    procesar_inscripcion(solicitud)
    estado = liberar_cupo(solicitud)

    assert estado == EstadoInscripcion.ACEPTADA
    assert solicitud.estado == EstadoInscripcion.ACEPTADA
    assert solicitud.cupo_disponible == 1


def test_transicion_lista_espera_a_pago_pendiente():
    """Verifica liberar cupo para una solicitud de espera sin pago."""
    solicitud = SolicitudInscripcion(25, 85, 0, False)

    procesar_inscripcion(solicitud)
    estado = liberar_cupo(solicitud)

    assert estado == EstadoInscripcion.PAGO_PENDIENTE
    assert solicitud.estado == EstadoInscripcion.PAGO_PENDIENTE
    assert solicitud.cupo_disponible == 1


def test_transicion_a_cancelada():
    """Verifica que una solicitud procesada pueda cancelarse."""
    solicitud = SolicitudInscripcion(25, 85, 1, True)

    procesar_inscripcion(solicitud)
    estado = cancelar_inscripcion(solicitud)

    assert estado == EstadoInscripcion.CANCELADA
    assert solicitud.estado == EstadoInscripcion.CANCELADA


def test_no_se_puede_procesar_dos_veces():
    """Verifica que una solicitud ya procesada no se procese de nuevo."""
    solicitud = SolicitudInscripcion(25, 85, 1, True)

    procesar_inscripcion(solicitud)

    with pytest.raises(ValueError, match="solicitudes pendientes"):
        procesar_inscripcion(solicitud)


def test_no_se_puede_confirmar_pago_si_no_esta_pendiente():
    """Verifica que solo se confirme el pago en estado pago pendiente."""
    solicitud = SolicitudInscripcion(25, 85, 1, True)

    procesar_inscripcion(solicitud)

    with pytest.raises(ValueError, match="confirmar el pago pendiente"):
        confirmar_pago(solicitud)


def test_no_se_puede_liberar_cupo_fuera_de_lista_espera():
    """Verifica que solo se libere cupo para solicitudes en espera."""
    solicitud = SolicitudInscripcion(25, 85, 1, True)

    procesar_inscripcion(solicitud)

    with pytest.raises(ValueError, match="liberar cupo"):
        liberar_cupo(solicitud)


def test_no_se_puede_cancelar_dos_veces():
    """Verifica que una solicitud cancelada no pueda cancelarse otra vez."""
    solicitud = SolicitudInscripcion(25, 85, 1, True)

    cancelar_inscripcion(solicitud)

    with pytest.raises(ValueError, match="ya está cancelada"):
        cancelar_inscripcion(solicitud)
