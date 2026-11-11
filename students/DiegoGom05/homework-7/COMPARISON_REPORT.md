# Reporte de Comparación: Pruebas Tradicionales vs Data-Driven

## Archivos comparados

| Enfoque     | Archivo de tests                  | Datos                              |
| ----------- | --------------------------------- | ---------------------------------- |
| Tradicional | `tests/test_order_traditional.py` | Escritos dentro de cada función    |
| Data-driven | `tests/test_order_data_driven.py` | `test_data/order_calculations.csv` |

Los dos archivos prueban **los mismos 10 escenarios** de la calculadora de órdenes, con las mismas entradas y los mismos valores esperados:

| #   | Escenario                           | Qué prueba                         |
| --- | ----------------------------------- | ---------------------------------- |
| 1   | `simple_single_item`                | Un item sin descuento ni envío     |
| 2   | `simple_multiple_items`             | Varios items con decimales         |
| 3   | `discount_save10_at_threshold`      | SAVE10 exactamente en $50          |
| 4   | `discount_save20_below_min`         | SAVE20 rechazado con $99.99        |
| 5   | `discount_invalid_code`             | Código inexistente                 |
| 6   | `discount_newuser_new_customer`     | NEWUSER con cliente nuevo          |
| 7   | `tax_rounding_decimals`             | Redondeo del impuesto              |
| 8   | `shipping_express`                  | Envío express (1.5×)               |
| 9   | `shipping_freeship_code`            | FREESHIP anula el envío            |
| 10  | `complex_multi_item_save20_express` | Varios items + descuento + express |

Resultado: **20 de 20 tests pasan** (10 en cada archivo).

---

## 1. Líneas de código (LOC)

**Cómo se midió:** con un script que usa el módulo `tokenize` de Python. Se cuentan como "líneas de código" las que no están vacías y no son comentarios ni docstrings.

| Métrica                                                        | Tradicional | Data-driven | Reducción  |
| -------------------------------------------------------------- | ----------- | ----------- | ---------- |
| Líneas totales del archivo                                     | 139         | 52          | **62.6 %** |
| Líneas de código (sin comentarios, docstrings ni vacías)       | 109         | 34          | **68.8 %** |
| Código + filas de datos en el CSV (34 + 10 filas + encabezado) | 109         | 45          | **58.7 %** |
| Funciones `def test_...`                                       | 10          | 1           | 90 %       |

La última fila es la comparación más justa, porque en el enfoque data-driven los datos siguen existiendo, solo que viven en el CSV. Aun contándolos, el enfoque data-driven necesita **casi 60 % menos líneas**.

La diferencia viene de la repetición. En el enfoque tradicional, cada test vuelve a escribir la creación de la orden, la llamada a `set_shipping`, `calculate_total` y las **5 aserciones**: unas 10 líneas por caso, de las cuales solo cambian los números. En el enfoque data-driven, esa lógica se escribe **una sola vez**.

---

## 2. Mantenibilidad

### ¿Qué tan fácil es agregar un caso nuevo?

|                             | Tradicional                                           | Data-driven                                                                                                              |
| --------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Qué hay que hacer           | Copiar una función, renombrarla y cambiar 5–8 valores | Agregar **1 fila** al CSV                                                                                                |
| Líneas agregadas            | ~11                                                   | 1                                                                                                                        |
| Hay que tocar código Python | Sí                                                    | No (en `test_order_calculator.py`); en el archivo de comparación solo se agrega el nombre al conjunto `COMPARISON_CASES` |
| Riesgo de error al copiar   | Alto: es fácil dejar un valor del test anterior       | Bajo: cada fila es independiente                                                                                         |

### ¿Qué tan fácil es modificar los tests existentes?

- **Si cambia una regla de negocio** (por ejemplo, el impuesto sube de 8 % a 10 %): en los dos enfoques hay que recalcular los valores esperados. En el data-driven se editan en una sola tabla, se pueden ordenar o filtrar en Excel y se ven todos juntos. En el tradicional están dispersos en 10 funciones.
- **Si cambia la API** (por ejemplo, `set_shipping` se renombra o recibe otro parámetro): en el tradicional hay que editar **10 funciones**; en el data-driven, **1 línea**.
- **Si se agrega un campo nuevo al resultado** (por ejemplo, `points_earned`): en el tradicional hay que agregar una aserción en cada test; en el data-driven se agrega una columna al CSV y una palabra a la tupla de campos.

