# TDD Process Documentation

Este documento describe cinco ciclos Red-Green-Refactor completos del Library Management System. Cada fragmento de código y cada fallo corresponden a los commits `RED:`, `GREEN:` y `REFACTOR:` de la rama, en el orden en que se hicieron.

## Overview

| Métrica               | Valor                                                           |
| --------------------- | --------------------------------------------------------------- |
| Commits del ciclo TDD | 103 (47 RED, 47 GREEN, 9 REFACTOR)                              |
| Pruebas               | 56 (47 funciones; las parametrizadas cuentan un caso por valor) |
| Cobertura             | 100% sentencias, 100% ramas                                     |
| Tiempo de la suite    | menos de 1 segundo                                              |

Orden de construcción: `Book` → `Member` → `Library` → late fees (`Loan` y reloj inyectado) → member categories → reservations. Cada parte arrancó con la prueba más simple posible y cada nueva regla empezó como una prueba que fallaba.

---

## Cycle #1: Book Availability Check

Este ciclo usa **Fake It** y **triangulación**: primero una prueba que se satisface con un valor fijo y luego otra que obliga a escribir la regla real.

### RED Phase

Antes de este ciclo, la prueba `test_should_be_available_when_copies_exist` se había pasado con `return True` (commit `GREEN: fake is_available by returning True`). La siguiente prueba rompe ese valor falso:

**Test Written**:

```python
def test_should_not_be_available_when_no_copies_exist():
    book = Book("1234567890", "Clean Code", "Robert C. Martin", copies=0)

    assert not book.is_available()
```

**Test Result**: FAIL - el método existe, pero siempre responde `True`.

```text
FAILED tests/test_book.py::test_should_not_be_available_when_no_copies_exist
    assert not True
1 failed, 3 passed
```

### GREEN Phase

**Code Written**:

```python
    def is_available(self):
        """Return True while at least one copy is on the shelf."""
        return self.available_copies > 0
```

**Test Result**: PASS - `4 passed`

### REFACTOR Phase

**Improvements Made**: las cuatro pruebas repetían `Book("1234567890", "Clean Code", "Robert C. Martin", copies=...)`. Se extrajo un helper para que cada prueba muestre solo el dato que le importa, el número de copias:

```python
ISBN = "1234567890"


def make_book(copies=1):
    """Arrange a valid book; only the number of copies changes between tests."""
    return Book(ISBN, "Clean Code", "Robert C. Martin", copies=copies)
```

**Design Decision**: `is_available()` devuelve un booleano en lugar del número de copias: quien pregunta "¿lo puedo prestar?" no necesita saber cuántas quedan, y `borrow()` lo reutiliza después para su propia validación. Que la refactorización se hiciera sobre el código de prueba también es intencional: las pruebas son código y se mantienen igual que el de producción.

---

## Cycle #2: Book Validation (ISBN and Title)

La validación se construyó en tres mini-ciclos (longitud del ISBN, solo dígitos, título obligatorio) y se refactorizó al final, cuando ya había suficiente código para ver la duplicación.

### RED Phase

**Test Written**:

```python
@pytest.mark.parametrize("title", ["", "   ", None])
def test_should_reject_missing_title(title):
    with pytest.raises(ValueError, match="Title"):
        Book(ISBN, title, "Robert C. Martin")
```

**Test Result**: FAIL - los tres casos crean el libro sin protestar.

```text
FAILED tests/test_book.py::test_should_reject_missing_title[]
    Failed: DID NOT RAISE ValueError
FAILED tests/test_book.py::test_should_reject_missing_title[   ]
    Failed: DID NOT RAISE ValueError
FAILED tests/test_book.py::test_should_reject_missing_title[None]
    Failed: DID NOT RAISE ValueError
3 failed, 13 passed
```

### GREEN Phase

**Code Written**: dos líneas en `__init__`, justo después de la validación del ISBN que ya existía:

