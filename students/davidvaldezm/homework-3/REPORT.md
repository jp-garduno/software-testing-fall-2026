# Reporte de análisis estático

## Alcance y método

Se creó una biblioteca de presupuestos personales como proyecto nuevo para esta
tarea. Contiene módulos de transacciones, presupuestos y almacenamiento, además
del inicializador del paquete. Permite registrar gastos, consultar categorías y
guardar datos mediante JSON. El primer commit incluye problemas intencionales,
como solicita el ejercicio. La comparación usa código realmente ejecutado: el
archivo `reports/pylint-before.txt` conserva la salida inicial y el historial
permite reproducirla sin modificar la versión final.

La validación inicial utilizó Python 3.12.14, Pylint 3.3.8, Black 25.1.0 e isort
6.0.1. Las dependencias directas tienen versiones fijas. Primero se ejecutaron
pruebas funcionales; después se aplicaron los analizadores, se corrigió el código
y se repitieron las comprobaciones. El entorno de integración continua utiliza
Python 3.11 para comprobar también la versión mínima declarada.

## Hallazgos y correcciones

Pylint encontró ocho diagnósticos: cuatro de longitud de línea, dos de
simplificación del flujo, uno de verificación de tipos y uno de importación sin
uso. El resultado inicial fue 9.46/10. Predominaron los problemas de estilo; las
pruebas ya pasaban, demostrando que comportamiento correcto y mantenibilidad son
dimensiones diferentes. Estas ubicaciones corresponden al código anterior:

| Ubicación inicial | Regla | Antes | Después |
| --- | --- | --- | --- |
| `src/budget.py:53` | R1703 | Condicional que retorna constantes booleanas | Retorno directo de la comparación |
| `src/budget.py:53` | R1705 | `else` después de `return` | Eliminación del bloque redundante |
| `src/storage.py:27` | C0123 | Comparación mediante `type(...) != int` | `isinstance`, rechazando explícitamente booleanos |
| `src/transactions.py:48` | C0301 | Diccionario de 103 caracteres en una línea | Diccionario distribuido por Black |
| `src/transactions.py:3` | W0611 | `import os` sin referencias | Importación eliminada |
| `test_budget.py:46` | C0301 | Parametrización de 113 caracteres | Argumentos repartidos en varias líneas |
| `test_budget.py:72` | C0301 | Casos de esquema en 112 caracteres | Lista formateada verticalmente |
| `test_budget.py:79` | C0301 | Casos de presupuesto en 201 caracteres | Estructuras divididas automáticamente |

Además, isort ordenó las importaciones y se eliminó una variable innecesaria.
No se cuentan estos cambios adicionales entre los ocho diagnósticos. La revisión
de tipos conservó una distinción importante: Python considera `bool` una subclase
de `int`, pero una versión booleana no es válida para nuestro esquema.

## Resultados y beneficios

La ejecución final obtuvo 10/10 en Pylint, sin advertencias. Las 27 pruebas
pasaron con 100% de cobertura de líneas y ramas medidas por pytest-cov. Bandit
no encontró problemas en los módulos de producción. Los nueve hooks pasaron al
ejecutarlos sobre todos los archivos; también se comprobó su ejecución durante
un commit real. Los resultados finales se conservan en `reports/`.

Trivy detectó después dos vulnerabilidades en dependencias: CVE-2026-32274
en Black y CVE-2025-71176 en pytest. Se actualizaron a Black 26.3.1 y pytest
9.0.3, versiones corregidas indicadas por el escáner, y se repitió la validación.
Esto muestra el valor de complementar Bandit con análisis de dependencias.

Una revisión manual podría detectar estos defectos, pero repetirla para cada
importación o línea consume atención que conviene dedicar al diseño. La
configuración requirió instalación, ajustes de rutas y comprobación del entorno;
no se midieron por separado esos tiempos, por lo que no se presenta una cifra
de ahorro inventada. El beneficio esperado es evitar discusiones repetitivas y
detectar regresiones antes de compartir cambios.

## Integración y recomendaciones

En el editor ejecutaría Black e isort al guardar y mostraría los diagnósticos de
Pylint. Antes del commit aplicaría los hooks rápidos. En cada PR, CI repetiría
todos los controles y las pruebas, exigiendo al menos 90% de cobertura. Se
mantienen permisos de lectura en el workflow y se limitan sus eventos a esta
entrega para reducir ejecuciones innecesarias.

Black resultó especialmente útil para resolver formatos sin decisiones manuales;
Pylint aportó mejoras de claridad y Bandit una revisión adicional de seguridad.
Usaría esta combinación en proyectos futuros. Como mejora, fijaría también las
dependencias transitivas y evaluaría análisis de tipos. La ausencia de alertas no
demuestra seguridad completa, y la cobertura total tampoco demuestra corrección
para todas las entradas. Persisten responsabilidades de revisión humana, como
evaluar requisitos y decidir si la escritura de archivos necesita atomicidad.
