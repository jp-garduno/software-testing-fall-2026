# Comparison Report: Traditional vs Data-Driven Testing

Ambas versiones prueban los **mismos 10 escenarios** del calculador de pedidos (pedido simple, SAVE10 en el
límite y debajo, SAVE20 en el límite, NEWUSER, redondeo de impuesto, envío express, FREESHIP, artículo con
cantidad 0 y un carrito complejo con SAVE20 y express) y verifican los mismos 5 valores de cada uno.

| | Traditional | Data-driven |
| - | ----------- | ----------- |
| Archivo de prueba | `tests/test_order_traditional.py` | `tests/test_order_data_driven.py` |
| Datos | escritos dentro de cada función | `test_data/comparison_orders.csv` |
| Funciones de prueba | 10 | 1 (parametrizada) |
| Pruebas que reporta pytest | 10 | 10 |
| Resultado | 10 passed | 10 passed |

## 1. Lines of Code

Conteo de líneas de código sin líneas en blanco, comentarios ni docstrings:

| Concepto | Traditional | Data-driven |
| -------- | ----------- | ----------- |
| Código Python | 111 | 12 |
| Datos (CSV, con encabezado) | 0 | 11 |
| **Total** | **111** | **23** |
| `assert` escritos | 50 | 1 |

- Reducción de código Python: (111 − 12) / 111 = **89%**.
- Reducción contando también el CSV: (111 − 23) / 111 = **79%**.

La diferencia crece con cada caso: en la versión tradicional cada escenario cuesta ~11 líneas de Python
(crear la orden, aplicar el código, configurar el envío y 5 asserts); en la versión data-driven cuesta
**una línea de CSV**.

## 2. Maintainability

**Agregar un caso.** Tradicional: copiar una función, renombrarla y cambiar 8-10 valores dispersos en el código;
es fácil olvidar uno y que la prueba pase por la razón equivocada. Data-driven: agregar una fila. El validador
de datos (`src/data_files.py`) revisa la fila antes de correr y, si algo está mal escrito, dice en qué línea.

**Cambiar una regla.** Si mañana el impuesto pasara de 8% a 9%, en las dos versiones hay que recalcular los
valores esperados, pero en la data-driven están en un solo archivo con columnas con nombre
(`expected_tax`), así que se pueden revisar como tabla o en Excel. En la tradicional hay 10 funciones que editar.

**Cambiar la API.** Si `set_shipping` cambiara de firma, la versión tradicional necesita 10 cambios y la
data-driven uno. Este es el ahorro más grande en mantenimiento: la lógica de la prueba existe una sola vez.

## 3. Readability

- **Un caso aislado** se lee mejor en la versión tradicional: todo está en la misma pantalla y no hay que
  abrir otro archivo.
- **El conjunto** se lee mejor en la data-driven: el CSV es una tabla donde se ven todos los escenarios lado a
  lado y salta a la vista qué falta (por ejemplo, que el CSV de comparación no tiene un caso de SAVE20 debajo del mínimo).
- **Organización:** la data-driven separa *qué* se prueba (datos, con columna `category`) de *cómo* se prueba
  (código). Los ids de pytest usan `test_name`, así que un fallo dice
  `test_order[shipping_express]` igual de claro que `test_shipping_express`.
- **Mensajes de error:** en la tradicional cada assert señala el componente exacto. En la data-driven un solo
  `assert order.calculate_total() == pytest.approx(expected)` compara el diccionario completo; pytest muestra
  qué llave no coincidió, pero el mensaje es un poco menos directo.

## 4. Coverage

| | Traditional | Data-driven (toda la tarea) |
| - | ----------- | ----------- |
| Escenarios del calculador | 10 | 36 (CSV principal) + 100 (generados con Faker) |
| Escenarios de validación de cliente | – | 39 |
| Flujos completos | – | 7 |

Con el mismo esfuerzo, la versión data-driven escala mucho más: los 100 pedidos generados se prueban con
la misma función de 12 líneas.

**Tiempo para agregar 10 casos más** (estimación propia, no medida con cronómetro):

| | Traditional | Data-driven |
| - | ----------- | ----------- |
| Líneas nuevas | ~110 de Python | 10 de CSV |
| Tiempo estimado | 20-30 min (copiar, editar, revisar cada función) | 5-10 min (calcular los esperados y escribir las filas) |

En los dos casos lo que más tiempo toma es calcular a mano los valores esperados; la diferencia está en todo
lo demás.

**Tiempo de ejecución:** las 10 pruebas tardan ~0.01 s en las dos versiones. Leer el CSV no tiene un costo
apreciable a esta escala.

## 5. Conclusion

**Cuándo usar data-driven:** cuando la *misma* lógica se verifica con muchas combinaciones de entradas:
reglas de negocio con tablas de valores, validaciones, cálculos con límites, regresión con datos generados.
También cuando otras personas (QA, negocio) deben poder leer o agregar casos sin tocar código.

**Cuándo usar tradicional:** cuando cada prueba tiene una preparación o verificación distinta (por ejemplo,
revisar que un código inválido no borre el anterior, o el orden de las llamadas en un flujo), o cuando son
pocos casos y separarlos en un archivo agrega más complejidad de la que ahorra. En esta tarea las dos conviven:
`test_order_calculator.py` tiene la tabla del CSV y además algunas pruebas puntuales escritas a mano.

| Pros de data-driven | Contras de data-driven |
| ------------------- | ---------------------- |
| Mucho menos código (89% menos en este caso) | Un caso queda repartido entre dos archivos |
| Agregar casos no requiere programar | Los datos mal escritos fallan de forma confusa si no se validan (por eso el validador) |
| Los datos se revisan como tabla y se pueden generar | Un solo assert general da mensajes menos específicos |
| La lógica de la prueba se mantiene en un solo lugar | Un error en la función de prueba afecta a todos los casos a la vez |
| Escala a cientos de casos sin cambiar código | Tentación de poner lógica (fórmulas) en los datos o de calcular los esperados con el mismo código que se prueba |
