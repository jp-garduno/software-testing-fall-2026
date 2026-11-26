# Homework 8: automatización de sistema con Selenium y Playwright

**Alumno:** David Valdez (`davidvaldezm`) · **Módulo:** 8, System Level Testing.

Las dos suites ejecutan 19 casos equivalentes contra la aplicación real TodoMVC React:
18 comportamientos correctos y una prueba que reproduce un defecto conocido de cancelación.
Behave ejecuta además ocho escenarios BDD reales con Selenium, reutilizando el mismo Page Object.
No se simula el DOM ni se reemplaza la aplicación con una implementación propia.

## Aplicación y defecto identificado

La [URL del enunciado](https://todomvc.com/examples/react/) devuelve HTTP 404. La aplicación React
publicada está en [React dist](https://todomvc.com/examples/react/dist/), destino predeterminado
de ambas suites. `TODO_URL` permite apuntar a otra instalación compatible.

En esta versión, al editar una tarea, Escape no cierra el editor ni descarta el texto.
`test_edit_cancel` usa `xfail(strict=True)` y su equivalente Playwright usa `test.fail`.
**Esto registra un defecto del producto; no significa que cancelar funcione.** Un arreglo del producto
hará fallar las suites por éxito inesperado hasta retirar esas marcas. Para reproducirlo sin la
clasificación de fallo conocido:

```sh
python -m pytest selenium/tests/test_todo_crud.py -k edit_cancel --runxfail
```

## Instalación

Desde `students/davidvaldezm/homework-8`, con Python 3.11+ y Node 22+:

```sh
python -m venv .venv
# PowerShell: .venv\Scripts\Activate.ps1
# Bash: source .venv/bin/activate
python -m pip install -r requirements.txt
npm ci --prefix playwright
```

Se necesita Google Chrome. Selenium Manager resuelve ChromeDriver; Playwright utiliza el canal
`chrome`. Ambos trabajan en modo headless: ventana Selenium y viewport Playwright a 1280 × 900.
Para utilizar el mismo Chrome for Testing
en ambas suites, configurar `CHROME_BINARY` con su ruta absoluta. El driver debe corresponder a
esa versión. No se usa el perfil personal del navegador.

```powershell
$env:CHROME_BINARY = 'C:/ruta/chrome-win64/chrome.exe'
# Opcional, solo si ya existe un driver compatible en caché:
$env:SE_OFFLINE = 'true'
```

## Ejecución

```sh
python -m pytest -v --cov=selenium/pages --cov-report=term-missing
npm test --prefix playwright
python -m behave --junit --junit-directory reports/live/bdd features
python scripts/benchmark.py
python scripts/performance.py
```

`benchmark.py` ejecuta primero Selenium y después Playwright con un solo worker, sin reintentos.
Conserva logs, JUnit, cobertura del código Python de automatización, JSON de Playwright y tiempos
en `reports/live/`. `performance.py` toma cinco muestras de navegación y operaciones verificadas.
Los resultados de la ejecución entregada están en `reports/submitted/` y se analizan en
[COMPARISON_REPORT.md](COMPARISON_REPORT.md) y [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md).
La cobertura corresponde al código de automatización Python, no al JavaScript remoto de TodoMVC.

Para inspección interactiva: `npm run test:debug --prefix playwright` o `HEADED=1` (PowerShell:
`$env:HEADED='1'`). Para ejecutar Playwright con dos workers:
`npm run test:parallel --prefix playwright`. La comparación entregada utiliza un worker.

## Escenarios equivalentes

| Grupo | Casos en cada framework | Verificaciones |
| --- | ---: | --- |
| Creación | 2 | Una tarea y varias en orden; contador activo |
| Finalización | 3 | Completar, reactivar y completar todas |
| Eliminación | 3 | Activa, completada y limpiar completadas conservando activas |
| Edición | 3 | Enter, Escape (defecto conocido) y pérdida de foco |
| Filtros | 4 | All, Active, Completed, conjunto vacío y regreso a All |
| Límites | 4 | Espacios vacíos, recorte, edición vacía que elimina y tareas duplicadas |
| **Total** | **19** | **18 aprobadas y 1 fallo esperado** |

Los ocho escenarios Behave cubren creación, finalización, eliminación, tres ejemplos de filtrado,
edición y limpieza de completadas. Cada escenario recibe un navegador nuevo y registra su cierre
antes de ejecutar acciones. Cada prueba pytest también utiliza un navegador nuevo; Playwright
proporciona un contexto nuevo por prueba. Los tests no dependen del orden ni de datos previos.

## Page Object Model y sincronización

- `selenium/pages/todo_page.py`: selectores, acciones y `WebDriverWait` para resultados concretos.
- `playwright/pages/TodoPage.js`: locators y acciones; las pruebas usan aserciones con reintentos.
- `features/steps/todo_steps.py`: vocabulario BDD, sin selectores ni llamadas WebDriver directas.
- `selenium/tests/` y `playwright/tests/`: comportamiento esperado y aserciones de negocio.

No se usan esperas fijas, clics forzados ni JavaScript para alterar el estado de las tareas.
Las capturas en `screenshots/` muestran la finalización múltiple. Los fallos generan evidencia en
`reports/live/failures/` o `playwright/test-results/`; Playwright conserva trazas de los fallos
inesperados. El contexto del defecto conocido se entrega en `reports/submitted/known-defect.md`.

## Calidad y CI (bonus D)

```sh
python -m black --check selenium features scripts
python -m pylint selenium/pages selenium/tests/*.py features/*.py features/steps/*.py scripts/*.py
npm run lint --prefix playwright
```

En PowerShell, si no se expanden los patrones de Pylint:

```powershell
$files = Get-ChildItem selenium,features,scripts -Recurse -Filter *.py | ForEach-Object FullName
python -m pylint $files
```

El workflow `.github/workflows/davidvaldezm-homework-8.yml` corre en push, pull request y ejecución
manual para esta entrega. Instala Chrome, ejecuta lint, las dos suites, BDD y métricas, y publica
reportes/capturas/trazas incluso si hay fallos. Los errores inesperados detienen el job.
El otro bonus elegido es **C: métricas de rendimiento**; no se afirma cobertura entre navegadores
ni regresión visual por el solo hecho de guardar capturas.
