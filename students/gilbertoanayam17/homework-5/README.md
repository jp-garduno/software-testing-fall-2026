# Homework 5: White Box Testing - TaskFlow System

## Description

TaskFlow es un sistema de gestión de tareas construido desde cero para practicar pruebas de caja blanca: modelo con validaciones y ciclo de vida, repositorio sobre una base de datos inyectada, servicio de negocio y un cliente de notificaciones (email/SMS) hacia una API externa. La suite combina pruebas unitarias, de integración y de mocking, y se guía con cobertura de sentencias y de ramas.

## Objectives

- Superar 80% de cobertura de sentencias, ramas y funciones (logrado: 99.61%, 100% y 97.78%).
- Probar el modelo `Task` de forma aislada y el servicio junto con el repositorio.
- Reemplazar toda dependencia externa (base de datos, API de notificaciones y reloj) por dobles de prueba.
- Documentar y justificar cada línea sin cubrir.

## Prerequisites

- Python 3.11+ (probado con 3.12 y 3.14)
- pytest y pytest-cov (en `requirements.txt`)

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v                                   # toda la suite
pytest tests/test_task_unit.py -v           # solo las pruebas unitarias
pytest -v --cov=src --cov-branch --cov-report=term-missing   # con cobertura
```

`pytest.ini` agrega `.` y `src` al path, así que `pytest` funciona igual que `python -m pytest`.

## Coverage Reports

```bash
pytest --cov=src --cov-branch --cov-report=html --cov-report=term-missing
```

Después abre `htmlcov/index.html`. `htmlcov/` está en `.gitignore`: las capturas en `reports/screenshots/` son la evidencia.

## Current Coverage

| Metric             | Achieved         |
| ------------------ | ---------------- |
| Statement Coverage | 99.61% (256/257) |
| Branch Coverage    | 100.00% (68/68)  |
| Function Coverage  | 97.78% (44/45)   |
| Line Coverage      | 99.61%           |

La única línea sin cubrir es `task.py:43`, el reloj real, y la justificación está en [coverage-analysis.md](reports/coverage-analysis.md#untested-code-paths).

## Test Summary

| File                                     | Cases   | Type                                      |
| ---------------------------------------- | ------- | ----------------------------------------- |
| `tests/test_task_unit.py`                | 51      | Unit: `Task` aislado                      |
| `tests/test_task_service_integration.py` | 19      | Integration: servicio + repositorio       |
| `tests/test_mocking.py`                  | 22      | Mocks, stubs, fakes y escenarios de error |
| `tests/test_coverage_edge_cases.py`      | 23      | Ramas y límites que dejó el reporte       |
| **Total**                                | **115** | 92 funciones de prueba, 0.20 s            |

Todas pasan. No hay pruebas `skip` ni `xfail`.

## Project Structure

```
homework-5/
├── README.md
├── requirements.txt          # pytest, pytest-cov
├── pytest.ini                # testpaths y pythonpath = . src
├── src/
│   ├── __init__.py
│   ├── task.py               # modelo, enums, validaciones, transiciones, vencimiento
│   ├── task_repository.py    # contrato Database, TaskFilter y TaskRepository
│   ├── task_service.py       # reglas de negocio y orquestación
│   └── notification_service.py  # email/SMS sobre un cliente HTTP inyectado
├── tests/
│   ├── conftest.py           # FakeClock, FakeDatabase y fixtures con mocks
│   ├── test_task_unit.py
│   ├── test_task_service_integration.py
│   ├── test_mocking.py
│   └── test_coverage_edge_cases.py
└── reports/
    ├── coverage-analysis.md  # Parte 3
    ├── analysis-report.md    # Parte 5
    ├── reflection.md
    └── screenshots/
```

## Features Implemented

- ✅ Modelo `Task` con validación de título (3-100), descripción (≤500), prioridad y fecha futura.
- ✅ Ciclo de vida solo hacia adelante `TODO → IN_PROGRESS → DONE`, con `ARCHIVED` alcanzable desde cualquier estado y terminal.
- ✅ Detección de tareas vencidas y comparación y orden de prioridades (`URGENT > HIGH > MEDIUM > LOW`).
- ✅ Repositorio CRUD con búsqueda combinable por estado, prioridad, rango de fechas y título parcial.
- ✅ Errores de infraestructura traducidos a errores de dominio (`RepositoryError`, `NotificationError`).
- ✅ Notificaciones best-effort: si fallan, se registra un warning y la operación sigue.
- ✅ Los tres tipos de doble: mocks verificados, stubs con `return_value`/`side_effect` y fakes (`FakeClock`, `FakeDatabase`).

## Design Decisions

La especificación deja abiertos algunos casos. Estas son las decisiones que tomé y que las pruebas verifican:

- **Tiempo inyectable:** todo el modelo lee la hora con `current_time()`, y las pruebas congelan y adelantan el reloj.
- **Fechas:** la fecha límite debe ser estrictamente futura; una tarea vence cuando `now > due_date`. Las tareas `DONE` o `ARCHIVED` nunca están vencidas.
- **Títulos únicos** sin distinguir mayúsculas ni espacios al inicio o al final. Una tarea puede conservar su propio título al editarse.
- **Descripción de más de 500 caracteres:** se rechaza en lugar de truncarse en silencio.
- **Borrado:** `delete_task` archiva (soft delete). `purge_task` borra definitivamente, pero solo tareas ya archivadas.
- **Notificaciones:** siempre por email. Las tareas `URGENT` también por SMS si hay teléfono configurado. Solo se toleran `NotificationError`; un error de configuración, como un correo inválido, sí se propaga.

## Author

Gilberto Anaya Mercado - Software Testing Fall 2026
