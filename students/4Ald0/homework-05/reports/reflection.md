# Reflexión

El aspecto más desafiante fue comprobar reglas temporales sin depender del
reloj del sistema. Una tarea puede ser válida al crearse y estar vencida
después, por lo que editar su descripción no debería obligar a reemplazar la
fecha anterior. El reloj controlable permitió reproducir esa situación sin
esperas. Además, una copia profunda del almacén falso duplicó el propio reloj
y produjo un fallo que la cobertura por sí sola no identificó como problema.
La prueba del comportamiento reveló la discrepancia y permitió corregir el
doble de prueba.

White box testing aprovecha la estructura interna del programa para seleccionar
casos: condiciones, excepciones, ramas y transiciones. Black box testing parte
del contrato y de las entradas y salidas esperadas, sin necesitar conocer la
implementación. Ambas perspectivas se complementan. En TaskFlow, las reglas de
unicidad y archivo proporcionaron expectativas externas, mientras que el
análisis de las decisiones del servicio señaló escenarios adicionales de
fallo y combinaciones que convenía verificar.

La cobertura sería útil en proyectos futuros como indicador para encontrar
zonas sin explorar y orientar revisiones. Sin embargo, alcanzar 100% no
demuestra que las aserciones sean suficientes ni que una base de datos real
respete los contratos simulados. En este trabajo las 112 pruebas pasaron y
se cubrieron todas las ramas instrumentadas, pero siguen siendo necesarias
pruebas de sistema para evaluar infraestructura, concurrencia y entrega real
de mensajes. La práctica más valiosa consiste en combinar métricas reproducibles
con verificaciones de efectos, aislamiento y manejo de errores, manteniendo
las pruebas lo bastante rápidas para ejecutarlas durante el desarrollo.
