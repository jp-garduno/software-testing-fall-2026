# Especificación de los datos de prueba

Este documento describe el formato de los archivos de `test_data/`, las reglas de negocio que asumí
y las convenciones que usé para nombrar y organizar los casos.

## 1. Interpretación de las reglas (decisiones tomadas)

| #  | Regla                                                           | Decisión                                                                                                                                                          |
|----|-----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | Mínimo de `SAVE10` ($50) y `SAVE20` ($100)                      | **Inclusivo**: con exactamente $50 / $100 sí aplica (estilo Amazon). El enunciado dice "> $50", pero su código de ejemplo rechaza solo si `subtotal < min_order`. |
| 2  | Peso del envío                                                  | `peso × cantidad` de cada producto, sumado. Si un producto no trae `weight`, cuenta como 0.                                                                       |
| 3  | Valores incorrectos                                             | Lanzan una **excepción** (no se crea/calcula el pedido).                                                                                                          |
| 4  | Precio negativo                                                 | Error: `El precio y la cantidad no deben ser negativos`.                                                                                                          |
| 5  | Cantidad negativa                                               | Error: `El precio y la cantidad no deben ser negativos`.                                                                                                          |
| 6  | Precio 0                                                        | Error: `El precio debe ser mayor que cero`.                                                                                                                       |
| 7  | Cantidad 0                                                      | **Válida**: el producto no se suma al subtotal ni al peso (pedido vacío = total 0 más envío por distancia).                                                       |
| 8  | Peso negativo                                                   | Error: `El peso no debe ser negativo`.                                                                                                                            |
| 9  | Distancia negativa                                              | Error: `La distancia no debe ser negativa` (se genera en `setShipping`).                                                                                          |
| 10 | Precio/cantidad que no son números, o `items` que no es arreglo | Error: `El precio y la cantidad deben ser números` / `Los productos deben ser un arreglo`.                                                                        |
| 11 | Redondeo                                                        | Cada monto (subtotal, descuento, impuesto, envío, total) se redondea a 2 decimales.                                                                               |
| 12 | `NEWUSER`                                                       | Solo aplica a `customer_type = "new"`; en un cliente regular no da descuento.                                                                                     |
| 13 | Código inexistente                                              | No da descuento y no lanza error.                                                                                                                                 |
| 14 | Fecha en pruebas de tarjeta                                     | Las pruebas usan la fecha fija `2026-11-11` para que no dependan del día en que se corren.                                                                        |

## 2. `order_calculations`: `test_data/orderCalculations.csv` (40 casos)

Una fila por caso. La primera fila es el encabezado. Los textos con comas van entre comillas dobles.

| Columna             | Tipo                              | Valores permitidos / formato                                                          |
|---------------------|-----------------------------------|---------------------------------------------------------------------------------------|
| `test_name`         | texto                             | Nombre descriptivo en español. Los casos que deben fallar empiezan con `(invalida)`.  |
| `items`             | texto (JSON con comillas simples) | `[{'name':'A','price':50,'quantity':1,'weight':1}]`. Puede ser `[]`.                  |
| `customer_type`     | texto                             | `new` o `regular`.                                                                    |
| `discount_code`     | texto                             | `NONE`, `SAVE10`, `SAVE20`, `FREESHIP`, `NEWUSER` o cualquier otro (código inválido). |
| `distance_km`       | número                            | Distancia en km. Un valor negativo es un caso de error.                               |
| `is_express`        | texto                             | `true` o `false`.                                                                     |
| `expected_subtotal` | número o `ERROR`                  | Con 2 decimales. **`ERROR`** indica que el pedido debe lanzar una excepción.          |
| `expected_discount` | número                            | Con 2 decimales (`0.00` en casos `ERROR`).                                            |
| `expected_tax`      | número                            | Con 2 decimales (`0.00` en casos `ERROR`).                                            |
| `expected_shipping` | número                            | Con 2 decimales (`0.00` en casos `ERROR`).                                            |
| `expected_total`    | número                            | Con 2 decimales (`0.00` en casos `ERROR`).                                            |

### Categorías y cantidad de casos

| Categoría                                                                                                                                                                  | Mínimo pedido | Casos  |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|--------|
| Pedidos simples                                                                                                                                                            | 3             | 7      |
| Validación de descuentos (límites, códigos inválidos, varios productos)                                                                                                    | 5             | 7      |
| Cálculo de impuestos                                                                                                                                                       | 4             | 4      |
| Cálculo de envío (peso, distancia, exprés, FREESHIP)                                                                                                                       | 6             | 6      |
| Pedidos complejos (varios productos, cantidad 0, valores máximos)                                                                                                          | 7             | 7      |
| Casos inválidos (`(invalida)`: precio -1, precio 0, cantidad -1, peso -2, distancia -50, precio no numérico, items no es arreglo, producto no es objeto, peso no numérico) | n/a           | 9      |
| **Total**                                                                                                                                                                  | **25**        | **40** |

## 3. `test_data/100PruebasAlAzar.csv` (100 casos generados)

