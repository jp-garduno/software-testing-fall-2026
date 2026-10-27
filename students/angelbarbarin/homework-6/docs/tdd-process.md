# TDD Process Documentation

Este documento describe 5 ciclos completos de Red-Green-Refactor del sistema de administración de la librería. Las salidas de pytest son las reales, copiadas de cada fase RED. Cada fase corresponde a un commit con prefijo `RED:`, `GREEN:` o `REFACTOR:` en el historial de la rama.

---

## Cycle #1: ISBN Validation

### RED Phase

**Test Written**:

```python
@pytest.mark.parametrize("isbn", ["123", "12345678901", "abcdefghij"])
def test_book_rejects_invalid_isbn(isbn):
    with pytest.raises(ValueError):
        make_book(isbn=isbn)
```

**Test Result**: FAIL. `Book` aceptaba cualquier cadena:

```
E       Failed: DID NOT RAISE <class 'ValueError'>
3 failed, 8 passed
```

### GREEN Phase

**Code Written** (lo mínimo, dentro del constructor):

```python
if not (isbn.isdigit() and len(isbn) in (10, 13)):
    raise ValueError("ISBN must have 10 or 13 digits")
self.isbn = isbn
```

**Test Result**: PASS. Todos los tests en verde.

### RED Phase (triangulation)

Los ISBN reales casi siempre se escriben con guiones, así que agregué un segundo test:

```python
def test_book_normalizes_isbn_with_hyphens():
    assert make_book(isbn="978-0-13-235088-4").isbn == "9780132350884"
```

**Test Result**: FAIL. La validación nueva rechazaba los guiones:

```
E           ValueError: ISBN must have 10 or 13 digits
FAILED tests/test_book.py::test_book_normalizes_isbn_with_hyphens
```

### GREEN Phase

```python
isbn = isbn.replace("-", "")
```

### REFACTOR Phase

**Improvements Made**: el constructor ya mezclaba asignación con tres reglas de validación (ISBN, guiones y título). Extraje dos métodos estáticos y una constante:

```python
VALID_ISBN_LENGTHS = (10, 13)

def __init__(self, isbn, title, author, total_copies=1):
    self.isbn = self._normalize_isbn(isbn)
    self.title = self._validate_title(title)
    ...

@staticmethod
def _normalize_isbn(isbn):
    digits = isbn.replace("-", "")
    if not (digits.isdigit() and len(digits) in VALID_ISBN_LENGTHS):
        raise ValueError("ISBN must have 10 or 13 digits")
    return digits
```

**Design Decision**: el libro guarda el ISBN **normalizado** (solo dígitos). La librería usa el ISBN como llave del catálogo, así que `978-0-13-235088-4` y `9780132350884` deben ser el mismo libro.

---

## Cycle #2: Borrowing Must Not Lose a Copy

### RED Phase

**Test Written**:

```python
def test_borrow_book_keeps_copy_when_member_reached_limit(library):
    library.register_member(Member("M002", "Luis Perez", max_borrow_limit=0))
    with pytest.raises(BorrowLimitExceededError):
        library.borrow_book("M002", ISBN)
    assert library.get_book(ISBN).available_copies == 2
```

**Test Result**: FAIL. La excepción sí se lanzaba, pero el libro ya había perdido una copia:

```
>       assert library.get_book(ISBN).available_copies == 2
E       AssertionError: assert 1 == 2
FAILED tests/test_library.py::test_borrow_book_keeps_copy_when_member_reached_limit
```

La primera versión de `borrow_book` hacía `book.borrow()` y luego `member.add_borrowed_book(isbn)`. Cuando el segundo paso fallaba, el primero ya había modificado el estado. Este test encontró un bug real de consistencia.

### GREEN Phase

**Code Written**: validar al miembro **antes** de tocar el libro.

```python
def borrow_book(self, member_id, isbn):
    book = self.get_book(isbn)
    member = self.get_member(member_id)
    if not member.can_borrow():
        raise BorrowLimitExceededError(f"{member.name} reached the borrow limit")
    book.borrow()
    member.add_borrowed_book(isbn)
```

