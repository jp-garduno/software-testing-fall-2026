# test: automatización E2E de TodoMVC (Homework 8)

## Cambios
- Selenium + Page Object Model (Python): 26 casos
- Playwright + Page Object Model (JavaScript): los mismos 26 casos
- BDD con Behave: 6 escenarios
- Bonus: regresión visual y métricas de rendimiento
- Reporte comparativo, README y capturas

## Resultados (Linux, copia local del build oficial, commit ff43b02)
| Suite | Resultado |
| --- | --- |
| Selenium | 25 passed, 1 xfailed |
| Playwright E2E | 26 passed (incluye 1 fallo esperado) |
| Behave | 6 escenarios y 25 pasos pasan |
| Visual | 5 passed |
| Performance | 1 passed |

## Defecto encontrado
La tecla Escape no cancela la edición y el texto se guarda al perder el foco.