# Especificación de los datos de prueba

Cuatro archivos en `test_data/`. Tres son el contrato que verifican las
pruebas; el cuarto es un conjunto de regresión generado.

| Archivo | Formato | Filas/casos | Mínimo del enunciado | Qué define |
| --- | --- | --- | --- | --- |
| `order_calculations.csv` | CSV | 35 | 25 | Montos de cada pedido |
| `customer_validation.json` | JSON | 39 | 30 | Validación de clientes |
| `order_workflows.json` | JSON | 5 | 3 | Flujos de extremo a extremo |
| `generated_orders.csv` | CSV | 100 | — | Regresión generada (bonus A) |

---

## `order_calculations.csv`

Una fila es un pedido completo con sus cinco montos esperados.

| Columna | Tipo | Qué guarda |
| --- | --- | --- |
| `test_name` | texto | Identificador único; sale en la salida de pytest |
| `category` | texto | Una de `simple`, `discount`, `tax`, `shipping`, `complex` |
| `items` | JSON | Lista de artículos, cada uno con `name`, `price`, `quantity`, `weight` |
| `customer_type` | texto | `regular` o `new` |
| `discount_code` | texto | El código, o `NONE` para no intentar ninguno |
| `distance_km` | número | Distancia de envío |
| `is_express` | texto | `true` o `false`, en minúsculas |
| `expected_subtotal` | número | Montos esperados, a dos decimales |
| `expected_discount` | número | |
| `expected_tax` | número | |
| `expected_shipping` | número | |
| `expected_total` | número | |
| `expected_error` | texto | Mensaje de `ValueError` esperado; vacío cuando el pedido es válido |

**La columna `items` es JSON dentro de una celda de CSV.** Las comillas dobles
van duplicadas, que es como el estándar CSV las escapa:

```csv
"[{""name"": ""Notebook"", ""price"": 25.0, ""quantity"": 1, ""weight"": 0.0}]"
```

El ejemplo del enunciado usa `[{name:Item1,price:50,...}]`, con las claves sin
comillas. Eso no es JSON válido ni literal de Python, así que no se puede leer
con `json.loads` ni con `ast.literal_eval`. Aquí se usa JSON porque `csv` y
`json` son de la librería estándar y `json.loads` no ejecuta nada de lo que
lee, a diferencia de `eval`.

**Cuando `expected_error` trae texto, las cinco columnas de montos van
vacías.** Esa fila afirma que construir el pedido lanza `ValueError` con ese
mensaje exacto, y nunca llega a calcular nada.

**Reparto por categoría**, contra los mínimos del enunciado:

| Categoría | Filas | Mínimo |
| --- | --- | --- |
| `simple` | 4 | 3 |
| `discount` | 8 | 5 |
| `tax` | 5 | 4 |
| `shipping` | 8 | 6 |
| `complex` | 10 | 7 |

---

## `customer_validation.json`

```json
{
  "description": "...",
  "reference_date": "2026-11",
  "test_cases": [
    {
      "test_name": "valid_standard",
      "category": "valid_customers",
      "customer": { "email": "...", "phone": "...", "address": {...},
                    "card_number": "...", "card_expiry": "MM/YY" },
      "expected_valid": true,
      "expected_errors": [],
      "reason": "Every field well formed"
    }
  ]
}
```

`expected_errors` es la lista **completa y en orden**, no un subconjunto. El
orden lo fija `validate_customer`: email, teléfono, calle, ciudad, estado,
código postal, tarjeta, vencimiento. Las pruebas comparan la lista entera, así
que una fila que espera un error no pasa si el código devuelve tres.

`reference_date` existe porque el vencimiento de una tarjeta depende de qué día
es hoy. Si el validador usara `datetime.now()`, una tarjeta `12/26` sería
válida este año y dejaría de serlo el siguiente, y la suite empezaría a fallar
sola sin que nadie tocara nada. La fecha de referencia está fija en
`customer_validator.py` como dato, no como reloj.

**Reparto por categoría**:

| Categoría | Casos | Mínimo |
| --- | --- | --- |
| `valid_customers` | 5 | 3 |
| `invalid_emails` | 6 | 4 |
| `invalid_phones` | 5 | 4 |
| `invalid_addresses` | 7 | 5 |
| `invalid_cards` | 9 | 8 |
| `multiple_errors` | 7 | 6 |

---

## `order_workflows.json`

Cada flujo encadena validación de cliente, descuento, envío y cálculo.

```json
{
  "workflow_name": "checkout_regular_with_save20",
  "description": "...",
  "customer": { ... },
  "items": [ ... ],
  "customer_type": "regular",
  "steps": [
    { "action": "validate_customer", "expected_result": true },
    { "action": "apply_discount", "code": "SAVE20", "expected_result": true },
    { "action": "set_shipping", "distance_km": 40, "is_express": false },
    { "action": "calculate_total" }
  ],
  "expected_customer_valid": true,
  "expected_discount_applied": true,
  "expected_order": { "subtotal": ..., "discount": ..., "tax": ..., "shipping": ..., "total": ... },
  "expected_outcome": "confirmed"
}
```

`expected_outcome` es `confirmed` solo cuando el cliente pasa la validación. Un
flujo con `rejected_customer` igual trae sus montos: el pedido se calcula, pero
no se confirma, y una prueba verifica que el rechazo del cliente no altera
ningún monto.

Los cinco flujos cubren: camino feliz con descuento, cliente nuevo con express,
cliente rechazado por tarjeta inválida, descuento rechazado por monto, y
`FREESHIP` sobre un envío que habría sido caro.

---

## `generated_orders.csv`

Cien pedidos producidos por `src/data_generator.py` con `random` sembrado. El
mismo semillero da siempre el mismo archivo, así que el CSV se puede regenerar
y comparar byte a byte.

```bash
PYTHONPATH=src python src/data_generator.py
```

**Estos datos son distintos a los de los otros tres archivos y conviene no
confundirlos.** Sus valores esperados salen de correr el propio calculador, así
que afirman *que el comportamiento no cambió*, no *que el comportamiento es
correcto*. Son una foto para detectar regresiones. La verificación de
corrección vive en `order_calculations.csv`, cuyos montos se calcularon con una
fórmula escrita aparte, desde el texto del enunciado, y después se contrastaron
contra la implementación.

Por eso las pruebas de `test_data_generator.py` no afirman montos: verifican
que los pedidos sean válidos, que haya variedad de códigos y modalidades, y que
el archivo se pueda releer.

---

## Validación de los datos

`src/data_validator.py` revisa los archivos antes de usarlos y reporta cada
problema con archivo, línea y columna:

```
order_calculations.csv:14 [expected_subtotal]: 'mucho' no es un numero
customer_validation.json [test_cases[7]]: un caso valido no puede traer errores esperados
```

Qué revisa: columnas faltantes, nombres repetidos, categorías desconocidas,
booleanos mal escritos, números que no son números, `items` que no es JSON o
al que le faltan campos, y en el JSON que un caso válido no declare errores y
que uno inválido sí los declare.

```python
from data_validator import exigir_datos_validos
exigir_datos_validos("test_data")   # lanza DataValidationError con todo junto
```

## Cómo agregar casos

Para los montos de pedidos, una línea en `order_calculations.csv`. Para
clientes, un objeto en `test_cases`. En los dos casos no hay que tocar ningún
archivo de pruebas: la suite recorre lo que encuentre.

Lo único que sí hay que tocar es `tests/test_order_data_driven.py`, y solo si
el caso nuevo debe entrar en la comparación de la Parte 3, porque ese archivo
elige diez escenarios por nombre a propósito.
