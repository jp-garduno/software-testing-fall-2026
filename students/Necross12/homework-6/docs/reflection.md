# Reflexión sobre TDD

## Impacto en el diseño

El TDD cambió varias de mis decisiones porque cada test me obligaba a pensar primero en cómo se iba a usar el código. El caso más claro fue el test «pedir superando el límite del miembro no descuenta la copia». Al escribirlo vi que, si el libro se descontaba antes de validar al miembro, una operación fallida dejaba el sistema en un estado inconsistente. Por eso `pedirLibro` consulta `puedePedir()` antes de llamar a `libro.pedir()`. Otro ejemplo es que `pedirLibro` recibe `fechaPrestamo` y `calcularRecargo` recibe `fechaActual` como parámetros con valor por defecto: lo hice para poder probar retrasos sin depender del reloj real. Las categorías de miembro también terminaron en una constante `CATEGORIAS` porque el segundo test de tarifas me mostró que repetir valores fijos no escalaba.

## Retos

Lo más difícil fue el cambio de hábito. Normalmente escribo el módulo completo, pruebo al final y hago commit cuando está terminado. Al principio escribí el código primero y luego dividí las pruebas para simular commits pequeños, lo cual no es TDD. Hasta el segundo bloque logré escribir la prueba, verla fallar y solo entonces escribir el código mínimo. También me costó resistir la tentación de implementar de más en la fase GREEN.

## Ventajas

Cada cambio tenía una red de seguridad. Cuando refactoricé (la validación del ISBN con una expresión regular, la extracción de `obtenerMiembroRegistrado`) los tests me avisaban de inmediato si rompía algo. Además, los nombres de los tests quedaron como una especificación legible del sistema, y los commits pequeños hicieron fácil ubicar dónde empezaba cada comportamiento.

## Comparación con test-after

Con test-after las pruebas se escriben mirando el código ya hecho, así que tienden a confirmar lo que existe en lugar de cuestionarlo. Lo comprobé al final: al revisar la cobertura encontré métodos que ninguna prueba exigía (`quitarReserva`, `notificarSiguienteEnCola`), valores por defecto de fechas sin probar y un error en `regresarLibro`: si el miembro devolvía un libro que no tenía registrado como préstamo, se borraba el préstamo de otra persona. Esos huecos estaban en código que escribí sin que un test lo pidiera, lo que confirma que sin el test primero se cuela código que nadie necesita. Las pruebas escritas después sirvieron para cubrirlos, pero llegaron tarde y el error de `regresarLibro` ya estaba ahí.

## Uso futuro

Usaría TDD en proyectos individuales o módulos con reglas de negocio claras, como este, donde conviene definir el comportamiento esperado antes de programarlo. Reduce el riesgo de romper funcionalidades sin saber dónde ocurrió el error y aporta un orden lógico. Lo usaría menos en código legacy sin pruebas, en prototipos que se van a desechar o con plazos muy ajustados donde todavía no está claro qué se va a construir, porque habría que reescribir muchos tests y las pruebas entorpecerían más de lo que ayudan.

## Aprendizaje

Me sorprendió lo pequeño que puede ser un paso y cuánto diseño sale de ellos. También cambié una idea: pensaba que el TDD servía sobre todo para pruebas de caja blanca, pero los tests que escribí describen comportamiento (qué pasa al pedir, reservar o devolver), no la estructura interna. La estructura la revisé después con el reporte de cobertura. Si repitiera el proyecto, haría commit RED y GREEN desde la primera prueba y escribiría únicamente el código que cada prueba pide.
