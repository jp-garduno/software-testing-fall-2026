const { Task, TaskStatus } = require("../src/task");
const { TaskRepository } = require("../src/taskRepository");
const { NotificationService } = require("../src/notificationService");

describe("Casos límite para cobertura de ramas", () => {
  // el `|| []` de canTransition solo se usa si el estado no está en el mapa de transiciones
  // agregada para cubrir el 100% de branch de las pruebas de unitarias
  test("Prueba unitaria (invalida): Estado desconocido no permite ninguna transición", () => {
    const task = new Task("Test task");
    task.status = "ESTADO_MAGICO_E_INEXISTENTE";
    expect(task.canTransition(TaskStatus.IN_PROGRESS)).toBe(false);
  });
});

// Las interfaces solo definen el contrato: cualquier uso real debe sustituirse por un mock
describe("Interfaces de dependencias externas", () => {
  test.each(["save", "findById", "findByTitle", "findAll", "delete"])(
    "Prueba unitaria: TaskRepository.%s exige ser reemplazado por un mock",
    async (metodo) => {
      await expect(new TaskRepository({})[metodo]()).rejects.toThrow(
        "Must be mocked in tests",
      );
    },
  );

  test.each(["sendEmail", "sendSms"])(
    "Prueba unitaria: NotificationService.%s exige ser reemplazado por un mock",
    async (metodo) => {
      await expect(new NotificationService()[metodo]()).rejects.toThrow(
        "Must be mocked in tests",
      );
    },
  );
});
