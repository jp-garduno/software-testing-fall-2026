# Homework 7: Data-Driven Test Suite

- **Alumno:** Luis-045
- **Rama:** `feat/Luis-045/homework-7`
- **Lenguaje:** Python 3.11 o superior

La entrega implementa el cálculo de pedidos, la validación de clientes y un
checkout con pago simulado y confirmación. Las pruebas usan pytest, con entradas
y resultados esperados en archivos CSV y JSON.

## Preparación

Con un entorno de Python 3.11 o superior activo, ejecuta desde la raíz del
repositorio:

```powershell
python -m pip install -r students/Luis-045/homework-7/requirements.txt
Set-Location students/Luis-045/homework-7
python -B -m pytest -q -p no:cacheprovider
```

## Resultados y cobertura

En Windows con Python 3.13.9 pasaron **95 pruebas**, con **100% de cobertura**
(203 de 203 sentencias y 72 de 72 ramas). El registro
está en [test_results.txt](test_results.txt) y el desglose por archivo en
[coverage_report.html](coverage_report.html).

Desde la carpeta de la entrega, puedes volver a medir la cobertura y generar
el HTML de coverage.py en una carpeta temporal:

```powershell
$reportDir = Join-Path ([IO.Path]::GetTempPath()) "homework-7-$PID"
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
$env:COVERAGE_FILE = Join-Path $reportDir ".coverage"
python -B -m pytest -v -p no:cacheprovider --cov=src --cov-branch --cov-fail-under=80.01 --cov-report=term-missing "--cov-report=html:$reportDir/html"
Remove-Item Env:COVERAGE_FILE
```

El reporte generado se abre desde el archivo `$reportDir/html/index.html`.

Para comprobar el formato y el estilo desde esta carpeta:

```powershell
python -B -m black --check src tests
python -B -m isort --check-only --profile black src tests
python -B -m pylint --rcfile=../../../.github/grading/pylintrc src tests
```

## Qué se prueba

| Archivo | Casos | Alcance |
| --- | ---: | --- |
| `test_order_calculator.py` | 38 | 30 filas CSV y ocho pruebas de cupones, entradas inválidas e importación |
| `test_customer_validator.py` | 31 | Contacto, domicilio, tarjeta y errores simultáneos |
| `test_order_traditional.py` | 10 | Diez escenarios con entradas y resultados en Python |
| `test_order_data_driven.py` | 10 | Los mismos diez escenarios seleccionados del CSV |
| `test_integration.py` | 6 | Cuatro pedidos confirmados y dos flujos bloqueados |

## Reglas del sistema

- `Order` aplica `SAVE10` desde $50 y `SAVE20` desde $100, con ambos límites
  incluidos. `NEWUSER` requiere un cliente nuevo. Un cupón válido reemplaza al
  anterior; un código desconocido, expirado o no aplicable no lo modifica.
- El envío usa el peso por unidad multiplicado por la cantidad y la distancia
  del pedido. La tarifa exprés multiplica el costo combinado por 1.5.
  `FREESHIP` también cubre el envío exprés. Para el ejemplo de 1 kg y 10 km del
  enunciado, la fórmula da $1.50 de envío y $55.50 de total.
- El cálculo usa `Decimal` y redondea subtotal, descuento, impuesto y envío a
  centavos con `ROUND_HALF_UP`. El impuesto es 8% del subtotal descontado.
  Cantidades cero y pedidos vacíos son válidos; valores negativos se rechazan.
- `validate_customer` devuelve todos los errores de formato en orden. La tarjeta
  se comprueba con Luhn y vence al terminar el mes impreso. El CVV, si se incluye,
  debe tener 3 o 4 dígitos. Las pruebas fijan la fecha de referencia para no
  depender del día de ejecución.
- `Checkout` requiere un cliente válido y un total calculado antes del pago.
  La simulación permite reintentar un pago rechazado. La confirmación incluye
  el identificador del pedido y el monto pagado. No se envían cargos ni se
  guardan datos de tarjeta.

Consulta [la comparación](COMPARISON_REPORT.md) para el análisis de las suites
y [la especificación de datos](TEST_DATA_SPEC.md) para agregar escenarios.
