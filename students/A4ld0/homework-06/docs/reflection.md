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

