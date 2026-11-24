# Comparación de Selenium y Playwright

## Método y resultados

Ejecución local del 23 de noviembre de 2026, Windows 11, Python 3.12.8, Node 22.19.0,
Selenium 4.38.0 y Playwright Test 1.56.1. Ambos utilizaron **Chrome for Testing 142.0.7444.61**,
headless y tamaño configurado a 1280 × 900 (ventana Selenium; viewport Playwright), con la misma aplicación remota:
[TodoMVC React](https://todomvc.com/examples/react/dist/).

`python scripts/benchmark.py` ejecutó Selenium primero y Playwright después, sin concurrencia
entre suites, con un worker y cero reintentos. Las dependencias y el driver ya estaban instalados.
Los tiempos de pared incluyen arranque del runner, fixtures, pruebas y cierre. No incluyen la
instalación de dependencias. Evidencia: [benchmark.json](reports/submitted/benchmark.json),
[Selenium](reports/submitted/selenium.txt) y [Playwright](reports/submitted/playwright.txt).

| Métrica | Selenium | Playwright |
| --- | ---: | ---: |
| Casos ejecutados | 19 | 19 |
| Casos con comportamiento correcto | 18 | 18 |
| Fallos conocidos reproducidos | 1 | 1 |
| Fallos inesperados | 0 | 0 |
| Tiempo total de pared | 115.68 s | 33.20 s |
| Promedio total / 19 casos | 6.088 s | 1.748 s |
| Setup medido por fixture (ver alcance abajo) | 1.943 s | 0.364 s |

Playwright tardó aproximadamente **3.48 veces menos** en esta corrida. Esta es una observación
de estas suites y este entorno, no una garantía general de rendimiento.

El setup instrumentado tiene alcances diferentes: Selenium mide creación del driver más navegación;
Playwright mide navegación dentro de la fixture `todo`, después de que el runner creó la página.
Por eso la última fila **no es una comparación directa del arranque del navegador**. Selenium crea
y cierra Chrome por caso; Playwright reutiliza un proceso y crea contextos aislados por caso. El
tiempo total sí incluye ambos ciclos de vida y refleja estas decisiones habituales de cada runner.

Limitaciones: una sola corrida secuencial; orden fijo; cachés y condiciones de red variables;
HTML remoto mutable; lanzamientos de navegador distintos; el área interior de la ventana Selenium
puede ser menor que el viewport Playwright por los bordes del navegador. La prueba de Escape espera hasta 10 s
en ambos frameworks antes de clasificar el defecto esperado, y ese tiempo está incluido.
No se midió capacidad del servidor ni se compararon navegadores diferentes.

## Defecto conocido: cancelación

Pasos reproducidos en ambos frameworks:

1. Crear `Draft` u `Original`.
2. Hacer doble clic en la etiqueta.
3. Reemplazar el texto por `Discard`.
4. Presionar Escape.

Esperado: editor cerrado y texto original conservado. Observado: el editor permanece abierto y
el texto modificado sigue presente; perder el foco lo guarda. Las suites conservan la expectativa
correcta: `xfail(strict=True)` en pytest y `test.fail` en Playwright. Si se arregla la aplicación,
el éxito inesperado exige retirar la marca. **No se omite la ejecución del caso.**

Playwright presenta `19 passed` al incluir el fallo esperado entre los resultados aceptados.
Eso significa **18 comportamientos aprobados y un defecto reproducido**, no 19 funciones correctas.
El [contexto del defecto](reports/submitted/known-defect.md) conserva el estado del DOM y la acción
que agotó la espera. Los fallos inesperados generan trazas y capturas en CI. El README muestra cómo ejecutar
Selenium con `--runxfail` para obtener un fallo convencional.

## Código y complejidad

Conteo físico de líneas, con blancos/comentarios incluidos; el conteo sin blancos se muestra
entre paréntesis. Se compara la misma cobertura funcional, sin dependencias ni reportes generados.

| Archivo o grupo | Selenium / Python | Playwright / JavaScript |
| --- | ---: | ---: |
| Page Object de tareas | 136 (114) | 65 (54) |
| Pruebas CRUD | 103 (72) | 87 (75) |
| Pruebas de filtros | 29 (24) | 23 (21) |

El POM Selenium concentra esperas explícitas para texto, conteo, estado, eliminación y edición.
También implementa lectura de etiquetas y conteo visible. El POM Playwright expone locators;
`expect(locator)` se encarga de reintentar las verificaciones desde los tests. No trasladé las
aserciones de negocio a los Page Objects para reducir artificialmente las líneas de prueba.

Ambos tienen decisiones para guardar con Enter, cancelar con Escape y guardar al perder el foco.
Selenium añade más coordinación entre comandos y resultados; Playwright añade el manejo uniforme
de `async/await`. Las diferencias de formato, docstrings, APIs expuestas y parametrización afectan
LOC: este conteo por sí solo no mide calidad ni complejidad ciclomática.

## Experiencia de desarrollo

| Aspecto | Selenium | Playwright | Observación de esta implementación |
| --- | --- | --- | --- |
| Instalación | Python, Chrome y driver compatible | npm y Chrome para el canal elegido | El Chrome local no coincidía con el driver; resolví ambos con el mismo Chrome for Testing |
| Esperas | `WebDriverWait` y condiciones explícitas | Comprobaciones automáticas y aserciones que reintentan | Sin `sleep`, clics forzados ni mutación del estado mediante JavaScript |
| Depuración | Excepciones y capturas tomadas por fixture | Inspector, HTML, trazas y capturas integrados | El fallo de Escape se puede inspeccionar sin repetir manualmente las acciones |
| Documentación | Secciones separadas por lenguaje y WebDriver | Guías del runner, locators, assertions y fixtures | Ambas documentan las piezas utilizadas; Playwright agrupa mejor este flujo de trabajo |
| Errores | `NoSuchElementException` o timeout de condición | Log del locator y de la espera que falla | El contador actual usa texto directo, sin el `strong` supuesto por ejemplos antiguos |
| Soporte IDE | Navegación Python y pytest | Extensión VS Code, ejecución y depuración del runner | Integraciones disponibles; no se hizo una evaluación comparativa de IDEs |

Selenium requiere sincronizar explícitamente las condiciones relevantes; su documentación explica
las [estrategias de espera](https://www.selenium.dev/documentation/webdriver/waits/).
Playwright comprueba visibilidad, estabilidad y otros requisitos antes de actuar, y ofrece
[aserciones con reintentos](https://playwright.dev/docs/actionability).

## Recomendaciones y aprendizaje

Elegiría Selenium para ampliar una suite WebDriver existente, aprovechar un Grid ya desplegado
o mantener equipos que ya trabajan con Python y Behave. Su integración BDD fue directa: las
definiciones de pasos reutilizan exactamente el POM de pytest.

Elegiría Playwright para un proyecto web nuevo que necesite aislamiento por contexto, trazas,
reportes y paralelismo con poca infraestructura adicional. Para esta tarea requirió un POM más
corto y la suite terminó antes. El comando paralelo está disponible, pero no se usó para inflar
la diferencia de esta comparación.

La lección principal fue verificar la aplicación antes de asumir que los ejemplos seguían vigentes:
cambiaron la URL, el DOM del contador y la implementación del toggle-all. También aprendí a separar
un defecto real del producto de un error en la automatización: cambiar la expectativa de Escape
habría producido una suite verde que validaba el comportamiento incorrecto.

## Calidad y alcance

La ejecución Selenium cubrió **84 de 86 sentencias (97.67 %)** de sus Page Objects y configuración
del navegador. Las dos líneas no cubiertas pertenecen al método de recarga que no utiliza esta
entrega. No es cobertura del código fuente de TodoMVC ni de la implementación JavaScript del POM.
Pylint dio 10.00/10; ESLint y Black finalizaron sin errores. Behave y las métricas adicionales
se conservan en los reportes adjuntos. Se eligieron los bonus C (rendimiento) y D (pipeline CI).
