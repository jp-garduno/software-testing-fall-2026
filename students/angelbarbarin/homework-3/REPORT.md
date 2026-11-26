# Reporte de análisis estático — Homework 3

**Alumno:** Angel Isaac Barbarín (`angelbarbarin`)
**Proyecto:** cotizador de cámaras de reversa (Python 3.13)
**Herramientas:** pre-commit, pylint 3.x, black, isort, bandit

## Resumen de resultados

| Métrica | Antes | Después |
|---|---|---|
| Calificación de pylint | **6.70/10** | **10.00/10** (+3.30) |
| Problemas en `src/` | 32 | 0 |
| Pruebas | 13 pasando | 14 pasando |
| Defectos funcionales detectados por las pruebas | 0 | 1 |

Evidencia: `pylint-report.txt` (antes) y `pylint-report-after.txt` (después).
El detalle de cada corrección está en [`FIXES.md`](FIXES.md).

## Cuántos problemas y de qué tipo

pylint reportó **33 problemas**: 32 en el código fuente y uno en la propia
configuración. Repartidos por categoría:

| Categoría | Total | Códigos encontrados |
|---|---|---|
| Convención (C) | 23 | `C0116` ×12, `C0114` ×3, `C0121` ×4, `C0115` ×2, `C0103`, `C0209` |
| Advertencia (W) | 8 | `W0102` ×2, `W0611` ×2, `W0702`, `W0612`, `W0613`, `W1514` |
| Refactorización (R) | 1 | `R1732` |
| Error (E) | 1 | `E0015` (en `.pylintrc`) |

El 70% son convenciones —documentación faltante, comparaciones con `None`,
nombres fuera de estilo— que no rompen nada hoy. Pero entre las 8 advertencias
había un bug que ya estaba cobrando de más.

## El hallazgo importante: el bug que las pruebas no vieron

`src/cotizador.py:14: W0102: Dangerous default value [] as argument`

El método `agregar_item` recibía `carrito=[]` por defecto. En Python ese valor
se evalúa **una sola vez**, al definir la función, así que todas las cotizaciones
que no pasan un carrito explícito comparten la misma lista:

```
Cliente A pide 1 cámara   -> 1 item
Cliente B pide 1 pantalla -> 2 items
Carrito del cliente B: ['CAM-001', 'PAN-007']
Total cotizado a B: 4756.00
```

El cliente B recibe la cámara del cliente A: en el negocio real, cobrarle de más
y descuadrar el inventario.

Lo grave no es el bug, sino quién lo encontró: **las 13 pruebas pasaban**. Todas
construían el carrito explícitamente, así que ninguna ejercía la ruta del valor
por defecto. Las pruebas dinámicas comprueban los caminos que alguien pensó en
escribir; el análisis estático revisa el código completo, incluidos los que nadie
ejerció. Esa es la diferencia entre pruebas estáticas y dinámicas, vista en un
caso concreto.

Al corregirlo agregué la prueba de regresión que habría fallado antes
(`test_carrito_no_se_comparte_entre_cotizaciones`): de ahí sale la prueba 14.

## Beneficios observados

El más evidente ya está contado: un defecto funcional encontrado por una
herramienta que **no ejecuta el código**, con toda la suite en verde.

El segundo es menos vistoso y más valioso a largo plazo: 12 de los 33 problemas
eran docstrings faltantes. Escribirlos me obligó a decir en una frase qué
garantiza cada función, y en dos casos descubrí que no lo tenía claro. El linter
no mejoró el código solo; me obligó a pensarlo.

El tercero es de proceso: los hooks corren en segundos y antes de que el commit
exista. Un problema de formato deja de consumir atención humana en una revisión
de código y pasa a ser algo que la máquina arregla sola.

## Cómo lo integraría en el flujo de un equipo

1. **Hooks locales obligatorios**, instalados en el `setup` del proyecto y no
   documentados en un README que nadie lee. Es la barrera más barata.
2. **La misma configuración en CI**, con `--fail-under` que rompa el build. Los
   hooks locales se saltan con `--no-verify`; el pipeline no.
3. **Adopción gradual en código existente.** Correr esto de golpe sobre una base
   con años encima arroja miles de avisos y el equipo lo desactiva en una semana;
   conviene aplicarlo solo a los archivos tocados en cada PR.
4. **Formato fuera de la revisión de código.** Si `black` lo aceptó, está bien.

## Recomendaciones de configuración

- **Fijar `rev` en todos los hooks.** Un hook sin versión fija puede cambiar de
  comportamiento entre dos corridas del mismo commit.
- **Desactivar lo mínimo, y con la razón escrita.** Aquí solo se desactivaron
  `format` (la autoridad es `black`; dos herramientas opinando lo mismo se
  contradicen) y `too-few-public-methods`. Cada exclusión lleva su comentario.
- **Activar `useless-suppression`.** Avisa cuando un `# pylint: disable` ya no
  hace falta, y evita que las exclusiones se acumulen como sedimento.
- **Escribir el `.pylintrc` a mano.** `--generate-rcfile` produce unas 600
  líneas casi todas con el valor por defecto y nadie las revisa; 40 líneas
  justificadas sí se revisan.
- **Un formateador y un linter, no dos linters.** `black` decide el formato y
  `pylint` la lógica. Solapar responsabilidades genera peleas entre herramientas
  que se acaban resolviendo desactivando reglas.