```python
    def __init__(self, isbn, title, author, copies=1):
        if len(isbn) not in (10, 13) or not isbn.isdigit():
            raise ValueError("ISBN must have 10 or 13 digits")
        if not title or not title.strip():
            raise ValueError("Title is required")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies
```

**Test Result**: PASS - `16 passed`

### REFACTOR Phase

**Improvements Made**: `__init__` mezclaba validación con asignación y el `(10, 13)` era un número mágico. Cada validación pasó a su propio método y la constante recibió nombre:

```python
"""Book: a title in the catalog and how many of its copies are on the shelf."""

from . import errors

VALID_ISBN_LENGTHS = (10, 13)


class Book:
    """A catalog entry whose copies can be lent out."""

    def __init__(self, isbn, title, author, copies=1):
        self._validate_isbn(isbn)
        self._validate_title(title)
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies

    @staticmethod
    def _validate_isbn(isbn):
        """Accept only an ISBN-10 or ISBN-13 written as plain digits."""
        if len(isbn) not in VALID_ISBN_LENGTHS or not isbn.isdigit():
            raise ValueError("ISBN must have 10 or 13 digits")

    @staticmethod
    def _validate_title(title):
        """Reject a missing or blank title."""
        if not title or not title.strip():
            raise ValueError("Title is required")
```

**Design Decision**: se distinguen dos tipos de error. Un argumento inválido (ISBN mal escrito, título vacío) es un `ValueError` estándar de Python; una regla de negocio rota (prestar un libro sin copias) es una subclase de `LibraryError` definida en `src/errors.py`. El caso `None` del título se agregó en la prueba parametrizada desde el inicio, por eso el `GREEN` usa `not title or not title.strip()` y no solo `strip()`.

---

## Cycle #3: Borrowing Is All-or-Nothing

Este es el ciclo en el que una prueba encontró un bug real de diseño.

### RED Phase

Hasta aquí `borrow_book` tomaba primero una copia del estante y después se la asignaba al miembro. ¿Qué pasa si el miembro ya está en su límite?

**Test Written**:

```python
def test_should_keep_copy_on_shelf_when_member_is_at_limit():
    library = make_library(copies=2, limit=1)
    library.borrow_book("M1", ISBN)

    with pytest.raises(errors.BorrowLimitExceededError):
        library.borrow_book("M1", ISBN)

    assert library.get_book(ISBN).available_copies == 1
```

**Test Result**: FAIL - el préstamo sí se rechaza, pero la copia ya se había tomado: quedan 0 copias en lugar de 1.

```text
FAILED tests/test_library.py::test_should_keep_copy_on_shelf_when_member_is_at_limit
    AssertionError: assert 0 == 1
1 failed, 30 passed
```

### GREEN Phase

**Code Written**: revisar el límite del miembro **antes** de tocar el libro.

```python
    def borrow_book(self, member_id, isbn):
        """Lend one copy of a book to a member."""
        member = self.get_member(member_id)
        if not member.can_borrow():
            raise errors.BorrowLimitExceededError(f"{member.name} already holds {member.max_borrow_limit} books")
        self.get_book(isbn).borrow()
        member.add_borrowed_book(isbn)
```

**Test Result**: PASS - `31 passed`

### REFACTOR Phase

**Improvements Made**: la regla del límite (y su mensaje) quedó copiada en `Library` y en `Member.add_borrowed_book`. Se movió a un solo método de `Member`, que ahora usan ambos:

```python
    def ensure_can_borrow(self):
        """Raise BorrowLimitExceededError if the member already holds as many books as allowed."""
        if not self.can_borrow():
            raise errors.BorrowLimitExceededError(f"{self.name} already holds {self.max_borrow_limit} books")
```

```python
    def borrow_book(self, member_id, isbn):
        """Lend one copy of a book to a member."""
        member = self.get_member(member_id)
        member.ensure_can_borrow()
        self.get_book(isbn).borrow()
        member.add_borrowed_book(isbn)
```

