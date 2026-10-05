# Black Box Testing Analysis Report

**Date**: 2026-09-23

## Executive Summary

Diseñé y ejecuté 56 pruebas (28 en Jest y 28 en pytest) sobre SecureBank usando
las cuatro técnicas del módulo, con una cobertura de línea de entre 85 % y 88 %.
Solo una de las técnicas encontró un error real, y no fue la que yo esperaba.

## Technique Effectiveness

**Equivalence Partitioning** fue la más fácil y con la que empecé. No encontró
ningún bug, pero me sirvió para notar cosas que la especificación no dice: al
listar las particiones del saldo inicial me pregunté qué pasa si abres una cuenta
Savings con $50, por debajo del mínimo de $100. Nadie lo define, así que tuve que
decidirlo. Creo que ese es su valor: te obliga a leer los requisitos con lupa.

**Boundary Value Analysis** fue la única que encontró un error. La prueba BV4-1
transfiere $4,999.99 y luego $0.01, que suman exactamente el límite diario de
$5,000, así que las dos deberían pasar. La segunda se rechazaba. El problema era
que en punto flotante esa suma da `5000.000000000001`, que es mayor que 5000. Lo
arreglé redondeando antes de comparar. Me llamó la atención que con cualquier
valor "normal" como $500 nunca lo habría visto.

**Decision Tables** fue la más tardada de armar. Lo complicado no fue llenar la
tabla sino decidir qué pasa cuando fallan dos condiciones a la vez: si no hay
fondos y además se pasa del límite, ¿qué error devuelvo? Una prueba solo puede
verificar uno, así que definí un orden de prioridad y lo documenté.

**State Transition Testing** fue la que más me gustó, porque es la única que prueba
el sistema en secuencia y no llamada por llamada. ST2 abre una cuenta suspendida y
luego deposita para ver si vuelve a Active; eso no lo detecta ninguna prueba de una
sola operación.

## Coverage Comparison

No medí la cobertura de cada técnica por separado, pero revisando qué líneas
quedaron sin marcar sí se ve la diferencia. Las pruebas de estado son las únicas
que entran a `freeze`, `unfreeze` y `close`, y las de BVA las únicas que llegan al
límite diario acumulado. En cambio EP y las tablas de decisión se solapan bastante,
porque las dos entran por `transfer`.

Lo que ninguna cubrió fue el pago de servicios completo: solo probé el pago
agendado y el beneficiario inválido, y quedaron fuera el pago inmediato y los
fondos insuficientes. También quedó fuera la concurrencia, que no sabría cómo
probar con estas técnicas.

## Real-World Application

En un proyecto real priorizaría BVA, porque encontró el único error con poco
esfuerzo. La combinaría con EP: una para reducir los valores a probar y la otra
para atacar los bordes de cada partición. Las tablas de decisión las usaría solo
cuando hay varias condiciones que se combinan, porque crecen muy rápido.

## Recommendations

Si lo volviera a hacer, armaría las tablas de decisión antes que las particiones,
porque fueron las que me hicieron notar las ambigüedades de los requisitos y
después tuve que regresar a corregir lo demás. También implementaría más filas de
las tablas que diseñé, para subir la cobertura de `payBill`, que es la función que
quedó con más ramas sin probar. Y agregaría pruebas de los montos menores a $0.01,
que el sistema rechaza pero yo no verifiqué.
