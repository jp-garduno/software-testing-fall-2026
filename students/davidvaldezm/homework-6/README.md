# Sistema de administración de biblioteca con TDD

Entrega de **David Valdez (`davidvaldezm`)**, Homework 6, módulo Test Driven Development.

Implementación en Python de catálogo, socios, préstamos, devoluciones y búsquedas. Incluye tres funciones avanzadas: multas, historial de préstamos y categorías de socios. Los datos se mantienen en memoria.

## Instalación y pruebas

Requiere Python 3.11 o superior. Desde esta carpeta:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m pytest --cov=src --cov-branch --cov-fail-under=90 --cov-report=term-missing --cov-report=html:coverage --cov-report=json:coverage.json
python -m black --check --workers 1 src tests
python -m isort --check-only --profile=black src tests
python -m pylint src tests
```

El reporte HTML incluido se abre en [coverage/index.html](coverage/index.html). Los resultados medidos están en [docs/verification.md](docs/verification.md). El workflow `Library TDD - David Valdez Homework 6` repite pruebas, formato y análisis estático en Python 3.11 y 3.12 y conserva el reporte como artefacto.

## Ejemplo de uso

```python
from datetime import date

from src.book import Book
from src.library import Library
from src.member import Member

clock = [date(2026, 1, 1)]
library = Library(today=lambda: clock[0])
library.add_book(Book("9780307476463", "Pedro Paramo", "Juan Rulfo", copies=2))
library.register_member(Member("M1", "Ana", category="student"))
loan = library.borrow_book("M1", "9780307476463")
assert loan.due_date == date(2026, 1, 15)
clock[0] = date(2026, 1, 18)
assert str(library.calculate_total_fees("M1")) == "3"
library.return_book("M1", "9780307476463")
assert library.get_member_history("M1")[0].returned_on == clock[0]
```

## Contratos y reglas

- `Book(isbn, title, author, copies=1)`: ISBN de 10 o 13 dígitos ASCII; título no vacío; copias enteras no negativas. Se valida el formato del ISBN, sin calcular su dígito verificador. `borrow()` y `return_copy()` protegen los límites del inventario.
- `Member(member_id, name, max_borrow_limit=None, category="student")`: identidad y nombre obligatorios; la lista `borrowed_books` contiene ISBN. No permite dos préstamos activos del mismo ISBN para un socio. Un límite explícito positivo sustituye el de su categoría.
- `Library`: registra libros y socios sin sobrescribir identificadores. `borrow_book(member_id, isbn)` devuelve un `Loan` inmutable. Las operaciones rechazadas conservan el inventario, los préstamos y el historial.
- `search_by_title()` y `search_by_author()`: búsqueda parcial sin distinguir mayúsculas; ignoran espacios externos. Una consulta vacía devuelve todo el catálogo; sin coincidencias devuelve `[]`. `get_available_books()` filtra por existencias.
- Todos los préstamos vencen 14 días naturales después del préstamo. El día de vencimiento no genera multa. `calculate_total_fees(member_id)` suma multas acumuladas de préstamos activos y devueltos usando `Decimal`. Las multas dejan de crecer al devolver el libro. Esta API no registra pagos.
- `get_member_history(member_id)` devuelve una tupla cronológica de registros inmutables, con fechas de préstamo, vencimiento y devolución. Un nuevo préstamo del mismo libro crea otro registro. No se permiten devoluciones anteriores al préstamo.
- `most_borrowed_book()` cuenta todos los eventos de préstamo, incluso préstamos ya devueltos. En empate gana el primer libro prestado; devuelve `None` sin historial.
- Identificadores desconocidos y operaciones inválidas generan `ValueError`. Para conservar consistencia, los préstamos se realizan mediante `Library`; sus modelos expuestos no deben modificarse por fuera de esa API. No hay persistencia ni control de concurrencia.

| Categoría | Límite predeterminado | Multa por día vencido |
| --- | ---: | ---: |
| `student` | 3 | $1.00 |
| `faculty` | 5 | $0.50 |
| `public` | 2 | $1.50 |

Las tasas diferenciadas son una decisión documentada porque el enunciado solicita tasas distintas sin fijar sus importes.

## Evidencia TDD

El historial conserva los commits `RED`, `GREEN` y `REFACTOR` originales. Cada nueva conducta se probó antes de implementarla. Las pruebas de caracterización posteriores se identifican como `REFACTOR`: verifican contratos ya implementados, sin presentar fallos ficticios.

```bash
git log --reverse --oneline origin/main..HEAD
git show <commit-RED>
git show <commit-GREEN>
```

- [Cinco ciclos completos](docs/tdd-process.md), con hashes, pruebas, fallos y decisiones de refactorización.
- [Registro de ejecuciones](docs/tdd-evidence.json), con la salida real de pytest en las fases registradas.
- [Reflexión](docs/reflection.md), de 500 a 700 palabras.

Los commits de conducta son pequeños; la documentación, el formateo y el reporte generado necesitan cambios mayores. Asistencia utilizada: Codex para implementación, ejecución de pruebas y documentación.
