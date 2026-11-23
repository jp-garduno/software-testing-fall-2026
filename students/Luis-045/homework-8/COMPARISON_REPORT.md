# Comparison Report: Selenium vs Playwright

- **Alumno:** Luis-045
- **Rama:** `feat/Luis-045/homework-8`
- **Fecha de validación:** 23 de noviembre de 2026

Las dos implementaciones automatizan los mismos 18 casos sobre TodoMVC React. Ambas aprobaron 17 y reprodujeron el defecto de cancelación con Escape. Playwright terminó antes en la ejecución medida; esta conclusión corresponde a la configuración y al equipo descritos aquí.

## 1. Execution Time Comparison

### Entorno y método

- Windows 11, compilación 10.0.26300, x64.
- Google Chrome 157.0.8103.79, headless, en ambas suites.
- Selenium 4.54.0, pytest 9.2.0, Python 3.12.14.
- Playwright Test 1.65.1, Node.js 22.14.0.
- URL: `https://todomvc.com/examples/react/dist/`.
- Una ejecución completa de cada suite con un worker, realizada consecutivamente, sin reintentos.
- Navegadores y dependencias ya instalados; las descargas e instalación no forman parte de la medición.

Los tiempos se toman de los runners, no de una estimación. `conftest.py` registra la sesión y las fases de pytest; el reporter de Playwright usa `FullResult.duration` y la fase `Before Hooks` de cada caso.

| Metric                        | Selenium | Playwright |
| ----------------------------- | -------: | ---------: |
| Total execution time          | 76.630 s |   21.021 s |
| Average per test              |  4.257 s |    1.168 s |
| Setup time, promedio por caso |  1.180 s |    0.348 s |
| Casos ejecutados              |       18 |         18 |
| Aprobados                     |       17 |         17 |
| Fallos esperados ejecutados   |        1 |          1 |
| Fallos inesperados            |        0 |          0 |

**Definiciones:** el tiempo total incluye la sesión del runner, preparación, pruebas, capturas y cierre de recursos. El promedio por caso es total / 18. Setup es el promedio de la fase de preparación por caso: obtención del navegador o contexto, navegación y datos preparados por fixtures/hooks. No significa tiempo de instalar paquetes.

Evidencia original:

- [Resultados Selenium](reports/selenium-results.json).
- [Resultados Playwright serial](reports/playwright-results.json).

En esta corrida Playwright usó aproximadamente 3.65 veces menos tiempo total. Hay una diferencia de ciclo de vida que explica parte del resultado: Selenium inicia y cierra Chrome por prueba, mientras Playwright mantiene un navegador por worker y crea un contexto aislado por caso. Se comparan las suites tal como están implementadas; la tabla no aísla solamente el coste del protocolo de automatización.

Ambos tiempos incluyen aproximadamente diez segundos dedicados a detectar que Escape no cierra el editor. Una medición aislada y con una aplicación remota depende también de la red, el equipo y las cachés; no establece una superioridad universal.

### Ejecución paralela

Playwright también se ejecutó con dos workers: **15.676 s**, con 17 aprobados, un fallo esperado y ningún fallo inesperado. Los perfiles independientes evitaron interferencia entre tareas. Esta corrida queda separada de la comparación serial: [resultados paralelos](reports/playwright-parallel-results.json).

### Reproducción

Desde `students/Luis-045/homework-8/`, después de instalar las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
npm.cmd --prefix playwright run test:serial
$env:PW_REPORT_NAME = "playwright-parallel-results.json"
npm.cmd --prefix playwright run test:parallel
$env:PW_REPORT_NAME = $null
```

## 2. Code Comparison

Se midieron el Page Object y los dos archivos de pruebas equivalentes de cada framework. LOC significa líneas físicas, incluyendo comentarios y blancos. Se excluyen configuración, dependencias, reporteros, fixtures compartidas, hooks de Behave y evidencia generada.

| Componente                     | Selenium | Playwright |
| ------------------------------ | -------: | ---------: |
| Page Object                    |  158 LOC |    112 LOC |
| Dos archivos de pruebas        |  164 LOC |    153 LOC |
| Total comparado                |  322 LOC |    265 LOC |
| Funciones/callbacks medidos    |       42 |         40 |
| Complejidad ciclomática media  |    1.095 |      1.100 |
| Complejidad ciclomática máxima |        2 |          2 |

Herramientas: mccabe 0.7.0 para Python y la regla `complexity` de ESLint 8.57.1 para JavaScript. La regla se ejecuta con umbral cero para extraer el valor de todas las funciones; sus advertencias son datos de medición, no errores de calidad de la entrega. Los analizadores no cuentan todas las construcciones de ambos lenguajes de forma idéntica.

Los datos por archivo y función están en [code-metrics.json](reports/code-metrics.json). Se reproducen con:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe reports/measure_code.py
```

Playwright necesitó 57 líneas físicas menos, aproximadamente un 17.7% del total de Selenium en el alcance medido. La diferencia principal está en sincronización: Selenium expresa las esperas de visibilidad, edición y actualización de listas; Playwright usa localizadores y comprobaciones reintentables.

La complejidad ciclomática es baja en ambos. No describe por sí sola el esfuerzo de mantener un selector o diagnosticar una carrera. La implementación Python coloca las aserciones funcionales en los tests; el objeto JavaScript también ofrece métodos `expect...` que encapsulan comprobaciones con espera.

## 3. Developer Experience

Evaluación basada en la preparación y ejecución de esta entrega:

| Aspect                | Selenium                                                       | Playwright                                                                     | Notes                                                                       |
| --------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| Setup difficulty      | Entorno Python y ChromeDriver resuelto por Selenium Manager    | npm ci y Chrome instalado configurado por channel                              | Ambos utilizaron el mismo Chrome; las versiones directas están fijadas      |
| Auto-waiting          | Se implementan esperas explícitas con WebDriverWait            | Los localizadores y expect esperan el estado esperado                          | No se usan pausas fijas                                                     |
| Debugging             | Capturas, traceback de pytest y ejecución visible              | Capturas, HTML, contexto del error y trazas cuando hay fallos inesperados      | La reproducción de Escape permite ver la diferencia de diagnóstico          |
| Documentation quality | Guías separadas de navegador, interacciones y esperas          | Guías del runner, fixtures, aserciones y depuración en una misma documentación | Ambas sirvieron para implementar el POM                                     |
| Error messages        | El timeout informa que no se cumplió la condición              | La aserción muestra editor esperado 0, recibido 1 y llamadas de espera         | Playwright aportó más contexto en el defecto observado                      |
| IDE support           | Tests Python y depuración de pytest desde editores compatibles | Extensión oficial de Playwright para VS Code y depuración de Node              | Las suites se verificaron por CLI; no se evaluó interacción con extensiones |

Documentación de referencia: [esperas de Selenium](https://www.selenium.dev/documentation/webdriver/waits/), [configuración de Playwright](https://playwright.dev/docs/test-configuration), [Trace Viewer](https://playwright.dev/docs/trace-viewer), [Playwright para VS Code](https://playwright.dev/docs/getting-started-vscode) y [hooks y pasos de Behave](https://behave.readthedocs.io/en/stable/api/).

El resultado de Behave fue **7 escenarios y 33 pasos aprobados**, sin pasos indefinidos o escenarios omitidos: [JSON de Behave](reports/behave-results.json). Reutilizar el POM de Selenium evitó duplicar los selectores en las definiciones de pasos.

## 4. Recommendations

### ¿Cuándo elegiría Selenium?

Cuando el proyecto ya tenga infraestructura WebDriver, Selenium Grid, utilidades Python o escenarios Behave que convenga reutilizar. En esta entrega permite compartir directamente el modelo de página entre pytest y BDD. Debe reservarse atención a las condiciones explícitas de espera y al ciclo de vida del navegador.

### ¿Cuándo elegiría Playwright?

Para iniciar una suite web con JavaScript donde interese tener fixtures, aislamiento por contexto, aserciones con espera, ejecución paralela y diagnóstico integrados. En esta implementación dio menos código de sincronización y tiempos totales menores. Esa recomendación se apoya en la prueba medida, no en una promesa para cualquier aplicación.

### ¿Qué aprendí?

El POM concentra el impacto de cambios del DOM: adaptar el contador a la versión publicada no exigió reescribir cada caso. El aislamiento permite ejecutar los mismos datos en paralelo. Una comparación de tiempos debe indicar si crea un navegador por prueba o reutiliza procesos.

Una prueba útil también puede revelar un defecto del sistema bajo prueba. Ajustar una expectativa para aceptar que Escape guarde o deje abierto el editor habría eliminado la comprobación pedida. Por eso el caso sigue ejecutándose con su expectativa original y su defecto registrado.

## Defecto TODO-001: cancelar la edición con Escape

**Requisito:** cancelar una edición debe cerrar el editor y conservar el título previo.

**Pasos reproducidos en ambos frameworks:**

1. Crear una tarea con el título `Original title`.
2. Hacer doble clic en su texto.
3. Reemplazar el borrador por `Discard this draft`.
4. Presionar Escape.
5. Esperar que desaparezca el editor y que el título siga siendo `Original title`.

**Resultado observado:** el editor permanece abierto con el borrador. La implementación publicada del input maneja Enter y blur, pero no Escape. La comprobación se dejó intacta; no se inyectó código ni se cambió la aplicación remota.

Evidencia:

- [Captura Selenium tras Escape](screenshots/selenium-test_cancel_edit.png).
- [Captura Playwright tras Escape](screenshots/playwright-cancel-edit.png).
- [Ejecución Selenium sin xfail: un fallo](reports/known-defect-selenium.json).
- [Ejecución Playwright sin test.fail: un fallo](reports/known-defect-playwright.json).

La marca es estricta: un resultado inesperadamente aprobado hace fallar la suite para revisar si el defecto se corrigió. En Selenium se limita además al tipo `TimeoutException`. En Playwright se activa después de preparar el borrador.

Para repetir las ejecuciones sin clasificar el defecto como esperado:

```powershell
$env:VERIFY_KNOWN_DEFECTS = "1"
$env:SELENIUM_REPORT_NAME = "known-defect-selenium.json"
.\.venv\Scripts\python.exe -m pytest -q selenium/tests/test_todo_crud.py::test_cancel_edit --tb=short

$env:PW_REPORT_NAME = "known-defect-playwright.json"
npm.cmd --prefix playwright run test:serial -- --grep "cancel edit"

$env:VERIFY_KNOWN_DEFECTS = $null
$env:SELENIUM_REPORT_NAME = $null
$env:PW_REPORT_NAME = $null
```

Ambos comandos de prueba deben terminar con código 1 mientras el defecto siga presente. Esto es evidencia del comportamiento de la app, no una entrega con todas sus funcionalidades aprobadas.

## Alcance

Se entregan las cuatro partes base. No se reclaman bonos de regresión visual, otros navegadores, métricas de rendimiento o CI/CD. Los tiempos de las suites corresponden al reporte comparativo obligatorio.
