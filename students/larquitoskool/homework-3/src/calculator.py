from src.advanced_operations import factorial, logarithm, power, square_root
from src.math_operations import AddNumbers, add_numbers, divide, multiply, subtract


class Calculator:
    """Clase principal de la calculadora que maneja el historial."""

    def __init__(self):
        self.history = []

    def execute_operation(self, operation, *args):
        result = None
        try:
            if operation == "add":
                result = add_numbers(args[0], args[1])
            elif operation == "subtract":
                result = subtract(args[0], args[1])
            elif operation == "multiply":
                result = multiply(args[0], args[1])
            elif operation == "divide":
                result = divide(args[0], args[1])
            elif operation == "power":
                result = power(args[0], args[1])
            elif operation == "sqrt":
                result = square_root(args[0])
            elif operation == "factorial":
                result = factorial(args[0])
            elif operation == "log":
                result = logarithm(args[0], args[1] if len(args) > 1 else 2.71828)
            else:
                print("Operación desconocida")
                return None

            self.history.append(f"{operation} {args} = {result}")
            return result

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None

    def print_history(self):
        print("--- Historial de Cálculos ---")
        if not self.history:
            print("No hay historial todavía.")
        for entry in self.history:
            print(entry)
        print("---------------------------")


def run_interactive_calculator():
    calc = Calculator()
    print("=============================")
    print("   Calculadora en Consola    ")
    print("=============================")
    print("Operaciones: add, subtract, multiply, divide, power, sqrt, factorial, log")

    while True:
        user_input = input(
            "Ingresa la operación y los números separados por espacio (o 'quit' / 'history'): "
        )
        parts = user_input.strip().split()

        if not parts:
            continue

        command = parts[0].lower()

        if command == "quit":
            print("Saliendo de la calculadora...")
            break
        elif command == "history":
            calc.print_history()
            continue

        try:
            args = [float(arg) for arg in parts[1:]]
            if command == "factorial":
                args = [int(args[0])]
            result = calc.execute_operation(command, *args)
            if result is not None:
                print(f"Resultado: {result}")
        except ValueError:
            print("Argumentos inválidos. Por favor, ingresa números.")


if __name__ == "__main__":
    run_interactive_calculator()
