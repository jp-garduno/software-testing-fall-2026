# Especificación de datos de prueba

Todos los archivos se codifican en UTF-8. Los valores monetarios esperados están
redondeados a dos decimales. `src/data_validation.py` verifica los esquemas antes
de ejecutar las pruebas y reporta errores de CSV por número de línea.

## `test_data/order_calculations.csv`

CSV con encabezado y 34 registros. La columna `items` contiene un arreglo JSON
entrecomillado; cada artículo tiene `name`, `price`, `quantity` y `weight`.

| Campo               | Tipo               | Significado                                    |
| ------------------- | ------------------ | ---------------------------------------------- |
| `test_name`         | texto              | Identificador único/descriptivo del caso       |
| `items`             | arreglo JSON       | Artículos del pedido                           |
| `customer_type`     | `new` / `regular`  | Elegibilidad de `NEWUSER`                      |
| `discount_code`     | código o `NONE`    | Código que se intenta aplicar                  |
| `distance_km`       | número no negativo | Distancia de envío                             |
| `is_express`        | `true` / `false`   | Multiplicador de envío express                 |
| `expected_subtotal` | número             | Suma de precio por cantidad                    |
| `expected_discount` | número             | Descuento aplicado                             |
| `expected_tax`      | número             | 8% del subtotal menos descuento                |
| `expected_shipping` | número             | Peso, distancia y velocidad                    |
| `expected_total`    | número             | Subtotal menos descuento más impuestos y envío |

Los 34 registros cubren pedidos simples, los cuatro códigos, sus límites,
impuestos, peso/distancia, express, envío gratis, varios artículos, cantidades
cero, importes altos y redondeos.

## `test_data/customer_validation.json`

Arreglo de 33 objetos. Cada registro contiene:

- `test_name`: identificador del escenario.
- `customer`: `email`, `phone`, `billing_address` y `credit_card`. La dirección
  usa `street`, `city`, `state` y `zip`; la tarjeta usa `number`, `expiration`
  (`MM/YYYY`) y `cvv`.
- `expected`: `is_valid` booleano y `errors`, lista ordenada de errores exactos.

Las categorías incluyen clientes válidos, formatos incorrectos, errores de
dirección, algoritmo de Luhn, expiración, CVV y múltiples errores simultáneos.
Las fechas de prueba de expiración se evalúan contra el 11 de noviembre de 2026,
por lo que los casos son reproducibles.

## `test_data/order_workflows.json`

Objeto con la propiedad `workflows`, una lista de cuatro flujos. Cada flujo tiene
un nombre y una lista ordenada de pasos. Acciones soportadas:

- `validate_customer`: comprueba `valid` y `errors`.
- `create_order`: crea el pedido después de validar al cliente.
- `calculate_total`: comprueba el desglose esperado.
- `process_payment`: simula aprobación, rechazo o bloqueo.

Los flujos cubren pago exitoso, envío gratis express, rechazo por cliente
inválido y pago declinado. No se realizan llamadas de red.