- Mismo formato que `orderCalculations.csv`; los nombres son `generated_1` ... `generated_100`.
- Lo crea `test_data/generateOrders.js` con Faker: 1 a 4 productos, precios de 5 a 150, cantidades de 1 a 5,
  pesos de 0.1 a 5, distancia de 0 a 200 km, código y tipo de cliente al azar.
- **Siempre son pedidos válidos** (valores positivos), por lo que ninguno es un caso `ERROR`.
- Se genera sin semilla: cada ejecución de `npm run test:generate` produce datos distintos.
- Los valores esperados se calculan dentro del generador con las mismas reglas del negocio.

## 4. `customer_validation`: `test_data/customerValidation.json` (32 casos)

Arreglo de objetos con esta estructura:

```json
{
  "test_name": "(invalido) email sin arroba",
  "category": "email invalido",
  "customer": {
    "email": "invalid-email",
    "phone": "(555) 123-4567",
    "billing_address": { "street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001" },
    "credit_card": { "number": "4532015112830366", "expiration": "12/2030", "cvv": "123" }
  },
  "expected": { "is_valid": false, "errors": ["Formato de correo electrónico inválido"] }
}
```

| Campo                      | Tipo             | Descripción                                                                                                                 |
|----------------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `test_name`                | texto            | Nombre en español; `(invalido)` al inicio si el cliente no es válido.                                                       |
| `category`                 | texto            | Una de las 6 categorías de abajo (campo extra que agregué para poder contar y agrupar).                                     |
| `customer.email`           | texto            | Debe cumplir `algo@dominio.ext`, sin espacios.                                                                              |
| `customer.phone`           | texto            | Formato `(XXX) XXX-XXXX`.                                                                                                   |
| `customer.billing_address` | objeto           | `street` y `city` no vacíos; `state` = 2 letras mayúsculas; `zip` = `12345` o `12345-6789`.                                 |
| `customer.credit_card`     | objeto           | `number` 13 a 19 dígitos que pasen Luhn; `expiration` `MM/YYYY` no vencida (vale hasta fin de mes); `cvv` de 3 o 4 dígitos. |
| `expected.is_valid`        | booleano         | `true` solo si `errors` está vacío.                                                                                         |
| `expected.errors`          | arreglo de texto | Mensajes **en el orden** en que se validan (email, teléfono, dirección, tarjeta).                                           |

Mensajes posibles: `Formato de correo electrónico inválido`, `Formato de teléfono inválido`,
`Calle inválida`, `Ciudad inválida`, `Estado inválido`, `Código postal inválido`,
`Número de tarjeta de crédito inválido`, `Formato de fecha de vencimiento inválido`,
`Tarjeta de crédito vencida`, `CVV inválido`.

| Categoría (`category`) | Mínimo pedido | Casos  |
|------------------------|---------------|--------|
| `valido`               | 3             | 3      |
| `email invalido`       | 4             | 4      |
| `telefono invalido`    | 4             | 4      |
| `direccion invalida`   | 5             | 5      |
| `tarjeta invalida`     | 8             | 10     |
| `errores multiples`    | 6             | 6      |
| **Total**              | **30**        | **32** |

## 5. `order_workflows`: `test_data/orderWorkflows.json` (5 flujos)

Objeto con la clave `workflows`; cada flujo tiene `name` y una lista ordenada de `steps`.

| `action`            | `data`                                                                 | `expected` (ejemplos)                                                              |
|---------------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| `validate_customer` | cliente con el formato de la sección 4                                 | `{ "valid": true, "errors": [] }`                                                  |
| `create_order`      | `items`, `customer_type`, `discount_code`, `distance_km`, `is_express` | `{ "status": "created" }` o `{ "status": "rejected" }` si el cliente no fue válido |
| `calculate_total`   | (sin `data`)                                                           | `{ "subtotal", "discount", "tax", "shipping", "total" }` o `{ "error": "..." }`    |
| `process_payment`   | (sin `data`)                                                           | `{ "status": "success", "amount": 94.47 }` o `{ "status": "not_processed" }`       |

Los números se comparan con 2 decimales; el resto, por igualdad exacta.

| Flujo                                        | Tipo                                         |
|----------------------------------------------|----------------------------------------------|
| pedido completo con SAVE20 y envio estandar  | válido                                       |
| cliente nuevo con NEWUSER y envio expres     | válido                                       |
| pedido con FREESHIP y varios productos       | válido                                       |
| (invalida) cliente con email y CVV invalidos | inválido: el pedido se rechaza y no se cobra |
| (invalida) pedido con precio negativo        | inválido: el total lanza error y no se cobra |

## 6. Convenciones

- Los nombres de caso están en español, descriptivos, y los negativos llevan el prefijo `(invalido)` / `(invalida)`.
- Los archivos de datos están en `test_data/` y las pruebas los leen con rutas relativas a `__dirname`.
- `npm run test:validate` revisa los tres archivos (campos requeridos, tipos y número de línea / caso).
