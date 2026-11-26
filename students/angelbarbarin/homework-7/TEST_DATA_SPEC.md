# Test Data Specification

Todos los datos de prueba viven en `test_data/`. Las pruebas no tienen datos escritos en el código: leen estos
archivos con los cargadores de `src/data_files.py`, que primero los validan (ver
[Validación de los datos](#validación-de-los-datos)).

| Archivo | Formato | Casos | Lo usa |
| ------- | ------- | ----- | ------ |
| `order_calculations.csv` | CSV | 36 | `tests/test_order_calculator.py` |
| `customer_validation.json` | JSON | 39 | `tests/test_customer_validator.py` |
| `order_workflows.json` | JSON | 7 flujos | `tests/test_integration.py` |
| `comparison_orders.csv` | CSV | 10 | `tests/test_order_data_driven.py` |
| `generated_orders.csv` | CSV | 100 | `tests/test_generated_orders.py` (generado con Faker) |

## Reglas de cálculo que asumen los datos

Los valores esperados siguen estas reglas. Donde el enunciado era ambiguo, se tomó la decisión indicada:

| Regla | Valor | Decisión tomada |
| ----- | ----- | --------------- |
| Subtotal | Σ precio × cantidad | – |
| `SAVE10` | 10% si subtotal **≥** $50 | El texto dice "> $50", pero el código base del enunciado usa `subtotal < min_order` para rechazar; se siguió el código, así que $50.00 exactos sí aplica |
| `SAVE20` | 20% si subtotal **≥** $100 | Igual que `SAVE10` |
| `FREESHIP` | Envío $0, sin descuento en dinero | Aplica aunque el envío sea express |
| `NEWUSER` | 15% | Solo para `customer_type = new` ("first order") |
| Códigos | Sin distinguir mayúsculas ni espacios | `" save10 "` equivale a `SAVE10`; un código inválido no borra el que ya estaba aplicado |
| Impuesto | 8% de (subtotal − descuento) | – |
| Envío | $4.00 base + $0.50/kg + $0.10/km | La tarifa base de $4.00 sale de la fila de ejemplo del enunciado (1 kg, 10 km → $5.50) |
| Express | Envío × 1.5 | Se multiplica todo el envío, incluida la base |
| Peso | peso × cantidad de cada artículo | – |
| Sin unidades | Envío $0 | Un pedido sin unidades (vacío o todo con cantidad 0) no se envía |
| Redondeo | A centavos, *half up*, en cada componente | El total es la suma de los componentes ya redondeados |
| Negativos | Error `InvalidOrderError` | Precio, cantidad, peso o distancia negativos |

## order_calculations.csv

Una fila por caso. Codificación UTF-8, separador coma; los campos con comas van entre comillas (estándar CSV).

| Columna | Tipo | Descripción |
| ------- | ---- | ----------- |
| `test_name` | texto, único | Nombre del caso; también es el id de la prueba en pytest |
| `category` | texto | `simple`, `discount`, `tax`, `shipping` o `complex` |
| `items` | JSON | Lista de objetos `{"name", "price", "quantity", "weight"}`; precio en USD, peso en kg, cantidad entera |
| `customer_type` | `new` \| `regular` | Tipo de cliente |
| `discount_code` | texto | Código tal como lo escribe el cliente; `NONE` = sin código |
| `distance_km` | número | Distancia de envío (puede ser negativa para probar el error) |
| `is_express` | `true` \| `false` | Envío express |
| `expected_subtotal` … `expected_total` | número con 2 decimales | Resultado esperado de cada componente |
| `expected_error` | texto | Vacío si el pedido es válido. Si no, fragmento del mensaje de `InvalidOrderError` y las columnas `expected_*` van vacías |

Ejemplo (la fila del enunciado):

```csv
test_name,category,items,customer_type,discount_code,distance_km,is_express,expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total,expected_error
simple_order,simple,"[{""name"":""Item1"",""price"":50,""quantity"":1,""weight"":1}]",regular,NONE,10,false,50.00,0.00,4.00,5.50,59.50,
```

La columna `items` es JSON válido (comillas dobles escapadas como `""` dentro del campo CSV), así que no se
necesita el truco de reemplazar comillas simples del ejemplo del enunciado.

Casos por categoría: simple 3, discount 10, tax 5, shipping 8, complex 10 (4 de ellos esperan error).

## customer_validation.json

Lista de casos:

```json
{
  "test_name": "invalid_card_expired_last_month",
  "category": "invalid_card",
  "today": "2026-11-30",
  "customer": {
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "billing_address": { "street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001" },
    "credit_card": { "number": "4532015112830366", "expiration": "12/2028", "cvv": "123" }
  },
  "expected": { "is_valid": false, "errors": ["Credit card is expired"] }
}
```

- `category`: `valid`, `invalid_email`, `invalid_phone`, `invalid_address`, `invalid_card` o `multiple_errors`.
- `today` (opcional): fecha con la que se juzga la expiración. Si falta se usa **2026-11-01**
  (`REFERENCE_DATE` en `tests/conftest.py`), para que los resultados no cambien con el día en que se corre.
- `expected.errors`: lista **completa y en orden**. El validador reporta en este orden: email, teléfono,
  dirección (calle, ciudad, estado, ZIP), tarjeta (número, expiración, CVV).
- Un campo ausente se omite del objeto `customer` (prueba el mensaje "… is required").

Reglas y mensajes:

| Campo | Regla | Mensaje |
| ----- | ----- | ------- |
| email | requerido; `usuario@dominio.tld` | `Email is required` / `Invalid email format` |
| phone | requerido; exactamente `(XXX) XXX-XXXX` | `Phone is required` / `Invalid phone format` |
| billing_address | objeto requerido | `Billing address is required` |
| street, city | no vacíos | `Street is required`, `City is required` |
| state | código de 2 letras de EE. UU. (incluye DC) | `Invalid state` |
| zip | `12345` o `12345-6789` | `Invalid ZIP code` |
| credit_card | objeto requerido | `Credit card is required` |
| number | 13-19 dígitos (se aceptan espacios y guiones) y algoritmo de Luhn | `Invalid credit card number` |
| expiration | `MM/YYYY`; vale hasta el último día de ese mes | `Invalid expiration date format` / `Credit card is expired` |
| cvv | 3 dígitos; 4 si la tarjeta es American Express (34/37) | `Invalid CVV` |

Las tarjetas válidas son números de prueba públicos que pasan Luhn (Visa 4532015112830366 y 4111111111111111,
Mastercard 5555555555554444, Amex 378282246310005). No son tarjetas reales.

## order_workflows.json

```json
{
  "reference_date": "2026-11-01",
  "workflows": [
    {
      "name": "declined_payment_flow",
      "description": "…",
      "gateway": { "declined_cards": ["4532015112830366"], "limit": 5000 },
      "steps": [
        { "action": "validate_customer", "data": { … }, "expected": { "valid": true } },
        { "action": "process_payment", "expected": { "status": "declined", "error": "Card declined" } }
      ]
    }
  ]
}
```

- `gateway` (opcional): configuración del `SimulatedPaymentGateway` (tarjetas rechazadas y límite por cargo).
- Cada paso se ejecuta con `OrderProcessor.run_step(action, data)` sobre el mismo procesador.
- `expected` es un **subconjunto**: solo se comparan las llaves listadas; los montos se comparan al centavo.

| action | data | Resultado |
| ------ | ---- | --------- |
| `validate_customer` | objeto cliente | `valid`, `errors` |
| `create_order` | `items`, `customer_type` | `status` (`created`/`rejected`), `order_id`, `items_count`, `error` |
| `apply_discount` | `code` | `applied`, `discount_code` |
| `set_shipping` | `distance_km`, `is_express` | `status` (`ok`/`error`) |
| `calculate_total` | – | `status`, `subtotal`, `discount`, `tax`, `shipping`, `total` |
| `process_payment` | – | `status` (`success`/`declined`/`error`), `transaction_id`, `amount`, `error` |
| `generate_confirmation` | – | `status` (`confirmed`/`error`), `order_id`, `email`, `total`, `message` |

## comparison_orders.csv

Mismo formato que `order_calculations.csv`. Son 10 filas copiadas de ese archivo: los mismos 10 escenarios
que `tests/test_order_traditional.py` tiene escritos a mano.

## generated_orders.csv (bonus A)

Mismo formato. Lo produce `tools/generate_orders.py` con Faker y semilla fija (2026): 100 pedidos de 1 a 5
artículos con precios, cantidades (0-6), pesos, distancias (0-1500 km), códigos (incluido uno inválido) y tipo
de cliente aleatorios. Los valores esperados **no** salen de `src/order_calculator.py`: los calcula un oráculo
independiente dentro del generador con fracciones exactas. Regenerarlo:

```bash
pip install Faker
python tools/generate_orders.py --count 100 --seed 2026
```

## Validación de los datos

`src/data_files.py` revisa los archivos antes de usarlos (bonus C). Antes de correr cualquier prueba,
`tests/conftest.py` valida toda la carpeta; si hay errores, pytest se detiene y lista cada problema así:

```
Invalid test data (2 problem(s)):
  order_calculations.csv:14: is_express must be true or false, got 'yes'
  customer_validation.json:212: invalid_zip: is_valid contradicts the errors list
```

| Archivo | Se verifica |
| ------- | ----------- |
| CSV | columnas requeridas, número de columnas por fila, `test_name` no vacío ni repetido, `items` como JSON con los 4 campos, `customer_type`, `discount_code` no vacío, números válidos, `true`/`false`, y que una fila con `expected_error` no tenga montos |
| customer JSON | JSON válido, lista, `test_name` único, `customer` objeto, `is_valid` booleano, `errors` lista y coherente con `is_valid` |
| workflows JSON | JSON válido, lista `workflows`, cada flujo con `name` y pasos con `action` y `expected` |

Para el CSV la línea es la del archivo (encabezado = línea 1). Para JSON es la línea donde aparece el
`test_name` del caso, o la que reporta el parser si el JSON está mal formado.

También se puede correr a mano: `python src/data_files.py test_data`.

## Cómo agregar un caso

1. Agrega una fila al CSV o un objeto al JSON con un `test_name` nuevo.
2. Calcula el resultado esperado a mano con las reglas de arriba (no con el código que se está probando).
3. Corre `pytest`: el validador revisa el formato y el caso aparece como una prueba más con su nombre.
