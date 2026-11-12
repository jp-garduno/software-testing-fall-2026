# Verificación local

Ejecutada con Python 3.12.14. La integración continua repite las verificaciones en Python 3.11 y 3.12.

| Verificación | Resultado |
| --- | --- |
| Pruebas | 94 aprobadas, ninguna omitida |
| Duración de pytest con cobertura | 0.70 segundos |
| Sentencias | 142/142 = 100% |
| Ramas | 42/42 = 100% |
| Pylint | 10.00/10, sin mensajes |
| Black | Formato verificado |
| isort | Importaciones verificadas |
| HTML de cobertura | Páginas y referencias locales verificadas |
| Reflexión | 573 palabras |

La duración corresponde a la medición que informa pytest; el tiempo total de arranque del proceso depende de la máquina y sus plugins. [Resumen de cobertura legible por máquina](coverage-summary.json).

```text
........................................................................ [ 76%]
......................                                                   [100%]
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.14-final-0 _______________

Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
src\__init__.py       0      0      0      0   100%
src\book.py          24      0     10      0   100%
src\library.py       64      0     16      0   100%
src\loan.py          17      0      0      0   100%
src\member.py        37      0     16      0   100%
-------------------------------------------------------------
TOTAL               142      0     42      0   100%
Coverage HTML written to dir coverage
Coverage JSON written to file coverage.json
Required test coverage of 90.0% reached. Total coverage: 100.00%
94 passed in 0.70s
```

Los reportes incluyen sólo `src/`, sin contar las pruebas como código cubierto. El workflow exige más de 90% de sentencias y más de 85% de ramas de manera separada. Los resultados de GitHub se consultan en el PR; esta página registra la ejecución local.
