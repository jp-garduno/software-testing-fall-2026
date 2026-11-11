# Especificación de datos de prueba

Todos los archivos se guardan en UTF-8, con nombres de caso únicos. Las rutas
se resuelven desde `__file__`; las pruebas no dependen del directorio de llamada.
Los fixtures se validan en `pytest_sessionstart` y los lectores se usan también
durante la parametrización. Un archivo mal formado detiene la ejecución con un
diagnóstico `ruta:línea: motivo`.

## order_calculations.csv y generated_orders.csv

| Campo | Tipo / significado |
|---|---|
| test_name | Texto único usado como ID legible de pytest |
| category | simple, discount, tax, shipping, complex o generated |
| items | Array JSON válido de objetos name, price, quantity, weight; las comillas se escapan mediante CSV estándar |
| customer_type | new o regular |
| discount_code | Código exacto; NONE representa ausencia de cupón |
| distance_km | Número; valores negativos sólo para casos que esperan error |
| is_express | Literal true o false, en minúsculas |
| expected_subtotal / expected_discount / expected_tax / expected_shipping / expected_total | Oráculos monetarios numéricos; vacíos cuando se espera ValueError |
| expected_error | Vacío para éxito o ValueError para entrada inválida |

`price` y `weight` son números y `quantity` es entero. La validación de esquema
permite valores negativos intencionales para que el sistema compruebe las reglas
de negocio. Cada caso exitoso compara las cinco cantidades; los casos inválidos
comprueban la excepción. La tolerancia monetaria es absoluta de 0.000001, sin
tolerancia relativa que pueda esconder errores en importes grandes.

Distribución base: simple=3, discount=9, tax=4, shipping=6, complex=9. Incluye
49.99/50/50.01, 100/100.01, clientes nuevos/regulares, cupón inválido/expirado,
redondeo, peso por cantidad, envío gratuito/express y valores inválidos.

## customer_validation.json

Array de objetos `{test_name, category, customer, expected}`.
`customer` contiene email, phone, billing_address (street, city, state, zip) y
credit_card (number, expiration, cvv). `expected` es exactamente
`{is_valid: boolean, errors: [texto, ...]}`. Se comprueba toda la lista de
errores en orden: email, teléfono, calle, ciudad, estado, ZIP, número de tarjeta,
caducidad y CVV. No se descartan errores adicionales.

Distribución: 3 clientes válidos, 4 emails inválidos, 4 teléfonos inválidos,
5 direcciones inválidas, 8 tarjetas inválidas y 6 casos de errores múltiples.
Fecha fija de prueba: 2026-11-10. Las fechas de los datos no se actualizan para
hacer pasar pruebas; se inyecta el reloj de referencia.

## order_workflows.json

Objeto con `reference_date` ISO y array `workflows`. Cada flujo tiene name,
order_id, payment_approved, steps y expected_payment_calls. Cada paso incluye
`action`, un objeto `data` si requiere entradas y `expected` con la salida
completa. Acciones: validate_customer, create_order, calculate_total,
process_payment y confirmation. Las compras completas recorren las cinco
etapas y verifican además idempotencia del pago. Los flujos negativos muestran
bloqueo por cliente inválido y pago rechazado. El mock sólo recibe el total,
nunca una tarjeta real; se verifican número y argumentos de todas las llamadas.

## Calidad y reproducción

`scripts/build_fixtures.py` guarda las expectativas del conjunto base como
literales revisables, independientes del código de producción. Los casos de
Faker usan semilla local fija y un cálculo independiente sin descuentos para
crear regresiones adicionales; no constituyen por sí solos prueba de las
reglas de cupones. `tests/test_data_validation.py` corrompe archivos temporales
para demostrar detección de columnas ausentes, tipos inválidos, JSON incorrecto
y acciones desconocidas con línea de origen.
