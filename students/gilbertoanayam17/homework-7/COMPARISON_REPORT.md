# Comparison Report - Traditional vs Data-Driven

Las dos suites prueban los mismos 10 escenarios de `Order` y hacen las mismas comprobaciones (los cinco montos del desglose). La única diferencia es dónde viven los datos.

- **Traditional** es `tests/test_order_traditional.py`, con diez funciones que llevan los datos escritos en el código.
- **Data-driven** es `tests/test_order_data_driven.py`, con una sola función parametrizada que lee `test_data/order_comparison.csv`.

## 1. Lines of Code

Para este conteo, "líneas de código" excluye líneas en blanco, comentarios y docstrings.

| Qué se cuenta                                            | Traditional | Data-driven | Reducción |
| -------------------------------------------------------- | ----------- | ----------- | --------- |
| Archivo de prueba, líneas totales                        | 151         | 20          | 86.8%     |
| Archivo de prueba, líneas de código                      | 116         | 10          | 91.4%     |
| Código de prueba + datos (encabezado y 10 filas del CSV) | 116         | 21          | 81.9%     |
| Lo anterior + el loader (16 líneas de `case_loaders.py`) | 116         | 37          | 68.1%     |

La última fila es la comparación más estricta, ya que le carga a la versión data-driven las 16 líneas que leen y convierten el CSV, aunque ese loader se escribe una sola vez y lo comparten tres suites. Aun así queda en menos de la tercera parte.

Desde mi punto de vista, lo importante no es la foto con 10 casos, sino cómo crece cada versión conforme se agregan más.

| Casos | Traditional (código de prueba) | Data-driven (código de prueba) | Data-driven (filas de datos) |
| ----- | ------------------------------ | ------------------------------ | ---------------------------- |
| 10    | 116                            | 10                             | 10                           |
| 100   | ~1,160                         | 10                             | 100                          |
| 500   | ~5,800                         | 10                             | 500                          |

La versión tradicional cuesta unas 11.6 líneas de código por caso, mientras que la data-driven cuesta una fila. Las cifras de 100 y 500 son una proyección de esa proporción, aunque el script del bonus B sí genera suites de ese tamaño y su versión tradicional de 500 casos, escrita en un formato más compacto, mide 3,781 líneas.

## 2. Maintainability

**Agregar un caso.** En la versión tradicional hay que copiar una función de unas 12 líneas, renombrarla y cambiar los valores en dos lugares (los datos y el diccionario esperado), por lo que es fácil dejar sin cambiar algún valor del caso copiado. En la versión data-driven se agrega una fila al CSV y no se toca Python, así que lo puede hacer incluso alguien que no programa.

**Actualizar un caso.** Es parecido en ambas, ya que solo se cambia un número. La diferencia está en encontrarlo, porque en el CSV todos los casos están alineados en la misma columna, mientras que en el código hay que recorrer 150 líneas.

**Cambiar la forma de probar.** Considero que aquí está la mayor diferencia. Si `Order` cambiara, por ejemplo, para recibir el cupón en el constructor, la versión tradicional necesitaría el mismo cambio en 10 funciones y la data-driven en una sola. Pasaría lo mismo si se quisiera agregar una comprobación a todos los casos.

**Lo que cuesta la versión data-driven.** A pesar de sus ventajas, no es gratis. Depende de un loader que también es código y puede tener errores, y un error de formato en una fila (como una comilla faltante en `items`) rompe la recolección de todo el archivo en lugar de una sola prueba. Además, el CSV no avisa de un error de dedo como lo haría un editor de código.

## 3. Readability

**Una prueba aislada se lee mejor en la versión tradicional.** Por ejemplo, `test_shipping_freeship_code` muestra en diez líneas el artículo, el cupón, el envío y el resultado esperado, sin necesidad de abrir otro archivo. Cuando falla, el nombre de la función y el número de línea llevan directo al problema.

**El conjunto se lee mejor en la versión data-driven.** En el CSV los diez escenarios caben en una pantalla y se comparan por columnas, por lo que se nota de inmediato que `shipping_weight_and_distance_standard` y `..._express` solo difieren en `is_express` y en el envío esperado. En el código esa misma comparación exige saltar entre funciones. También me parece que en la tabla es más fácil notar qué falta por probar.