**Design Decision**: toda operación que cambia estado valida **todas** sus precondiciones primero y modifica después. El mismo principio se aplicó a `return_book` (primero el miembro, que lanza `InvalidReturnError` si no tenía el libro, y luego el libro). La regla del límite pertenece a `Member` porque es el dueño del dato; `Library` solo coordina.

---

## Cycle #4: Overdue Days by Triangulation

### RED Phase

La primera prueba de `days_overdue` (una fecha **antes** del vencimiento debe dar 0) se pasó con `return 0`. La segunda prueba agrega ejemplos con otra respuesta y además cubre la frontera:

**Test Written**:

```python
@pytest.mark.parametrize(
    "on_date, expected_days",
    [(date(2026, 1, 15), 0), (date(2026, 1, 16), 1), (date(2026, 1, 18), 3)],
    ids=["on-due-date", "one-day-late", "three-days-late"],
)
def test_should_count_days_past_due_date_as_overdue(on_date, expected_days):
    loan = Loan("M1", "1234567890", BORROWED_ON)

    assert loan.days_overdue(on_date) == expected_days
```

**Test Result**: FAIL - el caso del día del vencimiento pasa por casualidad (0 es correcto ahí); los otros dos rompen el valor falso.

```text
FAILED tests/test_loan.py::test_should_count_days_past_due_date_as_overdue[one-day-late]
    assert 0 == 1
FAILED tests/test_loan.py::test_should_count_days_past_due_date_as_overdue[three-days-late]
    assert 0 == 3
2 failed, 39 passed
```

### GREEN Phase

**Code Written**:

```python
    def days_overdue(self, on_date):
        """Return how many days past the due date `on_date` falls."""
        return max(0, (on_date - self.due_date).days)
```

**Test Result**: PASS - `41 passed`

Sin el `max(0, ...)` la prueba anterior (5 días antes del vencimiento) daría `-5`. Las dos pruebas juntas fijan la regla completa: nada antes del vencimiento, nada el mismo día, un día por cada día después.

### REFACTOR Phase

**Improvements Made**: después de implementar `late_fee` (siguiente mini-ciclo), `14` y `1.0` eran números mágicos con significado de negocio. Se les dio nombre:

```python
"""Loan: one copy lent to one member, when it is due and what lateness costs."""

from datetime import timedelta

LOAN_PERIOD = timedelta(days=14)
DAILY_LATE_FEE = 1.0


class Loan:
    """A copy of a book lent to a member on a given date, due LOAN_PERIOD later."""

    def __init__(self, member_id, isbn, borrowed_on):
        self.member_id = member_id
        self.isbn = isbn
        self.due_date = borrowed_on + LOAN_PERIOD
```

**Design Decision**: el préstamo es su propia clase (`Loan`) en lugar de fechas sueltas dentro de `Library`: así las reglas de tiempo se prueban de forma aislada, sin catálogo ni miembros. Las fechas se pasan como parámetro (`on_date`) en vez de leer `date.today()`, lo que hace que estas pruebas sean deterministas. En `Library` la misma idea se convirtió en un **reloj inyectado** (`Library(clock=date.today)`), que en las pruebas es un `Mock`.

---

## Cycle #5: Notify the Next Member in Line (Mock)

### RED Phase

**Test Written**:

```python
def test_should_notify_first_member_in_line_when_copy_is_returned():
    notifier = Mock()
    library = make_library(notifier)
    library.reserve_book("M2", ISBN)
    library.reserve_book("M3", ISBN)

    library.return_book("M1", ISBN)

    notifier.notify.assert_called_once_with("M2", ISBN)
```

**Test Result**: FAIL - fallan las tres pruebas del archivo, porque el helper `make_library` ahora construye `Library(notifier=...)` y `Library` todavía no acepta ese parámetro.

