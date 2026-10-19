# White Box Testing & Coverage Analysis Report

## Executive Summary

Implementé TaskFlow en Python (modelo, repositorio, servicio de notificaciones y servicio de negocio) y lo probé
con 135 pruebas de caja blanca. La cobertura final es 100% de sentencias, ramas y funciones.

## Coverage Metrics Achievement

Empecé por el modelo `Task`, porque todo lo demás depende de él. Para cada `if` escribí una prueba por lado
de la decisión: título vacío, de 2, 3, 100 y 101 caracteres; cada transición válida e inválida; vencida o no
según el estado. Después escribí las pruebas de integración del servicio. Con eso la primera medición dio 87%.

Lo más difícil de cubrir fue lo que estaba detrás de un mock. `NotificationService` tenía 32%: en las pruebas
de integración lo reemplacé completo, así que su código nunca corría. La estrategia más efectiva fue mover la
frontera del mock: probar el servicio real y simular solo los clientes de correo y SMS. Lo segundo fue inyectar
fallas con `side_effect` para entrar en los `except` del repositorio.

## Challenges in Reaching Coverage Goals

El primer obstáculo fue el tiempo. Una tarea “vencida” necesita una fecha pasada, pero el modelo no permite
crearla. Lo resolví haciendo que `is_overdue()` y `check_overdue_tasks()` acepten un `now` opcional, y en una
prueba sustituí `datetime` por una subclase con reloj congelado.

El segundo fue que el último 13% costó 51 pruebas adicionales. Varias de esas pruebas valen
la pena (reintentos, errores de base de datos), pero otras, como verificar el texto exacto de cada mensaje,
aportan poco. Sí hubo rendimientos decrecientes.

## Benefits of Mocking External Dependencies

Sin mocks necesitaría una base de datos y un servidor SMTP para correr las pruebas; con mocks la suite completa
tarda 0.3 segundos y no tiene efectos secundarios. Además puedo provocar fallas difíciles de reproducir en la
vida real: un SMTP que falla dos veces y luego responde, o un disco lleno al guardar. También pude verificar el
orden de las interacciones: que primero se guarde y después se notifique, y que si guardar falla no se envíe
ningún correo.

El costo es que un mock solo es tan correcto como mi suposición sobre la dependencia real. Por eso usé
`Mock(spec=...)` y combiné tres tipos de doble: *stubs* para devolver datos, *mocks* para verificar llamadas y un
*fake* (`FakeDatabase`) para correr la lógica real del repositorio en los flujos completos.

## Trade-offs Between Coverage and Test Quality

No creo que 100% sea un objetivo en sí. Llegué ahí porque el sistema es pequeño, pero el 100% de ramas no
garantiza las 32 combinaciones de filtros de `search()` ni que el mock se comporte como el cliente real. Algunas
pruebas las escribí principalmente por la cobertura, como la de `__repr__`; las dejé porque son baratas, pero no
las considero valiosas. Mi criterio: cada prueba debe fallar si se rompe una regla de negocio; si solo existe
para pintar una línea de verde, es candidata a eliminarse. Para un proyecto real, 85-90% con buenas aserciones
me parece más sano.

## Lessons Learned

Me sorprendió que la cobertura detectó un error de diseño en mis pruebas, no en el código: estaba simulando
justo la clase que quería probar. También aprendí que la cobertura de ramas de Python no mide condiciones
dentro de una lambda, así que hay que revisar algunas cosas a mano.

La próxima vez correría la cobertura desde la primera prueba y diseñaría el código con el tiempo y las
dependencias inyectables desde el inicio. En el proyecto final pienso usar la cobertura como guía para encontrar
huecos, no como calificación.

## Conclusion

La cobertura muestra lo que no estoy probando; qué simular y qué riesgo aceptar sigue siendo mi decisión.