**Test Result**: PASS.

### REFACTOR Phase

Después llegó una segunda regla: no prestar el mismo libro dos veces al mismo miembro. Con dos validaciones, `borrow_book` empezó a crecer, así que extraje un guard:

```python
def borrow_book(self, member_id, isbn):
    book = self.get_book(isbn)
    member = self.get_member(member_id)
    self._ensure_can_borrow(member, isbn)
    book.borrow()
    member.add_borrowed_book(isbn)

@staticmethod
def _ensure_can_borrow(member, isbn):
    if isbn in member.borrowed_books:
        raise AlreadyBorrowedError(f"{member.name} already has {isbn}")
    if not member.can_borrow():
        raise BorrowLimitExceededError(f"{member.name} reached the borrow limit")
```

**Design Decision**: primero se validan todas las reglas y después se modifica el estado. Así una operación fallida nunca deja la librería a medias.

---

## Cycle #3: Late Fees with Fake It and Triangulation

### RED Phase

```python
def test_late_fee_is_zero_on_due_date(library, clock):
    library.borrow_book("M001", ISBN)
    clock.advance(14)
    assert library.calculate_late_fee("M001", ISBN) == Decimal("0")
```

**Test Result**: FAIL. `AttributeError: 'Library' object has no attribute 'calculate_late_fee'`

`clock` es un `FakeClock` definido en `conftest.py`. Se inyecta a `Library(clock=...)` para que los tests puedan "avanzar 17 días" en microsegundos, sin `sleep` ni depender de la fecha real.

### GREEN Phase (Fake It)

```python
def calculate_late_fee(self, member_id, isbn):
    return Decimal("0")
```

Es la implementación más tonta que pasa el test, a propósito. El siguiente test obliga a escribir la lógica real.

### RED Phase (triangulation)

```python
def test_late_fee_is_one_dollar_per_overdue_day(library, clock):
    library.borrow_book("M001", ISBN)
    clock.advance(17)
    assert library.calculate_late_fee("M001", ISBN) == Decimal("3.00")
```

```
E       AssertionError: assert Decimal('0') == Decimal('3.00')
```

### GREEN Phase

```python
def calculate_late_fee(self, member_id, isbn):
    loan = self.get_loan(member_id, isbn)
    days_overdue = max(0, (self._clock() - loan.due_date).days)
    return days_overdue * Decimal("1.00")
```

Un tercer test (miembro FACULTY con tarifa de $0.50) falló con `assert Decimal('4.00') == Decimal('2.00')`. Eso obligó a reemplazar el `Decimal("1.00")` fijo por `self.get_member(member_id).daily_late_fee`.

### REFACTOR Phase

**Improvements Made**: calcular los días de retraso es responsabilidad del préstamo, no de la librería. Lo moví a `Loan`:

```python
@dataclass(frozen=True)
class Loan:
    member_id: str
    isbn: str
    borrowed_on: date

    @property
    def due_date(self):
        return self.borrowed_on + LOAN_PERIOD

    def days_overdue(self, today):
        return max(0, (today - self.due_date).days)
```

```python
def calculate_late_fee(self, member_id, isbn):
    loan = self.get_loan(member_id, isbn)
    daily_fee = self.get_member(member_id).daily_late_fee
    return loan.days_overdue(self._clock()) * daily_fee
```

**Design Decision**: usé `Decimal` en lugar de `float` porque se trata de dinero. Con `float`, `0.1 + 0.2 != 0.3`, y los tests de montos serían frágiles.

---

## Cycle #4: Member Categories

### RED Phase

```python
@pytest.mark.parametrize(
    ("category", "limit"),
    [
        (MemberCategory.STUDENT, 3),
        (MemberCategory.FACULTY, 5),
        (MemberCategory.PUBLIC, 2),
    ],
)
def test_borrow_limit_depends_on_member_category(category, limit):
    assert Member("M002", "Dra. Ruiz", category=category).max_borrow_limit == limit
```

**Test Result**: ERROR. `ImportError: cannot import name 'MemberCategory' from 'member'`

### GREEN Phase

