# Reporte de análisis estático

## 1. Alcance y problemas encontrados

Study Task Planner es una aplicación de consola que administra tareas de estudio
mediante archivos JSON. La entrega contiene tres módulos
funcionales y un inicializador dentro de `src/`, con más de cien líneas de código.
La versión inicial incluyó defectos intencionales de mantenimiento para comparar
el comportamiento de los analizadores antes y después de corregirlos.

Pylint encontró ocho avisos de siete tipos y asignó 9.29/10. Hubo seis mensajes
de convención, una advertencia y una recomendación de refactorización. La única
categoría repetida fue la comprobación no idiomática de tipos, presente en dos
campos. No aparecieron errores fatales ni diagnósticos de complejidad. isort
detectó imports incorrectamente organizados en un archivo; Black aceptó el formato
inicial. Los diagnósticos originales están conservados en `reports/pylint-before.json`
y `reports/pylint-before.txt`, asociados al código del commit `3890861`.

## 2. Correcciones documentadas

Las ubicaciones corresponden a la versión inicial. Los ejemplos identifican las
expresiones cambiadas; el código completo está en el historial y los archivos actuales.

| Problema y herramienta | Ubicación inicial | Antes | Después |
| --- | --- | --- | --- |
| C0410, Pylint: imports múltiples | `src/storage.py:3` | `import os, json` | `import json` |
| W0611, Pylint: import sin uso | `src/storage.py:3` | `os` importado | Import innecesario eliminado |
| C0123, Pylint: comprobación de tipos | `src/storage.py:17,21` | `type(identifier) is not int` | `isinstance` y rechazo explícito de booleanos, también para prioridad |
| C0114, Pylint: documentación ausente | `src/tasks.py:1` | Sin docstring de módulo | Docstring descriptivo al inicio |
| C0103, Pylint: nombre inconsistente | `src/tasks.py:25` | `TaskName` | `task_name` |
| R1705, Pylint: rama redundante | `src/tasks.py:63` | `else` después de `return` | Cálculo posterior sin `else` |
| C0121, Pylint: comparación redundante | `src/tasks.py:66` | `task.completed == True` | `task.completed` |

La corrección de tipos necesitó especial cuidado: en Python, un booleano también
es instancia de entero. Reemplazar solamente `type` habría permitido identificadores
inválidos. Se añadió un rechazo explícito de booleanos para conservar la validación.
También se simplificó la condición de título vacío; esta mejora adicional no se
contabiliza como diagnóstico encontrado por Pylint.

## 3. Beneficios observados

Después de las correcciones, Pylint reportó cero avisos y 10.00/10. Black e isort
aceptaron todos los módulos. Bandit analizó el código sin encontrar problemas.
Estas herramientas identificaron automáticamente inconsistencias que una revisión
manual podría detectar, pero que son fáciles de omitir cuando la atención está
concentrada en la funcionalidad. Los informes permiten comprobar cada resultado
sin depender de una descripción subjetiva del cambio.

La preparación requirió resolver dependencias, configurar reglas y atender rutas
largas de Windows. No se midió de forma aislada su duración, por lo que no se
presenta una cifra de ahorro como resultado experimental. El beneficio esperado
es reducir correcciones repetitivas en futuras revisiones. Además, una comprobación
local recorrió comandos válidos, entradas rechazadas y persistencia de datos;
esta comprobación complementa el análisis y no representa cobertura de pruebas.

## 4. Integración en el equipo

En el editor ejecutaría Pylint continuamente y aplicaría Black al guardar. Antes
de cada commit, los nueve hooks revisarían exclusivamente la carpeta de esta
entrega. En integración continua ejecutaría los mismos comandos y versiones para
detectar diferencias de entorno o hooks omitidos. Los mensajes de commit deberían
seguir Conventional Commits y separar configuración, correcciones y documentación.

Las herramientas comparten un límite de 88 columnas, y el perfil de isort coincide
con Black para evitar cambios contradictorios. El filtro por carpeta protege el
trabajo de otros estudiantes. La instalación del hook y su ejecución completa
permanecen pendientes, al igual que la publicación. Los cinco commits requeridos
están registrados localmente. No se afirma una validación mediante
commit ni una calificación automática inexistentes.

## 5. Recomendaciones

Pylint aportó los diagnósticos más útiles; Black e isort redujeron decisiones
repetitivas de formato. Bandit ofrece una revisión adicional, aunque cero hallazgos
no demuestra ausencia de vulnerabilidades. Mantendría las reglas activas y
documentaría cualquier excepción futura. Incorporaría estas herramientas en nuevos
proyectos por su retroalimentación temprana y actualizaría las versiones mediante
cambios revisables, repitiendo las verificaciones antes de aceptar cada actualización.
