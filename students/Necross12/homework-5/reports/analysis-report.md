# White Box Testing & Coverage Analysis Report

## Executive Summary

Este informe resume mi experiencia al lograr una alta cobertura con pruebas de caja blanca, unitarias y de integración, sobre el sistema TaskFlow. La conclusión principal es que las pruebas con mocks exigen pensar cada caso con mucho detalle: deben ser concretas y exhaustivas para cubrir la mayor parte del código sin repetir la misma prueba.

## Coverage Metrics Achievement

Empecé por las pruebas unitarias de `Task` y después seguí con `TaskService`, planteando primero lo que haría un usuario (el camino normal) y avanzando hacia errores, valores límite y estados inválidos. Lo más útil fue el reporte HTML, que muestra cuántas veces se ejecutó cada línea y qué ramas faltan.

Llegué a 100% en sentencias, funciones y líneas, y a 97.36% en ramas (37 de 38). La rama pendiente era el `|| []` de `canTransition` (línea 60 de `task.js`), que solo se ejecuta con un estado inexistente. La cubrí con una prueba que asigna un estado inválido y todas las métricas quedaron en 100%.

## Challenges Encountered

Lo más difícil fueron las pruebas de integración con mocks: ordenarlos para reutilizarlos y mapear bien las funciones me trajo más errores de los que quería, y tuve que revisar varias veces los apuntes de clase. También hubo rendimientos decrecientes: pasar de 97.36% a 100% requirió una prueba completa para un caso que el sistema nunca produce por sí solo. Las cuatro suites corren en 0.771 s, por debajo del segundo que pedía la tarea.

## Benefits of Mocking

Los mocks permiten probar sin depender de elementos que todavía no existen (base de datos, correo), simular fallos difíciles de reproducir y verificar interacciones: argumentos exactos y orden de las llamadas (guardar antes de notificar).

Sin embargo, me costó más escribir las pruebas del punto 4 (fake, spy, stubs y reloj simulado) que las del punto 2, donde bastaba con `jest.fn()`. Tampoco noté ventaja de velocidad, porque aquí todo ocurre en memoria. Aun así, entiendo por qué en un caso real son indispensables.

## Coverage vs Quality Trade-offs

No creo que valga la pena cubrir el 100% de todo: hay código defensivo y casos muy improbables, y es más valioso revisar primero lo crítico. Solo escribí una prueba únicamente para subir el número: la del estado desconocido (línea 60). Su valor es bajo, pero es barata y documenta el comportamiento defensivo. Entre 80% bien pensado y 100% no veo gran diferencia, mientras se cubran los casos críticos.

## Lessons Learned

Me sorprendió tener 100% en sentencias y aun así una rama sin cubrir: la cobertura por sentencias no basta. En el proyecto final empezaría por los módulos individuales, que son los más fáciles de probar, y antes de la integración armaría los mocks y los comprobaría con una o dos pruebas, cuidando más los detalles. Esta estrategia importa sobre todo en proyectos grandes, donde hay que asegurar que nada se rompa.

## Conclusion

Las pruebas de caja blanca y la cobertura aportan información valiosa, pero deben complementarse con otras medidas de calidad: solo prueban lo que creemos correcto y no garantizan que se cumplan los requerimientos. Tener 100% de cobertura no significa que el código funcione al 100%, así que las pruebas deben diseñarse pensando en los resultados que buscamos y no en los que el código ya produce.
