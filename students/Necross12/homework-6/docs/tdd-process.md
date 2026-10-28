# Proceso TDD: 5 ciclos Rojo-Verde-Refactor

## Ciclo #1: Validación del ISBN

### Fase RED (Rojo)
**Prueba escrita**:
```js
test("(inválida) crear libro con ISBN de 9 dígitos", () => {
  expect(() => new Books("123456789", "Libro de prueba", "Autor")).toThrow(
    "El ISBN debe tener 10 o 13 dígitos",
  );
});
```
**Resultado**: FALLA – el constructor no lanzaba ningún error (`Received function did not throw`).

### Fase GREEN (Verde)
**Código escrito**:
```js
constructor(isbn, titulo, autor) {
  if (isbn.length !== 10 && isbn.length !== 13)
    throw new Error("El ISBN debe tener 10 o 13 dígitos");
}
```
**Resultado**: PASA

### Fase REFACTOR
**Mejoras realizadas**: al agregar la prueba del ISBN con letras (`"12345abcde"`), `length` ya no bastaba. Lo reemplacé por una expresión regular con nombre:
```js
const ISBN_VALIDO = /^(\d{10}|\d{13})$/;
if (!ISBN_VALIDO.test(isbn)) throw new Error("El ISBN debe tener 10 o 13 dígitos");
```
**Decisión de diseño**: una sola regla valida el largo y que sean solo dígitos, y vive en una constante con nombre en vez de condiciones sueltas.

## Ciclo #2: Límite de libros del miembro

### Fase RED (Rojo)
**Prueba escrita**:
```js
test("no puede pedir cuando llegó a su límite", () => {
  const miembro = new Member("Carlos", ["1234567890"], 2);
  miembro.pedir("0987654321");
  expect(miembro.puedePedir()).toBe(false);
});
```
**Resultado**: FALLA – `miembro.puedePedir is not a function`.

### Fase GREEN (Verde)
**Código escrito**:
```js
puedePedir() {
  return this.listaLibros.length < this.limiteLibros;
}

pedir(isbn) {
  this.listaLibros.push(isbn);
  return true;
}
```
**Resultado**: PASA

### Fase REFACTOR
**Mejoras realizadas**: la prueba «pedir un libro superando el límite» obligó a validar también dentro de `pedir()`. En vez de repetir la comparación, `pedir()` reutiliza `puedePedir()`:
```js
pedir(isbn) {
  if (!this.puedePedir())
    throw new Error("El miembro no puede tener más libros que su límite.");
  this.listaLibros.push(isbn);
  return true;
}
```
**Decisión de diseño**: la regla del límite vive en un solo método, así que cambiarla (por ejemplo, con categorías) solo requiere tocar un lugar.

## Ciclo #3: Pedir un libro sin descontar la copia si falla el límite

### Fase RED (Rojo)
**Prueba escrita**:
```js
test("(inválida) pedir superando el límite del miembro no descuenta la copia", () => {
  const lector = new Member("Lector", [], 1);
  biblioteca.agregarMiembro(lector);
  biblioteca.agregarLibro(principito);
  biblioteca.agregarLibro(corte);
  biblioteca.pedirLibro(lector.id, principito.isbn);

  expect(() => biblioteca.pedirLibro(lector.id, corte.isbn)).toThrow(
    "El miembro no puede tener más libros que su límite.",
  );
  expect(corte.copiasDisponibles).toBe(1);
});
```
**Resultado**: FALLA – la excepción sí se lanzaba, pero `copiasDisponibles` era 0 (`Expected: 1, Received: 0`), porque `libro.pedir()` se ejecutaba antes de que `miembro.pedir()` fallara.

### Fase GREEN (Verde)
**Código escrito**:
```js
pedirLibro(idMiembro, isbn) {
  const miembro = this.miembros.find((m) => m.id === idMiembro);
  const libro = this.libros.find((l) => l.isbn === isbn);
  if (!miembro.puedePedir())
    throw new Error("El miembro no puede tener más libros que su límite.");
  libro.pedir();
  miembro.pedir(isbn);
  return true;
}
```
**Resultado**: PASA

