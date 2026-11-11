# Especificación de Datos de Prueba

Este documento describe el formato de cada archivo de `test_data/`, los valores permitidos y las reglas de negocio que se usaron para calcular los resultados esperados.

| Archivo                    | Formato | Casos       | Lo usa                                                  |
| -------------------------- | ------- | ----------- | ------------------------------------------------------- |
| `order_calculations.csv`   | CSV     | 37          | `test_order_calculator.py`, `test_order_data_driven.py` |
| `customer_validation.json` | JSON    | 38          | `test_customer_validator.py`                            |
| `order_workflows.json`     | JSON    | 7 workflows | `test_integration.py`                                   |
| `generated_orders.csv`     | CSV     | 100         | `test_generated_orders.py` (Bonus A)                    |

Todos los archivos usan codificación **UTF-8** y terminan con salto de línea. Su formato se puede revisar con `python src/data_validator.py`.

---

## 1. `order_calculations.csv`

Cada fila es una orden. Las columnas `expected_*` tienen el resultado que debe dar `Order.calculate_total()`.

### Columnas

| Columna             | Tipo             | Valores permitidos        | Descripción                                |
| ------------------- | ---------------- | ------------------------- | ------------------------------------------ |
| `test_name`         | texto            | único, sin espacios       | Nombre del caso; pytest lo muestra como id |
| `items`             | lista JSON       | ver abajo                 | Productos de la orden                      |
| `customer_type`     | texto            | `new`, `regular`          | Tipo de cliente                            |
| `discount_code`     | texto            | `NONE` o cualquier código | `NONE` = no se aplica código               |
| `distance_km`       | número           | ≥ 0                       | Distancia de envío en km                   |
| `is_express`        | texto            | `true`, `false`           | Envío express (en minúsculas)              |
| `expected_subtotal` | número o `ERROR` | 2 decimales               | Subtotal esperado                          |
| `expected_discount` | número o `ERROR` | 2 decimales               | Descuento esperado                         |
| `expected_tax`      | número o `ERROR` | 2 decimales               | Impuesto esperado                          |
| `expected_shipping` | número o `ERROR` | 2 decimales               | Envío esperado                             |
| `expected_total`    | número o `ERROR` | 2 decimales               | Total esperado                             |

### Columna `items`

Es una lista JSON escrita con **comillas simples**, para que el CSV sea legible. El test la convierte con `.replace("'", '"')` antes de `json.loads`.

```
"[{'name':'Laptop','price':80,'quantity':1,'weight':2},{'name':'Mouse','price':15,'quantity':2,'weight':0.2}]"
```

| Campo      | Tipo   | Descripción                          |
| ---------- | ------ | ------------------------------------ |
| `name`     | texto  | Nombre del producto (sin apóstrofes) |
| `price`    | número | Precio unitario en USD               |
| `quantity` | entero | Cantidad (0 está permitido)          |
| `weight`   | número | Peso **unitario** en kg              |

La lista vacía `[]` representa un carrito vacío.

### Filas `ERROR`

Si las 5 columnas `expected_*` dicen `ERROR`, el caso tiene una entrada inválida y el test espera que se lance `ValueError`. Esto pasa con:

- `price`, `quantity` o `weight` negativos
- `distance_km` negativo
- `customer_type` distinto de `new` o `regular`

Las 5 columnas tienen que decir `ERROR` a la vez; el validador marca como error una fila con solo algunas.

### Categorías (prefijo de `test_name`)

| Prefijo     | Casos | Qué cubre                                                                                                        |
| ----------- | ----- | ---------------------------------------------------------------------------------------------------------------- |
| `simple_`   | 3     | Sin descuento ni envío                                                                                           |
| `discount_` | 9     | Códigos en el mínimo y debajo, código inválido, minúsculas, NEWUSER con cliente nuevo o regular, varios items    |
| `tax_`      | 4     | Montos redondos, después de descuento, redondeo, montos pequeños                                                 |
| `shipping_` | 7     | Solo peso, solo distancia, ambos, express, FREESHIP, FREESHIP + express, larga distancia                         |
| `complex_`  | 14    | Varios items + descuento + express, cantidad cero, orden vacía, valores máximos, decimales y las 5 filas `ERROR` |

