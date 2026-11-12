# Homework 7: Data-Driven Test Suite (E-Commerce Orders)

## Requisitos
Python 3.10+

## Instalacion
    python -m venv .venv
    source .venv/bin/activate      # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Ejecutar
    pytest -v                                        # todos los tests
    pytest tests/test_order_calculator.py -v         # un archivo
    pytest -v --cov=src --cov-report=term-missing --cov-report=html:coverage_report

El reporte de cobertura queda en `coverage_report/index.html`.

## Estructura
- `src/`: implementacion (calculadora, validador, motor de workflows)
- `tests/`: tests; `data_loader.py` centraliza la carga de datos
- `test_data/`: CSV y JSON con los casos (ver TEST_DATA_SPEC.md)
- `scripts/`: generadores y utilidades

## Decisiones de diseno
- Los umbrales de SAVE10/SAVE20 son inclusivos (>=).
- NEWUSER solo aplica a `customer_type="new"`.
- Valores negativos lanzan `ValueError`.
- Las fechas se inyectan (`today`) para tests deterministas.

## Documentos
COMPARISON_REPORT.md, TEST_DATA_SPEC.md