# Proceso TDD: cinco ciclos documentados

Las fases que siguen se ejecutaron durante el desarrollo. Los ejemplos de código
se extraen de los commits indicados, no se reconstruyen a partir de la solución final.
Los ciclos pueden contener pasos intermedios: se identifica explícitamente cuándo
la refactorización se realizó después de otras pruebas del mismo subsistema.

En total se registraron **54 fases RED, 54 GREEN y 8 REFACTOR**: 116 commits TDD.
Cada GREEN ejecutó la suite completa disponible en ese momento; cada RED ejecutó
la prueba nueva antes de modificar el código. Los primeros tres módulos produjeron
errores de importación porque todavía no existían; los otros 51 RED fallaron al
comprobar el comportamiento. No se interpretan como fallos válidos errores de sintaxis.

Los casos de integración posteriores son regresiones adicionales y se identifican
como tales. El archivo [tdd-runs.jsonl](evidence/tdd-runs.jsonl) conserva 62 registros,
uno por par RED/GREEN o por REFACTOR, con resultados, cambios y hashes completos.
Solo se normalizó la ruta absoluta de la entrega en las salidas archivadas.


## Ciclo 1: Validación de ISBN

### RED

La prueba rechaza letras, dígitos de ancho completo, números y None. La validación inicial comprobaba solamente la longitud.

Prueba escrita primero (e9b93da):

```python
@pytest.mark.parametrize("isbn", ["abcdefghij", "１２３４５６７８９０", 1234567890, None])
def test_reject_non_numeric_isbn(isbn):
    with pytest.raises(ValueError, match="ISBN"):
        Book(isbn, "Dune", "Herbert")
```

Resultado observado: `4 failed in 0.09s`. Código de salida: 1.

### GREEN

Implementación en e33a21a:

```python
    def __init__(self, isbn, title, author, total_copies=1):
        if not isinstance(isbn, str) or not isbn.isascii() or not isbn.isdigit() or len(isbn) not in (10, 13):
            raise ValueError("ISBN must have 10 or 13 digits")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
```

Resultado de la suite completa: `16 passed in 0.04s`. Código de salida: 0.

### REFACTOR

Se dio nombre al predicado valid_isbn para que la combinación de tipo, alfabeto y longitud resulte legible. Entre GREEN y REFACTOR se añadieron otras validaciones; los hashes conservan el orden real.

Código en 33c7c48:

```python
    def __init__(self, isbn, title, author, total_copies=1):
        valid_isbn = (
            isinstance(isbn, str) and isbn.isascii()
            and isbn.isdigit() and len(isbn) in (10, 13)
        )
        if not valid_isbn:
            raise ValueError("ISBN must have 10 or 13 digits")
        self.isbn = isbn
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Book title is required")
        self.title = title
        self.author = author
        if type(total_copies) is not int or total_copies < 0:
            raise ValueError("Total copies must be a nonnegative integer")
        self.total_copies = total_copies
        self.available_copies = total_copies
```

Resultado tras refactorizar: `24 passed in 0.05s`. Código de salida: 0.
Registros de evidencia: 9 y 12 en el archivo JSONL.


## Ciclo 2: Límite de préstamos de un miembro

### RED

El segundo préstamo superaba el límite y se añadía a la lista. La prueba exige una excepción y que la lista permanezca intacta.

Prueba escrita primero (1724413):

```python
def test_member_limit_preserves_list():
    member = Member("m1", "Ana", 1)
    member.add_borrowed_book("1234567890")
    with pytest.raises(ValueError, match="limit"):
        member.add_borrowed_book("1234567890123")
    assert member.borrowed_books == ["1234567890"]
```

Resultado observado: `1 failed in 0.08s`. Código de salida: 1.

### GREEN

Implementación en 3920e38:

```python
    def add_borrowed_book(self, isbn):
        if len(self.borrowed_books) >= self.max_borrow_limit:
            raise ValueError("Member borrowing limit reached")
        self.borrowed_books.append(isbn)
```

Resultado de la suite completa: `30 passed in 0.05s`. Código de salida: 0.

### REFACTOR

Se reutilizó can_borrow en vez de duplicar la comparación con el límite. Las pruebas de devolución y validación del límite también se incorporaron antes de esta refactorización.

Código en a089a0e:

```python
    def add_borrowed_book(self, isbn):
        if not self.can_borrow():
            raise ValueError("Member borrowing limit reached")
        self.borrowed_books.append(isbn)
```