### Ejemplo

```csv
test_name,items,customer_type,discount_code,distance_km,is_express,expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total
shipping_express,"[{'name':'Phone','price':300,'quantity':1,'weight':2}]",regular,NONE,30,true,300.00,0.00,24.00,6.00,330.00
complex_negative_price,"[{'name':'Bad','price':-10,'quantity':1,'weight':1}]",regular,NONE,10,false,ERROR,ERROR,ERROR,ERROR,ERROR
```

### Reglas de negocio usadas para calcular los esperados

| Concepto                                  | Regla                                                   |
| ----------------------------------------- | ------------------------------------------------------- |
| Subtotal                                  | Σ `price × quantity`                                    |
| SAVE10                                    | 10 % si el subtotal es **≥ $50**                        |
| SAVE20                                    | 20 % si el subtotal es **≥ $100**                       |
| NEWUSER                                   | 15 %, **solo** si `customer_type = new`                 |
| FREESHIP                                  | Envío = $0 (no descuenta del subtotal)                  |
| Código inválido o que no cumple el mínimo | Descuento = $0, no lanza error                          |
| Impuesto                                  | 8 % de (subtotal − descuento)                           |
| Envío                                     | (Σ `weight × quantity`) × $0.50 + `distance_km` × $0.10 |
| Express                                   | Envío × 1.5                                             |
| Total                                     | subtotal − descuento + impuesto + envío                 |
| Redondeo                                  | Cada componente se redondea a 2 decimales con `round()` |
| Tolerancia en los tests                   | ± $0.01 (`pytest.approx(abs=0.01)`)                     |

**Decisiones de diseño** (donde el enunciado era ambiguo):

1. **Mínimo inclusivo.** El texto dice "> $50", pero el código base del enunciado rechaza solo si `subtotal < min_order`. Se respetó el código, así que $50.00 exactos sí califica para SAVE10. Los casos `discount_save10_at_threshold` y `discount_save10_below_min` ($49.99) prueban el límite.
2. **NEWUSER revisa el tipo de cliente.** El código base no lo hacía, pero la regla dice "first order".
3. **El peso es unitario**, así que se multiplica por `quantity`.
4. **El ejemplo del enunciado no cuadra con las reglas.** Para `simple_order` (1 kg, 10 km) el enunciado da `shipping = 5.50`, pero con las reglas publicadas da `0.5 + 1.0 = 1.50`. Se usaron las reglas.
5. **Tolerancia absoluta.** Se cambió `rel=1e-2` por `abs=0.01`. Con `rel`, un valor esperado de 0 exige una coincidencia exacta, y en totales grandes se aceptan errores de varios dólares.

---

## 2. `customer_validation.json`

Una lista de casos. Cada caso tiene un cliente y el resultado esperado de `validate_customer()`.

### Estructura

```json
[
  {
    "test_name": "valid_customer_all_fields",
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
        "expiration": "12/2030",
        "cvv": "123"
      }
    },
    "expected": {
      "is_valid": true,
      "errors": []
    }
  }
]
```

| Campo               | Tipo            | Requerido | Descripción                                                         |
| ------------------- | --------------- | --------- | ------------------------------------------------------------------- |
| `test_name`         | texto           | sí, único | Nombre del caso                                                     |
| `customer`          | objeto          | sí        | Datos del cliente; cualquier campo puede faltar para probar errores |
| `expected.is_valid` | booleano        | sí        | `true` solo si `errors` está vacío                                  |
| `expected.errors`   | lista de textos | sí        | Errores esperados, **en orden**                                     |

### Reglas de validación