**Organización.** La versión data-driven separa la pregunta de cómo se prueba un pedido (10 líneas de Python) de la pregunta de qué pedidos se prueban (el CSV). Como los ids se toman de `test_name`, el reporte de pytest es igual de claro en las dos (`test_order_scenario[discount_invalid_code]` contra `test_discount_invalid_code`).

**El punto débil del CSV.** La columna `items` se lee mal, ya que es una lista JSON metida dentro de una celda. Para datos anidados conviene más JSON, y por eso mismo los clientes y los flujos de esta tarea están en JSON y no en CSV.

## 4. Coverage

| Suite                                           | Escenarios | Cobertura de `order_calculator.py` |
| ----------------------------------------------- | ---------- | ---------------------------------- |
| Traditional (10 pruebas)                        | 10         | 98%                                |
| Data-driven, mismos 10 escenarios               | 10         | 98%                                |
| Data-driven completa (`order_calculations.csv`) | 25         | 100%                               |

Con los mismos datos las dos formas cubren exactamente lo mismo, lo que muestra que la cobertura depende de los casos y no de cómo están escritos. La diferencia está en lo que cuesta llegar más lejos. La línea que les falta a las suites de 10 es la que rechaza `NEWUSER` para un cliente que no es nuevo, y en el CSV completo la cubre una sola fila (`complex_newuser_code_regular_customer`).

**Tiempo para agregar 10 casos más.** Lo que más tarda en ambas formas es calcular a mano los valores esperados (alrededor de dos minutos por caso), y eso no cambia. Lo que sí cambia es la escritura, que pasa de unas 120 líneas de código a 10 filas. Estimo unos 25 minutos para la versión data-driven y cerca de 45 para la tradicional, con más riesgo de errores por copiar y pegar. Por ejemplo, los 15 escenarios que `order_calculations.csv` tiene además de estos 10 son 15 filas, y como pruebas tradicionales serían unas 175 líneas más.

## 5. Conclusion

**Cuándo usar data-driven.** Considero que conviene en los siguientes casos.

- Cuando la misma lógica se prueba con muchas combinaciones de entrada y salida, como en cálculos, validaciones o reglas de negocio con valores límite.
- Cuando los casos van a crecer, o cuando los mantiene alguien que no programa (en ese caso con Excel o CSV).
- Cuando se quiere ver de un vistazo qué combinaciones están cubiertas.

**Cuándo usar pruebas tradicionales.** En cambio, me parece que son mejor opción en estos otros.

- Cuando son pocos casos y cada uno tiene pasos o comprobaciones distintos.
- Cuando la prueba verifica comportamiento y no valores, por ejemplo que se lance una excepción, el orden de unas llamadas o el estado después de varios pasos.
- Cuando meter el caso en la tabla obligaría a agregar columnas que casi siempre van vacías, o condicionales dentro de la prueba.

| Ventajas de data-driven                           | Desventajas de data-driven                                           |
| ------------------------------------------------- | -------------------------------------------------------------------- |
| Un caso nuevo es una fila, no código              | Hace falta un loader, que también hay que mantener                   |
| La lógica de la prueba se cambia en un solo lugar | Un error de formato en los datos tumba todas las pruebas del archivo |
| Los casos se comparan y se revisan como tabla     | Para entender un caso hay que abrir dos archivos                     |
| Escala sin que crezca el código                   | Todos los casos deben tener la misma forma                           |
| Personas que no programan pueden aportar casos    | Es tentador agregar filas sin pensar si prueban algo nuevo           |

En esta tarea, 93 de las 103 pruebas salen de solo 5 funciones de prueba más los archivos de datos, mientras que las otras 10 son las tradicionales que pide esta comparación. Por esto mismo, mi conclusión es que para un sistema de cálculos y validaciones como este el enfoque data-driven es el que mejor escala, y que las pruebas tradicionales siguen teniendo su lugar para los casos que no caben en una tabla.
