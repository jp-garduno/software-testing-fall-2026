# Análisis de pruebas de caja blanca en TaskFlow

## Resultados de cobertura

La suite final contiene 124 casos aprobados, organizados en pruebas unitarias, integración, mocking y límites. La medición sobre src registra 196 de 196 sentencias y 66 de 66 salidas de ramas ejecutadas. Las veinte funciones con cuerpo ejecutable también fueron invocadas, según los datos por función del JSON de coverage.py. La ejecución sin instrumentación de cobertura tomó 0.45 segundos en la captura del autor. Estos resultados superan los mínimos de la tarea, pero describen exclusivamente el código medido y no certifican la ausencia de defectos.

## Dificultades para alcanzar los objetivos

El trabajo empezó por las validaciones y las transiciones del modelo. Parametrizar las dieciséis combinaciones de estados permitió comprobar tanto las rutas permitidas como los estados terminales. Las fechas exigieron especial cuidado: crear una tarea con vencimiento futuro y avanzar después el reloj evita saltarse la validación para simular un vencimiento.

El problema más ilustrativo apareció al cargar tareas con un reloj distinto al del servicio. Una comprobación podía evaluar cada tarea con una referencia temporal diferente. Dos pruebas detectaron el fallo: una exigía usar el reloj del servicio y otra una sola consulta temporal para todo el lote. La corrección consistió en capturar una hora y compartirla durante la revisión. Los porcentajes altos obtenidos antes no habían revelado este problema.

## Beneficios y límites de los dobles

Los mocks con autospec mantienen los nombres y las firmas del repositorio y las notificaciones. Los stubs permiten preparar respuestas específicas, mientras que el fake en memoria conserva estado durante flujos de creación, actualización, terminación y archivo. El modelo y el servicio permanecen reales en esas pruebas.

Simular errores de persistencia permitió comprobar que no se emite un aviso de éxito si guardar falla. Los errores de correo y SMS, en cambio, no deben deshacer una operación persistida. Se verifican los argumentos, el orden de llamadas, el registro del fallo y el estado resultante. Sin estos dobles harían falta servicios externos y escenarios difíciles de reproducir; con ellos todavía queda pendiente validar los adaptadores reales cuando existan.

## Cobertura frente a calidad

Al ampliar el servicio quedaron dos líneas sin ejecutar en el manejo de errores de SMS. Añadir un escenario de fallo fue útil porque verificó una regla concreta de resiliencia, además de cubrir esas líneas. Escribir pruebas que simplemente llamaran métodos para elevar el porcentaje habría aportado menos confianza.

Las actualizaciones usan copias para que una validación inválida o un guardado fallido no alteren el objeto original. Esta propiedad se comprueba observando datos y marcas de tiempo, además de las llamadas al repositorio. La cobertura de funciones cuenta invocaciones; por sí sola no demuestra que todos los resultados de una función sean correctos.

## Aprendizajes

La caja blanca ayuda a seleccionar caminos internos que merecen atención: excepciones, decisiones, condiciones de salida y límites. Complementa las reglas observables del sistema y no sustituye su análisis. La experiencia mostró que una regresión temporal puede aparecer aun con cobertura de ramas completa. Mantener relojes controlados, dependencias explícitas y aserciones sobre consecuencias reales resulta más valioso que perseguir un porcentaje aislado.
