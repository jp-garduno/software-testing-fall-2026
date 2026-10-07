# Homework 4: Black Box Testing — SecureBank System

**Autor**: Angel Isaac Barbarín ([@angelbarbarin](https://github.com/angelbarbarin))
**Curso**: Software Testing, Fall 2026 — Módulo 4

## Description

Suite completa de pruebas de caja negra para **SecureBank**, un sistema de banca en línea con tres tipos de cuenta, cuatro estados, transferencias con límite diario, pagos de servicios, comisiones mensuales e historial de movimientos.

La suite aplica las cuatro técnicas del módulo — Particiones de Equivalencia, Análisis de Valores Límite, Tablas de Decisión y Transición de Estados — y está implementada **dos veces**: en Python con pytest y en JavaScript con Jest (bonus de doble implementación). Los diagramas del documento de diseño están hechos en Mermaid (bonus de diagramas visuales) y GitHub los renderiza directamente.

## Prerequisites

- Python 3.11+
- Node.js 22+ (solo para la versión JavaScript)

## Installation

```bash
# Python
pip install -r requirements.txt

# JavaScript
npm install
```

## Running Tests

```bash
# Python - todas las pruebas
pytest -v

# Python - una técnica en particular
pytest tests/test_boundary_values.py -v

# JavaScript - todas las pruebas
npm test
```

## Coverage Report

```bash
# Python: reporte en terminal + HTML en htmlcov/index.html
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html

# JavaScript: reporte en terminal + HTML en coverage/lcov-report/index.html
npm run test:coverage
```

## Project Structure

```
homework-4/
├── README.md
├── design/
│   └── test-design-document.md      # Parte 1: EP, BVA, tablas de decisión y estados
├── src/
│   ├── __init__.py
│   ├── banking_system.py            # Sistema bajo prueba (Python)
│   └── bankingSystem.js             # Sistema bajo prueba (JavaScript)
├── tests/
│   ├── conftest.py                  # Fixtures: reloj controlable y fábrica de cuentas
│   ├── test_equivalence_partitioning.py
│   ├── test_boundary_values.py
│   ├── test_decision_tables.py
│   ├── test_state_transitions.py
│   ├── helpers/fakeClock.js
│   ├── equivalencePartitioning.test.js
│   ├── boundaryValues.test.js
│   ├── decisionTables.test.js
│   └── stateTransitions.test.js
├── reports/
│   ├── test-execution-report.md     # Parte 3
│   ├── analysis-report.md           # Parte 4
│   ├── reflection.md
│   └── screenshots/
├── requirements.txt
├── package.json
├── pytest.ini
└── .gitignore
```

## Test Coverage

| Técnica | Casos de diseño | Pruebas (por lenguaje) |
| --- | --- | --- |
| Equivalence Partitioning | EP1–EP34 sobre 7 entradas | 40 |
| Boundary Value Analysis | BV1–BV48 sobre 10 fronteras | 50 |
| Decision Tables | 4 tablas (DT1–DT4) | 38 |
| State Transitions | ST1–ST18 | 24 |
| **Total** | | **152** |

- Cobertura de `src/`: 100% de líneas y ramas en ambos lenguajes.
- Efectividad: la suite detectó 15 de 15 defectos introducidos deliberadamente (ver `reports/test-execution-report.md`).

## What Was Tested

- **Transferencias**: monto mínimo ($0.01), precisión de centavos, límite diario por tipo de cuenta y su reinicio a medianoche, fondos suficientes, cuenta destino.
- **Estados de la cuenta**: Active, Suspended, Frozen y Closed, con todas las transiciones válidas y el rechazo de las inválidas.
- **Comisiones mensuales**: cobro el día 1, exención por saldo, suspensión por falta de fondos.
- **Pagos de servicios**: beneficiarios registrados, pagos inmediatos, programados y con fecha pasada.
- **Historial**: filtros por rango de fechas y exportación a CSV.
- **Apertura de cuentas**: tipo válido y saldo mínimo de apertura.

El reloj del sistema se inyecta como dependencia, así que las pruebas de fechas (medianoche, día 1 del mes, pagos programados) son deterministas y no dependen de cuándo se ejecuten.