```text
FAILED tests/test_reservations.py::test_should_queue_member_who_reserves_unavailable_book
    TypeError: Library.__init__() got an unexpected keyword argument 'notifier'
FAILED tests/test_reservations.py::test_should_reject_reservation_while_copies_are_available
    TypeError: Library.__init__() got an unexpected keyword argument 'notifier'
FAILED tests/test_reservations.py::test_should_notify_first_member_in_line_when_copy_is_returned
    TypeError: Library.__init__() got an unexpected keyword argument 'notifier'
3 failed, 51 passed
```

### GREEN Phase

**Code Written**: el constructor recibe el notificador y `return_book` avisa al primero de la fila:

```python
    def return_book(self, member_id, isbn):
        """Take back a member's copy of a book."""
        self.get_member(member_id).return_book(isbn)
        self.get_book(isbn).return_copy()
        loan = self._close_loan(member_id, isbn)
        self._fees_owed[member_id] = self._fees_owed.get(member_id, 0) + loan.late_fee(self._clock())
        waiting = self._reservations.get(isbn)
        if waiting and self._notifier:
            self._notifier.notify(waiting[0], isbn)
```

**Test Result**: PASS - `54 passed`

### REFACTOR Phase

**Improvements Made** (dos commits, después de los ciclos que apartan la copia y quitan la reserva):

1. `REFACTOR: use a deque for reservation queues`: una fila FIFO es exactamente `collections.deque`; `popleft()` es O(1) y el tipo comunica la intención.
2. `REFACTOR: extract first_in_line so borrow and return share the queue rule`: `borrow_book` y `return_book` repetían "mira la fila y toma el primero".

```python
    def _first_in_line(self, isbn):
        """Return the id of the member at the front of the book's queue, or None if nobody is waiting."""
        waiting = self._reservations.get(isbn)
        return waiting[0] if waiting else None
```

```python
    def return_book(self, member_id, isbn):
        """Take back a member's copy of a book."""
        self.get_member(member_id).return_book(isbn)
        self.get_book(isbn).return_copy()
        loan = self._close_loan(member_id, isbn)
        self._fees_owed[member_id] = self._fees_owed.get(member_id, 0) + loan.late_fee(self._clock())
        first_in_line = self._first_in_line(isbn)
        if first_in_line is not None and self._notifier is not None:
            self._notifier.notify(first_in_line, isbn)
```

**Design Decision**: `Library` no sabe cómo se avisa (correo, SMS, push); solo depende de un objeto con `notify(member_id, isbn)`. En las pruebas ese objeto es un `Mock`, y `assert_called_once_with("M2", ISBN)` verifica a la vez que se avisó una sola vez y que se respetó el orden FIFO (M2 reservó antes que M3). El notificador es opcional (`None` por defecto), por eso la condición revisa ambas cosas.

---

## Design Evolution

| Momento                 | Qué pidió la prueba                             | Cómo cambió el diseño                                                                |
| ----------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------ |
| `Book.return_copy`      | No aceptar devoluciones de más                  | Apareció `total_copies`, que antes no hacía falta                                    |
| Primer error de dominio | Prestar un libro sin copias                     | Módulo `src/errors.py` con `LibraryError` como base común                            |
| Límite en `Library`     | No perder la copia si el miembro está al límite | Validar todo antes de modificar; la regla pasó a `Member.ensure_can_borrow()`        |
| Búsquedas               | Título y autor                                  | Un solo `_search(field, text)` compartido                                            |
| Late fees               | Viajar en el tiempo en las pruebas              | Clase `Loan` y reloj inyectado en `Library`                                          |
| Multa tras devolver     | Que deje de crecer                              | Los préstamos se cierran y su multa se guarda como deuda                             |
| Categorías              | Límite y tarifa por tipo de miembro             | `MemberCategory` con atributos con nombre; la tarifa se fija en el `Loan` al prestar |
| Reservas                | Fila FIFO y aviso                               | Notificador inyectado (`Mock` en pruebas), `deque` y `_first_in_line`                |
