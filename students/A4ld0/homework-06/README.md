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
print(library.member_history("m1"))
print(library.search_books(genre="Sci-Fi", publication_year=1965, rating=4.5))
print(library.most_borrowed_book().title)  # Dune
```

## Contrato de la biblioteca

- Book recibe ISBN de 10 o 13 dígitos ASCII, título, autor y total_copies=1.
  No calcula el dígito de control del ISBN: el enunciado exige longitud y dígitos.
  Rechaza títulos vacíos y cantidades negativas, booleanas o no enteras.
- Member recibe member_id, name y max_borrow_limit=3. Cada miembro tiene su lista
  independiente de ISBN prestados. El límite es un entero no negativo.
- add_book y register_member rechazan identificadores duplicados para proteger
  los registros existentes. Los errores de operaciones se expresan con ValueError.
- borrow_book y return_book sincronizan ejemplares, miembros e historial.
  Un miembro puede tomar varias copias del mismo ISBN, dentro de su límite.
  La devolución cierra el préstamo activo más antiguo de ese miembro e ISBN.
- Las operaciones deben realizarse mediante Library para mantener coherencia
  entre las tres estructuras. No hay persistencia ni interfaz de usuario.

## Funciones avanzadas

- Multas: vencimiento 14 días después del préstamo. El día del vencimiento no
  genera multa; después se cobra $1 por día y ejemplar. Una devolución congela
  el cargo y el total conserva multas de préstamos devueltos. No se implementan pagos.
- Las fechas opcionales son datetime.date; al omitirlas se usa la fecha local actual.
  No se aceptan cadenas ni datetime.datetime. Una devolución anterior al préstamo
  se rechaza antes de modificar estado. as_of permite consultar multas a una fecha:
  no incluye días posteriores a esa fecha, aunque el libro se devuelva más tarde.
- search_books combina género, año y calificación con AND y coincidencia exacta.
  None omite un filtro; rating=0 sí filtra. Los metadatos son opcionales: género
  de texto, año entero y calificación numérica, sin imponer una escala de puntuación.
- El orden ascendente predeterminado es por título; sort_by admite title, author,
  publication_year y rating. Los textos se ordenan sin distinguir mayúsculas;
  valores ausentes quedan al final y los empates se resuelven por ISBN ascendente.
- search_by_title y search_by_author buscan subcadenas sin distinguir mayúsculas.
- member_history devuelve un reporte estructurado como lista de diccionarios:
  member_id, isbn, borrowed_on, due_on y returned_on (None si sigue activo).
  Es una instantánea independiente; modificarla no altera los préstamos.
- most_borrowed_book incluye todos los préstamos, incluso devueltos, devuelve
  un Book o None si no hay préstamos y resuelve empates por ISBN ascendente.

## Verificación y entregables

La suite contiene 97 casos: 49 básicos, 28 adicionales de funciones avanzadas
y 20 de integración/regresión. No hay pruebas omitidas ni dependencias externas
durante su ejecución. Los casos de fechas y multas usan fechas explícitas.

`tools/check_quality.py` verifica por separado sentencias >90 %, ramas >85 % y
duración del proceso completo de pruebas <2 segundos. El tiempo depende del equipo;
los resultados medidos están en [quality.json](docs/evidence/quality.json).
El informe HTML está en [coverage/index.html](coverage/index.html).

- [Proceso TDD: cinco ciclos completos](docs/tdd-process.md).
- [Reflexión técnica, 500–700 palabras](docs/reflection.md).
- [Evidencias y resultados](docs/verification.md).
- [Registro de ejecuciones reales](docs/evidence/tdd-runs.jsonl).

El historial contiene commits RED, GREEN y REFACTOR creados durante el desarrollo.
Los casos de integración añadidos después son regresiones adicionales: no se
presentan como fases RED. Se conserva el repositorio existente, según lo acordado.
