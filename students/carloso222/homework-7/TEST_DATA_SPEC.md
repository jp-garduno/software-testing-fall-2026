# Especificación de los datos de prueba

Todos los archivos están en `test_data/`, codificados en UTF-8. Los valida automáticamente
`src/data_validator.py` al iniciar `pytest` (bonus C): si falta un campo o un tipo es
incorrecto, la ejecución se detiene con un reporte `archivo:línea: mensaje`.

## Reglas de negocio y decisiones

| Tema                          | Decisión                                                                                                                                                                                                                                                                                                                           |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Umbral de `SAVE10` / `SAVE20` | El subtotal debe ser **estrictamente mayor** a 50 / 100 (el texto del enunciado dice "> $50"; el código de ejemplo usaba `<` y aceptaría exactamente 50). Un subtotal de 50.00 **no** recibe descuento; 50.01 sí. Los casos `*_at_threshold_rejected` lo cubren.                                                                   |
| `NEWUSER`                     | 15 % de descuento, válido **solo** para `customer_type = "new"`. Para un cliente `regular` el código se rechaza (`apply_discount` devuelve `False`, descuento 0).                                                                                                                                                                  |
| `FREESHIP`                    | Descuento 0 y envío 0 (también con envío exprés).                                                                                                                                                                                                                                                                                  |
| Códigos inválidos             | Cualquier código desconocido (o en minúsculas, p. ej. `save10`) no da descuento. Un código rechazado no borra uno ya aplicado.                                                                                                                                                                                                     |
| Un solo código                | Un pedido admite un único código de descuento.                                                                                                                                                                                                                                                                                     |
| Impuesto                      | 8 % de (subtotal - descuento), con el descuento ya redondeado a centavos.                                                                                                                                                                                                                                                          |
| Peso del envío                | `peso_total = Σ (weight × quantity)` en kg; `weight` es por unidad.                                                                                                                                                                                                                                                                |
| Envío                         | `0.50 × peso_total + 0.10 × distancia_km`; exprés = `× 1.5`; `FREESHIP` = 0.                                                                                                                                                                                                                                                       |
| Redondeo                      | Cada componente (subtotal, descuento, impuesto, envío) se redondea a 2 decimales **half-up** con `Decimal`. `total = subtotal - descuento + impuesto + envío` usando los componentes ya redondeados, así el desglose siempre suma.                                                                                                 |
| Cantidad cero                 | Válida: la línea aporta 0 al subtotal y al peso (caso `complex_zero_quantity_line`). Un pedido sin artículos da todo en 0.                                                                                                                                                                                                         |
| Valores negativos             | `price`, `quantity`, `weight` o `distance_km` negativos lanzan `ValueError` (no caben en el CSV porque no tienen totales esperados; se prueban en `test_order_calculator.py` y en el flujo `negative_price_order_rejected`). Una cantidad no entera, o un `customer_type` distinto de `new`/`regular`, también lanza `ValueError`. |
| Ejemplo del enunciado         | La fila de ejemplo del enunciado (artículo de 50, 1 kg, 10 km) indica envío 5.50, pero con la fórmula del propio enunciado el envío es 0.50×1 + 0.10×10 = **1.50** (total 55.50, no 59.50). Se siguió la fórmula; el caso quedó como `shipping_statement_example`.                                                                 |
| Fecha de referencia           | La validación de vencimiento recibe `today`. Las pruebas usan siempre `2026-01-15` (`REFERENCE_DATE` en `tests/data_loader.py` y `reference_date` en `order_workflows.json`). Una tarjeta es válida hasta el último día de su mes de vencimiento: `01/2026` es válida, `12/2025` está vencida.                                     |

## `order_calculations.csv` (33 filas)

Cabecera fija, separador coma, comillas dobles para campos con comas. Las filas se leen con `csv.DictReader`.

| Columna                                                                                         | Tipo                   | Descripción                                                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `test_name`                                                                                     | texto único            | Nombre del caso; también es el id de pytest. Prefijo = categoría.                                                                                                                                                       |
| `items`                                                                                         | JSON en una celda      | Lista de `{"name": str, "price": número, "quantity": entero, "weight": número}`. Las comillas dobles internas se escapan duplicándolas (`""`) según la regla del CSV; tras leer la celda es JSON válido (`json.loads`). |
| `customer_type`                                                                                 | `new` \| `regular`     | Tipo de cliente.                                                                                                                                                                                                        |
| `discount_code`                                                                                 | texto                  | Código o `NONE` si no hay código.                                                                                                                                                                                       |
| `distance_km`                                                                                   | número >= 0            | Distancia de envío.                                                                                                                                                                                                     |
| `is_express`                                                                                    | `true` \| `false`      | Envío exprés.                                                                                                                                                                                                           |
| `expected_subtotal`, `expected_discount`, `expected_tax`, `expected_shipping`, `expected_total` | número con 2 decimales | Valores esperados, calculados a mano.                                                                                                                                                                                   |
| `category`                                                                                      | texto                  | Columna extra (no la usa el cargador): `simple`, `discount`, `tax`, `shipping`, `complex`.                                                                                                                              |

