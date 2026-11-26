# Documentación del proceso TDD

Cinco ciclos Red-Green-Refactor del desarrollo del Library Management System.

---

## Ciclo #1: Disponibilidad de un libro

### RED

**Test escrito**:

```python
def test_book_is_available_when_copies_exist():
    book = Book("1234567890", "Test Book", "Author", copies=1)
    assert book.is_available() is True
```

**Resultado**: FAIL, `AttributeError: 'Book' object has no attribute 'is_available'`.

Después se escribió el segundo test, que obliga a generalizar:

```python
def test_book_is_not_available_when_no_copies():
    book = Book("1234567890", "Test Book", "Author", copies=0)
    assert book.is_available() is False
```

**Resultado**: FAIL, `assert True is False`.

### GREEN

**Código escrito** (primero "fake it", después generalización):

```python
def is_available(self):
    return True                      # pasa el primer test

def is_available(self):
    return self.available_copies > 0 # pasa ambos
```

**Resultado**: PASS, 4 tests en verde.

### REFACTOR

**Mejoras**: el enunciado pide `total_copies` y `available_copies`, así que se renombró `copies` a `total_copies` y `available_copies` se inicializa con ese valor.

```python
class Book:
    def __init__(self, isbn, title, author, total_copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
```

**Decisión de diseño**: `is_available()` devuelve un booleano y no un conteo, para que el llamador no tenga que interpretar números. Se añadió `test_book_has_total_copies` como test de caracterización, y pasa de inmediato.

---

## Ciclo #2: Validación de ISBN y título

### RED

**Test escrito**:

```python
def test_book_rejects_isbn_with_invalid_length():
    with pytest.raises(ValueError):
        Book("12345", "Test Book", "Author")
```

**Resultado**: FAIL, `DID NOT RAISE`.

Se repitió el ciclo con `test_book_rejects_isbn_with_non_digits` (`"12345abcde"`) y `test_book_requires_title` (`""`). Ambos fallaron con `DID NOT RAISE`.

### GREEN

**Código escrito** (tres pasos, uno por test):

```python
if len(isbn) not in (10, 13):
    raise ValueError("ISBN must be 10 or 13 digits")
# luego
if not isbn.isdigit() or len(isbn) not in (10, 13):
    raise ValueError("ISBN must be 10 or 13 digits")
# luego
if not title or not title.strip():
    raise ValueError("Title is required")
```

**Resultado**: PASS, 8 tests en verde.

### REFACTOR

**Mejoras**: las validaciones se extrajeron a métodos estáticos para que `__init__` quede legible.

```python
def __init__(self, isbn, title, author, total_copies=1):
    self._validate_isbn(isbn)
    self._validate_title(title)
    ...

@staticmethod
def _validate_isbn(isbn):
    if not isbn.isdigit() or len(isbn) not in (10, 13):
        raise ValueError("ISBN must be 10 or 13 digits")
```

**Decisión de diseño**: `Member` reutilizó el mismo patrón `_validate_name`, lo que mantiene el estilo uniforme entre clases.

---

## Ciclo #3: Regla del límite de préstamos en `Member`

### RED

**Test escrito**:

```python
def test_member_cannot_borrow_when_limit_reached():
    member = Member("M001", "Ana")
    member.add_borrowed_book("1111111111")
    member.add_borrowed_book("2222222222")
    member.add_borrowed_book("3333333333")
    assert member.can_borrow() is False
```

**Resultado**: FAIL, `assert True is False`, porque `can_borrow()` era un "fake it" que devolvía `True`.

Un segundo test, `test_add_borrowed_book_raises_error_when_limit_reached`, falló con `DID NOT RAISE`.

### GREEN

**Código escrito**:

```python
def can_borrow(self):
    return len(self.borrowed_books) < self.max_borrow_limit

def add_borrowed_book(self, isbn):
    if not self.can_borrow():
        raise ValueError("Borrow limit reached")
    self.borrowed_books.append(isbn)
```

**Resultado**: PASS, 9 tests en verde (con el test de duplicados incluido).

### REFACTOR

