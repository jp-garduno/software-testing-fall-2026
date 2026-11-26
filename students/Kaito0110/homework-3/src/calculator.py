from src.operations import (
    division,
    mayor,
    menor,
    modulo,
    multiplicacion,
    porcentaje,
    potencia,
    promedio,
    resta,
    suma,
)
from src.utils import mostrar_menu, mostrar_resultado, pedir_numero


def calcular(opcion, a, b):
    operaciones = {
        "1": suma,
        "2": resta,
        "3": multiplicacion,
        "4": division,
        "5": potencia,
        "6": modulo,
        "7": promedio,
        "8": mayor,
        "9": menor,
        "10": porcentaje,
    }

    if opcion in operaciones:
        return operaciones[opcion](a, b)

    return "Opcion no valida"


def iniciar_calculadora():
    while True:
        mostrar_menu()

        opcion = input("Selecciona una opcion: ")

        if opcion == "0":
            print("Calculadora cerrada")
            break

        a = pedir_numero("Ingresa el primer numero: ")
        b = pedir_numero("Ingresa el segundo numero: ")

        resultado = calcular(opcion, a, b)

        mostrar_resultado(resultado)


def prueba_suma():
    resultado = suma(5, 3)
    print("Prueba suma:", resultado)


def prueba_resta():
    resultado = resta(10, 4)
    print("Prueba resta:", resultado)


def prueba_multiplicacion():
    resultado = multiplicacion(5, 5)
    print("Prueba multiplicacion:", resultado)


def prueba_division():
    resultado = division(10, 2)
    print("Prueba division:", resultado)


def prueba_potencia():
    resultado = potencia(2, 3)
    print("Prueba potencia:", resultado)


def prueba_modulo():
    resultado = modulo(10, 3)
    print("Prueba modulo:", resultado)


if __name__ == "__main__":
    iniciar_calculadora()
