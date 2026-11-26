# Reflection — Homework 4

## ¿Qué fue lo más difícil?

Lo más difícil fue la especificación, no el código. Varias reglas de SecureBank dejan casos abiertos: si una cuenta suspendida puede transferir, qué pasa cuando una transferencia viola dos reglas a la vez, o a qué estado regresa una cuenta congelada cuyo saldo bajó del mínimo mientras estaba congelada. Antes de escribir una sola prueba tuve que decidir y documentar diez supuestos. Entendí que una prueba de caja negra solo es tan buena como la interpretación del requisito que la respalda, y que dejar esos supuestos por escrito es parte del trabajo del tester.

## ¿Qué aprendí sobre las pruebas de caja negra?

Que las técnicas se complementan más de lo que esperaba. EP me dio el mapa de entradas, BVA encontró la mayoría de los errores de comparación, las tablas de decisión me obligaron a resolver combinaciones de reglas y el modelo de estados reveló una transición que el enunciado no contemplaba. También aprendí que la cobertura engaña: tener 100% de líneas cubiertas no garantiza nada si las aserciones son débiles. Lo comprobé introduciendo defectos a propósito; uno de ellos pasó desapercibido para las pruebas de valores límite porque solo revisaban si la operación fallaba, no por qué.

## ¿Qué tanta confianza tengo en la calidad del sistema?

Alta para la lógica que la especificación define: las 152 pruebas pasan en Python y en JavaScript, y la suite detectó los 15 defectos que introduje. Mi confianza es menor en lo que queda fuera del alcance de estas técnicas, como transferencias simultáneas, zonas horarias alrededor de medianoche o la ejecución real de pagos programados. Ahí haría falta otro tipo de pruebas.
