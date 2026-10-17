const { Task, TaskStatus, TaskPriority } = require("./../src/task");
const { TaskService } = require("./../src/taskService");

/*
pruebas recomendadas:

Cobertura de pruebas (10 puntos): Al menos 10 pruebas, flujos de trabajo completos, cobertura de ramas >80%.
Calidad de simulación (8 puntos): Uso adecuado de simulaciones, verificación de interacciones, aislamiento de pruebas
Lógica de negocio (7 puntos): Pruebe las reglas de negocio, los escenarios de error y los casos límite.
*/

describe("TaskService Integration Tests", () => {
  let mockRepository;
  let mockNotificationService;
  let taskService;

  // el moc que se crea antes de las pruebas.
  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn(),
      findByTitle: jest.fn(),
      findAll: jest.fn(),
      delete: jest.fn(), // línea nueva
    };

    mockNotificationService = {
      sendEmail: jest.fn(),
      sendSms: jest.fn(),
    };

    taskService = new TaskService(mockRepository, mockNotificationService);
  });

  // tarea bien
  test("Integration: Creating task saves to repository and sends notification", async () => {
    mockRepository.findByTitle.mockResolvedValue(null);

    const task = await taskService.createTask(
      "Write tests",
      "Unit and integration tests",
      TaskPriority.HIGH,
    );

    expect(task.title).toBe("Write tests");
    expect(mockRepository.save).toHaveBeenCalledWith(task);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail.mock.calls[0][1]).toContain("New Task Created");
  });

  // titulo duoplicado
  test("Integration: Cannot create task with duplicate title", async () => {
    const existingTask = new Task("Existing Task");
    mockRepository.findByTitle.mockResolvedValue(existingTask);

    await expect(taskService.createTask("Existing Task")).rejects.toThrow(
      "already exists",
    );

    expect(mockRepository.save).not.toHaveBeenCalled();
    expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
  });

  // notificacion
  test("Integration: Status update saves and notifies", async () => {
    const task = new Task("Test Task");
    task.status = TaskStatus.TODO;
    mockRepository.findById.mockResolvedValue(task);

    const updatedTask = await taskService.updateTaskStatus(
      1,
      TaskStatus.IN_PROGRESS,
    );

    expect(updatedTask.status).toBe(TaskStatus.IN_PROGRESS);
    expect(mockRepository.save).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail.mock.calls[0][2]).toContain(
      "TODO",
    );
    expect(mockNotificationService.sendEmail.mock.calls[0][2]).toContain(
      "IN_PROGRESS",
    );
  });

  // El título distingue mayúsculas y minúsculas
  test("Integración: títulos con distinta mayusculas y minusculas se considera diferente", async () => {
    const task = new Task("Task");
    mockRepository.findByTitle.mockImplementation(async (title) =>
      title === "Task" ? task : null,
    );
    const task2 = await taskService.createTask("task");

    // task no es lo mismo que Task, así que se crea
    expect(mockRepository.findByTitle).toHaveBeenCalledWith("task");
    expect(task2.title).toBe("task");
    expect(mockRepository.save).toHaveBeenCalledWith(task2);
  });

  // Transición inválida
  test("Integración (invalida): rechaza una transición de estatus inválida", async () => {
    const task = new Task("Write tests");
    task.status = TaskStatus.DONE;
    mockRepository.findById.mockResolvedValue(task);

    await expect(taskService.updateTaskStatus(1, TaskStatus.IN_PROGRESS),).rejects.toThrow("Invalid transition");
    expect(mockRepository.save).not.toHaveBeenCalled();
    expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
  });

  // actualisar tarea inexistente
  test("Integración (invalida): actualizar el estatus de una tarea inexistente", async () => {
    mockRepository.findById.mockResolvedValue(null);

    await expect(taskService.updateTaskStatus(1, TaskStatus.IN_PROGRESS),).rejects.toThrow("Task 1 not found");
    expect(mockRepository.save).not.toHaveBeenCalled();
  });

  //actualisar tarea de forma corecta
  test("Integración : trancicion valida", async () => {
    const task = new Task("Write tests");
    task.status = TaskStatus.IN_PROGRESS;
    mockRepository.findById.mockResolvedValue(task);

    await taskService.updateTaskStatus(1, TaskStatus.DONE);
    expect(task.status).toBe(TaskStatus.DONE);

    expect(task.status).toBe(TaskStatus.DONE);
    expect(mockRepository.save).toHaveBeenCalledTimes(1);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
  });

  // tranciocion completa (pasr por los cuatro estados [como el avatar])
  test("Integración: flujo completo TODO → IN_PROGRESS → DONE → ARCHIVED", async () => {
    const task = new Task("Flujo completo");
    mockRepository.findById.mockResolvedValue(task);
    await taskService.updateTaskStatus(1, TaskStatus.IN_PROGRESS);
    expect(task.status).toBe(TaskStatus.IN_PROGRESS);
    await taskService.updateTaskStatus(1, TaskStatus.DONE);
    expect(task.status).toBe(TaskStatus.DONE);
    await taskService.updateTaskStatus(1, TaskStatus.ARCHIVED);
    expect(task.status).toBe(TaskStatus.ARCHIVED);

    // Cada cambio de estatus guarda y notifica (3 cambios = 3 veces)
    expect(mockRepository.save).toHaveBeenCalledTimes(3);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(3);

    // El último correo debe mencionar el paso DONE → ARCHIVED
    const ultimoMensaje = mockNotificationService.sendEmail.mock.calls[2][2];
    expect(ultimoMensaje).toContain("DONE");
    expect(ultimoMensaje).toContain("ARCHIVED");
  });

  test("Integración: Crear tarea pasando con todos los parámetros", async () => {
    mockRepository.findByTitle.mockResolvedValue(null);
    dia = 24 * 60 * 60 * 1000
    mañana = Date.now() + dia

    const task = await taskService.createTask(
      title = "Tarea completa",
      description = "Descripción dessscriptiva, asi bien descritiva",
      priority = TaskPriority.URGENT,
      dueDate = mañana,
    );

    expect(task.title).toBe("Tarea completa");
    expect(task.description).toBe('Descripción dessscriptiva, asi bien descritiva');
    expect(task.priority).toBe(TaskPriority.URGENT);
    expect(task.dueDate).toBe(mañana);
    expect(mockRepository.save).toHaveBeenCalledWith(task);
    expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
  });

  test("Integración (inválida): Cambiar una tarea al mismo estado", async () => {
    const task = new Task("Prueba");
    task.status = TaskStatus.TODO;
    mockRepository.findById.mockResolvedValue(task);

    await expect(
      taskService.updateTaskStatus(1, TaskStatus.TODO),
    ).rejects.toThrow("Invalid transition");

    expect(mockRepository.save).not.toHaveBeenCalled();
    expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
  });
});

// Start-Process coverage/lcov-report/index.html
