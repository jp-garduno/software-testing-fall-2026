# Cinco ciclos Red-Green-Refactor

Las referencias son hashes reales del historial de esta rama. En cada ciclo se añadió primero una prueba, se ejecutó pytest y se comprobó su fallo antes de implementar la conducta. GREEN sólo se confirmó después de ejecutar la suite completa satisfactoriamente. Cada REFACTOR también se verificó con la suite completa antes del commit.

Los siguientes fragmentos proceden de los commits indicados, por lo que muestran la evolución del código. Algunos refactors ocurrieron después de otros ciclos, cuando apareció suficiente contexto para justificar la extracción. El [registro de ejecuciones](tdd-evidence.json) conserva salidas RED/GREEN; los commits mantienen las pruebas completas y sus estados intermedios. Los cambios de caracterización posteriores comprueban contratos existentes y se etiquetan REFACTOR.


## Ciclo 1: Validación del ISBN

### RED — `a8f7ba0`

Se aceptan exactamente 10 o 13 dígitos ASCII. También se rechazan valores numéricos y dígitos Unicode para que el identificador conserve un formato estable.

```python
@pytest.mark.parametrize("isbn", ["123", "123456789X", "1" * 11, 1234567890, None, "Ù¡Ù¢Ù£Ù¤Ù¥Ù¦Ù§Ù¨Ù©Ù "])
def test_book_rejects_invalid_isbn(isbn):
    with pytest.raises(ValueError, match="ISBN"):
        Book(isbn, "Title", "Author")
```

Resultado observado:

```text
E   Failed: DID NOT RAISE ValueError
E   Failed: DID NOT RAISE ValueError
E   Failed: DID NOT RAISE ValueError
E   Failed: DID NOT RAISE ValueError
E   Failed: DID NOT RAISE ValueError
E   Failed: DID NOT RAISE ValueError
6 failed, 2 passed in 0.20s
```

### GREEN — `292966c`

Implementación mínima en `src/book.py`:

```python
def __init__(self, isbn, title, author, copies=1):
    if not isinstance(isbn, str) or len(isbn) not in (10, 13) or not isbn.isascii() or not isbn.isdigit():
        raise ValueError('ISBN must contain 10 or 13 ASCII digits')
    self.total_copies = copies
    self.available_copies = copies
    self.isbn = isbn
    self.title = title
    self.author = author
```

Resultado de la suite:

```text
8 passed in 0.04s
```

### REFACTOR — `4d09ba9`

La variable valid_isbn da nombre a la regla y separa su evaluación del error. No añade reglas de checksum que el enunciado no solicita.

```python
def __init__(self, isbn, title, author, copies=1):
    valid_isbn = isinstance(isbn, str) and len(isbn) in (10, 13) and isbn.isascii() and isbn.isdigit()
    if not valid_isbn:
        raise ValueError('ISBN must contain 10 or 13 ASCII digits')
    if not isinstance(title, str) or not title.strip():
        raise ValueError('Book title is required')
    if type(copies) is not int or copies < 0:
        raise ValueError('copies must be a nonnegative integer')
    self.total_copies = copies
    self.available_copies = copies
    self.isbn = isbn
    self.title = title
    self.author = author
```

La suite completa siguió pasando antes de confirmar este refactor; se conservaron todas las pruebas anteriores.


## Ciclo 2: Límite de préstamos del socio

### RED — `b2b244e`

Un socio con límite uno puede registrar el primer libro, pero debe rechazar un ISBN diferente después. La prueba también observa que ya no tiene capacidad.

```python
def test_member_cannot_exceed_custom_limit():
    member = Member("M1", "Ana", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="limit"):
        member.add_borrowed_book("1234567890123")
    assert member.can_borrow() is False
```

Resultado observado:

```text
E   Failed: DID NOT RAISE ValueError
1 failed, 34 passed in 0.20s
```

### GREEN — `35b3ae5`

Implementación mínima en `src/member.py`:

```python
def add_borrowed_book(self, isbn):
    if not self.can_borrow():
        raise ValueError('Borrow limit reached')
    self.borrowed_books.append(isbn)
```

Resultado de la suite:

```text
35 passed in 0.06s
```

### REFACTOR — `6bc5167`

La validación se extrae a validate_borrow para que Library pueda comprobar las restricciones antes de descontar inventario. Member mantiene la misma protección al utilizarse directamente.

```python
def validate_borrow(self, isbn):
    if isbn in self.borrowed_books:
        raise ValueError('Book already borrowed by this member')
    if not self.can_borrow():
        raise ValueError('Borrow limit reached')
```

La suite completa siguió pasando antes de confirmar este refactor; se conservaron todas las pruebas anteriores.


## Ciclo 3: Errores de devolución e integración

### RED — `2720441`

La API debe producir ValueError al recibir un socio desconocido. Una fuga de KeyError del diccionario sería un contrato distinto y por eso la prueba falló.

```python
def test_return_rejects_unknown_member(library):
    with pytest.raises(ValueError, match="Unknown member"):
        library.return_book("missing", "1234567890")
```

