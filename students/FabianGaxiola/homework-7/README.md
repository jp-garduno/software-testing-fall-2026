# Homework 7: Pruebas basadas en datos

Implementación Python de un sistema de cálculo de pedidos, validación de clientes
y procesamiento de pagos simulado. Los casos se mantienen fuera del código de
prueba en CSV y JSON.

## Estructura

- `src/order_calculator.py`: subtotal, descuentos, impuestos y envío.
- `src/customer_validator.py`: email, teléfono, dirección, Luhn y expiración.
- `src/order_processor.py`: coordinación de los pasos de un pedido.
- `src/data_validation.py`: revisión previa de CSV/JSON y errores con ubicación.
- `tests/`: pruebas parametrizadas, tradicionales, de integración y de datos.
- `test_data/`: 34 casos de cálculo, 33 casos de clientes y 4 flujos.

## Instalación y ejecución

Desde esta carpeta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

Para obtener cobertura:

```powershell
python -m pytest --cov=src --cov-report=term-missing
```

La suite se puede ejecutar desde cualquier directorio porque las rutas de datos
se resuelven desde los archivos de prueba. `pytest.ini` restringe la recolección
a `tests/`.

## Decisiones de negocio

- Los códigos `SAVE10` y `SAVE20` requieren un subtotal estrictamente superior
  a $50 y $100, respectivamente.
- `NEWUSER` aplica únicamente a clientes `new`; representa un primer pedido.
- Se aplica un único código por pedido. Un código no reconocido no concede
  descuento y elimina un código aplicado previamente.
- Impuesto, descuento y envío se redondean a centavos con redondeo comercial.
- El peso se calcula por unidad. El envío express multiplica el envío base por
  1.5; `FREESHIP` deja el costo de envío en cero.
- Los datos inválidos generan `ValueError` en el pedido; cantidades cero son
  aceptadas y valores negativos no.
- El flujo de pago es simulado y no envía datos a un proveedor externo.

## Archivos de resultados

- `test_results.txt`: salida de la última ejecución de pytest con cobertura.
- `coverage_report.html`: resumen HTML autocontenido de cobertura.
- `COMPARISON_REPORT.md`: análisis entre pruebas tradicionales y parametrizadas.
- `TEST_DATA_SPEC.md`: formatos, campos y criterios de los datos.

Los números de tarjeta del conjunto son números de prueba sintéticos; no se
procesan pagos reales.
