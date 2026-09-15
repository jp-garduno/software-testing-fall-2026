from operations import (
    suma,
    resta,
    multiplicacion,
    division,
    potencia,
    modulo,
    promedio,
    mayor,
    menor,
    porcentaje
)

from utils import mostrar_menu, pedir_numero, mostrar_resultado


def calcular(opcion, a, b):
    if opcion == "1":
        return suma(a, b)

    if opcion == "2":
        return resta(a, b)

    if opcion == "3":
        return multiplicacion(a, b)

    if opcion == "4":
        return division(a, b)

    if opcion == "5":
        return potencia(a, b)

    if opcion == "6":
        return modulo(a, b)

    if opcion == "7":
        return promedio(a, b)

    if opcion == "8":
        return mayor(a, b)

    if opcion == "9":
        return menor(a, b)

    if opcion == "10":
        return porcentaje(a, b)

    return "Opcion no valida"


def iniciar_calculadora():
    while True:
        mostrar_menu()

        opcion = input("Selecciona una opcion: ")

        if opcion == "0":
            print("Bye...")
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