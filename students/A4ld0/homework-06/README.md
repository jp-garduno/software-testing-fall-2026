# Tarea 6: sistema de biblioteca con TDD

Entrega de A4ld0 en el repositorio del curso. Implementación en Python, en memoria,
con Book, Member y Library. Funciones avanzadas: multas, filtros e historial.

## Instalación y pruebas

Requiere Python 3.12 o posterior. Desde esta carpeta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools/check_quality.py
```

Si `python` abre la tienda de Windows, usa la ruta de tu intérprete instalado.
En macOS/Linux, sustituye `.venv\Scripts\python.exe` por `.venv/bin/python`.
El entorno virtual no se incluye en Git; las dependencias están fijadas.

## Ejemplo

```python
from datetime import date
from src.book import Book
from src.member import Member
from src.library import Library

library = Library()
library.add_book(Book("1234567890", "Dune", "Frank Herbert", 2,
                      genre="Sci-Fi", publication_year=1965, rating=4.5))
library.register_member(Member("m1", "Ana"))
library.borrow_book("m1", "1234567890", borrowed_on=date(2026, 10, 1))
print(library.calculate_late_fees("m1", as_of=date(2026, 10, 18)))  # 3
library.return_book("m1", "1234567890", returned_on=date(2026, 10, 17))
print(library.calculate_late_fees("m1", as_of=date(2026, 11, 1)))  # 2