**Mejoras**: se eliminó el número mágico `3` con la constante `DEFAULT_BORROW_LIMIT`, y se extrajo `_has_borrowed(isbn)` porque `add_borrowed_book` y `return_book` repetían la misma comprobación.

```python
def _has_borrowed(self, isbn):
    return isbn in self.borrowed_books
```

**Decisión de diseño**: `add_borrowed_book` reutiliza `can_borrow()` en lugar de duplicar la regla. Hay una sola fuente de verdad para el límite.

---

## Ciclo #4: Cálculo de multas (`late_fees.py`)

### RED

**Tests escritos** (uno por vez):

```python
def test_no_fee_when_returned_on_due_date():
    assert calculate_late_fee(date(2026, 1, 1), date(2026, 1, 15)) == 0

def test_fee_is_one_dollar_per_day_overdue():
    assert calculate_late_fee(date(2026, 1, 1), date(2026, 1, 18)) == 3

def test_no_negative_fee_when_returned_early():
    assert calculate_late_fee(date(2026, 1, 1), date(2026, 1, 5)) == 0
```

**Resultados**: `ModuleNotFoundError`, luego `assert 0 == 3`, luego `assert -10 == 0`.

### GREEN

**Código escrito**: primero `return 0` (fake it). El segundo test obligó a calcular los días y el tercero a acotar el resultado.

```python
def calculate_late_fee(borrow_date, return_date, daily_rate=1):
    due_date = borrow_date + timedelta(days=14)
    days_late = (return_date - due_date).days
    return max(0, days_late) * daily_rate
```

**Resultado**: PASS. Un cuarto test (`daily_rate=2`) agregó la tarifa configurable.

### REFACTOR

**Mejoras**: se extrajeron `LOAN_PERIOD_DAYS`, `DEFAULT_DAILY_RATE` y `get_due_date()`.

```python
def get_due_date(borrow_date):
    return borrow_date + timedelta(days=LOAN_PERIOD_DAYS)
```

**Decisión de diseño**: la función recibe las fechas como parámetros y no llama a `date.today()`. Así los tests son deterministas y rápidos, y `Library` inyecta las fechas con valor por defecto `date.today()`.

---

## Ciclo #5: Atomicidad de `borrow_book` y `return_book`

Este ciclo muestra cómo los tests guiaron el diseño y destaparon un bug dos veces.

### RED

**Primer test**:

```python
def test_borrow_book_does_not_consume_copy_when_member_at_limit(library):
    first = Book("1111111111", "First", "Author")
    second = Book("2222222222", "Second", "Author")
    library.add_book(first)
    library.add_book(second)
    library.register_member(Member("M001", "Ana", max_borrow_limit=1))
    library.borrow_book("M001", "1111111111")
    with pytest.raises(ValueError):
        library.borrow_book("M001", "2222222222")
    assert second.available_copies == 1
```

**Resultado**: FAIL, `assert 0 == 1`. El código descontaba la copia antes de validar el límite del miembro.

### GREEN

**Primer arreglo**: validar con el miembro antes de tocar el libro.

```python
member.add_borrowed_book(isbn)
book.borrow()
```

Esto introdujo el bug inverso. Un segundo test, `test_borrow_book_does_not_register_loan_when_book_unavailable`, falló con `assert ['1234567890'] == []`: el miembro quedaba con un libro que nunca recibió.

**Segundo arreglo**: comprobar la disponibilidad primero.

```python
if not book.is_available():
    raise ValueError("No copies available")
member.add_borrowed_book(isbn)
book.borrow()
```

**Resultado**: PASS. Todas las validaciones ocurren antes de modificar estado. Se aplicó la misma idea a `return_book`, con un test donde Beto intenta devolver el libro de Ana.

### REFACTOR

**Mejoras**: `return_book` pasó a usar `_get_book()` en lugar de `self.books[isbn]`, y las búsquedas por título y autor compartieron el helper `_search_by()`. En los tests se introdujo un fixture de `library`.

**Decisión de diseño**: se adoptó la regla "validar todo antes de mutar nada". Cada operación del sistema es atómica sin necesitar rollback.