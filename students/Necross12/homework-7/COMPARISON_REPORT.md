# Comparison Report: Pruebas tradicionales vs. data-driven

Sistema bajo pruebas: `Order` (`src/orderCalculator.js`), en JavaScript con Jest.

Se escribieron los **mismos 10 escenarios** de dos formas distintas:

| Archivo                          | Enfoque                                                                          |
|----------------------------------|----------------------------------------------------------------------------------|
| `tests/orderTraditional.test.js` | 10 funciones `test()` independientes, con los datos escritos a mano              |
| `tests/orderDataDriven.test.js`  | 1 sola prueba con `test.each`, datos leídos de `test_data/orderCalculations.csv` |

Los 10 escenarios: pedido simple, límite de SAVE10 ($50), límite de SAVE20 ($100), NEWUSER en cliente nuevo, NEWUSER en cliente regular, código inválido, impuesto después del descuento, envío por peso (varios productos), FREESHIP y envío exprés (varios productos).

## 1. Líneas de código

Se contaron las líneas totales (`wc -l`) y las líneas de código, es decir, sin líneas vacías ni comentarios de línea completa (`grep -vE '^\s*$|^\s*//'`).

| Versión       | Líneas totales | Líneas de código |
|---------------|----------------|------------------|
| Tradicional   | 142            | 122              |
| Data-driven   | 58             | 53               |
| **Reducción** | **59.2 %**     | **56.6 %**       |

Reducción de código = (122 − 53) / 122 ≈ **56.6 %**.

**Aclaración:** la versión data-driven no cuenta el CSV porque ese archivo ya existe y lo comparte con `orderCalculator.test.js`. Si el CSV se hubiera escrito solo para estos 10 casos, el ahorro real sería menor. Aun así, el ahorro crece con cada caso nuevo, porque la estructura de la prueba se reutiliza.

Además, ~20 de las 53 líneas de la versión data-driven son elementos fijos (imports, lectura del CSV, conversión de tipos). Ese costo se paga una sola vez, sin importar si hay 10 o 1000 casos.

## 2. Mantenibilidad

**Agregar casos nuevos**
- Tradicional: hay que copiar una prueba completa (~12 líneas) y cambiar nombre, items, código, distancia y 5 valores esperados. Es fácil equivocarse al copiar y pegar, y el archivo se vuelve más difícil de seguir conforme crece.
- Data-driven: se agrega una fila al CSV y no se toca el código.

**Modificar pruebas existentes**
- Cambio de **datos** (por ejemplo, un descuento que pasa de 10 % a 12 %): en ambos enfoques se editan los valores esperados, pero en el tradicional hay que corregir cada prueba en varios puntos del código, mientras que en el CSV todos los datos están agrupados en un solo lugar.
- Cambio de **lógica** (por ejemplo, el calculador ahora devuelve `grandTotal` en vez de `total`): en el tradicional hay que editar 10 pruebas (50 `expect`); en el data-driven solo se edita el bloque de `expect`, una vez.
- Cambio en la **interfaz** de `Order` (por ejemplo, renombrar `setShipping`): igual, 10 lugares contra 1.

## 3. Legibilidad

- **Tradicional:** cada prueba se lee de forma aislada y el escenario queda a la vista (qué se arma, qué se espera). Es más explícito y todo está en un solo archivo, por lo que se entiende a la primera, pero es muy repetitivo y los patrones se pierden entre tantas líneas casi idénticas.
- **Data-driven:** la lógica cabe en una pantalla y la tabla del CSV permite comparar escenarios lado a lado. En contrapartida, para entender un caso hay que cruzar dos archivos, y un `items` en JSON dentro de una celda CSV (con comillas simples) es difícil de leer.
- **Organización:** el data-driven se organiza por categorías de datos (filas agrupadas); el tradicional, por nombre de prueba. Los nombres descriptivos del CSV hacen que el reporte de Jest se vea igual de claro en ambos casos.

**Opinión personal sobre JSON y CSV:** me resulta más fácil leer JSON que CSV en texto plano. El formato de los objetos anidados deja ver mejor qué datos entran, qué error se espera y qué se va a hacer, mientras que en el CSV los objetos se convierten en una lista larga dentro de una celda. En cambio, para datos simples el CSV es más amable, sobre todo con extensiones del editor que lo muestran como tabla. Frente a las pruebas tradicionales, tener toda la información a la mano en un solo lugar es muy cómodo: una vez que se entiende cómo funciona la prueba, es más fácil leer un CSV o un JSON que perderse navegando entre muchas pruebas casi iguales.

