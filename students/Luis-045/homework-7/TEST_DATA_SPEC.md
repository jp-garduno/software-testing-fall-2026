# Especificación de datos de prueba

Los archivos viven en `test_data/` y usan UTF-8. Las expectativas son valores
fijos calculados a partir de las reglas del enunciado. El lector de pruebas
no usa el código de producción para calcular los resultados esperados.

## `order_calculations.csv`

Una fila representa un pedido. La columna `items` contiene un arreglo JSON
de objetos con `name`, `price`, `quantity` y `weight`. El peso se expresa
en kg por unidad. Cuando el JSON va entre comillas del CSV, cada comilla
interior se duplica, por ejemplo:

```csv
"[{""name"":""Item1"",""price"":50,""quantity"":1,""weight"":1}]"
```

| Columna | Tipo y significado |
| --- | --- |
| `test_name` | Nombre único que pytest usa como ID. |
| `category` | `simple`, `discount`, `tax`, `shipping` o `complex`. |
| `items` | Arreglo JSON. Precio y peso son números; cantidad es un entero. |
| `customer_type` | `regular` o `new`. |
| `discount_code` | Código del cupón, o `NONE` si no se aplica ninguno. |
| `distance_km` | Distancia numérica en km. |
| `is_express` | `true` o `false`. |
| `expected_subtotal`, `expected_discount`, `expected_tax`, `expected_shipping`, `expected_total` | Importes en dólares con dos decimales. Vacíos si se espera un error. |
| `expected_discount_applied` | `true` o `false` para un cupón proporcionado. Vacío si no hay cupón o la entrada es inválida. |
| `expected_error` | Mensaje exacto de `ValueError` en entradas inválidas. Vacío para un cálculo normal. |
| `comparison` | `true` si la fila pertenece a la suite de comparación. |

Distribución: 3 pedidos simples, 9 de descuentos, 4 de impuestos, 6 de envío
y 8 complejos. Los casos complejos incluyen cantidad cero, valores negativos
y un pedido de gran magnitud.

## `customer_validation.json`

Arreglo de objetos con `test_name` único, `category`, `customer` y
`expected`. Un cliente válido tiene `email`, `phone` en formato
`(XXX) XXX-XXXX`, `billing_address` con `street`, `city`, `state` y
`zip`, y `credit_card` con `number`, `expiration` (`MM/YYYY`) y
`cvv` opcional. Los datos de tarjeta son de prueba. El código postal se
mantiene como texto para preservar ceros iniciales.

`expected` contiene `is_valid` (booleano) y `errors` (lista de mensajes
en el orden contacto, domicilio y tarjeta). Para los casos inválidos se
pueden omitir campos o usar `null` deliberadamente. La fecha de referencia
de esta suite es el 10 de noviembre de 2026.

Distribución: 3 clientes válidos, 4 emails inválidos, 4 teléfonos inválidos,
5 domicilios inválidos, 8 tarjetas inválidas, 6 clientes con varios errores y
1 registro nulo.

## `order_workflows.json`

El objeto raíz contiene `reference_date` en formato ISO (`YYYY-MM-DD`) y
el arreglo `workflows`. Cada flujo tiene `name`, `order_id` y una lista
ordenada de `steps`. Se crea una sesión de checkout por flujo.

Cada paso tiene `action`, un objeto opcional `data` con argumentos por
nombre y exactamente una expectativa: `expected` con la respuesta completa,
o `expected_error` con el mensaje de `ValueError`.

| Acción | Entrada en `data` | Resultado esperado |
| --- | --- | --- |
| `validate_customer` | `customer`, con el formato descrito arriba | `valid` y `errors` |
| `create_order` | `items`; opcionales: `customer_type`, `discount_code` y `shipping` con `distance_km` e `is_express` | `status: "created"` y `discount_applied` |
| `calculate_total` | Ninguna | `subtotal`, `discount`, `tax`, `shipping` y `total` |
| `process_payment` | `approved` opcional (por defecto `true`) | `status: "success"` con `amount`, o `status: "declined"` |
| `confirm_order` | Ninguna | `status: "confirmed"`, `order_id` y `total` |

Los seis flujos cubren envío estándar, descuento de primera compra con
envío exprés, envío gratis con reintento de pago, configuración de envío
por defecto, rechazo del cliente y rechazo de un pedido inválido.
