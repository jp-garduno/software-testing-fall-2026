# Homework 7: Data-Driven Test Suite

- **Alumno:** Luis-045
- **Rama:** `feat/Luis-045/homework-7`
- **Lenguaje:** Python 3.11 o superior

La entrega implementa el cálculo de pedidos, la validación de clientes y un
checkout con pago simulado y confirmación. Las pruebas usan pytest, con entradas
y resultados esperados en archivos CSV y JSON.

## Preparación

Desde la raíz del repositorio:

```sh
cd students/Luis-045/homework-7
python -m venv .venv
```

Activa el entorno con `source .venv/bin/activate` en Bash o
`.\.venv\Scripts\Activate.ps1` en PowerShell. Luego instala las dependencias:

```sh
python -m pip install -r requirements.txt
```

## Ejecutar y reproducir los reportes

```sh
python -m pytest -q
python -m pytest -v --color=no --cov=src --cov-report=term-missing --cov-report=json
python scripts/render_coverage.py
```

La segunda orden mide sentencias y ramas en `src/`, escribe `coverage.json` y
exige una cobertura combinada de al menos 81%. La tercera crea
[`coverage_report.html`](coverage_report.html), que se puede abrir sin conexión.
[`test_results.txt`](test_results.txt) contiene la salida de la ejecución final.

Resultado en Windows con Python 3.13.9: **87 pruebas aprobadas** y **95.22% de
cobertura combinada** (196 de 202 sentencias y 63 de 70 ramas).

Para comprobar el formato y el estilo desde esta carpeta:

```sh
python -m black --check src tests scripts
python -m isort --check-only --profile black src tests scripts
python -m pylint --rcfile=../../../.github/grading/pylintrc src tests scripts
```

## Qué se prueba

| Archivo | Casos | Alcance |
| --- | ---: | --- |
| `test_order_calculator.py` | 31 | 30 filas CSV y una prueba sobre el cambio de cupón |
| `test_customer_validator.py` | 31 | Contacto, domicilio, tarjeta y errores simultáneos |
| `test_order_traditional.py` | 10 | Diez escenarios con entradas y resultados en Python |
| `test_order_data_driven.py` | 10 | Los mismos diez escenarios seleccionados del CSV |
| `test_integration.py` | 5 | Tres pedidos confirmados y dos flujos bloqueados |

## Reglas del sistema

- `Order` aplica `SAVE10` desde $50 y `SAVE20` desde $100, con ambos límites
  incluidos. `NEWUSER` requiere un cliente nuevo. Un cupón válido reemplaza al
  anterior; un código desconocido, expirado o no aplicable no lo modifica.
- El envío usa el peso por unidad multiplicado por la cantidad y la distancia
  del pedido. La tarifa exprés multiplica el costo combinado por 1.5.
  `FREESHIP` también cubre el envío exprés. Para el ejemplo de 1 kg y 10 km del
  enunciado, la fórmula da $1.50 de envío y $55.50 de total.
- El cálculo usa `Decimal` y redondea subtotal, descuento, impuesto y envío a
  centavos con `ROUND_HALF_UP`. El impuesto es 8% del subtotal descontado.
  Cantidades cero y pedidos vacíos son válidos; valores negativos se rechazan.
- `validate_customer` devuelve todos los errores de formato en orden. La tarjeta
  se comprueba con Luhn y vence al terminar el mes impreso. El CVV, si se incluye,
  debe tener 3 o 4 dígitos. Las pruebas fijan la fecha de referencia para no
  depender del día de ejecución.
- `Checkout` requiere un cliente válido y un total calculado antes del pago.
  La simulación permite reintentar un pago rechazado. La confirmación incluye
  el identificador del pedido y el monto pagado. No se envían cargos ni se
  guardan datos de tarjeta.

Consulta [la comparación](COMPARISON_REPORT.md) para el análisis de las suites
y [la especificación de datos](TEST_DATA_SPEC.md) para agregar escenarios.
