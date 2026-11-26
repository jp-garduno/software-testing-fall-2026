/*
PLAN DE PRUEBAS (mis notas)

Título: validar longitudes 2, 3, 50, 99, 100 y 101 (límites)
Fecha de vencimiento: un día antes (inválida) y un día después (válida)

Título        : cadena (3-100 caracteres, obligatorio)
Descripción   : cadena (opcional, máximo 500 caracteres)
Estado        : enum (TODO, IN_PROGRESS, DONE, ARCHIVED)
Prioridad     : enum (LOW, MEDIUM, HIGH, URGENT)
dueDate       : fecha y hora (debe ser en el futuro cuando se crea)
createdAt     : fecha y hora (se genera automáticamente)
updatedAt     : fecha y hora (se actualiza automáticamente)

TODO → IN_PROGRESS → DONE → ARCHIVED
  ↓         ↓          ↓
ARCHIVED ← ARCHIVED ← ARCHIVED
ARCHIVED es un pozo: nada sale, pero todo entra.

Prioridades: casos mayor, igual y menor.
*/

const { Task, TaskStatus, TaskPriority } = require("../src/task");

// ---------------------------------------------------------------
// Creación de tareas
// ---------------------------------------------------------------
describe("Task Creation", () => {
  // todo correcto
  test("Unit test: Create task with valid data", () => {
    const dueDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
    const task = new Task(
      "Write unit tests",
      "Complete homework 5",
      TaskPriority.HIGH,
      dueDate,
    );
    expect(task.title).toBe("Write unit tests");
    expect(task.description).toBe("Complete homework 5");
    expect(task.status).toBe(TaskStatus.TODO);
    expect(task.priority).toBe(TaskPriority.HIGH);
    expect(task.dueDate).toBe(dueDate);
  });

  // título corto
  test("Unit test: Reject title with fewer than 3 characters", () => {
    expect(() => new Task("ab")).toThrow("at least 3 characters");
  });

  // título largo
  test("Unit test: Reject title exceeding 100 characters", () => {
    const longTitle = "a".repeat(101);
    expect(() => new Task(longTitle)).toThrow("not exceed 100 characters");
  });

  // Valores límite del título: 3, 50, 99 y 100 son válidos
  test.each([3, 50, 99, 100])(
    "Prueba unitaria: Acepta título de %i caracteres",
    (longitud) => {
      const task = new Task("a".repeat(longitud));
      expect(task.title).toHaveLength(longitud);
    },
  );

  // Título vacío
  test("Prueba unitaria (invalida): Título vacío", () => {
    expect(() => new Task("")).toThrow("at least 3 characters");
  });

  test("Prueba unitaria (invalida): Tarea sin título", () => {
    expect(() => new Task()).toThrow("at least 3 characters");
  });

  // Sin descripción: queda vacía por defecto
  test("Prueba unitaria: Tarea sin descripción queda vacía", () => {
    const task = new Task("Prueba");
    expect(task.description).toBe("");
  });

  // Descripción de exactamente 500: se conserva completa
  test("Prueba unitaria: Descripción de 500 caracteres se conserva", () => {
    const task = new Task("Prueba", "a".repeat(500));
    expect(task.description).toHaveLength(500);
  });

  // Descripción de 501: el código NO lanza error, la recorta a 500
  test("Prueba unitaria: Descripción de 501 caracteres se recorta a 500", () => {
    const task = new Task("Prueba", "a".repeat(501));
    expect(task.description).toHaveLength(500);
  });

  // Valores por defecto: prioridad LOW, estado TODO, fechas automáticas
  test("Prueba unitaria: Valores por defecto al crear la tarea", () => {
    const task = new Task("Prueba");
    expect(task.priority).toBe(TaskPriority.LOW);
    expect(task.status).toBe(TaskStatus.TODO);
    expect(task.dueDate).toBeNull();
    expect(task.createdAt).toBeInstanceOf(Date);
    expect(task.updatedAt).toBeInstanceOf(Date);
  });
});

// ---------------------------------------------------------------
// Transiciones de estado
// ---------------------------------------------------------------
describe("Status Transitions", () => {
  // TODO a IN_PROGRESS: correcta
  test("Unit test: Valid transition from TODO to IN_PROGRESS", () => {
    const task = new Task("Test task");
    expect(task.canTransition(TaskStatus.IN_PROGRESS)).toBe(true);
  });

  // DONE a IN_PROGRESS: incorrecta (hacia atrás)
  test("Unit test: Invalid backward transition", () => {
    const task = new Task("Test task");
    task.status = TaskStatus.DONE;
    expect(task.canTransition(TaskStatus.IN_PROGRESS)).toBe(false);
  });

  // IN_PROGRESS a TODO: incorrecta (hacia atrás)
  test("Prueba unitaria(invalida): Cambio de IN_PROGRESS a TODO", () => {
    const task = new Task("Test task");
    task.status = TaskStatus.IN_PROGRESS;
    expect(task.canTransition(TaskStatus.TODO)).toBe(false);
  });

  // TODO a DONE: incorrecta (se salta IN_PROGRESS)
  test("Prueba unitaria (invalida): Cambio de TODO a DONE", () => {
    const task = new Task("Test task");
    expect(task.canTransition(TaskStatus.DONE)).toBe(false);
  });

  // IN_PROGRESS a DONE: correcta
  test("Prueba unitaria: Cambio de IN_PROGRESS a DONE", () => {
    const task = new Task("Test task");
    task.status = TaskStatus.IN_PROGRESS;
    expect(task.canTransition(TaskStatus.DONE)).toBe(true);
  });

  // De cualquier estado se puede ir a ARCHIVED: correcta
  test.each([TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])(
    "Prueba unitaria: Cambio de %s a ARCHIVED",
    (estadoInicial) => {
      const task = new Task("Test task");
      task.status = estadoInicial;
      expect(task.canTransition(TaskStatus.ARCHIVED)).toBe(true);
    },
  );

  // ARCHIVED es un pozo: no sale a ningún estado (incluido él mismo)
  test.each([
    TaskStatus.TODO,
    TaskStatus.IN_PROGRESS,
    TaskStatus.DONE,
    TaskStatus.ARCHIVED,
  ])("Prueba unitaria: Inválida de ARCHIVED a %s", (estadoDestino) => {
    const task = new Task("Test task");
    task.status = TaskStatus.ARCHIVED;
    expect(task.canTransition(estadoDestino)).toBe(false);
  });
});

