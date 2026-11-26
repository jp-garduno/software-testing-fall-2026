# Homework 8: End-to-End Test Automation – TodoMVC

**Alumno**: Angel Isaac Barbarín (`angelbarbarin`)

Pruebas de sistema de la aplicación [TodoMVC React](https://todomvc.com/examples/react/dist/) con **Selenium**
(Python + pytest), **Playwright** (JavaScript + @playwright/test) y **BDD** (behave), las tres sobre el patrón
**Page Object Model**, más un reporte comparando ambos frameworks.

## Resultados

| Suite | Pruebas | Resultado |
| ----- | ------- | --------- |
| Selenium (`pytest`) | 30 | ✅ 30 passed |
| BDD (`behave`, también corre dentro de `pytest`) | 9 escenarios, 38 pasos | ✅ passed |
| Playwright – CRUD y filtros | 30 | ✅ 30 passed |
| Playwright – bonus A (regresión visual) | 5 | ✅ 5 passed |
| Playwright – bonus C (rendimiento) | 2 | ✅ 2 passed |

Evidencia en `screenshots/` y el análisis en [COMPARISON_REPORT.md](COMPARISON_REPORT.md).

## Aplicación bajo prueba

El enunciado enlaza `https://todomvc.com/examples/react/`, que hoy responde **404**. La app está en
`https://todomvc.com/examples/react/dist/`, y ese es el valor por defecto de todas las suites. Se puede cambiar
con la variable `BASE_URL`, por ejemplo para probar una copia local:

```bash
git clone --depth 1 https://github.com/tastejs/todomvc.git
cd todomvc/examples/react/dist && python -m http.server 8765
# en otra terminal:  BASE_URL=http://localhost:8765/
```

La versión de React no guarda nada en `localStorage`: recargar la página deja la lista vacía. Por eso cada prueba
empieza con la página recién cargada y las pruebas no dependen unas de otras.

## Selenium + BDD (Python)

Requisitos: Python 3.10+ y Google Chrome. Selenium Manager descarga solo el chromedriver correcto.

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt

pytest -v                      # 30 pruebas de Selenium + los escenarios BDD
pytest selenium/tests -v       # solo Selenium
behave features                # solo BDD, con la salida de Gherkin
```

Variables opcionales: `HEADED=1` (ver el navegador), `BASE_URL`, `CHROME_BINARY`, `CHROMEDRIVER_PATH` y
`CHROMEDRIVER_ARGS` (ver `selenium/driver_factory.py`). Si una prueba falla, se guarda una captura en
`screenshots/selenium-failures/` (o `bdd-failures/`).

## Playwright (JavaScript)

Requisitos: Node.js 22+.

```bash
cd playwright
npm install
npx playwright install chromium
npx playwright test                 # las 37 pruebas
npm run test:crud                   # solo CRUD y filtros
npx playwright show-report          # reporte HTML con trazas y diffs
```

**Regresión visual (bonus A):** las imágenes base están en `playwright/tests/__screenshots__/` y se generaron en
Linux con Chromium. Las fuentes se ven distinto en otro sistema operativo, así que en una máquina nueva primero
hay que crear sus propias bases con `npm run update-snapshots` y después correr las pruebas normalmente.

## Estructura

```
homework-8/
├── selenium/
│   ├── pages/todo_page.py          # Page Object (Selenium) con esperas explícitas
│   ├── driver_factory.py           # Crea Chrome (headless por defecto)
│   ├── tests/conftest.py           # Navegador por sesión, página nueva por prueba, captura al fallar
│   ├── tests/test_todo_crud.py     # Crear, completar, borrar, editar (19 pruebas)
│   ├── tests/test_todo_filter.py   # Filtros All / Active / Completed (11 pruebas)
│   └── requirements.txt
├── playwright/
│   ├── pages/TodoPage.js           # Page Object (Playwright), auto-waiting
│   ├── tests/todo-crud.spec.js     # Mismos escenarios que Selenium
│   ├── tests/todo-filter.spec.js
│   ├── tests/visual.spec.js        # Bonus A: regresión visual
│   ├── tests/performance.spec.js   # Bonus C: métricas de rendimiento
│   ├── tests/__screenshots__/      # Imágenes base de la regresión visual
│   ├── reports/performance.md      # Último reporte de rendimiento
│   ├── playwright.config.js
│   └── package.json
├── features/
│   ├── todo.feature                # 9 escenarios Gherkin (incluye un Scenario Outline)
│   ├── environment.py              # Hooks de behave (navegador, capturas)
│   ├── steps/todo_steps.py         # Pasos que reutilizan el Page Object de Selenium
│   └── test_bdd_scenarios.py       # Corre behave desde pytest
├── screenshots/                    # Evidencia de las ejecuciones
├── requirements.txt
├── pytest.ini
├── COMPARISON_REPORT.md
└── README.md
```

## Escenarios cubiertos

| Área | Selenium y Playwright (mismos casos) |
| ---- | ------------------------------------ |
| Creación | una tarea, varias en orden, aparece en la lista y limpia el campo, ignora texto vacío, recorta espacios |
| Completar | marcar, desmarcar, varias, marcar todas con la flecha |
| Borrar | una tarea, una completada, "Clear completed", borrar la última oculta el pie |
| Editar | cambiar el texto, doble clic entra en edición, salir sin cambios conserva el texto, guardar al perder el foco, texto vacío borra la tarea, recorta espacios |
| Filtros | All, Active, Completed, All seleccionado por defecto, completar desde Active, agregar desde Completed, limpiar desde Completed, filtro por nombre, nombre inválido |

## Hallazgos sobre la aplicación

- **El enlace del enunciado da 404**: la app está en `/examples/react/dist/`.
- **Escape no cancela la edición.** La especificación de TodoMVC dice que Escape debe descartar los cambios, pero
  en esta versión de React Escape no hace nada y, al salir del campo, se guarda el texto modificado. Por eso
  "Cancel edit" se probó como *salir de la edición sin cambios* y se documenta aquí como defecto de la app en vez
  de dejar una prueba fallando.
- **El botón "Clear completed" solo existe visualmente cuando hay tareas completadas** (atributo `hidden`).
- **La casilla "marcar todas" está encima de su etiqueta**: en Selenium, hacer clic en la etiqueta lanza
  `ElementClickInterceptedException`; hay que hacer clic en el `input`.

## Bonus

- **A – Regresión visual**: 5 estados clave (vacío, lista mixta, filtro Completed, edición, todo completado) se
  comparan contra imágenes base con un margen de 1% de píxeles; el reporte HTML muestra *expected / actual / diff*.
- **C – Métricas de rendimiento**: tiempos de carga con la Navigation Timing API y duración de operaciones con 50
  tareas (agregar, marcar todas, cambiar filtro, limpiar). Genera `playwright/reports/performance.json` y
  `performance.md`, y falla si una operación excede un presupuesto amplio.

## Cómo se ejecutó para esta entrega

Las ejecuciones de `screenshots/` y los tiempos del reporte se tomaron en un entorno Linux sin acceso a
todomvc.com, contra una **copia local de la misma app** (el `dist/` del repositorio `tastejs/todomvc`, que se
comparó con la versión publicada: mismo HTML y el mismo bundle). Se usó Chromium 153 con un chromedriver 147
y la opción `--disable-build-check`. En una máquina normal (y en el CI del curso) las pruebas corren contra el
sitio real sin configurar nada.
