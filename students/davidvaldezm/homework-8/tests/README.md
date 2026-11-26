# Plan e índice de pruebas de sistema

Este directorio reúne el plan de aceptación. Las suites ejecutables mantienen la organización
por framework solicitada en Homework 8:

- [Selenium CRUD](../selenium/tests/test_todo_crud.py)
- [Selenium filtros](../selenium/tests/test_todo_filter.py)
- [Playwright CRUD](../playwright/tests/todo-crud.spec.js)
- [Playwright filtros](../playwright/tests/todo-filter.spec.js)
- [Escenarios BDD](../features/todo.feature) y [pasos ejecutables](../features/steps/todo_steps.py)

## Matriz de aceptación

| Caso | Acción | Resultado esperado | Selenium | Playwright |
| --- | --- | --- | --- | --- |
| 01 | Crear una tarea | Texto exacto y una fila | `test_create_single` | `create single` |
| 02 | Crear varias | Orden y contador activo correctos | `test_create_multiple` | `create multiple` |
| 03 | Completar | Checkbox marcado; cero activas | `test_complete_task` | `complete task` |
| 04 | Reactivar | Checkbox desmarcado; una activa | `test_uncomplete_task` | `uncomplete task` |
| 05 | Completar todas | Tres checkboxes marcados; cero activas | `test_complete_all` | `complete all` |
| 06 | Eliminar activa | Lista vacía | `test_delete_single` | `delete single` |
| 07 | Eliminar completada | Lista vacía | `test_delete_completed` | `delete completed` |
| 08 | Limpiar completadas | Solo permanecen activas; contador dos | `test_clear_completed` | `clear completed` |
| 09 | Editar con Enter | Editor cerrado y texto nuevo | `test_edit_enter` | `edit enter` |
| 10 | Cancelar con Escape | Editor cerrado y texto original | `test_edit_cancel` | `edit cancel` |
| 11 | Editar y perder foco | Editor cerrado y texto guardado | `test_edit_blur` | `edit blur` |
| 12 | Crear espacios | No se agrega fila | `test_blank_creation` | `blank creation` |
| 13 | Crear con espacios externos | Texto recortado | `test_trim_creation` | `trim creation` |
| 14 | Guardar edición vacía | Se elimina la tarea | `test_blank_edit_deletes` | `blank edit deletes` |
| 15 | Crear textos duplicados y eliminar uno | Permanece una tarea | `test_duplicate_tasks` | `duplicate tasks` |
| 16 | Filtrar All | Tres textos exactos | `test_filter[All]` | `filter All` |
| 17 | Filtrar Active | Dos textos exactos | `test_filter[Active]` | `filter Active` |
| 18 | Filtrar Completed | Un texto exacto | `test_filter[Completed]` | `filter Completed` |
| 19 | Filtrar sin coincidencias y regresar | Vacío en Completed; tarea presente en All | `test_empty_filter` | `empty filter` |

## Criterios de ejecución y evaluación

Todos los casos utilizan sesiones aisladas, sin datos de otras pruebas. Los filtros regresan a All
y comprueban que no alteraron las tareas. Las acciones se sincronizan con condiciones observables
y tienen límites de espera. Ninguna prueba se considera aprobada por completar solo los clics.

El caso 10 reproduce un defecto de la aplicación publicada y se ejecuta como fallo esperado
estricto en ambos frameworks. No hay fallos inesperados en la ejecución entregada. El resto de
los casos debe aprobar sin reintentos. El detalle y la reproducción están en el
[informe comparativo](../COMPARISON_REPORT.md).

Behave agrega ocho escenarios y 37 pasos: crear, completar, eliminar, tres filtros mediante
Scenario Outline, editar y limpiar. Reutiliza el POM Selenium, sin duplicar selectores.

## Evidencia y comandos

- [Resultados Selenium](../reports/submitted/selenium.txt)
- [Resultados Playwright](../reports/submitted/playwright.txt)
- [Resultados BDD](../reports/submitted/bdd.txt)
- [Tiempos comparados](../reports/submitted/benchmark.json)
- [Captura Selenium](../screenshots/selenium-completed.png)
- [Captura Playwright](../screenshots/playwright-completed.png)

Desde la raíz de la entrega: `python -m pytest`, `npm test --prefix playwright` y
`python -m behave features`. Las instalaciones, variables de entorno y reportes de CI se explican
en el [README principal](../README.md).