Resultado observado:

```text
E   KeyError: 'missing'
1 failed, 49 passed in 0.22s
```

### GREEN — `7749b8e`

Implementación mínima en `src/library.py`:

```python
def return_book(self, member_id, isbn):
    if member_id not in self.members:
        raise ValueError('Unknown member')
    member = self.members[member_id]
    book = self.catalog[isbn]
    member.return_book(isbn)
    book.return_copy()
```

Resultado de la suite:

```text
50 passed in 0.08s
```

### REFACTOR — `f2ef49e`

Las comprobaciones compartidas de socios y libros pasan a _participants. Prestar y devolver conservan el mismo tratamiento de identificadores inválidos sin duplicarlo.

```python
def _participants(self, member_id, isbn):
    if member_id not in self.members:
        raise ValueError('Unknown member')
    if isbn not in self.catalog:
        raise ValueError('Unknown book')
    return self.members[member_id], self.catalog[isbn]
```

La suite completa siguió pasando antes de confirmar este refactor; se conservaron todas las pruebas anteriores.


## Ciclo 4: Cálculo de multas

### RED — `098dbf5`

Los ejemplos distinguen fecha de préstamo, vencimiento exacto, primer día de retraso y varios días vencidos. La regla inicial usa un dólar por día y Decimal.

```python
@pytest.mark.parametrize("as_of, expected", [(date(2026, 1, 1), "0"), (date(2026, 1, 15), "0"), (date(2026, 1, 16), "1"), (date(2026, 1, 20), "5")])
def test_late_fee_respects_due_date_boundary(as_of, expected):
    assert Loan("M1", "1234567890", date(2026, 1, 1)).late_fee(as_of) == Decimal(expected)
```

Resultado observado:

```text
E   AttributeError: 'Loan' object has no attribute 'late_fee'
E   AttributeError: 'Loan' object has no attribute 'late_fee'
E   AttributeError: 'Loan' object has no attribute 'late_fee'
E   AttributeError: 'Loan' object has no attribute 'late_fee'
4 failed, 56 passed in 0.25s
```

### GREEN — `7e633c3`

Implementación mínima en `src/loan.py`:

```python
def late_fee(self, as_of):
    return Decimal(max(0, (as_of - self.due_date).days))
```

Resultado de la suite:

```text
60 passed in 0.10s
```

### REFACTOR — `f1f92a6`

El plazo deja de ser un literal dentro de due_date y se expresa mediante LOAN_PERIOD_DAYS = 14. La fórmula monetaria permanece independiente de cómo Library obtiene la fecha.

```python
@property
def due_date(self):
    return self.borrowed_on + timedelta(days=LOAN_PERIOD_DAYS)
```

La suite completa siguió pasando antes de confirmar este refactor; se conservaron todas las pruebas anteriores.


## Ciclo 5: Historial de préstamos y devoluciones

### RED — `34f75bd`

Devolver un libro debe registrar su fecha y conservar intacta la instantánea entregada al prestar. Actualizar únicamente las existencias no cumplía el historial.

```python
def test_history_records_return_without_mutating_original_snapshot(dated_library):
    library, clock = dated_library
    borrowed = library.borrow_book("M1", "1234567890")
    clock[0] = date(2026, 1, 18)
    library.return_book("M1", "1234567890")
    assert (library.get_member_history("M1")[0].returned_on, borrowed.returned_on) == (clock[0], None)
```

Resultado observado:

```text
E   assert (None, None) == (datetime.dat... 1, 18), None)
E
E     At index 0 diff: None != datetime.date(2026, 1, 18)
E     Use -v to get more diff
1 failed, 75 passed in 0.26s
```

### GREEN — `80cf2a2`

Implementación mínima en `src/library.py`:

```python
def return_book(self, member_id, isbn):
    member, book = self._participants(member_id, isbn)
    member.return_book(isbn)
    book.return_copy()
    index = next(i for i, loan in enumerate(self._loans)
                 if loan.member_id == member_id and loan.isbn == isbn and loan.returned_on is None)
    self._loans[index] = replace(self._loans[index], returned_on=self._today())
```

Resultado de la suite:

```text
76 passed in 0.11s
```

### REFACTOR — `6fa54fb`

La devolución localiza una sola vez el préstamo activo y captura una sola fecha antes de cambiar estado. Esa misma referencia sirve para validar fechas y reemplazar el registro inmutable.

```python
def return_book(self, member_id, isbn):
    member, book = self._participants(member_id, isbn)
    index = next((i for i, loan in enumerate(self._loans)
                  if loan.member_id == member_id and loan.isbn == isbn and loan.returned_on is None), None)
    if index is None:
        raise ValueError('Book not borrowed by this member')
    returned_on = self._today()
    if self._loans[index].borrowed_on > returned_on:
        raise ValueError('Return date cannot be before borrowing date')
    member.return_book(isbn)
    book.return_copy()
    self._loans[index] = replace(self._loans[index], returned_on=returned_on)
```

La suite completa siguió pasando antes de confirmar este refactor; se conservaron todas las pruebas anteriores.