**Ganador: data-driven.**

---

## 3. Legibilidad

**Tradicional:**

- ✅ Cada test se entiende solo, sin abrir otro archivo.
- ✅ Es más fácil de depurar con un _breakpoint_, porque los valores están a la vista.
- ❌ Con muchos casos, el archivo se vuelve largo y repetitivo. Es difícil ver _qué cambia_ entre un caso y otro, porque el 90 % del texto es igual.

**Data-driven:**

- ✅ El CSV funciona como una **tabla de especificación**: cada fila es un escenario y se pueden comparar casos lado a lado.
- ✅ Personas que no programan (QA, analistas, el cliente) pueden leer y proponer casos.
- ✅ pytest muestra cada caso con su nombre: `test_order[shipping_express]`.
- ❌ Para entender un caso hay que abrir dos archivos (el test y el CSV).
- ❌ La columna `items` (JSON dentro de un CSV) es menos legible que un diccionario de Python.

**Organización:** el data-driven organiza mejor los tests. Los nombres con prefijo (`simple_`, `discount_`, `tax_`, `shipping_`, `complex_`) agrupan los casos por categoría dentro del CSV, y la lógica de verificación es una sola.

**Ganador:** data-driven cuando hay muchos casos similares. Con 2 o 3 casos, el tradicional se lee igual de bien.

---

## 4. Cobertura

|                                                              | Tradicional                                                           | Data-driven                                  |
| ------------------------------------------------------------ | --------------------------------------------------------------------- | -------------------------------------------- |
| Escenarios en el archivo de comparación                      | 10                                                                    | 10                                           |
| Escenarios en la suite completa (`test_order_calculator.py`) | —                                                                     | 37 (32 de cálculo + 5 de entradas inválidas) |
| Tiempo estimado para agregar 10 casos más                    | 20–30 min (copiar, pegar, editar y revisar 10 funciones; ~110 líneas) | 5–10 min (10 filas en el CSV)                |
| Líneas nuevas para 10 casos                                  | ~110                                                                  | 10                                           |

Con el enfoque data-driven fue práctico llegar a 37 casos en la suite principal, incluyendo casos límite (orden vacía, cantidad cero, valores máximos, $49.99 contra $50.00). Hacer lo mismo de forma tradicional habría producido un archivo de unas **400 líneas**.

**Tiempo de ejecución:** con 10 casos no hay una diferencia medible. Los dos archivos corren en 0.01–0.02 s. La parametrización de pytest genera un test independiente por fila, así que la velocidad no es un factor para elegir entre ellos.

---

## 5. Conclusión

### Cuándo usar cada enfoque

**Data-driven** conviene cuando:

- Se prueba **la misma lógica con muchas combinaciones de entrada** (cálculos, validaciones, reglas de negocio). Este es el caso de la calculadora de órdenes y del validador de clientes.
- Los casos cambian seguido o los mantiene alguien que no programa.
- Se quieren cubrir valores límite de forma sistemática.

**Tradicional** conviene cuando:

- Cada test tiene **una lógica distinta** (configuración especial, _mocks_, varios pasos, verificaciones diferentes).
- Hay pocos casos y separar los datos solo agrega complejidad.
- Se prueba un error muy específico que necesita contexto propio, como `test_apply_discount_return_values` en `test_order_calculator.py`.

En la práctica, **lo mejor es combinarlos**, como en este proyecto: data-driven para el grueso de los escenarios y algunos tests tradicionales para comportamientos puntuales.

### Pros y contras del testing data-driven

| Pros                                                             | Contras                                                                                                           |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 58–69 % menos código en este proyecto                            | Hay que abrir dos archivos para entender un caso                                                                  |
| Agregar un caso es agregar una fila                              | Errores de formato en el CSV/JSON pueden romper la carga de todos los tests                                       |
| Separa _qué_ se prueba (datos) de _cómo_ se prueba (lógica)      | Los casos con lógica distinta no caben bien en una tabla                                                          |
| Los datos se pueden revisar en Excel y reutilizar en otros tests | Estructuras anidadas (como `items`) quedan incómodas en CSV                                                       |
| Un cambio en la API se corrige en un solo lugar                  | Depurar un caso concreto requiere filtrar por su `id` (`pytest -k nombre`)                                        |
| Fomenta cubrir más escenarios y valores límite                   | Los valores esperados se pueden copiar de la implementación por error en vez de calcularse de forma independiente |
