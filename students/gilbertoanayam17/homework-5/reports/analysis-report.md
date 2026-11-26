# White Box Testing & Coverage Analysis Report

## Executive Summary

Este reporte reflexiona sobre la cobertura alcanzada en TaskFlow con pruebas de caja blanca. La suite final tiene 115 casos y alcanza 99.61% de sentencias, 100% de ramas y 97.78% de funciones. El hallazgo principal es que la cobertura muestra qué código se ejecutó, pero no si las pruebas detectan errores.

## Coverage Metrics Achievement

No se llegó ahi escribiendo pruebas al azar, sino midiendo después de cada archivo. Primero escribí las pruebas unitarias del modelo, que dejaron `task.py` en 98.9%, aunque el global seguía en 59%. Después conecté el servicio al repositorio real sobre una base de datos falsa en memoria: un solo flujo de crear, actualizar y completar atraviesa las tres capas, y la cobertura pasó a 88%. Esa fue la estrategia más efectiva. Al final leí `term-missing` y escribí una prueba para cada rama pendiente.

Lo más difícil de cubrir fueron las ramas que traducen errores, porque un `DatabaseError` o un HTTP 503 no ocurren solos; hubo que provocarlos con `side_effect`.

## Challenges Encountered

El obstáculo principal fue el tiempo: con el reloj real, el caso exacto de la fecha límite no se puede repetir. Lo resolví haciendo que el modelo lea la hora desde `current_time()` y reemplazándola en las pruebas con un reloj falso que puedo adelantar.

Los rendimientos decrecientes sí se notaron. Del 88% al 97.85% hicieron falta 22 pruebas; del 97.85% al 99.69%, otras 23. La última línea, el reloj real, no la cubrí: probarla volvería a depender de la hora del sistema.

## Benefits of Mocking

Simular las dependencias externas aportó tres cosas:

1. **Velocidad**: la suite completa corre en 0.20 segundos sin correo ni base de datos reales.
2. **Aislamiento**: cuando una prueba falla, el problema está en el componente probado, no en la red.
3. **Flexibilidad**: se pueden provocar fallas difíciles de reproducir, como una conexión rechazada o una cuota de SMS agotada.

Sin embargo, también agregaron complejidad: un `Mock()` sin `spec` acepta llamadas a métodos inexistentes y la prueba pasa por la razón equivocada. Por eso todos usan `spec=`. Escribir las pruebas fue más fácil, pero obligó a elegir el doble correcto: un mock verifica una llamada, y un fake, el estado final.

## Coverage vs Quality Trade-offs

El hallazgo más útil vino de la mutación. `notification_service.py` estaba al 100% de sentencias y ramas, y aun así cambiar `>= 400` por `> 400` no rompía ninguna prueba, porque solo se probaba con 503. Además, coverage.py cuenta `if a or b` como una sola decisión, así que 100% de ramas no prueba cada condición.

Admito que alguna prueba, como la de la diagonal al final de la URL, existe más por la cobertura que por el riesgo. No creo que valga la pena perseguir el 100%. El balance que encontré fue usar la cobertura para encontrar código que nunca se ejecutó y usar valores límite y mutación para revisar que las aserciones sí detectan errores.

## Lessons Learned

Me sorprendió que la cobertura dependa tanto del diseño. Inyectar el reloj, la base de datos y el cliente HTTP hizo alcanzable cada rama. Si `Task` llamara a `datetime.now()` directamente, las pruebas de vencimiento serían frágiles. La próxima vez diseñaría esos puntos de inyección desde el inicio. En proyectos futuros usaré la cobertura como piso en CI, alrededor de 80%, y leeré `term-missing` en lugar de perseguir el número.

## Conclusion

La cobertura es una herramienta, no una meta: indica dónde falta probar, pero la calidad la confirman los valores límite y la mutación.
