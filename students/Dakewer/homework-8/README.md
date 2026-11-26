# Homework 8: End-to-End Test Automation

Pruebas E2E de [TodoMVC React](https://todomvc.com/examples/react/) con Selenium
(Python), Playwright (JavaScript) y BDD con Behave.

## Contenido

| Parte | Ubicación | Casos |
| --- | --- | ---: |
| Selenium + Page Object Model | `selenium/` | 26 |
| Playwright + Page Object Model | `playwright/` | 26 (los mismos) |
| BDD (Gherkin + Behave) | `features/` | 6 escenarios |
| Reporte comparativo | `COMPARISON_REPORT.md` | |
| Bonus A: regresión visual | `playwright/tests/visual/` | 5 |
| Bonus C: métricas de rendimiento | `playwright/tests/performance/`, `PERFORMANCE_REPORT.md` | 1 |
| Evidencia | `screenshots/` | |

## Resultados

Ejecutados en Linux contra la copia local del build oficial (commit `ff43b02`):

| Suite | Resultado |
| --- | --- |
| Selenium | 25 passed, 1 xfailed (defecto conocido) |
| Playwright E2E | 26 passed (incluye 1 fallo esperado) |
| Behave | 6 escenarios, 25 pasos, todos pasan |
| Visual | 5 passed |
| Performance | 1 passed |

## Requisitos

Python 3.10+, Node.js 20+, Google Chrome y Git.

## Instalación

Desde `homework-8/`:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r selenium/requirements.txt

cd playwright
npm ci
npx playwright install chromium
cd ..
```

## Elegir la aplicación bajo prueba

Por defecto las pruebas usan `https://todomvc.com/examples/react/`.

Para usar una versión fija y sin depender de internet (la usada para los
resultados), en **otra terminal**:

```bash
python scripts/serve_app.py      # descarga el build y sirve en el puerto 7002
```

y en la terminal de pruebas:

```bash
export TODO_URL=http://127.0.0.1:7002/        # Windows: $env:TODO_URL="http://127.0.0.1:7002/"
```

## Ejecutar las pruebas

```bash
# Selenium (con reporte HTML)
cd selenium
pytest -v --html=../reports/selenium.html --self-contained-html
cd ..

# BDD, desde homework-8/
behave

# Playwright
cd playwright
npm test
npm run report                   # abre el reporte HTML
```

Ver el navegador: `HEADLESS=0 pytest` (Selenium y Behave) o
`npm test -- --headed` (Playwright).

## Bonus

```bash
cd playwright

# Regresión visual
npm run test:visual:update       # crear referencias propias (ver nota)
npm run test:visual              # comparar
VISUAL_DEMO_CHANGE=1 npm run test:visual   # provocar diferencias a propósito
npm run report

# Rendimiento: genera reports/performance/
npm run test:perf
```

**Nota:** las capturas de referencia incluidas se generaron en Linux contra la
copia local. El renderizado de fuentes cambia entre sistemas, así que en
Windows o macOS hay que ejecutar primero `test:visual:update`.

## Benchmark y conteo de líneas

Con el entorno virtual activo, el servidor local y `TODO_URL` configurados:

```bash
python scripts/benchmark.py --runs 7
python scripts/count_loc.py
```

## Variables de entorno

| Variable | Efecto |
| --- | --- |
| `TODO_URL` | URL de la aplicación |
| `HEADLESS=0` | Selenium con ventana visible |
| `CHROME_BINARY`, `CHROMEDRIVER` | Usar un Chrome o driver concretos |
| `SELENIUM_DRIVER_SCOPE=session` | Compartir un navegador entre tests |
| `PW_CHANNEL=chromium` | Playwright con Chromium completo |
| `PERF_ITERATIONS` | Repeticiones de la prueba de rendimiento (10) |

## Defecto conocido: cancelar edición

El build `ff43b02` no maneja la tecla Escape al editar: el campo sigue abierto y
al perder el foco se guarda el cambio. El test `cancel edit with escape` describe
el comportamiento correcto.

- Contra la URL local se marca como **fallo esperado** (si se corrige, avisará).
- Contra cualquier otra URL se ejecuta como test normal: si falla, esa versión
  tiene el mismo defecto.

## Decisiones de diseño

- Solo esperas explícitas en Selenium; no hay `sleep` ni esperas implícitas.
- Cada test carga la página de nuevo; la app no persiste datos, así que son
  independientes.
- Los tests no usan selectores directamente: pasan por el page object.
