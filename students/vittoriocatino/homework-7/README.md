# Tarea 7: Data-Driven Testing

**Alumno:** Vittorio Catino. **Lenguaje:** Python 3.11 o posterior.

Sistema local de procesamiento de pedidos con precios, descuentos, impuestos,
envío, validación de clientes y confirmaciones. Los pagos se simulan con mocks;
los datos personales y números de tarjeta de prueba son ficticios.

## Instalación y ejecución

Desde `students/vittoriocatino/homework-7/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:coverage_html
```

El reporte entregado se abre mediante `coverage_report.html`; los archivos de
`coverage_html/` deben mantenerse juntos para conservar los enlaces y estilos.
`test_results.txt` registra la ejecución real con cobertura. No se necesita
acceso a servicios externos para ejecutar la suite.

## Organización y trazabilidad

| Parte | Implementación / pruebas | Datos |
|---|---|---|
| Calculadora | `src/order_calculator.py`, `tests/test_order_calculator.py` | `test_data/order_calculations.csv`: 31 casos |
| Clientes | `src/customer_validator.py`, `tests/test_customer_validator.py` | `test_data/customer_validation.json`: 30 casos |
| Comparación | `tests/test_order_traditional.py`, `tests/test_order_data_driven.py` | Los mismos primeros 10 registros del CSV |
| Integración | `src/order_processor.py`, `tests/test_integration.py` | `test_data/order_workflows.json`: 3 compras completas y 2 flujos negativos |
| Bonus A | `scripts/generate_orders.py`, `tests/test_generated_orders.py` | 100 pedidos con Faker, semilla 2026 |
| Bonus C | `src/data_loader.py`, `tests/test_data_validation.py` | Validación de esquema previa a las pruebas |

El CSV base tiene 3 casos simples, 9 de descuentos, 4 de impuestos, 6 de envío
y 9 complejos. Las expectativas del conjunto base se escribieron explícitamente
en `scripts/build_fixtures.py`: no se calculan llamando al sistema bajo prueba.
Los 100 casos generados amplían la regresión sin reemplazar estos oráculos.

Para regenerar los datos de manera reproducible:

```bash
python scripts/build_fixtures.py
python scripts/generate_orders.py
```

## Supuestos y decisiones

- `SAVE10` requiere subtotal **mayor que** 50 y `SAVE20`, mayor que 100. Se
  priorizan las reglas escritas sobre el código inicial que acepta igualdad.
- `NEWUSER` sólo aplica a `customer_type="new"`, que representa una primera
  compra. No hay almacenamiento persistente de historial de clientes.
- Se permite un cupón por pedido. Aplicar un código inválido o no elegible
  limpia el anterior. `EXPIRED` es un código inválido; el enunciado no define
  calendario de vigencia para los cuatro códigos permitidos.
- Se usa `Decimal` y redondeo `ROUND_HALF_UP` a dos decimales por componente.
  El total es la suma de los importes mostrados. El peso es unitario y se
  multiplica por cantidad; express multiplica todo el envío base por 1.5.
- El ejemplo del enunciado de 1 kg y 10 km muestra envío de 5.50, aunque la
  fórmula da 1.50. Aquí se aplica la fórmula: `0.50 × kg + 0.10 × km`.
- Cantidad cero es válida; cantidades negativas o no enteras, precios, pesos y
  distancias negativos, valores no finitos y datos incompletos se rechazan con
  `ValueError`. No se impone un máximo no especificado; hay un caso de gran
  volumen. Un pedido vacío con distancia cero vale cero.
- La validación de email es sintáctica, sin DNS; teléfono usa exactamente
  `(XXX) XXX-XXXX`. Dirección exige calle, ciudad, estado de EE. UU. o DC y ZIP
  de cinco dígitos o ZIP+4. Luhn se aplica a 13–19 dígitos ASCII; se rechazan
  todos ceros. CVV admite tres o cuatro dígitos.
- Caducidad `MM/YYYY`: la tarjeta sirve durante todo ese mes. Se inyecta la
  fecha `2026-11-10` en las pruebas para que sus resultados no cambien con el
  reloj real. La API usa la fecha actual si no recibe una explícita.
- Las confirmaciones requieren pago aprobado y contienen ID y total. Un
  segundo intento después de pagar devuelve `already_paid` sin otro cargo.

`TEST_DATA_SPEC.md` documenta los formatos; `COMPARISON_REPORT.md` compara
las dos suites equivalentes y explica el alcance de las mediciones.
