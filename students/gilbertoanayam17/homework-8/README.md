# Homework 8: End-to-End Test Automation

## Description

Pruebas end-to-end de [TodoMVC React](https://todomvc.com/examples/react/dist/) con Selenium y con Playwright, ambas con Page Object Model, más los escenarios BDD del enunciado en Behave y una comparación de las dos herramientas en [COMPARISON_REPORT.md](COMPARISON_REPORT.md).

| Parte                 | Herramienta                               | Dónde                             | Resultado                    |
| --------------------- | ----------------------------------------- | --------------------------------- | ---------------------------- |
| 1. Selenium           | Selenium 4 + pytest                       | `selenium/`                       | 14 passed, 1 xfailed         |
| 2. Playwright         | Playwright + pytest-playwright            | `playwright/`                     | 14 passed, 1 xfailed         |
| 3. BDD                | Behave (sobre el page object de Selenium) | `features/`                       | 6 scenarios, 25 steps passed |
| 4. Comparison         | -                                         | `COMPARISON_REPORT.md`            | -                            |
| Bonus A (Visual)      | Selenium + Pillow                         | `tests/test_visual_regression.py` | 4 passed                     |
| Bonus C (Performance) | Selenium + Navigation Timing API          | `tests/test_performance.py`       | 7 passed                     |

La prueba `xfailed` de cada suite es `test_cancel_edit`, que falla por un defecto de la app y no de la prueba (ver [Known Defect](#known-defect)).

## Project Structure

```
homework-8/
├── selenium/
│   ├── pages/todo_page.py        # page object (Selenium)
│   ├── tests/
│   │   ├── test_todo_crud.py     # creación, completado, borrado y edición (12 pruebas)
│   │   └── test_todo_filter.py   # filtros All / Active / Completed (3 pruebas)
│   ├── conftest.py               # fixtures driver y todo_page
│   ├── firefox_driver.py         # crea el WebDriver (también lo usan BDD y los bonus)
│   └── requirements.txt
├── playwright/
│   ├── pages/todo_page.py        # page object (Playwright)
│   ├── tests/
│   │   ├── test_todo_crud.py
│   │   └── test_todo_filter.py
│   ├── conftest.py
│   ├── pytest.ini                # Firefox por defecto
│   └── requirements.txt
├── features/
│   ├── todo.feature              # el feature del enunciado, sin cambios
│   ├── environment.py            # abre y cierra Firefox para Behave
│   └── steps/todo_steps.py
├── tests/
│   ├── test_visual_regression.py # bonus A
│   ├── test_performance.py       # bonus C
│   ├── conftest.py               # Firefox compartido por los dos bonus
│   └── markdown_report.py        # escribe los reportes de los dos bonus
├── screenshots/
│   ├── selenium/                 # estado final de cada prueba de Selenium
│   ├── playwright/               # estado final de cada prueba de Playwright
│   └── visual/                   # baselines y reporte del bonus A
├── COMPARISON_REPORT.md
├── PERFORMANCE_REPORT.md         # generado por el bonus C
├── pytest.ini                    # suite de Selenium + bonus A y C
└── requirements.txt              # todas las dependencias
```

El enunciado muestra Playwright en JavaScript, pero el módulo también lista su versión para Python (`pip install playwright pytest-playwright`), y elegí esa para que las tres partes compartan lenguaje y runner. Por eso, en lugar de `TodoPage.js`, los specs y `package.json`, la carpeta `playwright/` tiene `pages/todo_page.py`, `test_todo_crud.py`, `test_todo_filter.py` y `requirements.txt`.

## Prerequisites

- Python 3.11+ (probado con 3.14)
- Conexión a internet, ya que las pruebas usan el sitio real
- No hace falta instalar Firefox ni geckodriver, porque Selenium Manager los descarga si no los encuentra

## Installation

Los comandos usan el launcher `py` de Windows con Python 3.14. Con otra versión basta cambiar el número, y en Linux o macOS se usa `python3` en lugar de `py -3.14`.

```bash
py -3.14 -m pip install -r requirements.txt
py -3.14 -m playwright install firefox
```

## Running Tests

Desde esta carpeta (`students/gilbertoanayam17/homework-8`) se corren de la siguiente forma, igual en PowerShell que en Git Bash.

```bash
py -3.14 -m pytest selenium/tests -v       # Parte 1
py -3.14 -m pytest playwright/tests -v     # Parte 2
py -3.14 -m behave features                # Parte 3
py -3.14 -m pytest tests -v                # Bonus A y C
py -3.14 -m pytest -v                      # Selenium + bonus A y C en una sola corrida
```

Se invocan con `py -3.14 -m` en lugar de `pytest` o `behave` a secas porque así funcionan aunque la carpeta `Scripts` de Python no esté en el PATH. Las dos suites de pytest corren por separado porque cada una tiene su propio `pages/todo_page.py`, y `pytest playwright/tests` toma automáticamente la configuración de `playwright/pytest.ini`.

Por defecto todas las pruebas abren una ventana de Firefox para que se vea lo que hacen. Para correrlas sin ventana se define `HEADLESS=1`, que funciona en las cuatro suites.

```bash
$env:HEADLESS = "1"; py -3.14 -m pytest selenium/tests -v      # PowerShell
HEADLESS=1 py -3.14 -m pytest selenium/tests -v                # Git Bash
```

En PowerShell la variable queda definida para toda la terminal, así que para volver a ver el navegador se borra con `Remove-Item Env:HEADLESS`. Las pruebas también corren sin ventana, sin necesidad de la variable, en servidores de integración continua (que definen `CI`) y en Linux sin entorno gráfico, donde Firefox no tendría dónde dibujar la ventana. Para ver Playwright más despacio se puede agregar `--slowmo 500`.

## Test Scenarios

Las dos suites tienen las mismas 15 pruebas con los mismos nombres.

| Escenario (rubric) | Pruebas                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------- |
| 1. Task Creation   | `test_create_single_task`, `test_create_multiple_tasks`, `test_task_appears_in_list`                    |
| 2. Task Completion | `test_mark_task_as_complete`, `test_unmark_completed_task`, `test_complete_multiple_tasks`              |
| 3. Task Deletion   | `test_delete_single_task`, `test_delete_completed_task`, `test_clear_all_completed`                     |
| 4. Task Filtering  | `test_view_all_tasks`, `test_view_active_tasks_only`, `test_view_completed_tasks_only`                  |
| 5. Task Editing    | `test_edit_task_text` (Enter), `test_cancel_edit` (Escape), `test_save_edited_task` (al perder el foco) |

## Design Decisions

| Tema                     | Decisión                                                                                            | Motivo                                                                                                           |
| ------------------------ | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| URL                      | `https://todomvc.com/examples/react/dist/`, en una constante `APP_URL` de cada page object          | La URL del enunciado (`/examples/react/`) ahora responde 404                                                     |
| Navegador                | Firefox en las dos herramientas, con ventana visible por defecto                                    | Comparar las dos herramientas con el mismo motor y poder ver lo que hace cada prueba                             |
| Ventana                  | 800 × 900                                                                                           | Desde 899 px de ancho, la barra lateral "learn" aparece después de cargar y mueve la app 300 px                  |
| Aislamiento (Selenium)   | Un solo Firefox para toda la sesión, y cada prueba recarga la página                                | La app guarda los todos solo en memoria, así que recargar deja la lista vacía y evita 5 s de arranque por prueba |
| Aislamiento (Playwright) | Un contexto nuevo por prueba (el comportamiento de pytest-playwright)                               | Es el aislamiento natural de Playwright                                                                          |
| Esperas                  | Esperas explícitas en cada acción del page object de Selenium, ninguna en el de Playwright          | Selenium no espera solo, mientras que Playwright espera a que el elemento sea accionable y `expect()` reintenta  |
| Screenshots              | Cada prueba guarda el estado final de la app en `screenshots/selenium/` o `screenshots/playwright/` | Evidencia de la ejecución, y en `test_cancel_edit` muestra el defecto                                            |

## Known Defect

En esta versión de TodoMVC React la tecla Escape no hace nada mientras se edita un todo, por lo que el campo de edición sigue abierto y, si después pierde el foco, guarda el texto que se quería descartar. La especificación de TodoMVC pide que Escape salga del modo edición y descarte los cambios, así que `test_cancel_edit` prueba ese comportamiento y está marcada con `@pytest.mark.xfail(strict=True)` en las dos suites. La marca deja la suite en verde sin ocultar el problema, y como es estricta, la prueba fallará el día que lo corrijan para avisar que hay que quitarla. El screenshot `screenshots/selenium/test_cancel_edit.png` muestra el editor todavía abierto después de presionar Escape.

## Bonus

### A. Visual Regression

`tests/test_visual_regression.py` reconstruye cuatro estados de la app (lista vacía, tres todos con uno completado, vista Active y vista Completed), toma una captura solo del recuadro de la app y la compara píxel por píxel con Pillow contra la de una corrida anterior.

- Las baselines se guardan por plataforma (`screenshots/visual/baseline/win32/`), ya que Windows y Linux dibujan las fuentes distinto. Si no hay baseline para la plataforma, la primera corrida la crea y pasa.
- Antes de cada captura se quita el foco (para que no salga el cursor parpadeando), las transiciones CSS terminan al instante (un todo completado tarda 0.4 s en volverse gris) y el puntero se deja sobre el título, por lo que ningún hover queda dibujado. Gracias a eso la imagen no depende de cuánto tarde la prueba ni de dónde quede el mouse, y es idéntica con ventana o sin ella. Firefox además usa un píxel de pantalla por píxel CSS, de modo que el escalado de pantalla de Windows no cambia el tamaño de las capturas.
- Un píxel cuenta como cambiado si algún canal de color se mueve más de 32/255, lo que ignora el antialiasing, y un estado falla si cambió más del 0.1% de sus píxeles.
- Cada corrida guarda sus capturas en `screenshots/visual/actual/` (que no se sube al repo) y reescribe `screenshots/visual/report.md` con el resultado de cada estado. Si alguno cambió, además deja una copia con los píxeles cambiados en rojo en `screenshots/visual/diff/`.

### C. Performance Metrics

`tests/test_performance.py` mide dos cosas con Selenium y cada corrida reescribe [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md) con los resultados.

- **Carga de la página.** Carga la app 5 veces en un perfil de Firefox nuevo, por lo que solo la primera llega con la caché vacía. De cada carga lee la Navigation Timing API del navegador (primer byte, `DOMContentLoaded` y evento `load`) y además mide desde la prueba el tiempo hasta que el campo de texto acepta escritura, que incluye la latencia de WebDriver.
- **Operaciones.** Mide 5 veces cada acción (agregar, completar, editar, borrar, filtrar y limpiar completados), siempre desde el mismo estado inicial y hasta que su efecto se ve en la página, ya que el tiempo incluye la espera explícita del page object.
- Las pruebas fallan si la mediana del evento `load` pasa de 5000 ms o la de una operación pasa de 1000 ms. Los límites son holgados a propósito, porque el sitio es real y la red cambia de una corrida a otra.

En la corrida que dejé en el reporte (con la ventana visible), la primera carga tardó 275 ms hasta el evento `load` y las siguientes 42 ms, ya que GitHub Pages permite guardar en caché el HTML y el bundle (por eso el primer byte llega en 0 ms una vez cacheado). En las operaciones, agregar, completar, filtrar y limpiar quedaron entre 13 y 62 ms, mientras que editar y borrar tardaron cerca de 300 ms. La diferencia no es de la app sino de Selenium, ya que esas dos acciones usan `ActionChains` (doble clic y hover) y cada movimiento del puntero dura 250 ms por defecto.
