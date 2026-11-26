# Reflexión sobre la práctica

El mayor reto de esta práctica fue comprobar que las pruebas detectaran errores importantes, además de ejecutar las líneas del programa. Los estados tenían reglas claras, pero las fechas y los fallos de persistencia podían producir resultados incorrectos sin que bajara mucho la cobertura. El caso de las tareas cargadas con un reloj distinto mostró esa diferencia: fue necesario definir qué hora debía gobernar la operación y escribir una regresión que verificara el comportamiento esperado.

Las pruebas de caja negra parten de entradas, salidas y reglas observables, sin necesitar conocer la estructura interna. La caja blanca utiliza también el código para identificar bifurcaciones, excepciones y rutas que necesitan pruebas. En TaskFlow esto ayudó a distinguir los efectos de un fallo al guardar de los efectos de un fallo al notificar. Ambas técnicas se complementan porque una regla funcional indica qué resultado debe obtenerse y la inspección interna revela caminos para comprobarlo.

La cobertura será útil en proyectos futuros como señal para encontrar zonas poco exploradas y detectar retrocesos al modificar código. Conviene acompañarla de pruebas de comportamiento, revisión de requisitos y una explicación del alcance medido. El resultado del cien por ciento en esta entrega corresponde al modelo y al servicio, con contratos externos aislados; no demuestra que funcionen proveedores reales que todavía no están implementados.

La principal lección es usar las métricas para orientar preguntas. Un porcentaje alto aporta confianza cuando las pruebas también verifican datos, restricciones, interacciones y consecuencias de los errores.
