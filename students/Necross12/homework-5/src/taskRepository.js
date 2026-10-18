// Interfaz de la capa de datos. En las pruebas siempre se reemplaza por un mock o un fake.
class TaskRepository {
  constructor(database) {
    this.database = database;
  }

  async save(task) {
    throw new Error("Must be mocked in tests");
  }

  async findById(taskId) {
    throw new Error("Must be mocked in tests");
  }

  async findByTitle(title) {
    throw new Error("Must be mocked in tests");
  }

  async findAll() {
    throw new Error("Must be mocked in tests");
  }

  async delete(taskId) {
    throw new Error("Must be mocked in tests");
  }
}

module.exports = { TaskRepository };
