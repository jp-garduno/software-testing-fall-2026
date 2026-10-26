# Proceso TDD: cinco ciclos documentados

Las fases que siguen se ejecutaron durante el desarrollo. Los ejemplos de código
se extraen de los commits indicados, no se reconstruyen a partir de la solución final.
Los ciclos pueden contener pasos intermedios: se identifica explícitamente cuándo
la refactorización se realizó después de otras pruebas del mismo subsistema.

En total se registraron **54 fases RED, 54 GREEN y 8 REFACTOR**: 116 commits TDD.
Cada GREEN ejecutó la suite completa disponible en ese momento; cada RED ejecutó
la prueba nueva antes de modificar el código. Los primeros tres módulos produjeron
errores de importación porque todavía no existían; los otros 51 RED fallaron al
comprobar el comportamiento. No se interpretan como fallos válidos errores de sintaxis.

Los casos de integración posteriores son regresiones adicionales y se identifican
como tales. El archivo [tdd-runs.jsonl](evidence/tdd-runs.jsonl) conserva 62 registros,
uno por par RED/GREEN o por REFACTOR, con resultados, cambios y hashes completos.
Solo se normalizó la ruta absoluta de la entrega en las salidas archivadas.

