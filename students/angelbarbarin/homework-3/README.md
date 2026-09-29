# Homework 3 — Static Testing: cotizador de camaras de reversa

**Alumno:** Angel Isaac Barbarin (`angelbarbarin`)
**Modulo:** 03 — Static Testing
**Lenguaje:** Python 3.11

## El proyecto

Mini cotizador para un negocio de venta e instalacion de camaras de reversa y
pantallas para coche. Calcula el total de una cotizacion a partir de un carrito
de productos, sumando el costo de instalacion segun la categoria, aplicando un
descuento acotado y el IVA.

Se eligio este dominio porque tiene reglas de negocio reales que validar
(descuento maximo, SKU con formato fijo, cantidades positivas) y porque permite
que un defecto de codigo tenga una consecuencia concreta y facil de explicar:
cobrarle de mas a un cliente.

### Estructura

```
students/angelbarbarin/homework-3/
├── README.md                     Este archivo
├── REPORT.md                     Reporte de analisis estatico
├── FIXES.md                      Correcciones de linting, antes y despues
├── STYLE_GUIDE.md                Guia de estilo (bonus)
├── .pre-commit-config.yaml       8 hooks de pre-commit
├── .pylintrc                     Configuracion de pylint
├── requirements.txt              Dependencias
├── pylint-report.txt             Salida de pylint (antes de corregir)
├── pylint-report-after.txt       Salida de pylint (despues de corregir)
├── .github/workflows/
│   └── static-analysis.yml       Workflow de CI (bonus)
├── src/
│   ├── __init__.py
│   ├── catalogo.py               Inventario y costos de instalacion
│   ├── validaciones.py           Validaciones de entrada
│   └── cotizador.py              Calculo de la cotizacion
└── tests/
    ├── __init__.py
    ├── test_catalogo.py
    ├── test_validaciones.py
    └── test_cotizador.py
```

## Instalacion

```bash
cd students/angelbarbarin/homework-3
pip install -r requirements.txt
```

## Como ejecutar las herramientas

Los comandos se ejecutan **desde la carpeta de la tarea**:

```bash
# Pruebas
PYTHONPATH=. python -m pytest -q

# Formato
black src tests
isort --profile=black src tests

# Analisis estatico
pylint src --rcfile=.pylintrc

# Seguridad (bonus)
bandit -r src --skip=B101
```

### Pre-commit

El repositorio del curso ya tiene su propio `.pre-commit-config.yaml` en la
raiz, que es el que gobierna los commits de todo el repo. El archivo de esta
carpeta es el entregable de la tarea y se ejecuta de forma explicita, desde la
**raiz del repositorio**:

```bash
pre-commit install --install-hooks
pre-commit install --hook-type commit-msg

pre-commit run --all-files \
  --config students/angelbarbarin/homework-3/.pre-commit-config.yaml
```

Las versiones (`rev`) de los hooks estan fijadas a las mismas que usa el repo
del curso, para reutilizar los entornos ya cacheados por pre-commit.

## Hooks configurados

| Hook | Repositorio | Que hace |
|---|---|---|
| `trailing-whitespace` | pre-commit-hooks | Elimina espacios al final de linea |
| `end-of-file-fixer` | pre-commit-hooks | Garantiza salto de linea final |
| `check-yaml` | pre-commit-hooks | Valida la sintaxis de los YAML |
| `check-json` | pre-commit-hooks | Valida la sintaxis de los JSON |
| `check-added-large-files` | pre-commit-hooks | Bloquea archivos de mas de 500 KB |
| `check-merge-conflict` | pre-commit-hooks | Impide commitear marcadores de conflicto |
| `detect-private-key` | pre-commit-hooks | Impide subir llaves privadas |
| `black` | psf/black | Formatea el codigo Python |
| `isort` | PyCQA/isort | Ordena los imports (perfil black) |
| `pylint` | PyCQA/pylint | Analisis estatico con `.pylintrc` |
| `bandit` | PyCQA/bandit | Linting de seguridad (bonus) |
| `conventional-pre-commit` | compilerla | Valida el formato del mensaje de commit |

Son 12 hooks; el minimo pedido era 5.

## Notas sobre la configuracion

- **`.pylintrc` escrito a mano, no generado.** `pylint --generate-rcfile`
  produce unas 600 lineas, casi todas con el valor por defecto. Un archivo de
  40 lineas donde cada exclusion lleva su razon escrita es mas facil de revisar
  y mas dificil de que crezca sin control.
- **Se desactiva lo minimo.** Solo `format` (la autoridad sobre el formato es
  `black`, y tener dos herramientas opinando lo mismo genera conflictos) y
  `too-few-public-methods`. Se activa `useless-suppression`, que avisa cuando
  hay un `# pylint: disable` que ya no hace falta: evita que las exclusiones se
  acumulen como sedimento.
- **`--fail-under=9.0` en CI.** Sin un umbral que rompa el pipeline, el linter
  es una sugerencia que todo el mundo ignora.

## Reporte

El analisis —cuantos problemas se encontraron, de que tipo y que aprendi— esta
en [`REPORT.md`](REPORT.md). El detalle de cada correccion, con el codigo antes
y despues, esta en [`FIXES.md`](FIXES.md).

Resultado: la calificacion de pylint paso de **6.70/10 a 10.00/10**, y la suite
de pruebas paso de 13 a 14 casos (se agrego la prueba de regresion del defecto
que el analisis estatico encontro y las pruebas no).
