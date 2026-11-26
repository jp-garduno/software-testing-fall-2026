# Test Data Specification

Todos los datos de prueba están en `test_data/`. Cada archivo alimenta una suite y cada fila, objeto o flujo es una prueba, que se identifica en la salida de pytest por su nombre.

| Archivo                    | Formato | Casos | Suite que lo usa                   |
| -------------------------- | ------- | ----- | ---------------------------------- |
| `order_calculations.csv`   | CSV     | 25    | `tests/test_order_calculator.py`   |
| `order_comparison.csv`     | CSV     | 10    | `tests/test_order_data_driven.py`  |
| `order_calculations.xlsx`  | Excel   | 25    | `tests/test_order_excel.py`        |
| `customer_validation.json` | JSON    | 30    | `tests/test_customer_validator.py` |
| `order_workflows.json`     | JSON    | 3     | `tests/test_integration.py`        |

## General Conventions

- **Nombres.** Van en `snake_case`, son únicos dentro del archivo y deben decir qué se prueba en vez de solo numerarlo (por ejemplo `discount_save20_below_minimum` y no `test_6`). La primera palabra es la categoría.
- **Montos esperados.** Son exactos al centavo. Las pruebas comparan con igualdad y sin tolerancia, por lo que un error de un centavo hace fallar el caso.
- **Codificación.** Todos los archivos están en UTF-8, y las rutas se resuelven desde `tests/` y no desde el directorio actual.
- **Fecha de referencia.** Las vigencias de tarjeta se evalúan al **15 de junio de 2025** (`REFERENCE_DATE` en `tests/case_loaders.py`). Por ejemplo, una tarjeta `06/2025` todavía es válida, mientras que una `05/2025` ya expiró.

## Order Cases (`order_calculations.csv` and `order_comparison.csv`)

Cada fila es un caso. `order_comparison.csv` tiene las mismas columnas y contiene los 10 escenarios que la Parte 3 también escribe a mano en `test_order_traditional.py`.

| Columna             | Tipo       | Valores                                                                              |
| ------------------- | ---------- | ------------------------------------------------------------------------------------ |
| `test_name`         | texto      | Nombre único con prefijo de categoría                                                |
| `items`             | lista JSON | Artículos del pedido (ver abajo)                                                     |
| `customer_type`     | texto      | `new` o `regular`                                                                    |
| `discount_code`     | texto      | `SAVE10`, `SAVE20`, `FREESHIP`, `NEWUSER`, `NONE` (sin cupón) o cualquier otro texto |
| `distance_km`       | número     | Distancia de envío (un valor negativo se cobra como 0)                               |
| `is_express`        | booleano   | `true` o `false`                                                                     |
| `expected_subtotal` | número     | Suma de precio × cantidad                                                            |
| `expected_discount` | número     | Monto descontado, que es `0.00` si el cupón no existe o no aplica                    |
| `expected_tax`      | número     | 8% de (subtotal - descuento)                                                         |
| `expected_shipping` | número     | kg × $0.50 + km × $0.10, multiplicado por 1.5 si es exprés (y `0.00` con `FREESHIP`) |
| `expected_total`    | número     | subtotal - descuento + impuesto + envío                                              |

**Columna `items`.** Es una lista JSON escrita con comillas simples y encerrada entre comillas dobles, ya que contiene comas, como en el siguiente ejemplo.

```csv
"[{'name':'Toaster','price':40,'quantity':1,'weight':4}]"
```

Cada artículo lleva `name` (texto, sin apóstrofos), `price` (precio unitario), `quantity` y `weight` (kg por unidad). El peso del pedido es la suma de peso × cantidad.

**Categorías.** La primera palabra de `test_name` indica la categoría del caso.

| Prefijo     | Casos | Qué cubre                                                                                                                |
| ----------- | ----- | ------------------------------------------------------------------------------------------------------------------------ |
| `simple_`   | 3     | Pedidos sin cupón ni envío (un artículo, una cantidad mayor a uno y varios artículos)                                    |
| `discount_` | 5     | Cupón justo en su mínimo, por debajo del mínimo, código inexistente y cupón sobre varios artículos                       |
| `tax_`      | 4     | Redondeo hacia abajo y hacia arriba, e impuesto sobre el monto ya descontado                                             |
| `shipping_` | 6     | Solo peso, solo distancia, ambos, estándar contra exprés, valores fraccionarios y envío gratis                           |
| `complex_`  | 7     | Varios artículos con cupón y envío, cupón rechazado, cantidad cero, valores negativos, medios centavos y valores máximos |

**Cómo calcular los valores esperados.** Cada monto se redondea a centavos antes de usarlo en el siguiente, y medio centavo siempre sube. La siguiente tabla lo muestra con el caso `complex_half_cent_amounts_round_up` (3 × $21.45, `SAVE10`, 1.5 kg, 10 km, exprés).

| Monto     | Cálculo                        | Sin redondear | Esperado |
| --------- | ------------------------------ | ------------- | -------- |
| Subtotal  | 3 × 21.45                      | 64.35         | 64.35    |
| Descuento | 64.35 × 10%                    | 6.435         | 6.44     |
| Impuesto  | (64.35 - 6.44) × 8%            | 4.6328        | 4.63     |
| Envío     | (1.5 × 0.50 + 10 × 0.10) × 1.5 | 2.625         | 2.63     |
| Total     | 64.35 - 6.44 + 4.63 + 2.63     |               | 65.17    |

**Dos diferencias con el enunciado.** La fila de ejemplo del enunciado (`simple_order`) indica $5.50 de envío para 1 kg y 10 km, pero con las tarifas escritas ($0.50 por kg y $0.10 por km) el resultado es $1.50, por lo que estos datos siguen las tarifas escritas. Además, aunque el texto dice "orders > $50", el código que da el enunciado acepta el cupón desde $50.00 exactos, así que los datos siguen al código (`discount_save10_at_minimum`).

