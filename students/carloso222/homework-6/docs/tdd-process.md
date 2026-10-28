# Proceso TDD: 5 ciclos Red-Green-Refactor

Cada ciclo muestra la prueba que escribí primero, el error real que dio pytest,
el código mínimo para pasarla y el refactor que vino después. Entre paréntesis
va el commit del historial donde se puede ver cada fase.

---

## Ciclo 1: Saber si un libro está disponible

### RED (`RED: should report whether a book is available`)

**Prueba escrita:**

```python
def test_book_is_not_available_when_it_has_zero_copies():
    book = Book("1234567890", "Test Book", "Author", total_copies=0)
    assert book.is_available() is False
```

**Resultado:** FALLA

```text
E       AttributeError: 'Book' object has no attribute 'is_available'
2 failed, 3 passed
```

Falló por la razón correcta: el método todavía no existía.

### GREEN (`GREEN: implement Book.is_available`)

**Código escrito:**

```python
def is_available(self):
    return self.available_copies > 0
```

**Resultado:** PASA (5 passed)

### REFACTOR

No hizo falta, el código era de una línea.

**Decisión de diseño:** `is_available()` regresa `True`/`False` en lugar de un
número. Quien pregunta "¿lo puedo prestar?" no tiene que comparar nada, y el
número sigue disponible en `available_copies`.

---

## Ciclo 2: Validar el ISBN

### RED (`RED: should validate isbn length and digits`)

**Prueba escrita** (una prueba parametrizada con 9, 11, 12 y 14 dígitos):

```python
@pytest.mark.parametrize("isbn", ["123456789", "12345678901", "123456789012", "12345678901234"])
def test_book_rejects_isbn_with_wrong_length(isbn):
    with pytest.raises(InvalidBookError, match="10 or 13"):
        Book(isbn, "Test Book", "Author")
```

**Resultado:** FALLA

```text
E   ModuleNotFoundError: No module named 'src.exceptions'
1 error during collection
```

Ni siquiera existía la excepción `InvalidBookError`, así que la prueba no pudo
cargarse.

### GREEN (`GREEN: validate isbn in Book constructor`)

**Código escrito:** creé `exceptions.py` y agregué las validaciones directo en el
constructor:

```python
if not isinstance(isbn, str) or not isbn.isdigit():
    raise InvalidBookError("ISBN must contain only digits")
if len(isbn) not in (10, 13):
    raise InvalidBookError("ISBN must be 10 or 13 digits")
```

**Resultado:** PASA (15 passed)

### REFACTOR (`REFACTOR: extract validation helpers and VALID_ISBN_LENGTHS`)

En el siguiente ciclo agregué validación de título y de copias, y el constructor
se llenó de `if`. Saqué cada regla a su propio método (`_validate_isbn`,
`_validate_title`, `_validate_copies`) y el número mágico `(10, 13)` a la
constante `VALID_ISBN_LENGTHS`. Las 20 pruebas siguieron en verde.

**Decisión de diseño:** reviso primero que sea texto con solo dígitos y después
la longitud. Así un valor como `None` o el número `1234567890` da un error claro
en lugar de tronar en `len()`. Tampoco quito guiones: la tarea dice "10 o 13
dígitos", entonces `"123-456-789"` se rechaza.

---

## Ciclo 3: Límite de préstamos del miembro

### RED (`RED: should record borrowed books up to the limit`)

**Prueba escrita:**

```python
def test_add_borrowed_book_raises_beyond_limit():
    member = Member("M1", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1111111111")
    with pytest.raises(BorrowLimitReachedError):
        member.add_borrowed_book("2222222222")
```

**Resultado:** FALLA

```text
E       AttributeError: 'Member' object has no attribute 'add_borrowed_book'.
        Did you mean: 'borrowed_books'?
3 failed, 33 passed
```

### GREEN (`GREEN: implement add_borrowed_book with limit check`)

**Código escrito:**

```python
def add_borrowed_book(self, isbn):
    if not self.can_borrow():
        raise BorrowLimitReachedError(
            f"{self.name} has reached the limit of {self.max_borrow_limit} books"
        )
    self.borrowed_books.append(isbn)
```

**Resultado:** PASA (36 passed)

### REFACTOR

No hubo en este ciclo. Más adelante, al agregar las categorías de miembro, el
límite dejó de ser un `3` fijo y pasó a venir de `MemberCategory`. Las pruebas de
este ciclo siguieron pasando sin cambios.

**Decisión de diseño:** la regla vive en `Member` para que el objeto nunca quede
en un estado inválido. Además, `Library.borrow_book` revisa el límite **antes**
de tocar el libro, para que un préstamo rechazado no le quite una copia al
estante. Eso lo protege la prueba `test_failed_borrow_over_limit_leaves_book_on_shelf`.

