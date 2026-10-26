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


## Reglas y decisiones

- El ISBN es una cadena de 10 o 13 dígitos ASCII; no se exige checksum porque el enunciado solo solicita longitud y dígitos.
- El título debe ser una cadena con contenido. Las copias son enteros no negativos; no se aceptan booleanos.
- Cada miembro tiene una lista independiente y un límite predeterminado de tres libros. No puede tomar dos préstamos simultáneos del mismo ISBN.
- Los ISBN e identificadores de miembros duplicados se rechazan con `ValueError`. Un identificador o ISBN desconocido en las operaciones de biblioteca produce `KeyError`.
- Un préstamo rechazado por disponibilidad o límite no cambia inventario ni libros del miembro. Una devolución debe corresponder a un préstamo activo.
- El vencimiento ocurre 14 días después del préstamo. La multa es cero hasta esa fecha y aumenta $1 por cada día posterior.
- Al devolver un libro se conserva el importe acumulado hasta la devolución. Los totales incluyen multas de préstamos activos y devueltos; no se implementan pagos.
- `Library(today=...)` permite inyectar un reloj. En producción usa `date.today`; las pruebas controlan las fechas sin esperas ni servicios externos.


## Filtros e historial

Los metadatos opcionales se suministran al crear el libro, por ejemplo:

```python
book = Book("1234567890", "Dune", "Frank Herbert",
            genre="Science Fiction", publication_year=1965, rating=4.8)
```

El género se compara completo sin distinguir mayúsculas; el año es exacto y la calificación mínima es inclusiva. Los filtros se combinan con AND. Los libros sin el metadato requerido no satisfacen ese filtro.

La ordenación es ascendente por título de forma predeterminada. Se admiten `title`, `author`, `isbn`, `publication_year` y `rating`; los empates se resuelven por ISBN. Al ordenar datos numéricos ausentes se usa cero.

Las búsquedas básicas admiten subcadenas sin distinguir mayúsculas. El historial conserva el orden de los préstamos, incluyendo repeticiones después de una devolución. El libro más prestado cuenta cada préstamo exitoso; en empate gana el primero prestado y, sin movimientos, devuelve `None`.


## Resultados verificados

Entorno: Windows, Python 3.13.9, pytest 9.1.1, pytest-cov 7.1.0 y coverage 7.17.0.

| Comprobación | Resultado |
| --- | --- |
| Suite completa | 72 pruebas aprobadas; ninguna omitida |
| Tiempo sin cobertura | 0.07 segundos en una ejecución final |
| Tiempo con cobertura HTML y JSON | 0.37 segundos |
| Sentencias | 127 de 127: 100% |
| Ramas | 32 de 32: 100% |
| Black / isort | Sin cambios pendientes |
| Pylint con reglas de la clase | 10.00/10 |

Los tiempos varían por equipo. Los porcentajes provienen de los contadores separados de sentencias y ramas del JSON, además del reporte HTML.
