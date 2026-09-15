## Test Type: Security Testing

**Category**: Non-Functional

**Purpose**: Verificar que cada rol (alumno, profesor, admin) solo pueda
acceder y modificar lo que le corresponde, protegiendo la integridad
académica y la privacidad de los datos.

**Examples**:

1. Al cambiar el ID en la URL de calificaciones (ej. /alumno/45/calificacion
   por /alumno/46/calificacion), el sistema debe bloquear el acceso
   (403/404) y no mostrar ni permitir modificar la calificación ajena.
2. Un alumno que intenta acceder a una URL del panel de profesor debe
   ser bloqueado o redirigido a su propia vista, sin ver funciones de
   gestión de calificaciones.
3. Las contraseñas no deben transmitirse ni almacenarse en texto plano
   (verificable en consola/inspector del navegador).

**Priority**: Critical

**Justification**: Una falla aquí no solo rompe una función, sino que
compromete la integridad académica y la privacidad de datos de otros
usuarios — es un riesgo legal y de confianza, no solo técnico.

---

## Test Type: Reliability Testing

**Category**: Non-Functional

**Purpose**: Asegurar que el sistema no pierda el progreso o los datos
del usuario ante fallas técnicas o interrupciones, especialmente
durante exámenes y entregas con tiempo límite.

**Examples**:

1. Durante un examen con temporizador, el sistema debe guardar
   automáticamente cada respuesta y pausar el temporizador si aplica,
   además de respetar la ventana de disponibilidad del examen (ej. si
   abre de 1pm a 3pm, debe cerrar a las 3pm sin importar el tiempo
   restante del alumno).
2. Si la conexión se corta a la mitad de la subida de un archivo de
   tarea, el sistema debe detectar la subida incompleta, notificar al
   alumno que falló, y evitar que quede un archivo corrupto o vacío
   registrado como entrega válida.
3. Si el servidor de Canvas se cae por completo durante un examen, al
   restablecerse el servicio el alumno debe poder recuperar su progreso
   guardado hasta ese punto, sin perder sus respuestas.

**Priority**: Critical

**Justification**: Que un alumno pierda un examen completo o una
entrega por una falla técnica ajena a él genera reclamos de
calificación, pérdida de confianza en la plataforma y posibles
conflictos académicos serios.

---

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Verificar que Canvas responda con tiempos aceptables y
mantenga el servicio estable durante los momentos de mayor carga, como
el cierre de un semestre o la fecha límite de una entrega masiva.

**Examples**:

1. La página de entrega de tareas carga y procesa el envío en menos de
   3 segundos incluso cuando cientos de alumnos entregan en el mismo
   horario límite.
2. El gradebook (con cientos de alumnos y decenas de tareas) calcula y
   muestra promedios sin demoras notables al abrirlo.
3. El sistema soporta que cientos de alumnos de un mismo grupo inicien
   un quiz simultáneamente sin caídas ni retrasos en el guardado de
   respuestas.

**Priority**: Critical

**Justification**: Un cuello de botella de rendimiento en los momentos
de mayor carga (entregas masivas, cierre de semestre) puede impedir que
alumnos completen acciones críticas a tiempo, con el mismo efecto que
una falla total, aunque el sistema técnicamente "funcione".

---

## Test Type: Usability Testing

**Category**: Non-Functional

**Purpose**: Verificar que estudiantes, profesores y administradores
puedan realizar sus tareas principales (entregar, calificar, configurar
un curso) de forma intuitiva, sin necesitar capacitación extensa ni
cometer errores por mala interfaz.

**Examples**:

1. Un alumno nuevo debe poder encontrar la lista de sus cursos activos
   desde la pantalla principal (dashboard) sin necesitar ayuda externa
   o tutorial.
2. Un alumno debe distinguir claramente entre su promedio "actual"
   (basado en tareas ya calificadas) y su promedio "proyectado/posible"
   (incluyendo tareas aún pendientes).
3. La navegación entre materias/cursos debe ser consistente: un alumno
   inscrito en 6 materias debe poder cambiar entre ellas sin perderse ni
   confundir el contenido de un curso con otro.

