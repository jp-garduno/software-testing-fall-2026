# Tarea 7: Suite de pruebas basada en datos (Data-Driven)

Sistema de procesamiento de pedidos de comercio electrónico en Python, probado con
pruebas parametrizadas cuyos datos viven en archivos externos (CSV y JSON). Los datos
están separados de la lógica de prueba: agregar un caso nuevo normalmente es agregar
una fila, no código.

## Contenido

**Partes obligatorias**

- **Parte 1 - Calculadora de pedidos** (`src/order_calculator.py`, `src/discounts.py`):
  subtotal, descuentos (`SAVE10`, `SAVE20`, `FREESHIP`, `NEWUSER`), impuesto del 8 %,
  envío por peso y distancia (con envío exprés) y total.
- **Parte 2 - Validación de clientes** (`src/customer_validator.py`, `src/validation_rules.py`):
  correo, teléfono `(XXX) XXX-XXXX`, dirección de facturación, tarjeta (Luhn), vencimiento
  `MM/AAAA` y CVV. Devuelve `{"is_valid": bool, "errors": [mensajes]}`.
- **Parte 3 - Comparación** (`tests/test_order_traditional.py` vs
  `tests/test_order_data_driven.py` y `COMPARISON_REPORT.md`).
- **Parte 4 - Integración** (`src/order_workflow.py`, `tests/test_integration.py`,
  `test_data/order_workflows.json`): 7 flujos de extremo a extremo, incluidos flujos con pago rechazado.

**Bonus (opciones A y C)**

- **Opción C - Validación de datos**: antes de ejecutar cualquier prueba, `tests/conftest.py`
  (hook `pytest_sessionstart`) valida los archivos de `test_data/` (campos obligatorios, tipos,
  `items` como JSON) y aborta con un reporte `archivo:línea: mensaje` si algo está mal.
  Código en `src/data_checks.py`, `src/orders_csv_check.py`, `src/json_data_check.py` y
  `src/data_validator.py`; pruebas en `tests/test_data_validator.py`.
- **Opción A - Generación de datos**: `src/order_generator.py` genera 100 pedidos válidos con
  Faker y los guarda en `test_data/generated_orders.csv`. Las pruebas en
  `tests/test_order_generator.py` verifican que cada fila pase por `Order`.

## Estructura

```text
homework-7/
├── src/
│   ├── order_calculator.py     # clase Order
│   ├── discounts.py            # reglas de códigos de descuento
│   ├── customer_validator.py   # validate_customer()
│   ├── validation_rules.py     # reglas por campo (email, teléfono, Luhn, ...)
│   ├── order_workflow.py       # flujo: validar -> crear -> total -> pagar
│   ├── data_checks.py          # (bonus C) utilidades de validación de datos
│   ├── orders_csv_check.py     # (bonus C) validación de CSV
│   ├── json_data_check.py      # (bonus C) validación de JSON
│   ├── data_validator.py       # (bonus C) validate_all() y reporte
│   └── order_generator.py      # (bonus A) generador con Faker
├── tests/
│   ├── data_loader.py          # carga de datos con rutas relativas a __file__
│   ├── conftest.py             # valida los datos antes de las pruebas
│   ├── test_order_calculator.py
│   ├── test_customer_validator.py
│   ├── test_order_traditional.py
│   ├── test_order_data_driven.py
│   ├── test_integration.py
│   ├── test_data_validator.py
│   └── test_order_generator.py
├── test_data/
│   ├── order_calculations.csv      # 33 casos
│   ├── customer_validation.json    # 37 casos
│   ├── order_workflows.json        # 7 flujos
│   └── generated_orders.csv        # 100 pedidos generados (bonus A)
├── scripts/make_coverage_report.py # genera coverage_report.html
├── README.md
├── COMPARISON_REPORT.md
├── TEST_DATA_SPEC.md
├── coverage_report.html
├── test_results.txt
├── pytest.ini
└── requirements.txt
```

## Instalación

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Ejecutar las pruebas

Desde la carpeta `students/carloso222/homework-7`:

```bash
python -m pytest -v
```

Con cobertura:

```bash
python -m pytest -v --cov=src --cov-report=term-missing
```

Reporte HTML y resultados guardados:

```bash
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov > test_results.txt
python scripts/make_coverage_report.py   # crea coverage_report.html (un solo archivo)
```

Regenerar los 100 pedidos del bonus A:

```bash
python -m src.order_generator
```

## Resultados

| Métrica                             | Resultado                                                        |
| ----------------------------------- | ---------------------------------------------------------------- |
| Pruebas                             | 268 aprobadas, 0 fallidas                                        |
| Cobertura de `src/`                 | 99 % (421 sentencias, 1 sin cubrir: el `__main__` del generador) |
| Casos en `order_calculations.csv`   | 33 (mínimo 25)                                                   |
| Casos en `customer_validation.json` | 37 (mínimo 30)                                                   |
| Flujos en `order_workflows.json`    | 7 (mínimo 3)                                                     |

## Decisiones de diseño (resumen)

Detalle completo en `TEST_DATA_SPEC.md`.

- `SAVE10` / `SAVE20` exigen un subtotal **estrictamente mayor** a 50 / 100 (el enunciado dice "> $50").
- `NEWUSER` solo es válido si `customer_type == "new"`.
- Cantidad 0 es válida (la línea aporta 0); valores negativos lanzan `ValueError`.
- Los códigos de descuento distinguen mayúsculas y minúsculas.
- La fecha de referencia de las pruebas de vencimiento es fija (`2026-01-15`); nunca se usa el reloj real.
- Los datos se leen con rutas relativas al archivo de prueba (`Path(__file__)`), por lo que
  `pytest` funciona desde cualquier directorio.
