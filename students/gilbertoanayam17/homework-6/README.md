# Homework 6: TDD Feature Development - Library Management System

## Description

Sistema de gestión de biblioteca construido con Test Driven Development estricto: cada comportamiento empezó como una prueba que fallaba (RED), se implementó con el mínimo código para pasarla (GREEN) y después se limpió con todas las pruebas en verde (REFACTOR). El historial de commits de la rama `feat/gilbertoanayam17/homework-6` muestra cada uno de esos pasos con las etiquetas `RED:`, `GREEN:` y `REFACTOR:`.

## Features

**Core (Part 1)**

- `Book`: ISBN (10 o 13 dígitos), título obligatorio, autor, `total_copies` y `available_copies`; `is_available()`, `borrow()` y `return_copy()`.
- `Member`: id, nombre, libros prestados y límite de préstamo (3 por defecto); `can_borrow()`, `add_borrowed_book()` y `return_book()`.
- `Library`: catálogo y miembros; `add_book`, `register_member`, `borrow_book`, `return_book`, `search_by_title`, `search_by_author` y `get_available_books`. Un préstamo se valida por completo antes de modificar nada.

**Advanced (Part 3)**

1. **Late fees**: el préstamo vence 14 días después; se cobra por cada día de retraso. La multa queda registrada al devolver el libro y deja de crecer.
2. **Member categories**: Student (3 libros, $1.00/día), Faculty (5 libros, $0.50/día) y Public (2 libros, $1.50/día).
3. **Book reservations**: fila FIFO por libro para los que no tienen copias; al devolverse una copia se avisa al primero de la fila y la copia se le aparta.

Las reglas de negocio lanzan errores propios que heredan de `LibraryError` (`src/errors.py`).

## Prerequisites

- Python 3.11+ (probado con 3.14)
- pytest y pytest-cov (en `requirements.txt`)

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v
```

En Windows con varias versiones de Python instaladas: `py -3.14 -m pytest -v`. `pytest.ini` agrega la carpeta del proyecto al path, así que las pruebas importan desde `src` sin configuración extra.

La suite completa corre en menos de un segundo: el tiempo se controla con un reloj inyectado (`Library(clock=...)`) y los avisos de reservas con un notificador inyectado; en las pruebas ambos son `unittest.mock.Mock`.

## Coverage

```bash
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:coverage
```

El reporte HTML queda en `coverage/index.html` y está incluido en el repositorio sin su archivo `.js` (el autograder pasa ESLint por todo JavaScript de la entrega), así que la tabla no se puede reordenar, pero el contenido es el mismo. Resultado: 100% de sentencias y 100% de ramas.

## Project Structure

```
homework-6/
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── src/
│   ├── book.py          # Book: datos, validación y copias
│   ├── member.py        # Member y MemberCategory
│   ├── library.py       # Library: catálogo, préstamos, multas y reservas
│   ├── loan.py          # Loan: fecha de vencimiento y multa
│   └── errors.py        # LibraryError y sus subclases
├── tests/
│   ├── test_book.py
│   ├── test_member.py
│   ├── test_library.py
│   ├── test_loan.py
│   ├── test_late_fees.py
│   ├── test_member_categories.py
│   └── test_reservations.py
├── docs/
│   ├── tdd-process.md   # Part 2: cinco ciclos Red-Green-Refactor documentados
│   └── reflection.md    # Part 5: reflexión sobre TDD
└── coverage/            # Reporte HTML de cobertura
```

## TDD Workflow

Cada commit es un paso del ciclo:

| Etiqueta    | Qué contiene                                                              | Estado de la suite |
| ----------- | ------------------------------------------------------------------------- | ------------------ |
| `RED:`      | Una sola prueba nueva (o un caso parametrizado) que describe lo que falta | Falla              |
| `GREEN:`    | El código mínimo para que esa prueba pase                                 | Pasa               |
| `REFACTOR:` | Una mejora de diseño sin cambiar el comportamiento                        | Pasa               |

Para revisar el historial: `git log --oneline main..feat/gilbertoanayam17/homework-6`.

## Documentation

- [docs/tdd-process.md](docs/tdd-process.md): cinco ciclos completos con la prueba, el fallo, el código y la refactorización.
- [docs/reflection.md](docs/reflection.md): reflexión sobre el diseño guiado por pruebas.
