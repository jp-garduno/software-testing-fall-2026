# Verificación local

Fecha: 2026-09-14. Entorno: Windows, Python 3.12.14.

| Verificación ejecutada | Resultado |
| --- | --- |
| Pylint 3.3.8, antes | 8 avisos; 9.29/10 |
| Pylint 3.3.8, después | 0 avisos; 10.00/10 |
| Black 25.1.0, `--check src` | 4 archivos aceptados |
| Black 26.3.1, `--check --diff src`, tras actualización de seguridad | 4 archivos aceptados, sin cambios |
| isort 6.0.1, `--check-only src` | Sin diferencias |
| Bandit 1.8.6, `-r src` | 0 hallazgos |
| pre-commit 4.3.0, `validate-config` | Configuración válida |
| Comprobación funcional local | 10 escenarios de CLI aceptados |
| Validación de datos | Persistencia correcta; booleanos rechazados como identificador y prioridad |

Los escenarios ejecutados cubrieron colección vacía, dos altas, completar una
tarea, listar pendientes, resumir progreso, título vacío, identificador inexistente,
prioridad fuera de rango y JSON inválido. Se comprobó que los errores no añadieran
tareas y que el JSON inválido no fuera sobrescrito. Se utilizaron archivos
temporales fuera de la entrega y se eliminaron al terminar.

Pendiente: instalación del hook, ejecución de los nueve hooks mediante pre-commit,
verificación con un commit real y calificación automática del PR. Los resultados
individuales de los analizadores no sustituyen esas verificaciones pendientes.

## Actualización de seguridad de Black

Se actualizó Black de 25.1.0 a 26.3.1 tanto en `requirements.txt` como en el
hook de pre-commit para corregir
[CVE-2026-32274](https://github.com/advisories/GHSA-3936-cmfr-pm3m).
La fila de Black 25.1.0 conserva el resultado histórico del análisis inicial.
Con la nueva versión, Black e isort aceptaron el código, Pylint mantuvo 10.00/10
y `python -m pip check` no detectó dependencias incompatibles.
La confirmación de cierre de la alerta corresponde al siguiente análisis del PR.
