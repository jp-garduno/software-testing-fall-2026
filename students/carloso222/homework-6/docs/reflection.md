<!-- BORRADOR: cámbialo con tus propias palabras y borra este comentario antes de entregar. -->

# Reflexión sobre TDD

## Impacto en el diseño

Escribir la prueba primero me obligó a pensar cómo se iba a **usar** cada clase
antes de pensar cómo iba a funcionar. El mejor ejemplo fue el tiempo. Para probar
las multas necesitaba que un libro tuviera 19 días de retraso, y no había forma
de hacerlo sin esperar o sin trucos con `datetime`. Por eso `Library` recibe un
`clock` en el constructor. Con eso, las pruebas de multas quedaron cortas y
fáciles de leer.

Con las reservas pasó algo parecido. Quería comprobar que se avisara a la
siguiente persona en la cola, así que el notificador terminó siendo una función
simple que en las pruebas reemplazo con un `Mock`. Ninguna de esas dos ideas la
tenía al empezar; las pruebas me llevaron a ellas.

TDD también mantuvo las clases pequeñas. La lógica de fecha de entrega y días de
retraso quedó en `Loan`, y no en `Library`, porque así era mucho más fácil de
probar por separado.

## Retos

Lo más difícil fue la disciplina en la fase GREEN. Cuando ya sabía cómo iba a
quedar un método, se sentía raro escribir solo lo mínimo para pasar la prueba.
Pero si me adelantaba, terminaba con código que ninguna prueba había pedido.

Otro reto fue decidir el tamaño de cada prueba. "Una aserción por prueba" suena
fácil, pero algunas cosas, como el reporte de historial, son un solo resultado
con varios campos. Decidí comparar el diccionario completo en una prueba, porque
partirlo en seis pruebas no hacía los errores más fáciles de entender.

También fue difícil ver que algunas pruebas pasaban desde el principio en la fase
RED, por ejemplo "no se notifica a nadie si no hay reservas". Aprendí que lo
importante es que el grupo de pruebas nuevas falle por la razón correcta.

## Beneficios

El beneficio más grande fue la confianza al refactorizar. Cuando cambié la cola
de reservas de una lista a un `deque`, o cuando saqué los filtros de búsqueda a
un método `_matches`, las pruebas me dijeron en menos de un segundo que todo
seguía funcionando.

Las pruebas también sirven como documentación. Leer los nombres de las pruebas
de `test_reservations.py` explica las reglas de las reservas mejor que un
párrafo.

## Comparación con escribir las pruebas después

En tareas anteriores escribí primero el código y después las pruebas. Esas
pruebas casi siempre confirmaban lo que el código ya hacía, incluyendo sus
errores. Con TDD, cada prueba empezó fallando, así que sé que de verdad puede
detectar un problema.

La cobertura salió casi sola: llegué a 100% de sentencias y de ramas sin escribir
pruebas extra "para cubrir", porque cada rama del código existe para pasar una
prueba que ya estaba escrita.

## Uso a futuro

Usaría TDD en lógica de negocio con reglas claras: multas, límites,
validaciones o cambios de estado, donde es fácil escribir un ejemplo de lo que
se espera. No lo usaría tanto en trabajo de exploración, como un prototipo de
interfaz o una librería nueva que todavía no conozco, porque ahí las pruebas
cambiarían todo el tiempo. Aun así, cambiaría a TDD en cuanto el diseño se
estabilice.

## Aprendizaje

Lo que más me sorprendió fue lo rápidas que son las pruebas: 123 pruebas en
menos de medio segundo, porque ninguna usa el reloj real, internet ni archivos.
Tampoco esperaba que TDD cambiara tanto mi diseño.

Si lo volviera a hacer, pensaría desde el principio en los casos límite (cola
vacía, campo faltante al ordenar, miembro que no existe) en lugar de
descubrirlos al final.
