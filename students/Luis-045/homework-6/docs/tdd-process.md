# Proceso TDD

Se documentan cinco ciclos ejecutados durante el desarrollo, con los commits y las salidas reales de cada fase. Los fragmentos muestran el código de ese momento; el código final incorpora validaciones y formato posteriores.

Comando utilizado desde la carpeta de la entrega: `.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider`.

Se agregó un caso por paso. Las pruebas de regresión que ya pasaban se registraron como GREEN, sin atribuirles un fallo inexistente. Los tiempos corresponden a cada ejecución y pueden variar entre equipos.


## Ciclo 1. Validación del ISBN

### RED

Commit: `7b4fe64`. La longitud correcta no bastaba: el ISBN con una letra era aceptado.

```python
def test_book_rejects_an_isbn_containing_letters():
    with pytest.raises(ValueError, match="ISBN"):
        Book("123456789X", "Dune", "Frank Herbert")
```

Resultado real: `1 failed, 3 passed in 0.06s`.


### GREEN

Commit: `5b65e35`. Implementación mínima que hizo pasar el caso:

```python
if len(isbn) not in (10, 13) or not isbn.isdigit():
    raise ValueError("ISBN must contain 10 or 13 digits")
```

Resultado real: `4 passed in 0.01s`.


### REFACTOR

Commit: `16dff0b`.

```python
self._validate_isbn(isbn)

@staticmethod
def _validate_isbn(isbn):
    if len(isbn) not in (10, 13) or not isbn.isdigit():
        raise ValueError("ISBN must contain 10 or 13 digits")
```

Se separó la regla del constructor para que la validación tuviera un nombre y pudiera evolucionar sin mezclarla con la asignación de propiedades.

Resultado real: `4 passed in 0.01s`.


## Ciclo 2. Préstamo sin ejemplares

### RED

Commit: `45be341`. Sin una guarda, el préstamo reducía el inventario de cero a menos uno.

```python
def test_borrow_rejects_an_unavailable_book():
    book = Book("1234567890", "Dune", "Frank Herbert", total_copies=0)
    with pytest.raises(ValueError, match="available"):
        book.borrow()
```

Resultado real: `1 failed, 9 passed in 0.09s`.


### GREEN

Commit: `ebbfcd5`. Implementación mínima que hizo pasar el caso:

```python
def borrow(self):
    if self.available_copies == 0:
        raise ValueError("No copies available")
    self.available_copies -= 1
```

Resultado real: `10 passed in 0.03s`.


### REFACTOR

Commit: `42695e1`.

```python
def borrow(self):
    if not self.is_available():
        raise ValueError("No copies available")
    self.available_copies -= 1
```

La operación reutiliza is_available() para mantener una sola definición de disponibilidad. Se conserva la excepción y se evita modificar las existencias cuando la operación falla.

Resultado real: `10 passed in 0.04s`.


## Ciclo 3. Límite del miembro

### RED

Commit: `26ebf00`. La lista aceptaba un segundo libro aunque el límite personalizado era uno.

```python
def test_member_cannot_exceed_a_custom_borrow_limit():
    member = Member("m1", "Luis", max_borrow_limit=1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="limit"):
        member.add_borrowed_book("1234567891")
```

Resultado real: `1 failed, 17 passed in 0.09s`.


### GREEN

Commit: `3af83a2`. Implementación mínima que hizo pasar el caso:

```python
def add_borrowed_book(self, isbn):
    if len(self.borrowed_books) >= self.max_borrow_limit:
        raise ValueError("Borrow limit reached")
    self.borrowed_books.append(isbn)
```

Resultado real: `18 passed in 0.04s`.


### REFACTOR

Commit: `d2d36b2`.

```python
def add_borrowed_book(self, isbn):
    if not self.can_borrow():
        raise ValueError("Borrow limit reached")
    self.borrowed_books.append(isbn)
```

Se sustituyó el cálculo duplicado por can_borrow(). Esto mantiene alineadas la consulta de capacidad y la validación que precede a cada préstamo.

Resultado real: `18 passed in 0.05s`.


## Ciclo 4. Búsqueda por autor

### RED

Commit: `05cc715`. El método search_by_author todavía no existía; la prueba produjo AttributeError.

```python
def test_search_by_author_matches_a_case_insensitive_substring(stocked_library):
    assert stocked_library.search_by_author("HERB") == [
        stocked_library.catalog["1234567890"]
    ]
```

Resultado real: `1 failed, 36 passed in 0.11s`.


### GREEN

Commit: `74118f9`. Implementación mínima que hizo pasar el caso:

```python
def search_by_author(self, author):
    return [book for book in self.catalog.values()
            if author.casefold() in book.author.casefold()]
```

Resultado real: `37 passed in 0.06s`.


### REFACTOR

Commit: `1d2bae6`.

```python
def search_by_author(self, author):
    return self._search("author", author)

def _search(self, field, query):
    return [book for book in self.catalog.values()
            if query.casefold() in getattr(book, field).casefold()]
```

Las búsquedas por título y autor compartían la misma regla de coincidencia parcial. Extraer _search() eliminó esa duplicación sin cambiar sus API públicas.

Resultado real: `37 passed in 0.04s`.


## Ciclo 5. Detener las multas al devolver

### RED

Commit: `75a194c`. La devolución del día 16 debía fijar la deuda en un dólar. Al consultar el día 20 se obtenían cinco: assert 5 == 1.

```python
def test_returned_loan_fee_stops_growing():
    loan = Loan("m1", "1234567890", date(2026, 10, 1),
                returned_on=date(2026, 10, 16))
    assert loan.fee_on(date(2026, 10, 20)) == 1
```

Resultado real: `1 failed, 43 passed in 0.10s`.