| Campo                             | Válido si…                                                                                   |
| --------------------------------- | -------------------------------------------------------------------------------------------- |
| `email`                           | Tiene la forma `usuario@dominio.tld`, sin espacios ni `..`, y el TLD tiene al menos 2 letras |
| `phone`                           | Formato exacto `(XXX) XXX-XXXX`                                                              |
| `billing_address.street` / `city` | No están vacíos ni son solo espacios                                                         |
| `billing_address.state`           | Código de estado de EE. UU. en mayúsculas (50 estados + DC)                                  |
| `billing_address.zip`             | `12345` o `12345-6789`                                                                       |
| `credit_card.number`              | 13 a 19 dígitos y pasa el algoritmo de **Luhn**; se permiten espacios y guiones              |
| `credit_card.expiration`          | Formato `MM/YYYY`, mes 01–12, y no vencida (válida hasta el último día del mes)              |
| `credit_card.cvv`                 | 3 o 4 dígitos (Amex usa 4)                                                                   |

### Mensajes de error

Los errores siempre aparecen en este orden: **email → teléfono → dirección → tarjeta**.

| Mensaje                      | Cuándo aparece                                            |
| ---------------------------- | --------------------------------------------------------- |
| `Missing email`              | `email` falta o está vacío                                |
| `Invalid email format`       | `email` tiene formato incorrecto                          |
| `Missing phone`              | `phone` falta o está vacío                                |
| `Invalid phone format`       | `phone` tiene formato incorrecto                          |
| `Missing billing address`    | Falta todo `billing_address`                              |
| `Missing street`             | `street` está vacío                                       |
| `Missing city`               | `city` está vacío                                         |
| `Invalid state`              | `state` no es un estado válido                            |
| `Invalid zip code`           | `zip` tiene formato incorrecto                            |
| `Missing credit card`        | Falta todo `credit_card`                                  |
| `Invalid credit card number` | Longitud incorrecta, caracteres no numéricos o falla Luhn |
| `Invalid expiration format`  | No es `MM/YYYY` o el mes no existe                        |
| `Credit card expired`        | La fecha ya pasó                                          |
| `Invalid CVV`                | No tiene 3 o 4 dígitos                                    |

### Fecha de referencia

Los tests validan la expiración con una **fecha fija: 10 de noviembre de 2026** (`REFERENCE_DATE`). Así, una tarjeta como `12/2030` no deja de ser válida con el paso del tiempo. La tarjeta del ejemplo del enunciado (`12/2025`) se cambió a `12/2030`, porque con esa fecha de referencia ya estaría vencida.

### Categorías

| Prefijo            | Casos | Mínimo pedido |
| ------------------ | ----- | ------------- |
| `valid_customer_`  | 3     | 3             |
| `invalid_email_`   | 6     | 4             |
| `invalid_phone_`   | 5     | 4             |
| `invalid_address_` | 7     | 5             |
| `invalid_card_`    | 10    | 8             |
| `multiple_`        | 7     | 6             |

### Números de tarjeta de prueba usados

| Número             | Tipo       | Luhn                        |
| ------------------ | ---------- | --------------------------- |
| `4532015112830366` | Visa       | ✅                          |
| `4111111111111111` | Visa       | ✅                          |
| `5555555555554444` | Mastercard | ✅                          |
| `378282246310005`  | Amex       | ✅                          |
| `4532015112830367` | —          | ❌ (último dígito cambiado) |

Son números públicos de prueba; ninguno es una tarjeta real.

---

## 3. `order_workflows.json`

Flujos de compra de punta a punta. Cada workflow es una lista de pasos que se ejecutan **en orden** y comparten un contexto (el cliente validado y la orden creada).

### Estructura

```json
{
  "workflows": [
    {
      "name": "complete_order_flow",
      "description": "Texto libre que explica el flujo",
      "steps": [
        {
          "action": "validate_customer",
          "data": { "customer": { "...": "..." } },
          "expected": { "valid": true, "errors": [] }
        }
      ]
    }
  ]
}
```

| Campo              | Tipo   | Requerido       | Descripción                                   |
| ------------------ | ------ | --------------- | --------------------------------------------- |
| `name`             | texto  | sí              | Nombre del workflow (id en pytest)            |
| `description`      | texto  | no              | Explicación para humanos                      |
| `steps`            | lista  | sí, no vacía    | Pasos en orden                                |
| `steps[].action`   | texto  | sí              | Una de las acciones de la tabla siguiente     |
| `steps[].data`     | objeto | según la acción | Entrada del paso                              |
| `steps[].expected` | objeto | no              | Solo se comparan las llaves que aparecen aquí |