// ---------------------------------------------------------------
// Fecha de vencimiento
// ---------------------------------------------------------------
describe("Validar fechas", () => {
  const UN_DIA = 24 * 60 * 60 * 1000;
  // ayer: inválida
  test("Prueba unitaria (invalida): Fecha de ayer", () => {
    const ayer = new Date(Date.now() - UN_DIA);
    expect(() => new Task("Test task", "", TaskPriority.LOW, ayer)).toThrow(
      "Due date must be in the future",
    );
  });

  // hace un segundo: inválida (límite "ahora")
  test("Prueba unitaria(invalida): Fecha de hace un segundo", () => {
    const haceUnSegundo = new Date(Date.now() - 1000);
    expect(
      () => new Task("Test task", "", TaskPriority.LOW, haceUnSegundo),
    ).toThrow("Due date must be in the future");
  });

  // mañana: válida
  test("Prueba unitaria: Acepta fecha de mañana", () => {
    const manana = new Date(Date.now() + UN_DIA);
    const task = new Task("Test task", "", TaskPriority.LOW, manana);
    expect(task.dueDate).toBe(manana);
  });

  // sin fecha: válida (la fecha es opcional)
  test("Prueba unitaria: Acepta tarea sin fecha de vencimiento", () => {
    const task = new Task("Test task");
    expect(task.dueDate).toBeNull();
  });
});

// ---------------------------------------------------------------
// Tarea vencida (isOverdue)
// ---------------------------------------------------------------
describe("Detección de tareas vencidas", () => {
  const UN_DIA = 24 * 60 * 60 * 1000;
  function crearTareaVencida() {
    const task = new Task("Test task");
    task.dueDate = new Date(Date.now() - UN_DIA);
    return task;
  }

  test("Prueba unitaria: Vencida si la fecha pasó y no está DONE", () => {
    expect(crearTareaVencida().isOverdue()).toBe(true);
  });

  test("Prueba unitaria: Aceptada si la fecha pasó pero está DONE", () => {
    const task = crearTareaVencida();
    task.status = TaskStatus.DONE;
    expect(task.isOverdue()).toBe(false);
  });

  test("Prueba unitaria: Aceptada si está ARCHIVED", () => {
    const task = crearTareaVencida();
    task.status = TaskStatus.ARCHIVED;
    expect(task.isOverdue()).toBe(false);
  });

  test("Prueba unitaria: Aceptada si la fecha es futura", () => {
    const task = new Task("Test task");
    task.dueDate = new Date(Date.now() + UN_DIA);
    expect(task.isOverdue()).toBe(false);
  });

  test("Prueba unitaria: Aceptada si no tiene fecha", () => {
    const task = new Task("Test task");
    expect(task.isOverdue()).toBe(false);
  });
});

// ---------------------------------------------------------------
// Comparación de prioridades
// ---------------------------------------------------------------
describe("Validar prioridad", () => {
  // Resultado: 1 si la primera es mayor, 0 si son iguales, -1 si es menor
  // mayor: URGENT contra MEDIUM
  test("Prueba unitaria: Prioridad mayor (URGENT vs MEDIUM)", () => {
    const tarea1 = new Task("prueba 1", "", TaskPriority.URGENT);
    const tarea2 = new Task("prueba 2", "", TaskPriority.MEDIUM);
    expect(tarea1.comparePriority(tarea2)).toBe(1);
  });

  // iguales
  test("Prueba unitaria: Prioridades iguales", () => {
    const tarea1 = new Task("prueba 1", "", TaskPriority.MEDIUM);
    const tarea2 = new Task("prueba 2", "", TaskPriority.MEDIUM);
    expect(tarea1.comparePriority(tarea2)).toBe(0);
  });

  // menor: LOW contra MEDIUM
  test("Prueba unitaria: Prioridad menor (LOW vs MEDIUM)", () => {
    const tarea1 = new Task("prueba 1", "", TaskPriority.LOW);
    const tarea2 = new Task("prueba 2", "", TaskPriority.MEDIUM);
    expect(tarea1.comparePriority(tarea2)).toBe(-1);
  });
});
