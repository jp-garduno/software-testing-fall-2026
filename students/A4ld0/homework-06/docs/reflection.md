# Reflexión sobre Test-Driven Development

Esta reflexión técnica se basa en el desarrollo y las ejecuciones registradas en
esta entrega, realizada con asistencia de Codex. Describe decisiones observables
del proyecto y no atribuye experiencias personales al estudiante. El ejercicio
permitió analizar cómo una biblioteca pequeña cambia cuando cada comportamiento
empieza por una prueba. El objetivo inicial parecía consistir en almacenar libros
y miembros, pero los casos de error mostraron que la responsabilidad principal
era conservar relaciones coherentes entre ejemplares, préstamos y personas.

TDD influyó especialmente en el orden de las operaciones. Una prueba del límite
de préstamos comprobó que rechazar una solicitud también debía conservar las
copias disponibles. La primera implementación descontaba el ejemplar antes de
consultar el límite del miembro. Aunque se producía una excepción, el estado
quedaba alterado. El caso fallido llevó a validar la capacidad antes de modificar
la biblioteca. Esta secuencia convirtió una regla de negocio en una decisión de
diseño concreta y verificable, en lugar de dejarla como una intención documental.

El manejo de fechas presentó otro desafío. No bastaba con multiplicar días por
una tarifa: era necesario distinguir vencimiento, fecha de consulta y devolución.
Las pruebas especificaron que el día de vencimiento no genera multa, que una
devolución detiene su crecimiento y que un reporte histórico no incluye días
posteriores a su fecha. Introducir fechas explícitas hizo reproducibles estos
casos. Después, extraer el cálculo de cada préstamo y reunir la validación de
fechas redujo duplicación sin cambiar los resultados. La refactorización tuvo
así una justificación apoyada por pruebas existentes.

La dificultad del enfoque estuvo en mantener pasos suficientemente pequeños.
Es tentador escribir varias funciones relacionadas cuando ya se conoce la
solución aproximada. Sin embargo, hacerlo reduce la oportunidad de comprobar
que cada prueba detecta realmente el comportamiento ausente. El historial de
esta entrega conserva fallos y soluciones separados, mientras que el registro
de ejecuciones permite contrastarlos. También distingue los casos adicionales
de integración, escritos después, de los ciclos originales. Esta separación
evita presentar toda prueba aprobada como evidencia automática de desarrollo
guiado por pruebas.

Entre los beneficios se observa una API centrada en operaciones reconocibles:
prestar, devolver, buscar y consultar historial. Las pruebas de miembros, libros
y biblioteca mantienen responsabilidades distintas, y las pruebas de integración
comprueban su colaboración. Las instantáneas del historial protegen los registros
internos frente a cambios en un reporte. Las pruebas parametrizadas expresan
familias de entradas inválidas o fechas límite sin repetir escenarios completos.
La cobertura ayuda a localizar caminos pendientes, aunque su porcentaje por sí
solo no demuestra que las expectativas representen correctamente el dominio.

En comparación con escribir pruebas al terminar, TDD obliga a concretar antes
qué resultado define el éxito y qué debe permanecer intacto cuando hay errores.
Las pruebas posteriores siguen siendo útiles para ampliar escenarios y detectar
regresiones; esta entrega también las incluye. La diferencia está en el momento
en que orientan el diseño. Un método ya implementado puede condicionar demasiado
las expectativas de quien lo prueba. Empezar por ejemplos de comportamiento
reduce ese riesgo, pero no reemplaza aclarar requisitos ambiguos con la persona
que solicita el sistema.
