# Reflexión técnica para revisión del autor

Este texto es un borrador basado en el trabajo realizado; David debe revisarlo para confirmar que refleja su aprendizaje personal antes de entregarlo como reflexión propia.

La mayor dificultad técnica fue convertir una descripción narrativa en expectativas verificables. Expresiones como “superar el mínimo” o “cumplir el umbral” no siempre coinciden con las desigualdades concretas de las reglas por tipo de cuenta. Por eso el diseño declara cómo se interpreta la igualdad, cuándo se cobran comisiones y qué operaciones se permiten en cada estado. Sin esas decisiones, dos implementaciones diferentes podrían parecer correctas frente al mismo enunciado.

El ejercicio muestra que probar una salida aislada resulta insuficiente para operaciones financieras. Una transferencia rechazada también debe conservar saldo, historial y límite disponible. Además, las pruebas de estados necesitan secuencias completas: alcanzar una suspensión, intentar una operación prohibida y restaurar el acceso mediante un depósito. Preparar esas situaciones usando la interfaz pública mantiene el enfoque de caja negra.

La confianza en el modelo es alta dentro del contrato documentado: los casos pasan, las ramas instrumentadas se ejecutan y las mutaciones introducidas son detectadas por la combinación de técnicas. Sin embargo, esa confianza no se extiende automáticamente a un banco real. Persistencia, autenticación, concurrencia y comunicación con otras instituciones requieren pruebas adicionales y un entorno distinto.

El siguiente paso de aprendizaje sería ampliar los escenarios temporales y contrastar este diseño con requisitos revisados por otra persona. También sería útil implementar un adaptador contra una API para conservar los mismos oráculos al cambiar la tecnología del sistema.
