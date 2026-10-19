# Homework 5: White Box Testing – TaskFlow System

## Description

Sistema de gestión de tareas (TaskFlow) implementado en Python, con una suite de pruebas de caja blanca:
pruebas unitarias del modelo, pruebas de integración del servicio con sus dependencias, análisis de cobertura
de sentencias/ramas y uso de dobles de prueba (mocks, stubs y fakes) para aislar la base de datos y los
servicios externos de correo y SMS.

## Objectives

- Superar 80% de cobertura de sentencias y 80% de cobertura de ramas
- Probar de forma aislada todos los métodos del modelo `Task`
- Probar flujos completos del `TaskService` con dependencias simuladas
- Documentar y justificar lo que la cobertura no alcanza a verificar

## Prerequisites

- Python 3.10+ (el curso usa 3.11+)
- pytest y pytest-cov (`requirements.txt`)

## Installation

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## Running Tests

Desde la carpeta `homework-5/` (el `pytest.ini` agrega `src/` al path):

```bash
# Todas las pruebas
pytest -v

# Un archivo
pytest tests/test_task_unit.py -v

# Con cobertura de sentencias y ramas
pytest -v --cov=src --cov-branch --cov-report=term-missing
```

## Coverage Reports

```bash
pytest --cov=src --cov-branch --cov-report=html --cov-report=term-missing
start htmlcov\index.html       # Windows
# open htmlcov/index.html      # macOS
```

`htmlcov/` se genera en cada corrida y está en `.gitignore`; la evidencia está en `reports/screenshots/`.

## Current Coverage

| Metric    | Result |
| --------- | ------ |
| Statement | 100% (293/293) |
| Branch    | 100% (96/96)   |
| Function  | 100% (40/40)   |
| Line      | 100%           |

Detalle, estrategia y rutas no verificadas: [reports/coverage-analysis.md](reports/coverage-analysis.md).

## Project Structure

```
homework-5/
├── src/
│   ├── task.py                  # Modelo: validación, transiciones, vencimiento, prioridad
│   ├── task_repository.py       # CRUD, búsqueda/filtros, traducción de errores de BD
│   ├── notification_service.py  # Correo/SMS con validación y reintentos (gateways externos)
│   └── task_service.py          # Reglas de negocio; orquesta repositorio y notificaciones
├── tests/
│   ├── conftest.py              # Fixtures y FakeDatabase
│   ├── test_task_unit.py        # Unitarias del modelo (aisladas)
│   ├── test_task_service_integration.py  # Integración servicio + repositorio + notificaciones
│   ├── test_coverage_edge_cases.py       # Casos límite añadidos tras el primer reporte
│   └── test_mocking.py          # Mocks vs stubs vs fakes, orden de llamadas, reintentos, reloj
└── reports/
    ├── coverage-analysis.md
    ├── analysis-report.md
    ├── reflection.md
    └── screenshots/
```

## Key Features Implemented

- Título obligatorio de 3-100 caracteres y único (sin distinguir mayúsculas); descripción de máximo 500
- Fecha límite en el futuro al crear y al actualizar
- Transiciones `TODO → IN_PROGRESS → DONE`, `ARCHIVED` desde cualquier estado y como estado terminal
- Borrado lógico (archivar) y borrado permanente solo de tareas archivadas
- Detección de tareas vencidas con notificación por cada una
- Búsqueda por estado, prioridad, rango de fechas y título parcial, combinables, ordenada por prioridad
- Un fallo del repositorio detiene la operación y no notifica; un fallo de notificación no rompe el flujo
- Tareas URGENT también envían SMS cuando hay número configurado
- Reintentos configurables en el envío de correo/SMS

## Test Summary

| Archivo | Pruebas |
| ------- | ------- |
| `test_task_unit.py` (unitarias) | 55 |
| `test_task_service_integration.py` (integración) | 29 |
| `test_coverage_edge_cases.py` | 36 |
| `test_mocking.py` | 15 |
| **Total** | **135 – todas pasan** |

Las cifras incluyen casos parametrizados. La suite completa corre en menos de 1 segundo.

## Code Quality

Formateado con black e isort (línea de 120) y analizado con pylint usando la configuración del curso: 10.00/10.

## Author

Angel Isaac Barbarín – Software Testing Fall 2026
