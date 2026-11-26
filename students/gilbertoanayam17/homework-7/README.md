# Homework 7: Data-Driven Test Suite - E-Commerce Order Processing

## Description

Este proyecto es un sistema de procesamiento de pedidos (cálculo de totales, validación de clientes y flujo de compra) que se prueba casi por completo con datos externos. La lógica de cada prueba está escrita una sola vez y los casos viven en archivos CSV, JSON y Excel dentro de `test_data/`, por lo que agregar un caso nuevo consiste en agregar una fila y no en escribir más código.

| Parte                  | Qué se prueba                                   | Datos                                 | Pruebas |
| ---------------------- | ----------------------------------------------- | ------------------------------------- | ------- |
| 1. Order Calculator    | Subtotal, descuento, impuesto, envío y total    | `order_calculations.csv`              | 25      |
| 2. Customer Validation | Email, teléfono, dirección y tarjeta            | `customer_validation.json`            | 30      |
| 3. Comparison          | Los mismos 10 escenarios, de las dos formas     | En el código / `order_comparison.csv` | 10 + 10 |
| 4. Integration         | Flujos completos de compra                      | `order_workflows.json`                | 3       |
| Bonus D (Excel)        | Los casos de pedidos, una hoja por categoría    | `order_calculations.xlsx`             | 25      |
| Bonus B (Performance)  | Tiempo de ejecución, tradicional vs data-driven | Suites generadas de 10 a 500 casos    | -       |

En total son **103 pruebas con 100% de cobertura** de `src/` (143 sentencias).

## Business Rules

Las reglas vienen del enunciado. En los puntos donde este me pareció ambiguo tomé una decisión, y en la siguiente tabla dejo cada una con su motivo.

| Tema                | Decisión                                                                                                                    | Motivo                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Mínimo de un cupón  | Es inclusivo, por lo que `SAVE10` ya aplica con $50.00 exactos y `SAVE20` con $100.00                                       | Así lo hace el `apply_discount` del enunciado, que además pide probar "valid codes at minimum thresholds"      |
| `NEWUSER`           | Solo se acepta si `customer_type` es `"new"`                                                                                | El cupón es "15% off first order"                                                                              |
| Redondeo            | Cada monto se redondea a centavos (medio centavo hacia arriba) y el siguiente se calcula sobre el monto ya redondeado       | De esta forma el total siempre es exactamente subtotal - descuento + impuesto + envío, igual que en un recibo  |
| Valores negativos   | Un artículo con precio, cantidad o peso negativo se ignora completo, mientras que una distancia negativa se cobra como 0 km | Una línea corrupta no debe poder bajar el total, y el CSV solo puede expresar montos esperados, no excepciones |
| Vigencia de tarjeta | La tarjeta sirve hasta el último día de su mes de expiración, y la fecha de "hoy" se puede inyectar (`today=`)              | Las pruebas usan una fecha fija (2025-06-15) para que un caso que pasa hoy siga pasando el año que entra       |
| Pago                | Se rechaza si el cliente no pasó la validación o si no hay un total mayor a cero                                            | No se debe cobrar a un cliente inválido ni un pedido vacío                                                     |

## Prerequisites

- Python 3.11+ (probado con 3.14)
- Las dependencias de `requirements.txt`, que son pytest, pytest-cov, openpyxl (para los datos en Excel) y matplotlib (solo para la gráfica del bonus B)

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v
```

En Windows con varias versiones de Python instaladas se puede usar `py -3.14 -m pytest -v`. El archivo `pytest.ini` agrega `src/` al path, así que no hace falta configurar nada más. Los archivos de datos se localizan a partir de la carpeta de las pruebas, por lo que la suite corre igual desde cualquier directorio.

Cada caso aparece con el nombre que tiene en su archivo de datos, lo que permite correr subconjuntos por nombre, como en los siguientes ejemplos.

```bash
pytest -k "discount"          # los casos de cupones, en todas las suites
pytest -k "Shipping"          # solo la hoja Shipping del Excel
pytest tests/test_integration.py -v
```

## Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

El resultado es 100% de sentencias. Los archivos `test_results.txt` y `coverage_report.html` se regeneran con el siguiente script.

```bash
python scripts/generate_reports.py
```

El reporte HTML es una sola página sin JavaScript, construida a partir del reporte JSON de coverage.py. Lo hice así ya que el autograder pasa ESLint por todo el JavaScript de la entrega, y el sitio que produce `coverage html` incluye un archivo de ese tipo.

## Bonus Features

**Option D - Excel Integration.** `tests/excel_loader.py` lee con openpyxl todas las hojas de `test_data/order_calculations.xlsx` (Simple, Discounts, Tax, Shipping y Complex), una por categoría de prueba. La hoja forma parte del nombre de cada prueba (por ejemplo `Shipping:shipping_weight_only`). El archivo de ejemplo se regenera desde el CSV con `python scripts/build_excel_sample.py`.

**Option B - Performance Comparison.** `python scripts/compare_performance.py` genera suites equivalentes de 10, 50, 100 y 500 casos en las dos formas, mide cuánto tarda cada una y guarda la tabla y la gráfica en `performance/`. El análisis está en [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md).

## Project Structure

```
homework-7/
├── src/
│   ├── order_calculator.py        # Clase Order (subtotal, descuento, impuesto, envío y total)
│   ├── customer_validator.py      # validate_customer y sus reglas en forma de tabla
│   └── checkout.py                # Clase Checkout (une validación, pedido, total y pago)
├── tests/
│   ├── case_loaders.py            # Lee CSV y JSON y entrega casos listos para pytest
│   ├── excel_loader.py            # Lee el libro de Excel (bonus D)
│   ├── test_order_calculator.py   # Parte 1
│   ├── test_customer_validator.py # Parte 2
│   ├── test_order_traditional.py  # Parte 3, 10 pruebas con los datos en el código
│   ├── test_order_data_driven.py  # Parte 3, las mismas 10 desde un CSV
│   ├── test_integration.py        # Parte 4
│   └── test_order_excel.py        # Bonus D
├── test_data/
│   ├── order_calculations.csv     # 25 casos de pedidos
│   ├── order_calculations.xlsx    # Los mismos 25, una hoja por categoría
│   ├── order_comparison.csv       # Los 10 escenarios de la Parte 3
│   ├── customer_validation.json   # 30 casos de clientes
│   └── order_workflows.json       # 3 flujos de compra
├── scripts/
│   ├── generate_reports.py        # test_results.txt y coverage_report.html
│   ├── build_excel_sample.py      # CSV -> Excel (bonus D)
│   └── compare_performance.py     # Mediciones y gráfica (bonus B)
├── performance/
│   ├── results.csv                # Tiempos medidos
│   └── execution_time.png         # Gráfica
├── README.md
├── COMPARISON_REPORT.md           # Parte 3, tradicional vs data-driven
├── TEST_DATA_SPEC.md              # Formato de cada archivo de datos
├── PERFORMANCE_REPORT.md          # Bonus B, análisis de los tiempos
├── coverage_report.html
├── test_results.txt
├── requirements.txt
└── pytest.ini
```

## Documentation

- [TEST_DATA_SPEC.md](TEST_DATA_SPEC.md) describe las columnas, tipos y convenciones de cada archivo de datos, y cómo agregar un caso.
- [COMPARISON_REPORT.md](COMPARISON_REPORT.md) compara líneas de código, mantenimiento, legibilidad y cobertura de las dos formas de escribir las pruebas.
- [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md) analiza los tiempos de ejecución con 10, 50, 100 y 500 casos.
