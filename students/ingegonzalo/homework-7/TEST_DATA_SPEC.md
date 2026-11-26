# Test Data Specification

## 1. `order_calculations.csv`
Una fila = un caso. Codificacion UTF-8, separador coma, primera fila = encabezado.

| Columna | Tipo | Descripcion |
|---|---|---|
| test_name | string unico, snake_case | Identificador (aparece en el reporte de pytest) |
| items | lista JSON con comillas simples | `[{'name':..,'price':..,'quantity':..,'weight':..}]`; el campo va entre comillas dobles. No usar apostrofes en nombres |
| customer_type | `new` \| `regular` | Tipo de cliente |
| discount_code | string \| `NONE` | `NONE` = sin codigo |
| distance_km | float >= 0 | Distancia de envio |
| is_express | `true` \| `false` | Envio express |
| expected_subtotal / _discount / _tax / _shipping / _total | float (2 decimales) | Resultados esperados |

Convencion de nombres: prefijos `simple_`, `save10_`/`save20_`/`newuser_`, `tax_`, `ship_`, `complex_`, `edge_`.
Los valores negativos NO van en el CSV (lanzan `ValueError`); se prueban en test_order_calculator.py.

## 3. `customer_validation.json`
Arreglo de objetos:
{
  "test_name": "string unico",
  "category": "valid | invalid_email | invalid_phone | invalid_address | invalid_card | multiple_errors",
  "customer": { "email", "phone", "billing_address": {street, city, state, zip},
                "credit_card": {number, expiration "MM/YYYY", cvv} },
  "expected": { "is_valid": bool, "errors": [string] }
}
Los errores se listan en el orden: email, phone, street, city, state, zip, number, expiration, cvv.
Mensajes: Invalid email format, Invalid phone format, Street is required, City is required,
Invalid state, Invalid zip code, Invalid credit card number, Invalid expiration date format,
Credit card expired, Invalid CVV.
Se genera con `python scripts/build_customer_data.py`.

## 4. `order_workflows.json`
{ "workflows": [ { "name": "...", "steps": [ { "action", "data" (opcional), "expected" } ] } ] }

Acciones: validate_customer, create_order, apply_discount, set_shipping, calculate_total,
process_payment, generate_confirmation.
`expected` es un subconjunto: solo se verifican las claves indicadas (floats con tolerancia 0.01).

## 5. Reglas generales
- Rutas relativas al archivo de test (`Path(__file__)`), nunca absolutas.
- Fecha de referencia fija en tests: 2026-01-15. Tarjetas validas usan expiracion 2099.