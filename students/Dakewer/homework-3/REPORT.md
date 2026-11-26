# Reporte de Análisis: Static Testing en Movie Picker

**Estudiante**: David Eduardo Páez Aguilar
**Proyecto**: Movie Picker (Alexa Skill, Python)

## 1. Issues encontrados

A lo largo de la configuración corrí `pre-commit run --all-files` 
varias veces sobre los ~20 archivos Python del 
proyecto (carpetas `handlers/` y `helpers/`, más 
`lambda_function.py`). Los issues se agrupan en tres 
categorías claras:

**Formato y estilo (la mayoría).** `end-of-file-fixer` 
corrigió 24 archivos a los que les faltaba un salto de línea 
final, y `black` reformateó 16 archivos por inconsistencias 
de espaciado, comillas y longitud de línea. `isort` reordenó 
los imports en al menos 5 archivos que no seguían un orden 
consistente entre librerías estándar, de terceros y locales. 
Ninguno de estos era un error funcional, pero sin la 
herramienta habrían quedado invisibles en una revisión 
manual normal — nadie revisa a mano si cada archivo 
termina con un newline.

**Imports sin usar (calidad de código).** `pylint` detectó 8 
imports importados pero nunca utilizados, repartidos en 6 
archivos distintos (por ejemplo `HandlerInput` y `Response` 
en `BaseIntentHandler.py`, o `import os` en `api.py`). 
Son residuos típicos de refactors donde se quita el uso de 
algo pero se olvida borrar el import.

**Un error real.** Al limpiar uno de esos imports sin usar 
(`OPCIONES_MENU` en `EliminarGenerosIntentHandler.py`), 
pylint detectó `E0602: Undefined variable 'ALGO_MAS'` — 
otra variable que se importaba en la misma línea y que sí se 
usaba en el código, pero que se había borrado por 
accidente junto con la que sí sobraba. Este fue el único 
issue de categoría "error" (no solo estilo) que encontramos, 
y habría causado un `NameError` en producción.

En total: **1 error funcional, 8 warnings de imports sin 
usar, y decenas de correcciones automáticas de 
estilo/formato**.

## 2. Beneficios observados

El caso más claro de valor fue el de `ALGO_MAS`: es 
exactamente el tipo de error que una revisión manual rápida 
pasaría por alto, porque el código "se ve bien" a simple vista 
— el error solo aparece al ejecutar esa rama específica del 
handler. Pylint lo atrapó en segundos, sin necesidad de 
invocar la skill.

También, al escribir tests unitarios para `utils.py`, 
descubrí que `get_random_phrase([])` lanza `IndexError` 
sin manejarlo — no es algo que un linter detecte, pero 
escribir el test forzó a pensar en el caso límite. Esto sugiere 
que static testing (linters) y tests unitarios se complementan: 
uno atrapa problemas de código muerto o sintaxis, el otro 
atrapa problemas de lógica y casos borde.

Un hallazgo adicional, no capturado por ninguna 
herramienta configurada aquí, fue un token de API 
hardcodeado directamente en `api.py`. Esto lo detecté por 
inspección manual, no por pylint — es justo el tipo de 
problema que una herramienta de seguridad como `bandit` 
sí habría marcado automáticamente.

En cuanto a tiempo: la configuración inicial (instalar pre-commit, 
escribir el `.pre-commit-config.yaml`, resolver 
problemas de PATH y codificación en Windows) tomó 
aproximadamente 1-2 horas, la mayoría en depuración 
de entorno más que en configuración en sí. Corregir los issues 
encontrados tomó menos de 30 minutos. El tiempo ahorrado 
a futuro es difícil de cuantificar, pero cada commit futuro se 
beneficia de la revisión automática sin costo adicional.

## 3. Integración en un flujo de equipo

Recomendaría tres capas, cada una con su momento:

- **IDE**: linting en tiempo real (PyCharm ya integra pylint) para feedback inmediato mientras se escribe código.
- **Pre-commit hook local**: como el configurado aquí, para atrapar problemas antes de que lleguen al repositorio compartido — evita que "se me olvidó" llegue a `main`.
- **CI/CD**: correr `pre-commit run --all-files` y `pytest` en cada Pull Request, como control final que no depende de que cada desarrollador tenga el hook instalado localmente.

## 4. Recomendaciones

De las herramientas usadas, `pylint` fue la más valiosa 
por encontrar el error real de `ALGO_MAS`; `black` e `isort` 
fueron las que más tiempo ahorraron al no tener que discutir 
estilo en revisiones de código. Cambiaría la configuración 
para agregar `bandit` (dado el hallazgo del token 
hardcodeado) y activar `isort --profile=black` desde el 
inicio para evitar conflictos entre ambas herramientas. 
Definitivamente usaría este flujo en proyectos futuros: el 
costo de configuración es bajo comparado con la reducción 
de errores triviales que de otra forma consumen tiempo de 
revisión humana.