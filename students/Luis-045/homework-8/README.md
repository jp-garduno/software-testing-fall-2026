# Homework 8: End-to-End Test Automation

- **Alumno:** Luis-045
- **Rama:** `feat/Luis-045/homework-8`
- **Aplicación:** TodoMVC React
- **Validación local:** 23 de noviembre de 2026, Windows 11, Chrome headless

La entrega cubre las cuatro partes base: Selenium con Python, Playwright con JavaScript, escenarios BDD ejecutables con Behave y un reporte comparativo con mediciones reales. Cada framework tiene 18 casos equivalentes: los 15 puntos del enunciado y tres casos de entrada límite.

## Resultado verificado

| Suite                   |         Casos aprobados | Fallos esperados ejecutados | Fallos inesperados |
| ----------------------- | ----------------------: | --------------------------: | -----------------: |
| Selenium / pytest       |                      17 |                           1 |                  0 |
| Playwright, un worker   |                      17 |                           1 |                  0 |
| Playwright, dos workers |                      17 |                           1 |                  0 |
| Behave                  | 7 escenarios / 33 pasos |                           0 |                  0 |

**El caso de cancelar con Escape detecta un defecto real de la aplicación publicada.** No está omitido: se ejecuta en ambos frameworks y comprueba que el editor se cierre y conserve el título original. Actualmente falla porque TodoMVC ignora Escape. Selenium lo registra con `xfail(strict=True)` y Playwright con `test.fail()`; una corrección de la aplicación producirá un resultado inesperadamente aprobado y obligará a actualizar la marca. El [reporte comparativo](COMPARISON_REPORT.md#defecto-todo-001-cancelar-la-edición-con-escape) contiene reproducción y evidencia sin esa marca.

Playwright muestra `18 passed` al aceptar el fallo esperado; el JSON desglosa correctamente **17 aprobados y 1 fallo esperado**. No significa que la cancelación funcione.

## Aplicación y URL

El MD indica `https://todomvc.com/examples/react/`, que devolvió HTTP 404 durante la preparación. La aplicación React publicada está en:

<https://todomvc.com/examples/react/dist/>

Ambos Page Objects utilizan esa ruta por defecto. Se puede cambiar sin editar el código:

```powershell
$env:TODO_BASE_URL = "https://todomvc.com/examples/react/dist/"
```

Los ejemplos del MD son una guía, no una copia del DOM actual: por ejemplo, el contador publicado es `.todo-count` y no contiene un elemento `strong`.

## Estructura

```text
homework-8/
├── selenium/
│   ├── pages/
│   │   ├── __init__.py
│   │   └── todo_page.py
│   ├── tests/
│   │   ├── test_todo_crud.py
│   │   └── test_todo_filter.py
│   ├── browser.py
│   └── requirements.txt
├── playwright/
│   ├── pages/
│   │   └── TodoPage.js
│   ├── tests/
│   │   ├── fixtures.js
│   │   ├── todo-crud.spec.js
│   │   └── todo-filter.spec.js
│   ├── metrics-reporter.js
│   ├── playwright.config.js
│   ├── package-lock.json
│   └── package.json
├── features/
│   ├── todo.feature
│   ├── environment.py
│   └── steps/
│       └── todo_steps.py
├── reports/
│   ├── selenium-results.json
│   ├── playwright-results.json
│   ├── playwright-parallel-results.json
│   ├── behave-results.json
│   ├── known-defect-selenium.json
│   ├── known-defect-playwright.json
│   ├── code-metrics.json
│   └── measure_code.py
├── screenshots/
├── .gitignore
├── conftest.py
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── COMPARISON_REPORT.md
└── README.md
```

Se conservan todos los nombres y carpetas exigidos. Los archivos auxiliares permiten iniciar navegadores, aislar pruebas, ejecutar Behave y reproducir las mediciones. El `requirements.txt` de la raíz delega al de `selenium/`; `pytest.ini` resuelve los imports sin convertir la carpeta `selenium/` en un paquete que oculte la librería instalada.

## Preparación en PowerShell

Requiere Python 3.11 o superior, Node.js 22 o superior, npm, Google Chrome instalado y acceso a Internet. Selenium Manager obtiene el ChromeDriver correspondiente. Playwright utiliza el mismo Chrome instalado mediante `channel: "chrome"`.

Ejecutar desde `students/Luis-045/homework-8/`:

```powershell
# Intérprete utilizado en este equipo; en otro equipo se puede usar python -m venv .venv.
$pythonBase = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $pythonBase -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm.cmd --prefix playwright ci
```

No se necesita activar el entorno virtual. Se usa `npm.cmd` para conservar los argumentos de línea de comandos en PowerShell. Las dependencias directas están fijadas y JavaScript incluye su lockfile.

## Ejecutar las pruebas

### Selenium

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Descubre los dos archivos de pruebas, crea un perfil nuevo de Chrome por caso, usa esperas explícitas y cierra el navegador incluso si una comprobación falla.

### Playwright

```powershell
# Dos workers, configuración predeterminada.
npm.cmd --prefix playwright test

# Un worker para la comparación con Selenium.
npm.cmd --prefix playwright run test:serial
```

Cada prueba recibe un contexto independiente. Se usan localizadores y comprobaciones que esperan el estado esperado. No hay reintentos que conviertan una ejecución fallida en una aprobada.

Para conservar otra medición paralela sin sobrescribir la serial:

```powershell
$env:PW_REPORT_NAME = "playwright-parallel-results.json"
npm.cmd --prefix playwright run test:parallel
$env:PW_REPORT_NAME = $null
```

### BDD / Behave

```powershell
.\.venv\Scripts\python.exe -m behave features -f json -o reports/behave-results.json -f progress
```

Los hooks crean y cierran un navegador por escenario. Los pasos reutilizan `selenium/pages/todo_page.py`. El feature incluye creación, finalización, eliminación, los tres ejemplos del filtro y guardar una edición: siete escenarios, sin pasos pendientes o indefinidos.

### Depuración

```powershell
$env:HEADED = "1"
.\.venv\Scripts\python.exe -m pytest -q
$env:HEADED = $null
npm.cmd --prefix playwright run test:headed
npm.cmd --prefix playwright run report
```

Selenium permite indicar un ejecutable específico con `SELENIUM_BROWSER_BINARY` o un driver con `SELENIUM_DRIVER`. Por defecto ambos los resuelve la instalación de Chrome y Selenium Manager.

## Correspondencia con el enunciado

| Grupo                    | Comprobaciones en ambos frameworks                                                           |
| ------------------------ | -------------------------------------------------------------------------------------------- |
| Creación                 | Una tarea; varias tareas; aparición del texto en la lista                                    |
| Finalización             | Completar; desmarcar; completar varias                                                       |
| Eliminación              | Eliminar una; eliminar una completada; limpiar todas las completadas conservando las activas |
| Filtros                  | All; Active; Completed, verificando textos exactos y orden                                   |
| Edición                  | Cambiar texto y guardar al perder foco; cancelar con Escape; guardar con Enter               |
| Casos límite adicionales | Ignorar espacios; recortar espacios exteriores; eliminar mediante una edición vacía          |

Los datos se crean mediante la interfaz. El aislamiento del perfil o contexto elimina la necesidad de compartir o limpiar manualmente tareas entre casos.

## Evidencias y mediciones

Los JSON de `reports/` contienen resultados, versiones y tiempos. `screenshots/` incluye una captura al terminar cada uno de los 18 casos de cada framework y los siete escenarios BDD: 43 capturas. Por ejemplo:

- [Selenium: creación de varias tareas](screenshots/selenium-test_create_multiple_tasks.png).
- [Playwright: filtro de completadas](screenshots/playwright-view-completed-tasks-only.png).
- [Playwright: editor abierto después de Escape](screenshots/playwright-cancel-edit.png).
- [BDD: creación](screenshots/bdd-add-a-new-todo.png).

Las capturas son evidencia de ejecución, no baselines de regresión visual. Los reportes HTML y trazas temporales de Playwright se generan localmente y no se versionan.

Para recalcular LOC y complejidad:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe reports/measure_code.py
```

## Calidad del código

Desde la misma carpeta:

```powershell
.\.venv\Scripts\python.exe -m black --check conftest.py selenium/browser.py selenium/pages selenium/tests features reports/measure_code.py
.\.venv\Scripts\python.exe -m isort --check-only --profile black conftest.py selenium/browser.py selenium/pages selenium/tests features reports/measure_code.py

$pythonFiles = @("conftest.py", "reports/measure_code.py") + @(Get-ChildItem -LiteralPath selenium,features -Recurse -Filter "*.py" | Select-Object -ExpandProperty FullName)
.\.venv\Scripts\python.exe -m pylint --rcfile=../../../.github/grading/pylintrc $pythonFiles

.\playwright\node_modules\.bin\eslint.cmd --no-eslintrc --config ../../../.github/grading/eslintrc.json "playwright/*.js" "playwright/pages/*.js" "playwright/tests/*.js"
.\playwright\node_modules\.bin\prettier.cmd --check "playwright/*.js" "playwright/pages/*.js" "playwright/tests/*.js"
```

Black, isort, Pylint y ESLint se comprobaron sobre los archivos de esta entrega; Pylint obtuvo 10.00/10.

## Alcance de entrega

Esta entrega implementa las cuatro partes base. No se reclaman puntos de los bonos opcionales. La rama conserva el formato solicitado por Luis-045, en lugar del nombre genérico del ejemplo del MD. Los commits siguen Conventional Commits.

Los resultados funcionales se expresan por casos E2E y escenarios BDD; no se presenta un porcentaje de cobertura interna del código de una aplicación remota.
