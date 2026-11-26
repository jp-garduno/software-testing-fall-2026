# Tarea 8 — BDD y pruebas de sistema

**Alumno:** Vittorio Catino. Selenium, Playwright y Behave implementados en Python.

Se prueba la aplicación oficial TodoMVC React. No se construye una aplicación
sustituta ni se simulan las interacciones del navegador.

## Instalación

Requisitos: Python 3.11 o posterior y Google Chrome instalado.

```bash
cd students/vittoriocatino/homework-8
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_all.py
```

Selenium Manager obtiene el controlador compatible con Chrome automáticamente.
Playwright usa `channel="chrome"`, por lo que ambos frameworks ejecutan el mismo
navegador instalado. No es necesario descargar los navegadores empaquetados de
Playwright. En CI se configura `CHROME_BINARY` con la ruta de Chrome instalada
manualmente. El workflow usa Chrome preinstalado en el runner Ubuntu y comprueba
su versión antes de ejecutar los tests, igual que el validador general del curso.

## Comandos separados

```bash
python -m pytest selenium/tests -q
python -m pytest playwright/tests -q
python -m behave features --junit --junit-directory reports/bdd-junit
python -m pytest -k cancel_edit --runxfail -q
```

El último comando muestra deliberadamente el defecto externo documentado en
`DEFECTS.md`. La suite normal conserva esas aserciones como fallas conocidas
estrictas. Los resultados se reportan como aprobados y xfailed por separado.

## Escenarios equivalentes

| Grupo | Casos por framework | Aserciones |
|---|---:|---|
| Creación | 3 | Uno, varios, texto recortado y presencia en lista |
| Completar | 3 | Completar, reactivar, completar varios; checkbox y contador |
| Eliminar | 3 | Activo, completado, limpiar sólo completados |
| Filtros | 3 | All, Active y Completed con lista y estados exactos |
| Editar | 3 | Guardar por Enter, cancelar por Escape, guardar por blur |

Cada framework implementa los 15 casos. BDD usa Given/When/Then, una tabla de
datos y un Scenario Outline para los tres filtros. Los pasos reutilizan el
Page Object de Playwright y se ejecutan con Behave.

## Diseño y aislamiento

- Los selectores y la sincronización están encapsulados en los Page Objects.
  Los tests sólo expresan acciones y resultados de negocio.
- Selenium usa esperas explícitas y vuelve a buscar filas tras cambios del DOM.
  Playwright usa locators y aserciones web-first. No se usan sleeps fijos.
- Cada caso empieza sin tareas. Selenium usa un perfil desechable y limpia el
  almacenamiento de la demo; Playwright/Behave crean un contexto nuevo por caso.
  Ninguna acción toca el perfil personal de Chrome ni una cuenta del usuario.
- El origen es configurable mediante `TODO_URL`. El valor por defecto es
  `https://todomvc.com/examples/react/dist/`, la versión React enlazada en
  `https://todomvc.com/`. La URL antigua del enunciado devuelve 404.
- Se capturan estados de creación, completado, filtro y cancelación por
  framework. Behave también captura cada escenario.
- La demo es externa y puede cambiar o no estar disponible. Los errores de
  conexión no se convierten en pruebas aprobadas ni se silencian con retries.

## Evidencia y comparación

`reports/` conserva salidas reales de pytest y Behave, JUnit XML, resultados
BDD JSON, tiempos de procesos, inicialización de navegador y operaciones de
los Page Objects. `screenshots/` contiene capturas reales. El runner se detiene
con código distinto de cero ante cualquier fallo inesperado.

`COMPARISON_REPORT.md` compara los mismos escenarios en el mismo Chrome y
explica las limitaciones de las mediciones. `PERFORMANCE_REPORT.md` corresponde
al bonus C. El workflow `.github/workflows/homework-8-vittoriocatino.yml` ejecuta
ambas suites y BDD en push/PR y publica reportes/capturas como artifacts
(bonus D). La ejecución local no se presenta como una ejecución de GitHub CI.

## Fuentes

- Enunciado: https://github.com/jp-garduno/software-testing-fall-2026/blob/main/08-system-level-testing/homework/homework-8.md
- Aplicación: https://todomvc.com/examples/react/dist/
- Selenium: https://www.selenium.dev/documentation/
- Playwright Python: https://playwright.dev/python/
- Behave: https://behave.readthedocs.io/
