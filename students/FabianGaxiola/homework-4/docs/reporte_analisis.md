# Análisis comparativo de técnicas de diseño de pruebas

## Introducción

Para validar el sistema de inscripción a cursos se aplicaron cuatro técnicas de diseño de pruebas: particiones de equivalencia, análisis de valores límite, tablas de decisión y pruebas de transiciones de estado. Cada técnica permitió detectar diferentes tipos de defectos y cubrir distintas características de las reglas de negocio. El sistema evaluado determina si una solicitud debe ser aceptada, rechazada, enviada a lista de espera o marcada como pago pendiente, considerando la edad del aspirante, su promedio, la disponibilidad de cupo y el estado del pago.

## Particiones de equivalencia

Las particiones de equivalencia fueron útiles para dividir las entradas en grupos que deberían producir un comportamiento similar. Por ejemplo, las edades entre 18 y 60 años forman una partición válida, mientras que las edades menores de 18 y mayores de 60 pertenecen a particiones inválidas. De forma similar, los promedios entre 70 y 100 representan datos válidos, y los valores fuera de ese rango representan datos inválidos.

La principal ventaja de esta técnica fue reducir la cantidad de pruebas necesarias. En lugar de probar cada edad posible, se seleccionaron representantes de cada grupo, como 25 para una edad válida, 17 para una edad inválida inferior y 61 para una edad inválida superior. Esta técnica fue efectiva para comprobar que el sistema clasifica correctamente datos válidos e inválidos. Sin embargo, por sí sola no garantiza que los límites exactos estén implementados correctamente. Por ejemplo, una prueba con edad 25 no permite verificar si el sistema acepta correctamente la edad mínima de 18 años.

## Valores límite

El análisis de valores límite se enfocó en los puntos donde normalmente aparecen errores de programación: los extremos de los rangos y los valores inmediatamente adyacentes. En este proyecto se probaron las edades 17, 18, 60 y 61, así como los promedios 69, 70, 100 y 101. También se evaluaron los cupos -1, 0 y 1.

Esta técnica resultó especialmente efectiva para identificar errores relacionados con operadores de comparación. Un error común sería utilizar `>` en lugar de `>=`, lo cual provocaría que una persona de 18 años fuera rechazada incorrectamente. También podría usarse `<` en lugar de `<=`, ocasionando que una persona de 60 años fuera excluida. Las pruebas de límite detectan estos defectos con mayor precisión que las particiones de equivalencia. Como limitación, se concentran en valores numéricos y no cubren suficientemente combinaciones complejas entre varias condiciones.

## Tablas de decisión

Las tablas de decisión permitieron analizar combinaciones de condiciones y resultados. En el sistema existen tres decisiones principales: que los datos personales sean válidos, que haya cupo disponible y que el pago haya sido realizado. Al combinar estas condiciones se obtienen diferentes acciones, como aceptar la inscripción, colocarla en lista de espera, marcar pago pendiente o rechazarla.

Esta técnica fue la más adecuada para validar la prioridad de las reglas. Por ejemplo, cuando los datos son inválidos, el sistema debe rechazar la solicitud incluso si existe cupo y el pago fue realizado. Asimismo, cuando no hay cupo y tampoco se ha realizado el pago, se definió que la solicitud debe enviarse a lista de espera. Sin una tabla de decisión, estas prioridades podrían quedar ambiguas y producir resultados inconsistentes. Su principal desventaja es que la cantidad de combinaciones puede aumentar rápidamente cuando existen muchas condiciones.

## Transiciones de estado

Las pruebas de transiciones de estado fueron esenciales porque una inscripción no solo depende de datos de entrada, sino también de su estado previo. Una solicitud puede iniciar como PENDIENTE y después cambiar a ACEPTADA, RECHAZADA, LISTA_ESPERA o PAGO_PENDIENTE. Posteriormente, una solicitud en PAGO_PENDIENTE puede convertirse en ACEPTADA al confirmar el pago, mientras que una solicitud en LISTA_ESPERA puede cambiar a ACEPTADA cuando se libera un cupo.

Esta técnica permitió validar secuencias de acciones y prevenir transiciones inválidas. Por ejemplo, no debe ser posible procesar una solicitud que ya fue aceptada, confirmar un pago que no está pendiente o cancelar una inscripción que ya fue cancelada. Las transiciones de estado fueron más efectivas que las otras técnicas para encontrar errores de flujo y reglas relacionadas con el ciclo de vida de la solicitud.

## Conclusión

Las cuatro técnicas se complementan. Las particiones de equivalencia reducen pruebas redundantes; los valores límite detectan errores en extremos; las tablas de decisión validan combinaciones y prioridades de reglas; y las transiciones de estado verifican el comportamiento secuencial del sistema. En este proyecto, las tablas de decisión y las transiciones de estado aportaron mayor cobertura funcional, mientras que los valores límite fueron los más importantes para detectar errores de comparación. La combinación de las cuatro técnicas produjo una estrategia de pruebas más completa que utilizar una sola técnica.