### Fase REFACTOR
**Mejoras realizadas**: las pruebas de miembro y libro no registrados dejaron `find` repetido en `pedirLibro` y `regresarLibro`. Lo extraje a dos métodos que además lanzan el error:
```js
obtenerMiembroRegistrado(id) {
  const miembro = this.miembros.find((m) => m.id === id);
  if (!miembro) throw new Error("El miembro no está registrado.");
  return miembro;
}
```
**Decisión de diseño**: primero se validan todas las condiciones y después se modifica el estado, para que una operación fallida no deje cambios a medias.

## Ciclo #4: Reservas con cola FIFO y notificación

### Fase RED (Rojo)
**Prueba escrita**:
```js
test("las reservas respetan el orden de llegada (FIFO)", () => {
  biblioteca.reservarLibro(pepe.id, principito.isbn);
  biblioteca.reservarLibro(ana.id, principito.isbn);
  expect(biblioteca.obtenerReservas(principito.isbn)).toEqual([pepe.id, ana.id]);
});
```
**Resultado**: FALLA – `biblioteca.reservarLibro is not a function`.

### Fase GREEN (Verde)
**Código escrito**:
```js
reservarLibro(idMiembro, isbn) {
  const cola = this.reservas.get(isbn) ?? [];
  cola.push(idMiembro);
  this.reservas.set(isbn, cola);
  return cola.length;
}

obtenerReservas(isbn) {
  return this.reservas.get(isbn);
}
```
**Resultado**: PASA

### Fase REFACTOR
**Mejoras realizadas**: al probar la notificación y quitar al miembro de la cola al pedir el libro, `obtenerReservas` devolvía `undefined` para libros sin cola y exponía el arreglo interno. Lo cambié para devolver una copia y extraje la lógica repetida a `quitarReserva` y `notificarSiguienteEnCola`:
```js
obtenerReservas(isbn) {
  return [...(this.reservas.get(isbn) ?? [])];
}

notificarSiguienteEnCola(libro) {
  const [siguiente] = this.obtenerReservas(libro.isbn);
  if (siguiente === undefined) return;
  this.obtenerMiembroRegistrado(siguiente).notificar(
    `El libro "${libro.titulo}" ya está disponible.`,
  );
}
```
**Decisión de diseño**: devolver una copia protege la cola de modificaciones externas, y `regresarLibro` y `pedirLibro` dejan de duplicar la manipulación de reservas.

## Ciclo #5: Recargos por retraso y categorías de miembro

### Fase RED (Rojo)
**Prueba escrita**:
```js
test("el estudiante paga $1 por día de retraso", () => {
  biblioteca.pedirLibro(pepe.id, corte.isbn, fechaPrestamo);
  expect(
    biblioteca.calcularRecargo(pepe.id, corte.isbn, new Date("2026-10-18T00:00:00Z")),
  ).toBe(3);
});
```
**Resultado**: FALLA – `biblioteca.calcularRecargo is not a function`.

### Fase GREEN (Verde)
**Código escrito**:
```js
calcularRecargo(idMiembro, isbn, fechaActual = new Date()) {
  const prestamo = this.prestamos.find(
    (p) => p.idMiembro === idMiembro && p.isbn === isbn,
  );
  const vencimiento = new Date(prestamo.fechaPrestamo.getTime() + 14 * 24 * 60 * 60 * 1000);
  const dias = Math.max(0, Math.floor((fechaActual - vencimiento) / (24 * 60 * 60 * 1000)));
  return dias * 1;
}
```
**Resultado**: PASA. Después agregué la prueba «el profesor paga $0.5 por día», que falló con `Expected: 2, Received: 4`, y moví la tarifa a la categoría del miembro (`tarifaRecargo`).

### Fase REFACTOR
**Mejoras realizadas**: eliminé los números mágicos, extraje el cálculo de días y llevé el límite y la tarifa de cada categoría a una sola tabla:
```js
const DIAS_PRESTAMO = 14;
const MS_POR_DIA = 24 * 60 * 60 * 1000;
function diasDeRetraso(vencimiento, fechaActual) {
  return Math.max(0, Math.floor((fechaActual - vencimiento) / MS_POR_DIA));
}

const CATEGORIAS = {
  estudiante: { limite: 3, tarifaRecargo: 1 },
  profesor: { limite: 5, tarifaRecargo: 0.5 },
  publico: { limite: 2, tarifaRecargo: 2 },
};
```
**Decisión de diseño**: agregar una categoría nueva ahora es agregar una entrada a `CATEGORIAS`, sin tocar `Library`. Recibir `fechaActual` por parámetro permite probar retrasos sin depender del reloj.
