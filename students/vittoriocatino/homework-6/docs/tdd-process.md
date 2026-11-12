# Registro del proceso TDD

## Ciclo 1: crear un libro

**RED.** Se escribió primero `test_book_is_created_with_metadata`. Al ejecutar la
suite, la importación de `Book` fallaba porque todavía no existía el módulo.

```python
book = Book("1234567890", "Clean Code", "Robert Martin")
assert book.title == "Clean Code"
```

**GREEN.** Se agregó la clase `Book` con ISBN, título, autor, copias totales y
copias disponibles. La prueba pasó sin incluir lógica de préstamos todavía.

**REFACTOR.** Se conservó el constructor pequeño y se tiparon sus parámetros;
las reglas de disponibilidad quedaron fuera hasta que una prueba las pidió.

## Ciclo 2: validar y prestar ejemplares

**RED.** Se añadieron pruebas para ISBN inválido, títulos vacíos y para el caso
sin copias disponibles. Fallaron por aceptar datos inválidos y no tener el
método `borrow`.

```python
with pytest.raises(ValueError):
    Book("123", "Clean Code", "Robert Martin")
```

**GREEN.** `Book` valida ISBN de 10 o 13 dígitos, impide copias negativas y
`borrow`/`return_copy` actualizan sólo `available_copies`.

**REFACTOR.** La condición repetida se concentró en `is_available`, de modo que
el método de préstamo expresa la regla de negocio en una sola línea.

## Ciclo 3: límites del miembro

**RED.** La prueba creó un miembro con límite uno, pidió un préstamo y verificó
que no pudiera pedir otro. Falló al no existir `Member`.

**GREEN.** Se implementaron `can_borrow`, `add_borrowed_book` y `return_book`.
El objeto mantiene únicamente los ISBN que están actualmente prestados.

**REFACTOR.** La validación de identidad, nombre y límite se dejó en el
constructor para que los demás métodos trabajen con un estado válido.

## Ciclo 4: circulación desde la biblioteca

**RED.** Se escribió una prueba de integración ligera: registrar libro y
miembro, prestar, devolver y comprobar que vuelve la copia disponible. Falló
porque `Library` no tenía catálogo ni flujo de préstamo.

**GREEN.** `Library` registra entidades, busca por título/autor y coordina el
préstamo. Si el miembro alcanzó su límite, restaura la copia para no dejar el
inventario inconsistente.

**REFACTOR.** La búsqueda de libro y miembro se extrajo a `_member_and_book`;
así todos los flujos informan los mismos errores para identificadores faltantes.

## Ciclo 5: tres funciones avanzadas

**RED.** Se agregaron pruebas para multas por atraso, reservas FIFO y categorías
de miembro. La suite falló porque no había tasas por categoría, ni colas, ni una
forma de notificar la siguiente reserva.

```python
library.reserve_book(second.member_id, book.isbn)
assert library.return_book(first.member_id, book.isbn) == second.member_id
```

**GREEN.** Las categorías `student`, `faculty` y `public` fijan límite y tarifa
diaria; las reservas se guardan en orden FIFO y `return_book` devuelve el ID
notificado. Las multas cuentan sólo préstamos activos vencidos.

**REFACTOR.** Las políticas de categorías viven en `Member.CATEGORY_RULES` y la
operación de cola se encapsuló en `next_reservation`. Esto evita duplicar reglas
en `Library` y mantiene las pruebas independientes.