### Acciones

| `action`            | `data`                                     | Resultado que se puede verificar en `expected`      |
| ------------------- | ------------------------------------------ | --------------------------------------------------- |
| `validate_customer` | `customer` (mismo formato de la sección 2) | `valid`, `errors`                                   |
| `create_order`      | `items` (lista de items), `customer_type`  | `status`: `created` o `error`                       |
| `apply_discount`    | `code`                                     | `applied`: `true` / `false`                         |
| `set_shipping`      | `distance_km`, `is_express`                | `status`: `set`                                     |
| `calculate_total`   | —                                          | `subtotal`, `discount`, `tax`, `shipping`, `total`  |
| `process_payment`   | —                                          | `status`: `success` / `failed`; `amount` o `reason` |

### Reglas de `process_payment` (pago simulado)

Las reglas se revisan en este orden:

| Condición               | Resultado                                 |
| ----------------------- | ----------------------------------------- |
| No se creó la orden     | `failed`, `reason: "No order"`            |
| El cliente no es válido | `failed`, `reason: "Invalid customer"`    |
| Total ≤ $0              | `failed`, `reason: "Invalid order total"` |
| En otro caso            | `success`, `amount: <total>`              |

### Workflows incluidos

| Workflow                            | Resultado del pago          |
| ----------------------------------- | --------------------------- |
| `complete_order_flow`               | success, $110.62            |
| `new_customer_express_flow`         | success, $68.59             |
| `invalid_customer_payment_rejected` | failed, Invalid customer    |
| `rejected_discount_codes_flow`      | success, $88.65             |
| `freeship_heavy_express_flow`       | success, $486.00            |
| `empty_order_payment_rejected`      | failed, Invalid order total |
| `invalid_order_data_flow`           | failed, No order            |

---

## 4. `generated_orders.csv` (Bonus A)

Tiene **exactamente las mismas columnas** que `order_calculations.csv` y lo genera `src/data_generator.py`:

| Campo           | Rango generado                                                            |
| --------------- | ------------------------------------------------------------------------- |
| `test_name`     | `generated_001` … `generated_100`                                         |
| Items por orden | 1 a 5                                                                     |
| `name`          | Palabra aleatoria de Faker                                                |
| `price`         | $0.99 a $500.00                                                           |
| `quantity`      | 1 a 5                                                                     |
| `weight`        | 0.1 a 15 kg                                                               |
| `customer_type` | `new` o `regular`                                                         |
| `discount_code` | `NONE`, `SAVE10`, `SAVE20`, `FREESHIP`, `NEWUSER` o `EXPIRED5` (inválido) |
| `distance_km`   | 0 a 2000                                                                  |
| `is_express`    | `true` con 30 % de probabilidad                                           |

Los valores esperados se calcularon con la implementación actual de `Order` (técnica _golden master_), así que este archivo detecta **regresiones**: si un cambio futuro altera algún cálculo, los tests fallan. La semilla fija (`--seed 42`) hace que el archivo siempre sea el mismo.

**No edites este archivo a mano.** Para regenerarlo, corre `python src/data_generator.py`.

---

## 5. Convenciones generales

- **Nombres de test**: `snake_case`, con prefijo de categoría y descriptivos (`discount_save20_below_min`, no `test7`).
- **Montos**: en USD, con 2 decimales en los valores esperados.
- **Rutas**: los tests construyen las rutas a partir de su propio archivo, así que funcionan sin importar desde qué carpeta se corra `pytest`.
- **Valores especiales**: `NONE` en `discount_code` significa sin código; `ERROR` en las columnas `expected_*` significa que se espera `ValueError`.
- **Antes de hacer commit**: corre `python src/data_validator.py` para detectar archivos vacíos, JSON mal formado, columnas faltantes o tipos incorrectos, con el número de línea del problema.
