# Informe de análisis: White Box Testing

## Logro de las métricas de cobertura

La implementación de TaskFlow obtuvo 100% de cobertura de sentencias y ramas:
187 líneas ejecutables y 54 destinos de ramas. También se ejecutaron los 29
cuerpos de funciones Python con nombre identificados por coverage.py. Las 112
pruebas comprobaron validaciones, transiciones, búsquedas, persistencia y
notificaciones. El trabajo comenzó por el modelo y continuó con las operaciones
del servicio. La parametrización permitió describir todas las parejas de
estados y los límites temporales sin repetir grandes bloques de preparación.
Los escenarios de error complementaron las comprobaciones de éxito para
alcanzar las ramas que suelen quedar fuera de una prueba superficial.

## Dificultades para alcanzar los objetivos

La dificultad más reveladora estuvo en la relación entre tiempo y persistencia.
El almacén falso copiaba profundamente la tarea y, junto con ella, copiaba el
reloj controlado. Al avanzar el tiempo, una tarea recuperada seguía observando
el instante anterior. Una prueba de edición de tareas vencidas detectó ese
problema aunque la primera medición completa ya mostraba 100% de cobertura.
La corrección conservó copias independientes de los datos y una referencia
compartida al reloj. Otro punto importante fue evitar que un guardado fallido
alterara la tarea original. El servicio valida y modifica una copia antes de
persistirla; las pruebas comprueban que el objeto anterior conserva sus valores.

## Beneficios de simular dependencias externas

Los mocks permitieron provocar fallos de conexión, errores de correo y fallos
de SMS de forma determinista. También hicieron posible verificar argumentos,
número de llamadas y el orden entre guardar y notificar. Los stubs devolvieron
resultados concretos, como una tarea existente o la ausencia de coincidencias.
El repositorio falso agregó estado suficiente para comprobar flujos completos
sin infraestructura. Sin estas técnicas harían falta servicios configurados,
credenciales y limpieza de datos, y las pruebas dependerían de disponibilidad
y latencia externas. Su coste fue preparar respuestas coherentes y cuidar que
los dobles representaran adecuadamente el comportamiento que se quería observar.

## Cobertura frente a calidad de las pruebas

El resultado numérico no demuestra que todos los defectos posibles hayan sido
descartados. Una llamada puede cubrir una rama sin verificar sus efectos
correctamente. Por eso los casos comprueban también ausencia de guardados ante
validaciones inválidas, conservación del estado, destinatarios y continuidad
del flujo cuando falla una notificación. No se añadieron exclusiones para
inflar el porcentaje ni pruebas que se limitaran a invocar métodos sin evaluar
resultados. Alcanzar 100% fue razonable por el tamaño reducido del sistema;
seguir agregando casos equivalentes tendría rendimientos decrecientes. Sería
más útil incorporar contratos reales o pruebas de mutación que duplicar
afirmaciones ya cubiertas.

## Aprendizajes y aplicación futura

La experiencia muestra que las decisiones internas ayudan a elegir entradas,
pero la evaluación debe centrarse en comportamientos observables. La tabla de
transiciones convirtió reglas del enunciado en expectativas comprobables. El
reloj inyectado eliminó esperas y permitió explorar el límite exacto del
vencimiento. En otro proyecto convendría definir antes los contratos temporales
y de persistencia para reducir discrepancias entre dobles y adaptadores. La
suite normal terminó en 0.75 segundos; con instrumentación y reportes tardó
2.84 segundos. Estas mediciones permiten distinguir rapidez funcional del coste
de recopilar evidencia. La cobertura seguirá siendo una señal de revisión,
acompañada de requisitos claros y aserciones que puedan revelar errores reales.
