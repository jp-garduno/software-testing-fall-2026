# Homework 7: Data-Driven Test Suite

Suite de pruebas **data-driven** para un sistema de procesamiento de órdenes de e-commerce, en **Python + pytest**.

La lógica de las pruebas está en `tests/` y los datos en archivos externos en `test_data/` (CSV y JSON). Agregar un caso de prueba nuevo es agregar una fila o un objeto al archivo de datos, sin tocar código.

## Contenido

```
homework-7/
├── src/
│   ├── order_calculator.py        # Subtotal, descuentos, impuesto, envío y total
│   └── customer_validator.py      # Email, teléfono, dirección y tarjeta (Luhn)
├── tests/
│   ├── test_order_calculator.py   # Data-driven con order_calculations.csv
│   ├── test_customer_validator.py # Data-driven con customer_validation.json
│   ├── test_order_traditional.py  # 10 tests sin parametrizar (comparación)
│   ├── test_order_data_driven.py  # Los mismos 10 tests, parametrizados
│   └── test_integration.py        # Workflows de punta a punta
├── test_data/
│   ├── order_calculations.csv     # 37 casos
│   ├── customer_validation.json   # 38 casos
│   └── order_workflows.json       # 7 workflows
├── README.md
├── COMPARISON_REPORT.md           # Análisis tradicional vs data-driven
├── TEST_DATA_SPEC.md              # Formato de los archivos de datos
├── coverage_report.html
├── test_results.txt
└── requirements.txt
```

## Requisitos

- Python 3.10 o superior
- Las dependencias de `requirements.txt`: `pytest` y `pytest-cov`

## Instalación

Desde la carpeta `homework-7/`:

```bash
python -m venv venv

# Activar el entorno virtual
source venv/Scripts/activate      # Windows (Git Bash)
venv\Scripts\activate             # Windows (CMD / PowerShell)
source venv/bin/activate          # macOS / Linux

pip install -r requirements.txt
```

## Cómo correr las pruebas

| Qué                                    | Comando                                                                     |
| -------------------------------------- | --------------------------------------------------------------------------- |
| Todas las pruebas                      | `pytest`                                                                    |
| Con detalle de cada caso               | `pytest -v`                                                                 |
| Solo la calculadora de órdenes         | `pytest tests/test_order_calculator.py -v`                                  |
| Solo el validador de clientes          | `pytest tests/test_customer_validator.py -v`                                |
| Comparación tradicional vs data-driven | `pytest tests/test_order_traditional.py tests/test_order_data_driven.py -v` |
| Pruebas de integración                 | `pytest tests/test_integration.py -v`                                       |
| Un caso específico por nombre          | `pytest -k discount_save10_at_threshold -v`                                 |

Cada caso data-driven aparece con su `test_name`, por ejemplo:

```
tests/test_order_calculator.py::test_order_calculation[shipping_express] PASSED
tests/test_customer_validator.py::test_customer_validation[invalid_email_missing_at] PASSED
tests/test_integration.py::test_workflow[complete_order_flow] PASSED
```

## Generar los reportes de resultados

```bash
# Resultados de todas las pruebas, con la tabla de cobertura al final
pytest -v --cov=src --cov-report=term-missing --color=no > test_results.txt

# Reporte de cobertura en HTML (se crea la carpeta htmlcov/)
pytest --cov=src --cov-report=html
cp htmlcov/index.html coverage_report.html
```

Para ver el reporte completo, con el detalle línea por línea de cada archivo, abre `htmlcov/index.html` en el navegador. La carpeta `htmlcov/` no se sube al repositorio.

## Resultados

| Archivo de pruebas           | Tests                 |
| ---------------------------- | --------------------- |
| `test_order_calculator.py`   | 38                    |
| `test_customer_validator.py` | 43                    |
| `test_order_traditional.py`  | 10                    |
| `test_order_data_driven.py`  | 10                    |
| `test_integration.py`        | 8                     |
| **Total**                    | **109 (todos pasan)** |

Cobertura de `src/`: **100 %** (`order_calculator.py` y `customer_validator.py`).

## Agregar un caso de prueba nuevo

1. Abre el archivo de datos que corresponda:
   - Cálculo de órdenes: `test_data/order_calculations.csv`
   - Validación de clientes: `test_data/customer_validation.json`
   - Flujo completo: `test_data/order_workflows.json`
2. Agrega una fila o un objeto con el formato descrito en [`TEST_DATA_SPEC.md`](TEST_DATA_SPEC.md).
3. Corre `pytest -v`. El caso nuevo aparece con su nombre.

## Documentación

- [`TEST_DATA_SPEC.md`](TEST_DATA_SPEC.md): formato de cada archivo de datos, valores permitidos y reglas de negocio.
- [`COMPARISON_REPORT.md`](COMPARISON_REPORT.md): comparación entre pruebas tradicionales y data-driven (líneas de código, mantenibilidad, legibilidad, cobertura y conclusiones).
