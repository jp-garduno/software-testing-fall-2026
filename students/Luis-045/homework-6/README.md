# Homework 6: Library Management System

- **Alumno:** Luis-045
- **Módulo:** 6 — Test Driven Development
- **Rama:** `feat/Luis-045/homework-6`

Implementación en Python del núcleo de libros, miembros y biblioteca. Incluye las tres funciones avanzadas seleccionadas: multas por retraso, búsquedas con filtros e historial de préstamos.

Toda la entrega se encuentra en esta carpeta, hermana de `homework-5`.


## Preparación en PowerShell

Requiere Python 3.11 o superior. La ruta del ejemplo corresponde al Python 3.13.9 utilizado en este equipo; ajústala si tu instalación está en otra ubicación. Los comandos usan directamente el entorno, sin requerir activación.

```powershell
Set-Location "C:\Users\luisf\OneDrive\Documentos\pruebas\software-testing-fall-2026\students\Luis-045\homework-6"
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Dependencias de pruebas: pytest, pytest-cov y coverage. Black, isort y Pylint permiten repetir las comprobaciones de calidad.


## Pruebas y cobertura

Desde la carpeta de esta entrega:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:coverage --cov-report=json:coverage/coverage.json
Start-Process .\coverage\index.html
```

[Reporte HTML incluido](coverage/index.html). [Datos de cobertura](coverage/coverage.json). La configuración local mide únicamente `src/` y activa ramas; no incluye tests ni el entorno virtual en el porcentaje.


## Comprobaciones de calidad

Ejecutar desde la misma carpeta:

```powershell
.\.venv\Scripts\python.exe -m black --check src tests
.\.venv\Scripts\python.exe -X utf8 -m isort --check-only --profile black src tests
.\.venv\Scripts\python.exe -m pylint --rcfile=../../../.github/grading/pylintrc src tests
```

El modo UTF-8 evita problemas de codificación en Windows con la prueba de ISBN que contiene dígitos Unicode. Pylint utiliza las reglas existentes de la clase.


## API y responsabilidades

| Componente | Operaciones |
| --- | --- |
| `Book` | `is_available()`, `borrow()`, `return_copy()` |
| `Member` | `can_borrow()`, `add_borrowed_book(isbn)`, `return_book(isbn)` |
| `Library` | `add_book(book)`, `register_member(member)`, `borrow_book(member_id, isbn)`, `return_book(member_id, isbn)` |
| Búsquedas básicas | `search_by_title(title)`, `search_by_author(author)`, `get_available_books()` |
| Multas | `get_due_date(member_id, isbn)`, `calculate_late_fees(member_id)` |
| Filtros | `search_with_filters(genre=None, publication_year=None, min_rating=None, sort_by="title")`, con argumentos por nombre |
| Historial | `get_member_history(member_id)`, `most_borrowed_book()` |

`Loan` es un registro inmutable con miembro, ISBN, fecha de préstamo, fecha de devolución y vencimiento calculado. El reporte de historial devuelve una tupla de estos registros.
