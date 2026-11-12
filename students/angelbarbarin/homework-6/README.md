# Homework 6: Library Management System (TDD)

**Alumno**: Angel Isaac Barbarín (`angelbarbarin`)
**Lenguaje**: Python 3.10+ con pytest

Sistema de administración de una librería construido con **Test Driven Development estricto**. Cada comportamiento se escribió primero como un test que falla (`RED`), después con el código mínimo para pasarlo (`GREEN`) y al final con una mejora de diseño sin cambiar el comportamiento (`REFACTOR`). El historial de commits de la rama muestra los 98 pasos de ese ciclo.

## Features

**Core (Part 1)**

- `Book`: ISBN (10 o 13 dígitos, acepta guiones), título obligatorio, copias totales y disponibles, `is_available()`, `borrow()` y `return_copy()`
- `Member`: id, nombre, libros prestados, límite de préstamos (3 por defecto), `can_borrow()`, `add_borrowed_book()` y `return_book()`
- `Library`: `add_book`, `register_member`, `borrow_book`, `return_book`, `search_by_title`, `search_by_author` y `get_available_books`

**Advanced (Part 3)**: 3 funcionalidades

1. **Member Categories**: STUDENT, FACULTY y PUBLIC, con límites de 3, 5 y 2 libros y tarifas de $1.00, $0.50 y $1.50 por día
2. **Late Fee Calculation**: el préstamo vence a los 14 días; la multa es la tarifa de la categoría por cada día de retraso; `total_fees_for_member` suma los préstamos activos vencidos y las multas ya cobradas
3. **Book Reservation System**: cola FIFO por libro; solo se reservan libros sin copias; al devolver una copia se notifica al primero de la cola a través de un notificador inyectado

## Project Structure

```
homework-6/
├── README.md
├── requirements.txt
├── pytest.ini
├── .coveragerc
├── .gitignore
├── src/
│   ├── book.py
│   ├── member.py
│   ├── library.py
│   ├── loan.py
│   ├── reservation.py
│   └── exceptions.py
├── tests/
│   ├── conftest.py          # FakeClock y fixture compartido de Library
│   ├── test_book.py
│   ├── test_member.py
│   ├── test_library.py
│   ├── test_late_fees.py
│   └── test_reservations.py
├── docs/
│   ├── tdd-process.md       # Part 2: 5 ciclos documentados
│   └── reflection.md        # Part 5: reflexión
└── coverage/                # Reporte HTML de cobertura
```

## Setup

```bash
cd students/angelbarbarin/homework-6
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

## Running the Tests

```bash
pytest
```

Con cobertura de statements y branches, y el reporte HTML en `coverage/`:

```bash
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:coverage
```

Después abre `coverage/index.html` en el navegador.

## Results

| Métrica            | Resultado | Requisito |
| ------------------ | --------- | --------- |
| Tests              | 49        | ≥ 35      |
| Statement coverage | 100%      | > 90%     |
| Branch coverage    | 100%      | > 85%     |
| Tiempo de la suite | ~0.2 s    | < 2 s     |
| Commits TDD        | 98        | ≥ 30      |

## Design Notes

- **Reloj inyectable**: `Library(clock=...)` recibe una función que regresa la fecha de hoy. Los tests usan `FakeClock.advance(days)`, así que no dependen de la fecha real ni esperan.
- **Notificador inyectable**: `Library(notifier=...)`. Los tests usan `unittest.mock.Mock`; si no se pasa ninguno se usa un `NullNotifier`.
- **Dinero con `Decimal`**: evita errores de redondeo de `float` en las multas.
- **Validar antes de modificar**: `borrow_book` revisa todas las reglas antes de quitar una copia, para que una operación fallida nunca deje el sistema inconsistente.

## Commit Convention

```
RED: should <comportamiento esperado>
GREEN: <implementación mínima>
REFACTOR: <mejora sin cambiar comportamiento>
```

Para ver el historial completo:

```bash
git log --oneline --reverse main..HEAD
```