## Order Cases in Excel (`order_calculations.xlsx`)

Son los mismos 25 casos, repartidos en cinco hojas, una por categoría (`Simple`, `Discounts`, `Tax`, `Shipping` y `Complex`).

- La primera fila de cada hoja tiene los nombres de columna, idénticos a los del CSV.
- Las celdas pueden estar tipadas, con los montos y la distancia como números y con `is_express` como `TRUE`/`FALSE`, aunque también se aceptan como texto.
- `items` es texto con el mismo formato que en el CSV.
- Las filas completamente vacías, como las que quedan al final de una hoja, se ignoran.
- El nombre de la hoja se antepone al de la prueba, por ejemplo `Tax:tax_rounds_up`.

Para agregar una categoría basta con crear otra hoja con la misma fila de encabezados. El archivo de ejemplo se genera desde el CSV con `python scripts/build_excel_sample.py`.

## Customer Cases (`customer_validation.json`)

El archivo es una lista de objetos como el siguiente.

```json
{
  "test_name": "invalid_card_expired_last_month",
  "customer": {
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "billing_address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip": "10001"
    },
    "credit_card": {
      "number": "4532015112830366",
      "expiration": "05/2025",
      "cvv": "123"
    }
  },
  "expected": { "is_valid": false, "errors": ["Credit card expired"] }
}
```

La siguiente tabla resume la regla de cada campo y el mensaje que se reporta cuando no se cumple.

| Campo                    | Regla para ser válido                                                               | Mensaje si falla             |
| ------------------------ | ----------------------------------------------------------------------------------- | ---------------------------- |
| `email`                  | Formato `nombre@dominio.tld`, con un solo `@`, sin espacios y con punto tras el `@` | `Invalid email format`       |
| `phone`                  | Exactamente `(XXX) XXX-XXXX`                                                        | `Invalid phone format`       |
| `billing_address.street` | Texto no vacío                                                                      | `Missing street`             |
| `billing_address.city`   | Texto no vacío                                                                      | `Missing city`               |
| `billing_address.state`  | Código de dos letras mayúsculas de un estado de EE. UU. (o DC)                      | `Invalid state`              |
| `billing_address.zip`    | `XXXXX` o `XXXXX-XXXX`                                                              | `Invalid zip code`           |
| `credit_card.number`     | De 13 a 19 dígitos que cumplen el algoritmo de Luhn                                 | `Invalid credit card number` |
| `credit_card.cvv`        | 3 o 4 dígitos                                                                       | `Invalid CVV`                |
| `credit_card.expiration` | `MM/YYYY` con mes de 01 a 12                                                        | `Invalid expiration date`    |
| `credit_card.expiration` | No anterior al mes de la fecha de referencia                                        | `Credit card expired`        |

- `expected.errors` debe listar los mensajes **en el orden de esta tabla**, ya que la prueba compara la lista completa. Para un cliente válido es `[]`.
- Un campo ausente o `null` cuenta como inválido, igual que un bloque completo (`billing_address` o `credit_card`) ausente.
- Los números de tarjeta son números de prueba públicos, no tarjetas reales.

**Categorías.** Según la primera palabra de `test_name`, los casos son `valid_` (3), `invalid_email_` (4), `invalid_phone_` (4), `invalid_address_` (5), `invalid_card_` (8) y `multiple_` (6, con dos o más errores a la vez).

## Workflows (`order_workflows.json`)

El archivo es un objeto con la lista `workflows`. Cada flujo tiene un `name` y sus `steps`, que se ejecutan en orden sobre una misma sesión de `Checkout`. Un paso se ve como el siguiente.

```json
{
  "action": "create_order",
  "data": {
    "items": [
      { "name": "Backpack", "price": 39.99, "quantity": 1, "weight": 0.9 }
    ],
    "customer_type": "regular",
    "discount_code": "FREESHIP",
    "shipping": { "distance_km": 300, "is_express": true }
  },
  "expected": { "status": "created", "discount_applied": true }
}
```

- `action` es el nombre de un método de `Checkout` y `data` son sus argumentos (se omite si no lleva).
- `expected` lista solo los campos del resultado que se quieren comprobar, por lo que los demás no se revisan.

| `action`            | `data`                                                                    | Campos del resultado                                                               |
| ------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `validate_customer` | `customer`, el mismo objeto que en `customer_validation.json`             | `valid` (booleano), `errors` (lista)                                               |
| `create_order`      | `items` y, como opcionales, `customer_type`, `discount_code` y `shipping` | `status` (`created`), `discount_applied` (booleano)                                |
| `calculate_total`   | -                                                                         | `subtotal`, `discount`, `tax`, `shipping`, `total`                                 |
| `process_payment`   | -                                                                         | `status` (`success` o `declined`), `amount_charged` y, si se cobró, `confirmation` |

Los tres flujos son un cliente regular con `SAVE20` y envío estándar, un cliente nuevo con `NEWUSER` y envío exprés, y una tarjeta expirada que termina en pago rechazado.

## Adding a Test Case

1. Elegir el archivo según lo que se prueba y la categoría del caso.
2. Agregar la fila u objeto con un nombre único que empiece con el prefijo de la categoría.
3. Calcular los valores esperados a mano con las reglas de este documento, no copiando la salida del programa.
4. Correr `pytest -k <nombre_del_caso>`. No hay que tocar ningún archivo de `tests/`.
5. Si el caso es de pedidos, correr `python scripts/build_excel_sample.py` para que el Excel siga igual al CSV.