```python
class MemberCategory(Enum):
    STUDENT = "student"
    FACULTY = "faculty"
    PUBLIC = "public"


BORROW_LIMITS = {
    MemberCategory.STUDENT: 3,
    MemberCategory.FACULTY: 5,
    MemberCategory.PUBLIC: 2,
}
```

`max_borrow_limit` cambió su default de `3` a `None`. Si no se indica, se toma de la categoría. Así el test original `test_member_has_default_borrow_limit_of_three` siguió pasando sin cambios, porque STUDENT es la categoría default.

El siguiente ciclo (tarifa diaria por categoría) agregó un segundo diccionario, `DAILY_LATE_FEES`, con las mismas llaves.

### REFACTOR Phase

**Improvements Made**: dos diccionarios paralelos con las mismas llaves son una señal de que falta un concepto. Los agrupé:

```python
@dataclass(frozen=True)
class CategoryRules:
    borrow_limit: int
    daily_late_fee: Decimal


CATEGORY_RULES = {
    MemberCategory.STUDENT: CategoryRules(3, Decimal("1.00")),
    MemberCategory.FACULTY: CategoryRules(5, Decimal("0.50")),
    MemberCategory.PUBLIC: CategoryRules(2, Decimal("1.50")),
}
```

**Design Decision**: agregar una categoría nueva ahora es una sola línea, y es imposible definir el límite de una categoría y olvidar su tarifa.

---

## Cycle #5: Reservations and Notifications

### RED Phase

```python
@pytest.fixture
def notifier():
    return Mock()


def test_return_book_notifies_first_member_in_queue(busy_library, notifier):
    busy_library.reserve_book("M002", ISBN)
    busy_library.reserve_book("M003", ISBN)
    busy_library.return_book("M001", ISBN)
    notifier.notify.assert_called_once_with("M002", busy_library.get_book(ISBN))
```

**Test Result**: ERROR. `TypeError: Library.__init__() got an unexpected keyword argument 'notifier'`

### GREEN Phase

```python
def __init__(self, clock=date.today, notifier=None):
    ...
    self._notifier = notifier

def return_book(self, member_id, isbn):
    ...
    queue = self._reservations[isbn]
    if queue:
        self._notifier.notify(queue.popleft(), book)
```

### RED Phase (edge case)

¿Qué pasa si la librería no tiene canal de notificación? (Se muestra el test ya refactorizado con `build_busy_library`. En el commit RED original el escenario se armaba a mano.)

```python
def test_reservations_advance_without_notifier(clock):
    library = build_busy_library(clock)
    library.reserve_book("M002", ISBN)
    library.return_book("M001", ISBN)
    assert library.reservations_for(ISBN) == []
```

```
E           AttributeError: 'NoneType' object has no attribute 'notify'
```

### GREEN Phase (Null Object)

```python
class NullNotifier:
    def notify(self, member_id, book):
        """Ignore the notification."""

self._notifier = notifier or NullNotifier()
```

### REFACTOR Phase

**Improvements Made**: `Library` manejaba directamente un `defaultdict(deque)`. Extraje una clase con un vocabulario propio:

```python
class ReservationQueue:
    def __init__(self):
        self._queues = defaultdict(deque)

    def add(self, isbn, member_id):
        self._queues[isbn].append(member_id)

    def pop_next(self, isbn):
        queue = self._queues[isbn]
        return queue.popleft() if queue else None

    def members_waiting(self, isbn):
        return list(self._queues[isbn])
```

**Design Decision**: el notificador se **inyecta** (inversión de dependencias). En los tests es un `Mock` que verifica la llamada sin enviar correos reales. En producción podría ser un servicio de email o SMS sin tocar `Library`. El patrón Null Object evita llenar el código de `if self._notifier is not None`.

---

## Summary

| Métrica                        | Valor                   |
| ------------------------------ | ----------------------- |
| Tests                          | 49 (42 funciones, algunas parametrizadas) |
| Commits RED / GREEN / REFACTOR | 42 / 42 / 14            |
| Statement coverage             | 100%                    |
| Branch coverage                | 100%                    |
| Tiempo de la suite             | ~0.2 s                  |
