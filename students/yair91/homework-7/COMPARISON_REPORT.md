# Tradicional contra guiado por datos

Los dos archivos de la Parte 3 cubren **los mismos diez escenarios** con las
mismas afirmaciones: subtotal, descuento, impuesto, envío y total de cada uno.
Lo único que cambia es dónde viven los datos.

- `tests/test_order_traditional.py` — diez funciones, datos escritos adentro
- `tests/test_order_data_driven.py` — una función parametrizada, datos en `test_data/order_calculations.csv`

Todos los números de este reporte están medidos, no estimados. Los comandos
para reproducirlos están al final.

## 1. Líneas de código

| | Tradicional | Guiado por datos | Reducción |
| --- | --- | --- | --- |
| Líneas totales | 144 | 41 | **71.5 %** |
| Sin vacías ni comentarios | 108 | 26 | **75.9 %** |
| Funciones de prueba | 10 | 2 | 80 % |
| Casos ejecutados | 10 | 11 | — |

El archivo guiado por datos ejecuta un caso más porque además de los diez
escenarios incluye una prueba que verifica que los diez nombres sigan
existiendo en el CSV. Sin esa guarda, renombrar una fila del CSV haría que el
escenario desapareciera en silencio y la suite seguiría en verde con nueve
casos en lugar de diez.

La reducción real es mayor de lo que dice el 75 %: las 26 líneas del archivo
guiado por datos son **constantes** respecto al número de escenarios. Las 108
del tradicional crecen a razón de unas 11 por escenario.

## 2. Mantenibilidad

**Agregar un caso nuevo.** En el tradicional son unas 11 líneas: una función,
el armado del pedido y cinco afirmaciones. En el guiado por datos es una línea
en el CSV y un nombre en la lista `ESCENARIOS`. Para los otros archivos de la
entrega, que no filtran por nombre, es una sola línea en el CSV y nada más.

**Cambiar una regla.** Si la tasa de impuesto pasara de 8 % a 9 %, en el
tradicional hay que recalcular a mano los diez valores de `tax` y los diez de
`total`, repartidos en 144 líneas. Es tedioso y es exactamente donde se cuela
un error de dedo. En el guiado por datos se regenera la columna del CSV con el
mismo script que la produjo.

**Dónde duele el guiado por datos.** El salto de contexto. Ver una falla y
entender qué se estaba probando obliga a abrir el CSV y buscar la fila. Por eso
cada archivo de datos de esta entrega trae una columna `reason` o `category`
que no se usa para decidir nada: solo viaja al mensaje de error.

## 3. Legibilidad

El tradicional gana cuando lees **una** prueba. Todo está a la vista: entradas,
pasos y resultado esperado, sin abrir nada más. Para alguien que llega nuevo al
código, `test_save10_justo_en_el_minimo` se entiende sin contexto.

El guiado por datos gana cuando lees **todas**. Las 35 filas del CSV caben en
una pantalla y se leen como una tabla de decisión: se ve de un vistazo qué
combinaciones están cubiertas y cuáles faltan. En el tradicional esa misma
visión exige leer 144 líneas y llevar la cuenta en la cabeza.

Hay un efecto que no esperaba: el formato tabular **hace visibles los huecos**.
Al acomodar los casos en columnas salta a la vista que no había ninguna fila
con cantidad cero, y de ahí salió `complex_zero_quantity_contributes_nothing`.
Escribiendo funciones sueltas ese hueco no se nota.

## 4. Cobertura y costo de crecer

| | Tradicional | Guiado por datos |
| --- | --- | --- |
| Escenarios cubiertos | 10 | 10 |
| Tiempo de ejecución (promedio de 3 corridas) | 0.030 s | 0.010 s |
| Líneas para 10 escenarios más | ~110 | ~10 (una por fila del CSV) |
| Archivos a tocar | 1 | 1 (el CSV) |

El tiempo favorece al guiado por datos, pero la diferencia es de milisegundos
y no es el argumento. Con 10 casos no importa; el punto es que el costo de
agregar el caso 50 es el mismo que el del caso 11, y en el tradicional no.

En la entrega completa esto se nota: las 256 pruebas de la suite salen de 35
filas de CSV, 39 casos de JSON, 5 flujos y unas pocas funciones. Escritas una
por una serían más de dos mil líneas.

## 5. Conclusión

**Guiado por datos cuando** el mismo camino de código se recorre con muchas
combinaciones de entrada: tablas de precios, reglas de descuento, validaciones
de formato, matrices de decisión. Mientras más se parezcan los casos entre sí,
más gana.

**Tradicional cuando** cada prueba hace algo distinto: montar un estado
particular, verificar una secuencia de llamadas, comprobar que algo lanza en el
momento preciso. Meter eso en una tabla obliga a inventar columnas que solo
aplican a una fila, y la tabla se vuelve más difícil de leer que el código que
reemplaza.

**Lo que funciona mejor es mezclarlos**, y es lo que hace esta entrega: los
montos y las validaciones van por CSV y JSON, mientras que las reglas que no se
expresan como un número —que un código rechazado no pise al anterior, que
`FREESHIP` no descuente del precio— viven como funciones sueltas en
`test_order_calculator.py`.

**Lo que hay que cuidar.** Los datos son código y necesitan el mismo rigor. Un
CSV con una columna corrida no hace fallar la prueba: la hace pasar con los
valores equivocados. Por eso esta entrega incluye `src/data_validator.py`, que
revisa los archivos antes de usarlos y reporta cada problema con archivo, línea
y columna.

Y un riesgo más sutil: si los valores esperados se generan llamando al código
que se va a probar, la prueba ya no prueba nada, solo confirma que el código
coincide consigo mismo. Los valores de `order_calculations.csv` se calcularon
con una fórmula escrita aparte, desde el texto del enunciado, y después se
contrastaron contra la implementación. `test_data/generated_orders.csv` sí sale
del código, y por eso está marcado como datos de regresión: sirve para detectar
que algo cambió, no para demostrar que algo está bien.

## Cómo reproducir los números

```bash
# Líneas
wc -l tests/test_order_traditional.py tests/test_order_data_driven.py
grep -vcE '^\s*$|^\s*#' tests/test_order_traditional.py

# Casos ejecutados
pytest tests/test_order_traditional.py --collect-only -q
pytest tests/test_order_data_driven.py --collect-only -q

# Tiempo
pytest tests/test_order_traditional.py -q
pytest tests/test_order_data_driven.py -q
```
