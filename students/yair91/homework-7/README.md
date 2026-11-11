# Homework 7: Data-Driven Test Suite

Suite guiada por datos para un sistema de procesamiento de pedidos de comercio
electrónico. Los datos de prueba viven en archivos CSV y JSON, fuera del código
de las pruebas.

**Autor**: Emmanuel Arias (`yair91`) · Módulo 7 · Fall 2026

## Resultados

```
256 passed
Cobertura de src/   100 % (306/306 sentencias)
Pylint              10.00/10
```

| Parte | Entregable | Casos |
| --- | --- | --- |
| 1 · Order Calculator | `src/order_calculator.py` + `test_data/order_calculations.csv` | 35 filas (mínimo 25) |
| 2 · Customer Validation | `src/customer_validator.py` + `test_data/customer_validation.json` | 39 casos (mínimo 30) |
| 3 · Comparison Analysis | `tests/test_order_traditional.py` y `tests/test_order_data_driven.py` | 10 escenarios en las dos formas |
| 4 · Integration | `test_data/order_workflows.json` | 5 flujos (mínimo 3) |
| Bonus A | `src/data_generator.py` | 100 pedidos de regresión |
| Bonus C | `src/data_validator.py` | Validación de los archivos de datos |

## Prerrequisitos

- Python 3.9 o mayor. El código evita sintaxis posterior a 3.9, así que también
  corre en el 3.11 que pide el curso.
- Las dependencias de `requirements.txt`.

## Instalación

```bash
cd students/yair91/homework-7
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Correr las pruebas

```bash
pytest -v
```

Con cobertura:

```bash
pytest --cov=src --cov-report=term-missing
```

Reporte HTML navegable, archivo por archivo:

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html          # Linux: xdg-open
```

El resumen de cobertura que se entrega está en
[`coverage_report.html`](coverage_report.html), y la salida completa de la
corrida en [`test_results.txt`](test_results.txt).

Una suite a la vez:

```bash
pytest tests/test_order_calculator.py -v      # Parte 1
pytest tests/test_customer_validator.py -v    # Parte 2
pytest tests/test_order_traditional.py -v     # Parte 3, versión tradicional
pytest tests/test_order_data_driven.py -v     # Parte 3, versión guiada por datos
pytest tests/test_integration.py -v           # Parte 4
pytest tests/test_data_validator.py -v        # Bonus C
pytest tests/test_data_generator.py -v        # Bonus A
```

Linting con la misma configuración que usa el workflow de calificación:

```bash
pylint --rcfile=../../../.github/grading/pylintrc src tests
```

## Estructura

```
homework-7/
├── src/
│   ├── order_calculator.py      Parte 1: subtotal, descuento, impuesto, envío
│   ├── customer_validator.py    Parte 2: email, teléfono, dirección, Luhn, vencimiento
│   ├── data_generator.py        Bonus A: 100 pedidos de regresión reproducibles
│   └── data_validator.py        Bonus C: revisa los archivos de datos
├── tests/
│   ├── conftest.py              rutas y carga de los archivos de datos
│   ├── test_order_calculator.py
│   ├── test_customer_validator.py
│   ├── test_order_traditional.py
│   ├── test_order_data_driven.py
│   ├── test_integration.py
│   ├── test_data_generator.py
│   └── test_data_validator.py
├── test_data/
│   ├── order_calculations.csv   35 filas
│   ├── customer_validation.json 39 casos
│   ├── order_workflows.json     5 flujos
│   └── generated_orders.csv     100 pedidos generados
├── README.md
├── COMPARISON_REPORT.md         Parte 3: tradicional contra guiado por datos
├── TEST_DATA_SPEC.md            formato de cada archivo de datos
├── coverage_report.html
├── test_results.txt
├── pytest.ini
└── requirements.txt
```

El formato de cada archivo de datos está documentado en
[`TEST_DATA_SPEC.md`](TEST_DATA_SPEC.md), y la comparación de la Parte 3 con
sus números medidos en [`COMPARISON_REPORT.md`](COMPARISON_REPORT.md).

## Decisiones que el enunciado deja abiertas

**`NEWUSER` solo aplica a clientes nuevos.** La regla dice "15% off first
order", pero el código de arranque del enunciado no revisa el tipo de cliente,
así que aceptaría el código para cualquiera. Aquí un cliente `regular` que
intente `NEWUSER` recibe `False` y no obtiene descuento.

**El envío suma peso y distancia.** `peso × 0.50 + distancia × 0.10`, y express
multiplica ese total por 1.5. El enunciado lista las dos reglas sin decir si se
suman o si una reemplaza a la otra.

**El impuesto no grava el envío.** Es 8 % de (subtotal − descuento), tal como
está escrito, así que el envío se agrega después de calcularlo.

**Cantidad cero es válida; los negativos no.** El enunciado pide casos borde
con "zero quantity, negative values" sin decir qué debe pasar. Aquí un artículo
con cantidad cero es legítimo y aporta 0 al subtotal, mientras que un precio,
peso, cantidad o distancia negativos lanzan `ValueError` con un mensaje
específico. Las filas con `expected_error` en el CSV cubren esos casos.

**El vencimiento se compara contra una fecha fija.** `customer_validator.py`
usa noviembre de 2026 como referencia en vez de `datetime.now()`. Con el reloj
real, una tarjeta `12/26` sería válida hoy y dejaría de serlo el año que viene,
y la suite empezaría a fallar sola sin que nadie tocara nada.

## Sobre los datos y por qué importa de dónde salen

Los montos de `order_calculations.csv` **no** se generaron llamando al
calculador. Se calcularon con una fórmula escrita aparte, redactada desde el
texto del enunciado, y después se contrastaron contra la implementación: 0
desviaciones en las 35 filas. Lo mismo con los errores esperados de
`customer_validation.json`, escritos a mano y contrastados después.

Si los valores esperados salieran del código que se va a probar, la prueba no
probaría nada: solo confirmaría que el código coincide consigo mismo.

La única excepción es `generated_orders.csv`, que sí sale del calculador y está
marcado como conjunto de regresión. Sirve para detectar que algo cambió, no
para demostrar que algo está bien.

## Sobre el bonus A y Faker

El enunciado sugiere Faker para generar datos. Aquí no se usa: el workflow de
calificación instala únicamente el `requirements.txt` de la raíz del
repositorio, donde Faker no aparece, así que una prueba que lo importara
fallaría al calificar.

El generador usa `random` con semilla fija, de la librería estándar. Eso da algo
que Faker no da de entrada: el mismo semillero produce siempre el mismo
archivo, y un conjunto de regresión que cambia en cada corrida no sirve para
detectar regresiones.

```bash
PYTHONPATH=src python src/data_generator.py
md5 test_data/generated_orders.csv     # el mismo hash en cada corrida
```
