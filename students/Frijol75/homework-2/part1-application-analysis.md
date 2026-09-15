## Application: Canvas LMS

**Purpose**: Canvas es una plataforma de gestión de aprendizaje (Learning
Management System, LMS) desarrollada por Instructure. Su propósito es
centralizar digitalmente la entrega de tareas, la calificación, la
aplicación de exámenes y la comunicación entre profesores y alumnos,
facilitando la administración académica de un curso sin depender de
procesos en papel o dispersos en distintas herramientas.

**Target Users**:

- Alumnos, que entregan tareas, presentan exámenes y revisan sus calificaciones.
- Profesores, que crean contenido, exámenes, y califican el trabajo de los alumnos.
- Administradores del sistema (o del SaaS), que gestionan cuentas, roles, permisos y configuración institucional.

**Key Features**:

1. Entrega de tareas mediante subida de archivos.
2. Calificación de tareas y gestión de calificaciones (gradebook).
3. Exámenes/quizzes en línea, con autocalificación cuando aplica.
4. Bandeja de entrada y notificaciones (push y por correo electrónico).
5. Organización del contenido del curso por módulos o semanas.
6. Calendario de seguimiento de pendientes y fechas límite.
7. Foros de discusión entre alumnos y profesores.

**Technology Stack**: Canvas es una aplicación web accesible desde
navegador, y cuenta además con app móvil nativa para iOS y Android. Los
alumnos suelen usar la versión web para entregar trabajos formales, y la
app móvil para revisar pendientes y notificaciones de forma rápida.

**Critical Functions**: Las funciones consideradas "mission-critical"
son aquellas cuya falla implica una pérdida directa para el alumno o un
riesgo de integridad académica: la entrega de tareas, la presentación de
exámenes, el cálculo y despliegue correcto de calificaciones, y el
sistema de roles y permisos (que un usuario no pueda ver ni modificar
información de otro). La organización del curso por módulos también se
considera crítica, ya que si el contenido no carga o se desordena, el
alumno no puede saber qué debe realizar. En contraste, funciones como la
bandeja de notificaciones, los foros de discusión y el calendario se
consideran de menor criticidad, ya que existen canales alternos
(correo, comunicación directa en clase) y, en el caso del calendario,
es una vista de conveniencia sobre información que ya existe en cada
tarea o examen individualmente.
