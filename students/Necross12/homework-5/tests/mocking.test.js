/*
PARTE 4: MOCKING Y AISLAMIENTO

Mock:   Verifica llamadas (cuántas veces, con qué argumentos y en qué orden)
Stub:   Devuelve respuestas predefinidas (mockResolvedValue / mockRejectedValue)
Fake:   Implementación simple que sí funciona (MocClonRepository, guarda en memoria)
Spy:    Registra las llamadas, pero deja correr el código real (jest.spyOn)
Dummy:   El torpecito de la familia, no se usa.
*/

const { Task, TaskStatus, TaskPriority } = require("../src/task");
const { TaskService } = require("../src/taskService");
const { mockSerevicesCrut, mockServiceNotification, MocClonRepository } = require("./helpers/mockTask");

describe("Mocking y aislamiento de pruebas", () => {
  let mockRepository;
  let mockNotificationService;
  let taskService;

  // Se crean los mocks antes de cada prueba
  beforeEach(() => {
    mockRepository = mockSerevicesCrut();
    mockNotificationService = mockServiceNotification();
    taskService = new TaskService(mockRepository, mockNotificationService);
  });

  // Errores en el repositorio
  describe("Errores del repositorio", () => {
    test("Integration: Handle repository failure gracefully", async () => {
      mockRepository.findByTitle.mockResolvedValue(null);
      mockRepository.save.mockRejectedValue(new Error("Database connection failed"));

      await expect(taskService.createTask("Test Task")).rejects.toThrow("Database connection failed");
      expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
    });

    test("Integración (invalida): si findByTitle falla, no se guarda ni se notifica", async () => {
      mockRepository.findByTitle.mockRejectedValue(new Error("Database timeout"));

      await expect(taskService.createTask("Test Task")).rejects.toThrow("Database timeout");
      expect(mockRepository.save).not.toHaveBeenCalled();
      expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
    });

    test("Integración (invalida): si findById falla al cambiar de estatus, no se guarda ni se notifica", async () => {
      mockRepository.findById.mockRejectedValue(new Error("Database unavailable"));

      await expect(taskService.updateTaskStatus(1, TaskStatus.IN_PROGRESS)).rejects.toThrow("Database unavailable");
      expect(mockRepository.save).not.toHaveBeenCalled();
      expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
    });

    test("Integración (invalida): si save falla al cambiar de estatus, no se notifica", async () => {
      mockRepository.findById.mockResolvedValue(new Task("Write tests"));
      mockRepository.save.mockRejectedValue(new Error("Disk full"));

      await expect(taskService.updateTaskStatus(1, TaskStatus.IN_PROGRESS)).rejects.toThrow("Disk full");
      expect(mockNotificationService.sendEmail).not.toHaveBeenCalled();
    });
  });

  // Errores del servicio de notificaciones (API externa)
  describe("Errores de notificaciones", () => {
    let warnSpy;

    // el servicio avisa con console.warn cuando falla el correo; lo silencio para no ensuciar la salida
    beforeEach(() => {
      warnSpy = jest.spyOn(console, "warn").mockImplementation(() => {
      });
    });

    afterEach(() => {
      warnSpy.mockRestore();
    });

    test("Integration: Notification failure should not prevent task creation", async () => {
      mockRepository.findByTitle.mockResolvedValue(null);
      mockNotificationService.sendEmail.mockRejectedValue(new Error("SMTP server unavailable"));
      const task = await taskService.createTask("Test Task");

      expect(task.title).toBe("Test Task");
      expect(mockRepository.save).toHaveBeenCalledTimes(1);
      expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    });

    test("Integración: si el correo falla, se deja constancia con un aviso", async () => {
      mockRepository.findByTitle.mockResolvedValue(null);
      mockNotificationService.sendEmail.mockRejectedValue(new Error("SMTP server unavailable"));
      await taskService.createTask("Test Task");

      expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining("SMTP server unavailable"));
    });

    test("Integración: si el correo falla al cambiar de estatus, el cambio queda guardado", async () => {
      const task = new Task("Write tests");
      mockRepository.findById.mockResolvedValue(task);
      mockNotificationService.sendEmail.mockRejectedValue(new Error("SMTP server unavailable"));
      const updatedTask = await taskService.updateTaskStatus(1, TaskStatus.IN_PROGRESS);

      expect(updatedTask.status).toBe(TaskStatus.IN_PROGRESS);
      expect(mockRepository.save).toHaveBeenCalledTimes(1);
    });
  });

  // Mock: verificar interacciones
  describe("Verificación de interacciones (mocks)", () => {
    // argumentos exactos, y sendSms (dummy) nunca se usa
    test("Integración: sendEmail recibe destinatario, asunto y cuerpo exactos", async () => {
      mockRepository.findByTitle.mockResolvedValue(null);
      await taskService.createTask("Write tests");
      expect(mockNotificationService.sendEmail).toHaveBeenCalledWith("user@example.com", "New Task Created", "Task 'Write tests' has been created",);
      expect(mockNotificationService.sendSms).not.toHaveBeenCalled();
    });

    // orden: primero se guarda y después se notifica
    test("Integración: el repositorio guarda ANTES de notificar", async () => {
      mockRepository.findByTitle.mockResolvedValue(null);
      await taskService.createTask("Write tests");
      const ordenSave = mockRepository.save.mock.invocationCallOrder[0];
      const ordenEmail = mockNotificationService.sendEmail.mock.invocationCallOrder[0];
      expect(ordenSave).toBeLessThan(ordenEmail);
    });

    // cada cambio de estatus manda su propio correo, en orden
    test("Integración: cada cambio de estatus notifica con el mensaje correcto", async () => {
      const task = new Task("Flujo");
      mockRepository.findById.mockResolvedValue(task);
      await taskService.updateTaskStatus(1, TaskStatus.IN_PROGRESS);
      await taskService.updateTaskStatus(1, TaskStatus.DONE);

      expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(2);
      expect(mockNotificationService.sendEmail).toHaveBeenNthCalledWith(1, "user@example.com", "Task Status Updated", "Task 'Flujo' changed from TODO to IN_PROGRESS");
      expect(mockNotificationService.sendEmail).toHaveBeenNthCalledWith(2, "user@example.com", "Task Status Updated", "Task 'Flujo' changed from IN_PROGRESS to DONE");
    });
  });

  // Stub: respuestas predefinidas
  describe("Respuestas predefinidas (stubs)", () => {
    // primera llamada: no existe; segunda llamada: ya existe
    test("Integración: el stub responde distinto en cada llamada (título repetido)", async () => {
      const existente = new Task("Repetida");
      mockRepository.findByTitle
        .mockResolvedValueOnce(null)
        .mockResolvedValueOnce(existente);

      await taskService.createTask("Repetida");
      await expect(taskService.createTask("Repetida")).rejects.toThrow("already exists");

      // solo la primera se guardó y notificó
      expect(mockRepository.save).toHaveBeenCalledTimes(1);
      expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    });
  });

  // Fake: repositorio en memoria (flujo real sin stubs)
  describe("Repositorio en memoria (fake)", () => {
    let fakeRepository;

    beforeEach(() => {
      fakeRepository = new MocClonRepository();
      taskService = new TaskService(fakeRepository, mockNotificationService);
    });

    test("Integración: flujo completo TODO → IN_PROGRESS → DONE → ARCHIVED con ids reales", async () => {
      const task = await taskService.createTask("Flujo con fake", "", TaskPriority.HIGH);
      expect(task.id).toBe(1);

      await taskService.updateTaskStatus(task.id, TaskStatus.IN_PROGRESS);
      await taskService.updateTaskStatus(task.id, TaskStatus.DONE);
      await taskService.updateTaskStatus(task.id, TaskStatus.ARCHIVED);

      const guardada = await fakeRepository.findById(task.id);
      expect(guardada.status).toBe(TaskStatus.ARCHIVED);

      // 1 correo por la creación + 3 por los cambios de estatus
      expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(4);
    });

    // aquí no configuro findByTitle: el fake detecta el duplicado solo
    test("Integración (invalida): el fake detecta el título duplicado", async () => {
      await taskService.createTask("Única");
      await expect(taskService.createTask("Única")).rejects.toThrow("already exists");

      expect(await fakeRepository.findAll()).toHaveLength(1);
      expect(mockNotificationService.sendEmail).toHaveBeenCalledTimes(1);
    });

    test("Integración (invalida): una tarea ARCHIVED ya no cambia de estatus", async () => {
      const task = await taskService.createTask("Para archivar");
      await taskService.updateTaskStatus(task.id, TaskStatus.ARCHIVED);

      await expect(taskService.updateTaskStatus(task.id, TaskStatus.IN_PROGRESS)).rejects.toThrow("Invalid transition");
    });
  });

  // Spy: código real + registro de llamadas
  describe("Espía (spy)", () => {
    test("Integración: el fake guarda de verdad y además se registra la llamada a save", async () => {
      const fakeRepository = new MocClonRepository();
      const saveSpy = jest.spyOn(fakeRepository, "save");
      taskService = new TaskService(fakeRepository, mockNotificationService);

      const task = await taskService.createTask("Con spy");

      expect(saveSpy).toHaveBeenCalledWith(task);
      expect(await fakeRepository.findById(task.id)).toBe(task);
    });
  });

  // Tiempo controlado
  describe("Tiempo controlado", () => {
    // regreso el reloj real para no afectar a otras pruebas
    afterEach(() => {
      jest.useRealTimers();
    });

    test("Integración: updatedAt toma la hora simulada al cambiar de estatus", async () => {
      jest.useFakeTimers().setSystemTime(new Date("2026-10-17T10:00:00Z"));
      taskService = new TaskService(new MocClonRepository(), mockNotificationService,);
      const task = await taskService.createTask("Con reloj");

      jest.setSystemTime(new Date("2026-10-17T12:00:00Z"));
      await taskService.updateTaskStatus(task.id, TaskStatus.IN_PROGRESS);

      expect(task.createdAt).toEqual(new Date("2026-10-17T10:00:00Z"));
      expect(task.updatedAt).toEqual(new Date("2026-10-17T12:00:00Z"));
    });
  });
});
