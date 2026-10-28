# Reflexión sobre TDD

## Impacto en el diseño

Escribir la prueba primero me obligó a pensar cómo se iba a usar cada clase
antes de pensar cómo iba a funcionar por dentro. El mejor ejemplo fue el tiempo.
Para probar las multas necesitaba que un libro tuviera 19 días de retraso, y no
quería esperar ni hacer trucos con `datetime`. Por eso `Library` recibe un `clock`
en el constructor, y en las pruebas uso un `FakeClock` que puedo adelantar con
`clock.advance(19)`. Esa decisión no la tenía pensada al empezar; la prueba me
llevó a ella.

Lo mismo pasó con las reservas. Para comprobar que se avisara al primero de la
cola, el notificador terminó siendo una función que en las pruebas reemplazo con
un `Mock`. Así pude probar el comportamiento sin construir un sistema de correos.
También noté que TDD mantiene las clases pequeñas: la fecha de entrega y los días
de retraso quedaron en `Loan`, porque ahí eran mucho más fáciles de probar solos.

## Retos

El reto más grande fue la disciplina. En la fase GREEN es tentador escribir el
método completo de una vez, pero la regla es escribir solo lo mínimo para que la
prueba pase. Me costó aceptar versiones "incompletas" del código, sabiendo que la
siguiente prueba las iba a obligar a crecer.

Otro reto fue entender qué significa que una prueba falle "por la razón correcta".
Algunas fases RED no fallaron con un `assert`, sino con un `ModuleNotFoundError`
porque la excepción todavía no existía. Y en el ciclo de reservas, de seis
pruebas nuevas cuatro fallaron y dos ya pasaban. Aprendí que lo importante es que
el grupo de pruebas nuevas falle por algo que el código todavía no hace, no que
fallen todas.

También tuve problemas que no eran de TDD sino del entorno: mi `venv` apuntaba a
una ruta vieja, el hook de pre-commit no arrancaba y Git no podía manejar rutas
muy largas de otra carpeta del repositorio. Resolverlo me enseñó que un flujo de
commits pequeños y frecuentes depende de tener las herramientas bien configuradas.

## Beneficios

El beneficio más claro fue la confianza al refactorizar. Cambié la cola de
reservas de una lista a un `deque`, saqué los filtros de búsqueda a un método
`_matches` y reutilicé el historial en el cálculo de multas. En cada cambio corrí
las pruebas y en menos de un segundo supe que nada se había roto.

Además, las pruebas funcionan como documentación. Los nombres de
`test_reservations.py` explican las reglas de las reservas mejor que un párrafo.

## Comparación con escribir las pruebas después

En la tarea de caja blanca escribí las pruebas después del código, buscando
cubrir líneas y ramas. Esas pruebas confirmaban lo que el código ya hacía,
incluyendo sus posibles errores. Con TDD cada prueba empezó fallando, así que sé
que de verdad puede detectar un problema. Y la cobertura salió casi sola: 100% de
sentencias y de ramas sin escribir pruebas extra, porque cada rama existe para
pasar una prueba que ya estaba escrita.

## Uso a futuro

Usaría TDD en lógica con reglas claras, como multas, límites, validaciones o
cambios de estado, donde es fácil escribir un ejemplo de lo que se espera. No lo
usaría tanto al explorar algo nuevo, como un prototipo de interfaz o una librería
que no conozco, porque ahí las pruebas cambiarían todo el tiempo. Una vez que el
diseño se estabiliza, sí cambiaría a TDD.

## Aprendizaje

Me sorprendió lo rápidas que son las pruebas: 123 pruebas en menos de un segundo,
porque ninguna usa el reloj real, internet ni archivos. También me sorprendió ver
el historial de commits al final: se lee como la historia de cómo creció el
sistema, prueba por prueba.

Si lo volviera a hacer, configuraría y probaría el entorno (venv, pre-commit y
Git) antes de empezar, y pensaría desde el inicio en los casos límite, como la
cola vacía, el campo faltante al ordenar o el miembro que no existe.
