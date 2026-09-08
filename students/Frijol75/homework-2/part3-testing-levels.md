## Unit Testing

**Scope**: Funciones y métodos individuales, aislados del resto del
sistema (sin UI, sin base de datos, sin red).

**What to Test**:

- Función de cálculo de promedio de calificaciones (maneja tareas sin calificar, listas vacías, ponderaciones).
- Función de validación de fecha límite (si una entrega llegó a tiempo o tarde, dado un timestamp).
- Función de cálculo de puntaje en quizzes de opción múltiple (respuesta correcta vs. incorrecta, puntos parciales si aplica).

**Tools**: Jest (si el frontend/backend es JavaScript) o JUnit/PyTest, dependiendo del stack.

**Coverage Goal**: 80% de cobertura de código en la lógica de negocio (cálculos, validaciones).

**Example Test Cases**:

1. calcularPromedio([80, 90, 100]) debe regresar 90.
2. calcularPromedio([80, 90, null]) debe ignorar la tarea sin calificar y regresar 85.
3. calcularPromedio([]) no debe generar error, debe regresar un valor definido (ej. null o "N/A").

**Estimated Number of Tests**: ~120-150 pruebas unitarias.

---

## Integration Testing

**Scope**: Interacción entre dos o más módulos del sistema trabajando
juntos (ej. entregas + base de datos + notificaciones, o login +
sistema de roles).

**What to Test**:

- Que al entregar una tarea se cree el registro correspondiente y se dispare la notificación al profesor.
- Que al terminar un quiz autocalificado, el puntaje se refleje correctamente en el gradebook.
- Que el módulo de autenticación se comunique bien con el módulo de roles/permisos al iniciar sesión.

**Tools**: Postman o REST Assured para pruebas de API, Cypress para flujos integrados.

**Coverage Goal**: Cubrir el ~90% de las rutas de integración de los flujos críticos (entrega, calificación, login).

**Example Test Cases**:

1. Al subir una tarea, verificar que se cree el registro en base de datos y se envíe notificación al profesor asignado.
2. Al terminar un quiz autocalificado, verificar que el puntaje se refleje correctamente en el gradebook sin retraso.
3. Al hacer login, verificar que el token de sesión generado dé acceso solo a los recursos correspondientes al rol del usuario.

**Estimated Number of Tests**: ~60-80 pruebas de integración.

---

## System Testing

**Scope**: La aplicación completa funcionando de extremo a extremo,
simulando el uso real, sin aislar componentes.

**What to Test**:

- Flujo completo de un alumno: login → entrar a curso → ver módulo → entregar tarea → recibir notificación de calificación.
- Flujo completo de un profesor: crear curso → subir contenido → crear examen → calificar → publicar notas.
- Comportamiento del sistema en condiciones reales (multi-dispositivo, multi-navegador, carga normal).

**Tools**: Selenium, Cypress o Playwright para pruebas end-to-end automatizadas, además de pruebas manuales exploratorias.

**Coverage Goal**: Cubrir los flujos de negocio principales de cada rol (alumno, profesor, admin).

**Example Test Cases**:

1. Un alumno puede iniciar sesión, ver todos sus cursos activos, entrar a uno, y entregar una tarea sin errores.
2. Un profesor puede crear un examen con distintos tipos de pregunta, publicarlo, y verificar que se autocalifique correctamente al ser respondido.
3. Un administrador puede crear una cuenta de curso, asignar profesores y alumnos, y verificar que los roles definidos apliquen correctamente en toda la plataforma.

**Estimated Number of Tests**: ~40-50 escenarios end-to-end.

---

## Acceptance Testing

**Scope**: Validar que el sistema cumple con lo que la institución
educativa realmente necesita, generalmente evaluado por los propios
usuarios finales (UAT - User Acceptance Testing).

**What to Test**:

- Que el flujo de entrega y calificación cumpla el reglamento académico de la institución (ej. penalización por retraso, fechas límite).
- Que los reportes o boletas generados cumplan el formato que la escuela necesita para trámites oficiales.
- Que la experiencia general sea aceptable para profesores no muy técnicos, sin requerir soporte constante.

**Tools**: Pruebas manuales con usuarios reales (profesores y alumnos piloto), listas de criterios de aceptación acordados con la institución.

**Coverage Goal**: 100% de los criterios de aceptación definidos con la institución.

**Example Test Cases**:

1. Un grupo piloto de profesores usa Canvas durante un módulo completo y confirma que puede calificar sin ayuda del equipo de soporte.
2. La escuela valida que el reporte final de calificaciones exportado coincide con el formato requerido por control escolar.
3. Los alumnos piloto confirman que pueden completar el ciclo de entrega-calificación sin errores de comprensión.

**Estimated Number of Tests**: ~15-20 criterios de aceptación validados con usuarios reales.
