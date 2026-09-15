"""Validaciones de entrada del cotizador.

Cada funcion responde una pregunta cerrada sobre un dato de entrada y no
produce efectos secundarios, de modo que sea trivial probarlas por separado.
"""

DESCUENTO_MAXIMO = 30
LARGO_SKU = 7
LADA_MEXICO = "52"
LARGO_TELEFONO_CON_LADA = 12


def validar_sku(sku: str) -> bool:
    """Un SKU valido es una cadena de exactamente siete caracteres."""
    if sku is None:
        return False
    return len(sku) == LARGO_SKU


def validar_cantidad(cantidad: object) -> bool:
    """Una cantidad valida es un entero estrictamente positivo."""
    try:
        cantidad_entera = int(cantidad)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False
    return cantidad_entera > 0


def validar_descuento(porcentaje: float) -> bool:
    """El descuento debe estar entre 0 y DESCUENTO_MAXIMO por ciento."""
    return 0 <= porcentaje <= DESCUENTO_MAXIMO


def normalizar_telefono(telefono: str) -> str:
    """Deja solo digitos y quita la lada de Mexico si viene incluida."""
    limpio = "".join(caracter for caracter in telefono if caracter.isdigit())
    if len(limpio) == LARGO_TELEFONO_CON_LADA and limpio.startswith(LADA_MEXICO):
        limpio = limpio[len(LADA_MEXICO) :]
    return limpio