**Priority**: High

**Justification**: Una mala usabilidad no impide técnicamente que el
sistema funcione, pero genera errores humanos costosos (entregas mal
hechas, alumnos que no ven su calificación real a tiempo) y aumenta la
carga de soporte para la escuela.

---

## Test Type: Regression Testing

**Category**: Functional

**Purpose**: Asegurar que actualizaciones, nuevas funciones o
correcciones de bugs en Canvas no rompan funcionalidades que ya
trabajaban correctamente.

**Examples**:

1. Al agregar una nueva función de "rúbricas mejoradas" para calificar,
   verificar que el cálculo del promedio general del curso sigue siendo
   correcto.
2. Al actualizar el módulo de exámenes para agregar nuevos tipos de
   pregunta, verificar que los quizzes ya creados con el formato
   anterior se sigan autocalificando bien.
3. Al lanzar una nueva versión de la app móvil, verificar que las
   entregas de tareas desde el navegador web sigan funcionando igual.

**Priority**: High

**Justification**: Sin regresión, cada actualización es un riesgo de
romper procesos críticos (entregas, calificaciones) que ya eran
confiables, y muchas veces el error pasa desapercibido hasta que un
usuario real lo reporta.

---

## Test Type: Compatibility Testing

**Category**: Non-Functional

**Purpose**: Verificar que Canvas funcione correctamente a través de
distintos navegadores, sistemas operativos y dispositivos (web y
móvil), ya que alumnos y profesores no usan todos el mismo entorno.

**Examples**:

1. La plataforma web debe verse y funcionar igual en Chrome, Safari,
   Firefox y Edge.
2. La app móvil debe comportarse consistentemente en las versiones
   recientes de iOS y Android.
3. Un alumno debe poder empezar una tarea desde su laptop y continuar
   revisándola desde el celular sin que el contenido se vea roto o
   incompleto.

**Priority**: Medium

**Justification**: No afecta a todos los usuarios por igual, pero una
escuela tiene mezcla real de navegadores y equipos, así que ignorarlo
excluye a una parte de los usuarios sin que sea culpa de ellos.

---

## Test Type: Boundary/Validation Testing

**Category**: Functional

**Purpose**: Verificar que el sistema valide correctamente los límites y
tipos de datos permitidos al subir archivos, escribir texto o ingresar
calificaciones, evitando errores o abusos.

**Examples**:

1. Al subir un archivo de tarea que excede el tamaño máximo permitido,
   el sistema debe rechazarlo con un mensaje claro, no fallar
   silenciosamente ni truncar el archivo.
2. El sistema debe restringir los tipos de archivo aceptados (ej. .pdf,
   .docx) y rechazar formatos no permitidos o potencialmente maliciosos.
3. Al capturar una calificación manualmente, el sistema debe rechazar
   valores fuera de rango (ej. una calificación de 150 sobre 100).

**Priority**: High

**Justification**: Sin esta validación, se pueden generar datos
corruptos en el gradebook o abrir una puerta de seguridad, afectando
tanto la integridad de datos como la seguridad.

---

## Test Type: Accessibility Testing

**Category**: Non-Functional

**Purpose**: Verificar que estudiantes con discapacidades (visuales,
motrices, auditivas) puedan usar Canvas de forma efectiva, cumpliendo
estándares como WCAG.

**Examples**:

1. Un alumno con discapacidad visual debe poder navegar Canvas usando
   un lector de pantalla, incluyendo la entrega de tareas y revisión de
   calificaciones.
2. Los videos de clases o instrucciones deben contar con subtítulos o
   transcripción disponible para alumnos con discapacidad auditiva.
3. Toda la plataforma debe ser navegable solo con teclado (sin mouse)
   para alumnos con dificultad motriz.

**Priority**: Medium

**Justification**: Es un requisito legal en muchas instituciones y
afecta directamente la equidad de acceso educativo, aunque impacta a un
subconjunto más pequeño de usuarios que las fallas funcionales
críticas.
