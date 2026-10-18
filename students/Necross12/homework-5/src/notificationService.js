// Interfaz del servicio externo de notificaciones. En las pruebas siempre se reemplaza por un mock.
class NotificationService {
  async sendEmail(recipient, subject, body) {
    throw new Error("Must be mocked in tests");
  }

  async sendSms(phoneNumber, message) {
    throw new Error("Must be mocked in tests");
  }
}

module.exports = { NotificationService };
