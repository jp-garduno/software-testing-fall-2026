function mockSerevicesCrut() {
  return {
    save: jest.fn(),
    findById: jest.fn(),
    findByTitle: jest.fn(),
    findAll: jest.fn(),
    delete: jest.fn(),
  };
}

function mockServiceNotification() {
  return {
    sendEmail: jest.fn(),
    sendSms: jest.fn(),
  };
}

class MocClonRepository {
  constructor() {
    this.tasks = new Map();
    this.nextId = 1;
  }

  async save(task) {
    if (!task.id) task.id = this.nextId++;
    this.tasks.set(task.id, task);
  }

  async findById(id) {
    return this.tasks.get(id) || null;
  }

  async findByTitle(title) {
    for (const task of this.tasks.values()) {
      if (task.title === title) return task;
    }
    return null;
  }

  async findAll() {
    return [...this.tasks.values()];
  }

  async delete(id) {
    return this.tasks.delete(id);
  }
}

module.exports = {
  mockSerevicesCrut,
  mockServiceNotification,
  MocClonRepository
};
