def suma(a, b):
    return a + b


def resta(a, b):
    return a - b


def multiplicacion(a, b):
    return a * b


def division(a, b):
    if b == 0:
        return "No se puede dividir entre 0"
    return a / b


def potencia(a, b):
    return a**b


def modulo(a, b):
    if b == 0:
        return "No se puede calcular el modulo"
    return a % b


def promedio(a, b):
    return (a + b) / 2


def mayor(a, b):
    if a > b:
        return a
    return b


def menor(a, b):
    if a < b:
        return a
    return b


def porcentaje(numero, valor_porcentaje):
    return numero * valor_porcentaje / 100