## 4. Cobertura

Con los 10 escenarios ambos enfoques recorren las mismas ramas de `Order`, así que **la cobertura de código es idéntica**. La diferencia está en la velocidad de ampliarla y en cuántos escenarios se pueden probar:

|                                           | Tradicional                      | Data-driven                                                  |
|-------------------------------------------|----------------------------------|--------------------------------------------------------------|
| Escenarios probados                       | 10                               | 10 (el CSV tiene 40 y hay 100 aleatorios en otro CSV)        |
| Tiempo estimado para agregar 10 casos más | ~15–20 min (≈ 120 líneas nuevas) | ~3–5 min (10 filas, 0 líneas de código)                      |
| Líneas de código tras agregar 10 casos    | ≈ 242                            | ≈ 53 (sin cambio)                                            |

Los tiempos de agregar casos son estimaciones, no se midieron con cronómetro.

**Escalabilidad real:** `orderCalculator.test.js` es data-driven y ejecuta 140 casos desde CSV (40 escritos a mano + 100 aleatorios) más 4 pruebas directas, en unos 0.4 s. Hacer lo mismo de forma tradicional habría requerido más de 1,500 líneas de código.

**Tiempo de ejecución** (Jest, 5 corridas cada una, solo el archivo): tradicional ≈ 0.22–0.36 s, data-driven ≈ 0.21–0.37 s. La diferencia es despreciable: el cálculo es en memoria y casi todo el tiempo es el arranque de Jest. El data-driven paga un costo mínimo extra por leer y convertir el CSV.

## 5. Conclusión

**Cuándo usar cada enfoque**

| Usar tradicional cuando…                                            | Usar data-driven cuando…                                                                          |
|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| Hay pocos casos y cada uno es muy distinto                          | Muchos casos comparten la misma lógica y cambian solo las entradas/salidas (misma estructura)     |
| El escenario requiere pasos especiales (mocks, esperas, secuencias) | Se espera que la lista de casos crezca                                                            |
| Se quiere máxima claridad para quien lee la prueba                  | Se quiere que alguien que no programa pueda aportar casos desde una hoja de cálculo (CSV / Excel) |

**Ventajas del data-driven**
- Mucho menos código repetido (−56.6 % en este caso).
- Agregar casos es barato y no requiere tocar la lógica.
- La lógica de verificación se corrige en un solo lugar.
- Los datos pueden reutilizarse entre suites (aquí, el mismo CSV alimenta dos archivos de prueba).
- Permite generar datos de forma programática (los 100 pedidos aleatorios con Faker) y validarlos antes de correr las pruebas.
- Se aprecia mejor la estructura de las pruebas: qué variables cambian entre un caso y otro.

**Desventajas del data-driven**
- Hay que escribir un cargador/parser, y los errores de formato (comillas, comas sin entrecomillar, tipos, líneas vacías) pueden romper toda la suite. Me pasó al corregir nombres con comas, y el validador de datos lo detectó.
- Un fallo apunta a una fila de datos, no a una línea de código, por lo que depurar toma un paso extra.
- Los casos con comportamiento distinto (como el que lanza un error por precio negativo) necesitan banderas especiales (`expectError`) o quedan mejor como pruebas aparte.
- Los datos y la lógica viven en archivos separados, lo que reduce la legibilidad de un caso individual.
- Los valores individuales y la intención de cada prueba se ven menos que en una prueba escrita a mano.

**Recomendación:** usar data-driven para las reglas de cálculo (descuentos, impuestos, envío), que son las que más casos tienen, y dejar pruebas tradicionales para escenarios con lógica única o manejo de errores muy específico.

Ambos enfoques tienen pros y contras, y lo mejor es usar cada uno donde encaja. Si se necesita cuidar la estructura y la legibilidad de la prueba (ver qué se mide y qué no) o hay un elemento externo particular, el tradicional es ideal. Si se va a reutilizar la misma arquitectura cambiando solo variables o nombres, el data-driven es mucho mejor, y además permite que otras áreas (por ejemplo QA o negocio) aporten casos sin leer código, lo que ayuda a romper la visión de túnel que se puede crear como desarrollador.
