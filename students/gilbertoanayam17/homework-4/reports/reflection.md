# Reflection

## What was most challenging?

Lo más difícil no fue escribir las pruebas sino decidir qué debía pasar cuando la
especificación no lo decía. Me pasó con la tabla de transferencias: si no hay
fondos y además se pasa del límite, ¿qué error devuelvo? Una prueba solo puede
verificar uno, así que inventé un orden de prioridad y lo anoté como supuesto.

Lo otro que me costó fue mantener las dos implementaciones con los mismos casos.
Usé los mismos IDs en ambas suites para compararlas, pero aun así las revisé a
mano varias veces.

## What did you learn about black box testing?

Aprendí que estas técnicas no solo sirven para encontrar errores, también para ver
si los requisitos están completos. Equivalence Partitioning y las tablas de
decisión no encontraron bugs, pero sí me hicieron notar varios huecos en la
especificación.

Boundary Value Analysis fue la excepción: encontró un error de verdad. Transferir
$4,999.99 y luego $0.01 suma justo el límite de $5,000, pero en punto flotante da
un poquito más y el sistema lo rechazaba. Nunca lo habría visto con valores de en
medio.

## How confident are you in the quality of the banking system?

Confío a medias. Las 56 pruebas pasan y la cobertura anda entre 85 % y 88 %, pero
justamente ese 12 % que falta me dice que hay funciones que no revisé, sobre todo
el pago de servicios. Tampoco hay nada que pruebe qué pasa con dos transferencias
al mismo tiempo. Diría que confío en lo que probé, no en todo el sistema.