---

## Ciclo 4: Multas por retraso

### RED (`RED: should charge late fees for overdue books`)

**Prueba escrita:**

```python
def test_student_is_charged_one_dollar_per_overdue_day(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    clock.advance(14 + 5)
    loan = library.return_book("S1", CLEAN_CODE)
    assert loan.fee_charged == 5.00
```

**Resultado:** FALLA

```text
E       AssertionError: assert 0.0 == 5.0
E        +  where 0.0 = Loan(member_id='S1', isbn='9780132350884',
           borrowed_on=datetime.date(2026, 10, 1), returned_on=datetime.date(2026, 10, 20),
           fee_charged=0.0).fee_charged
10 failed, 80 passed
```

El mensaje ayuda: muestra que el libro se regresó 19 días después, así que las
fechas estaban bien y solo faltaba calcular la multa.

### GREEN (`GREEN: charge late fees by member category`)

**Código escrito** (dentro de `Library.return_book`):

```python
today = self._clock()
loan.returned_on = today
loan.fee_charged = loan.days_overdue(today) * member.daily_late_fee
```

y `calculate_late_fees()`, que suma las multas ya cobradas más las que se siguen
acumulando en libros que no se han regresado.

**Resultado:** PASA (90 passed)

### REFACTOR (`REFACTOR: reuse member history in calculate_late_fees`)

`calculate_late_fees()` recorría todos los préstamos y filtraba por miembro a
mano. Cuando después hice el historial (`get_member_history`), cambié el ciclo
para reutilizarlo y quité el filtro duplicado. Las 120 pruebas siguieron en verde.

**Decisión de diseño:** el tiempo se inyecta. `Library(clock=...)` recibe una
función que regresa la fecha de hoy. En las pruebas uso un `FakeClock` y hago
`clock.advance(19)` en lugar de esperar 19 días o parchar `datetime`. Por eso
todas las pruebas corren en menos de medio segundo.

---

## Ciclo 5: Reservas en cola (FIFO)

### RED (`RED: should notify and hold returned books for first in queue`)

**Prueba escrita:**

```python
def test_returned_reserved_book_is_held_for_first_in_queue(library):
    library.borrow_book("S1", REFACTORING)
    library.reserve_book("S2", REFACTORING)
    library.return_book("S1", REFACTORING)
    with pytest.raises(ReservationError, match="held for member S2"):
        library.borrow_book("F1", REFACTORING)
```

**Resultado:** FALLA

```text
FAILED test_first_member_in_queue_is_notified_when_book_returns
FAILED test_returned_reserved_book_is_held_for_first_in_queue
       Failed: DID NOT RAISE ReservationError
FAILED test_first_in_queue_can_borrow_and_leaves_the_queue
FAILED test_queue_is_served_in_fifo_order
4 failed, 8 passed
```

Ya se podía reservar, pero cualquiera podía llevarse el libro cuando regresaba,
aunque no estuviera en la cola. La cola no servía de nada.

### GREEN (`GREEN: notify and hold returned books for reservers`)

**Código escrito:**

```python
def _claim_reservation(self, member_id, isbn):
    queue = self._reservations.get(isbn)
    if not queue:
        return
    if queue[0] != member_id:
        raise ReservationError(f"Book {isbn} is held for member {queue[0]}")
    queue.pop(0)
```

Además agregué `_notify_next_in_queue()`, que se llama al regresar un libro.

**Resultado:** PASA (102 passed)

### REFACTOR (`REFACTOR: use deque for reservation queues`)

Cambié la lista con `pop(0)` por `collections.deque` con `popleft()`, que dice
directamente "esto es una cola FIFO". `get_reservation_queue()` sigue regresando
una lista copia para que nadie modifique la cola interna.

**Decisión de diseño:** el notificador es una función que recibe el constructor
(`notifier(member_id, isbn)`). En las pruebas paso un `Mock` y reviso
`assert_called_once_with("S2", REFACTORING)`. Así probé las notificaciones sin
tener que construir envío de correos.

---

## Cómo evolucionó el diseño

| Empezó como | Terminó como | Por qué |
|---|---|---|
| Validaciones dentro de `__init__` | Métodos `_validate_*` + `VALID_ISBN_LENGTHS` | El constructor creció (ciclo 2) |
| Límite fijo de 3 libros | `MemberCategory` con límite y tarifa por categoría | Categorías Estudiante/Profesor/Público |
| `date.today()` dentro de los métodos | `clock` inyectado | Probar multas sin esperar días (ciclo 4) |
| Cola de reservas como lista | `deque` + `_claim_reservation` | FIFO real (ciclo 5) |
| Filtros de búsqueda con `continue` | Método `_matches` + `SORTABLE_FIELDS` | Refactor después de agregar orden |
