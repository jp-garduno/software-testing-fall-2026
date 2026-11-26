def mostrar_menu():
    print("\nCALCULADORA")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicacion")
    print("4. Division")
    print("5. Potencia")
    print("6. Modulo")
    print("7. Promedio")
    print("8. Mayor")
    print("9. Menor")
    print("10. Porcentaje")
    print("0. Salir")


def pedir_numero(mensaje):
    numero = float(input(mensaje))
    return numero


def mostrar_resultado(resultado):
    print("Resultado:", resultado)


def convertir_entero(numero):
    return int(numero)


def es_positivo(numero):
    return numero > 0


def es_negativo(numero):
    return numero < 0


def es_cero(numero):
    return numero == 0


def mostrar_mensaje(mensaje):
    print(mensaje)


def pedir_opcion():
    opcion = input("Selecciona una opcion: ")
    return opcion


def confirmar_salida():
    respuesta = input("Quieres salir? ")
    return respuesta.lower() == "si"


def separar():
    print("------------------------")


def titulo():
    print("Calculadora")


def mostrar_datos(a, b):
    print("Primer numero:", a)
    print("Segundo numero:", b)


def mostrar_operacion(nombre):
    print("Operacion seleccionada:", nombre)


def limpiar_pantalla():
    print("\n" * 3)
