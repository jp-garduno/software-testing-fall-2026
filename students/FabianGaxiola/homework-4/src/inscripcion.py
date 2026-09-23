"""Módulo para gestionar el proceso de inscripción de estudiantes."""

from dataclasses import dataclass
from enum import Enum


class EstadoInscripcion(str, Enum):
    """Representa los posibles estados de una solicitud de inscripción."""

    PENDIENTE = "PENDIENTE"
    ACEPTADA = "ACEPTADA"
    RECHAZADA = "RECHAZADA"
    LISTA_ESPERA = "LISTA_ESPERA"
    PAGO_PENDIENTE = "PAGO_PENDIENTE"
    CANCELADA = "CANCELADA"


@dataclass
class SolicitudInscripcion:
    """Almacena los datos necesarios para procesar una inscripción.

    Attributes:
        edad: Edad de la persona solicitante.
        promedio: Promedio académico de la persona solicitante.
        cupo_disponible: Cantidad de lugares disponibles.
        pago_realizado: Indica si la persona ya realizó el pago.
        estado: Estado actual de la solicitud.
    """

    edad: int
    promedio: float
    cupo_disponible: int
    pago_realizado: bool
    estado: EstadoInscripcion = EstadoInscripcion.PENDIENTE


def validar_datos(edad: int, promedio: float) -> bool:
    """Valida que la edad y el promedio cumplan los requisitos.

    Args:
        edad: Edad de la persona solicitante.
        promedio: Promedio académico de la persona solicitante.

    Returns:
        True si la edad está entre 18 y 60 y el promedio entre 70 y 100.
        False en caso contrario.
    """
    return 18 <= edad <= 60 and 70 <= promedio <= 100


def procesar_inscripcion(solicitud: SolicitudInscripcion) -> EstadoInscripcion:
    """Procesa una solicitud pendiente según sus datos, cupo y pago.

    Args:
        solicitud: Solicitud de inscripción que se desea procesar.

    Returns:
        El nuevo estado asignado a la solicitud.

    Raises:
        ValueError: Si la solicitud no se encuentra en estado pendiente.
    """
    if solicitud.estado != EstadoInscripcion.PENDIENTE:
        raise ValueError("Solo se pueden procesar solicitudes pendientes")

    if not validar_datos(solicitud.edad, solicitud.promedio):
        solicitud.estado = EstadoInscripcion.RECHAZADA
    elif solicitud.cupo_disponible <= 0:
        solicitud.estado = EstadoInscripcion.LISTA_ESPERA
    elif not solicitud.pago_realizado:
        solicitud.estado = EstadoInscripcion.PAGO_PENDIENTE
    else:
        solicitud.estado = EstadoInscripcion.ACEPTADA

    return solicitud.estado


def confirmar_pago(solicitud: SolicitudInscripcion) -> EstadoInscripcion:
    """Confirma el pago de una solicitud con pago pendiente.

    Args:
        solicitud: Solicitud cuyo pago se desea confirmar.

    Returns:
        El estado actualizado de la solicitud.

    Raises:
        ValueError: Si la solicitud no tiene un pago pendiente.
    """
    if solicitud.estado != EstadoInscripcion.PAGO_PENDIENTE:
        raise ValueError("Solo se puede confirmar el pago pendiente")

    solicitud.pago_realizado = True

    if solicitud.cupo_disponible > 0:
        solicitud.estado = EstadoInscripcion.ACEPTADA
    else:
        solicitud.estado = EstadoInscripcion.LISTA_ESPERA

    return solicitud.estado