Casos por categoría: simple 3, descuentos 9, impuesto 5, envío 9, complejos 7 (total 33).
Los "valores máximos" son `9999.99 × 100` con 20 000 km (`complex_maximum_values`).

## `customer_validation.json` (37 casos)

Lista de objetos:

```json
{
  "test_name": "invalid_email_missing_at",
  "customer": {
    "email": "...",
    "phone": "(555) 123-4567",
    "billing_address": {
      "street": "...",
      "city": "...",
      "state": "NY",
      "zip": "10001"
    },
    "credit_card": { "number": "...", "expiration": "12/2030", "cvv": "123" }
  },
  "expected": { "is_valid": false, "errors": ["Invalid email format"] }
}
```

| Campo               | Tipo            | Notas                                                                                            |
| ------------------- | --------------- | ------------------------------------------------------------------------------------------------ |
| `test_name`         | texto           | Nombre y id de pytest.                                                                           |
| `customer`          | objeto          | Datos del cliente (todo texto). Puede estar incompleto (`{}`): lo que falta es inválido.         |
| `expected.is_valid` | booleano        |                                                                                                  |
| `expected.errors`   | lista de textos | En orden fijo: email, teléfono, calle, ciudad, estado, zip, número de tarjeta, vencimiento, CVV. |

Mensajes de error: `Invalid email format`, `Invalid phone format`, `Invalid street address`,
`Invalid city`, `Invalid state`, `Invalid zip code`, `Invalid credit card number`,
`Invalid expiration date format`, `Credit card expired`, `Invalid CVV`.

Reglas: email `local@dominio.tld` sin espacios ni puntos consecutivos; teléfono exactamente
`(XXX) XXX-XXXX`; calle y ciudad no vacías; estado de 2 letras MAYÚSCULAS (50 estados + DC);
zip de 5 dígitos o ZIP+4 (`12345-6789`); tarjeta solo dígitos (sin espacios ni guiones), 13 a 19
dígitos y suma de Luhn; vencimiento `MM/AAAA` con mes 01-12 y no pasado; CVV de 3 o 4 dígitos.

Categorías (por prefijo): `valid_*` 4, `invalid_email_*` 5, `invalid_phone_*` 5,
`invalid_address_*` 6, `invalid_card_*` 11, `multiple_errors_*` 6 (incluye el cliente vacío `{}`).

## `order_workflows.json` (7 flujos)

```json
{
  "reference_date": "2026-01-15",
  "workflows": [
    {
      "name": "...",
      "description": "...",
      "steps": [
        {
          "action": "validate_customer",
          "data": { "...": "..." },
          "expected": { "valid": true, "errors": [] }
        },
        {
          "action": "create_order",
          "data": {
            "items": [],
            "customer_type": "regular",
            "discount_code": "SAVE10",
            "distance_km": 10,
            "is_express": false
          },
          "expected": { "status": "created" }
        },
        { "action": "calculate_total", "expected": { "total": 79.76 } },
        {
          "action": "process_payment",
          "expected": { "status": "success", "amount": 79.76 }
        }
      ]
    }
  ]
}
```

| Campo              | Tipo                                                                            | Notas                                                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `reference_date`   | `YYYY-MM-DD`                                                                    | "Hoy" para el vencimiento de tarjetas.                                                                                                                  |
| `workflows[].name` | texto único                                                                     | Id de pytest.                                                                                                                                           |
| `steps[].action`   | `validate_customer` \| `create_order` \| `calculate_total` \| `process_payment` |                                                                                                                                                         |
| `steps[].data`     | objeto                                                                          | Obligatorio en `validate_customer` (el cliente) y `create_order` (`items`, y opcionales `customer_type`, `discount_code`, `distance_km`, `is_express`). |
| `steps[].expected` | objeto                                                                          | **Subconjunto** del resultado: solo se comparan las claves listadas (los números con tolerancia de 0.005).                                              |

Resultados posibles: `create_order` -> `created` o `rejected` (con `reason`);
`calculate_total` -> desglose o `failed`; `process_payment` -> `success`, `declined`
(`Invalid payment information`: cliente no validado o inválido) o `failed` (`No order created`).
Flujos: 3 exitosos, 2 con pago rechazado (tarjeta con Luhn inválido y tarjeta vencida), 1 pago sin pedido y 1 pedido rechazado por precio negativo.

## `generated_orders.csv` (100 filas, bonus A)

Mismas columnas que `order_calculations.csv` (`category` = `generated`). Generado con
`python -m src.order_generator` (semilla 2026, Faker para los nombres de artículo). Los valores
esperados son una **instantánea de regresión** calculada con `Order` (no se verificaron a mano):
sirven para detectar cambios de comportamiento, mientras que `order_calculations.csv`
es el conjunto con valores verificados a mano. `NEWUSER` solo se genera para clientes `new`.

## Convenciones

- Nombres en `snake_case` y con prefijo de categoría; un nombre describe condición y resultado.
- Los datos no dependen del reloj, la zona horaria ni el directorio de trabajo.
- Números de tarjeta de prueba públicos (Visa `4111111111111111`, Mastercard `5500000000000004`,
  Amex `378282246310005`); no son tarjetas reales.
