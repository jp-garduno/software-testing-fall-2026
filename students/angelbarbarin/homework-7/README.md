# Homework 7: Data-Driven Test Suite – E-Commerce Order Processing

**Alumno**: Angel Isaac Barbarín (`angelbarbarin`)
**Lenguaje**: Python 3.10+ con pytest

Sistema de procesamiento de pedidos (cálculo de totales, validación de clientes y flujo completo de compra)
probado con **pruebas basadas en datos**: los casos viven en archivos CSV y JSON dentro de `test_data/` y el
código de prueba solo sabe cómo ejecutar uno. Agregar un escenario es agregar una fila.

## Resultados

| | |
| - | - |
| Pruebas | **308 pasan** (`test_results.txt`) |
| Cobertura | **100%** de sentencias y ramas en `src/` (`coverage_report.html`) |
| Datos | 36 cálculos (CSV), 39 clientes (JSON), 7 flujos (JSON), 100 pedidos generados (CSV) |
| Pylint | 10.00/10 con la configuración del curso |
| Bonus | **A** (generador con Faker) y **C** (validación de los datos con número de línea) |

## Instalación

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## Cómo correr las pruebas

Desde la carpeta `homework-7/` (el `pytest.ini` agrega `src/` al path):

```bash
pytest -v                                         # todas
pytest tests/test_order_calculator.py -v          # solo el calculador
pytest -k "freeship" -v                           # casos cuyo nombre contiene "freeship"
pytest tests/test_order_traditional.py tests/test_order_data_driven.py -v   # comparación
```

Cobertura y reportes:

```bash
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=json
python tools/coverage_report.py                   # coverage.json -> coverage_report.html
pytest -v > test_results.txt
```

Validar los datos sin correr las pruebas, y regenerar los 100 pedidos de Faker:

```bash
python src/data_files.py test_data
python tools/generate_orders.py --count 100 --seed 2026
```

## Estructura

```
homework-7/
├── src/
│   ├── order_calculator.py     # Parte 1: subtotal, descuentos, impuesto, envío, total
│   ├── customer_validator.py   # Parte 2: email, teléfono, dirección, tarjeta (Luhn), expiración, CVV
│   ├── order_processor.py      # Parte 4: flujo validar → crear → descuento → envío → total → pago → confirmación
│   └── data_files.py           # Carga y validación de los archivos de datos (bonus C)
├── tests/
│   ├── conftest.py             # Valida test_data/ antes de correr y fija la fecha de referencia
│   ├── test_order_calculator.py      # 36 casos del CSV + pruebas puntuales de entrada inválida
│   ├── test_customer_validator.py    # 39 casos del JSON
│   ├── test_order_traditional.py     # Parte 3: 10 pruebas escritas a mano
│   ├── test_order_data_driven.py     # Parte 3: las mismas 10 desde CSV
│   ├── test_integration.py           # 7 flujos completos desde JSON
│   ├── test_generated_orders.py      # 100 pedidos generados con Faker (bonus A)
│   └── test_data_files.py            # Pruebas del validador de datos (bonus C)
├── test_data/
│   ├── order_calculations.csv
│   ├── customer_validation.json
│   ├── order_workflows.json
│   ├── comparison_orders.csv
│   └── generated_orders.csv
├── tools/
│   ├── generate_orders.py      # Generador con Faker y oráculo independiente
│   └── coverage_report.py      # Genera coverage_report.html (un solo archivo)
├── COMPARISON_REPORT.md
├── TEST_DATA_SPEC.md
├── coverage_report.html
├── test_results.txt
├── requirements.txt
└── pytest.ini
```

## Funcionalidad

- **Calculador**: `SAVE10`, `SAVE20`, `FREESHIP` y `NEWUSER` (solo clientes nuevos); impuesto de 8%; envío con
  base de $4.00 + $0.50/kg + $0.10/km, express ×1.5; dinero con `Decimal` y redondeo a centavos; rechaza precios,
  cantidades, pesos y distancias negativos. Las decisiones sobre las partes ambiguas del enunciado están en
  [TEST_DATA_SPEC.md](TEST_DATA_SPEC.md#reglas-de-cálculo-que-asumen-los-datos).
- **Validador**: devuelve *todos* los errores en un orden fijo, con mensajes estables que los datos comparan
  literalmente.
- **Flujo de compra**: cada paso recibe y devuelve un diccionario, así que un flujo completo se describe en
  JSON. El pago usa una pasarela simulada y determinista (tarjetas rechazadas y límite configurables).

## Bonus

- **A – Generación de datos**: `tools/generate_orders.py` crea 100 pedidos realistas con Faker (semilla fija,
  reproducible). Los valores esperados los calcula un oráculo propio con fracciones exactas, no el código que
  se prueba, así que el archivo sirve para detectar regresiones.
- **C – Validación de datos**: antes de correr, `conftest.py` valida todos los archivos de `test_data/` (campos
  requeridos, tipos, JSON de artículos, nombres repetidos, coherencia de los esperados) y, si algo falla,
  detiene pytest listando cada problema como `archivo:línea: mensaje`.

## Documentación

- [TEST_DATA_SPEC.md](TEST_DATA_SPEC.md): formato de cada archivo de datos, reglas y cómo agregar casos.
- [COMPARISON_REPORT.md](COMPARISON_REPORT.md): análisis de la versión tradicional contra la data-driven.
