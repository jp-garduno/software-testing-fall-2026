// Interfaz del servicio externo de notificaciones. En las pruebas siempre se reemplaza por un mock.
class NotificationService {
  async sendEmail(recipient, subject, body) {
    void recipient;
    void subject;
    void body;
    throw new Error("Must be mocked in tests");
  }

  async sendSms(phoneNumber, message) {
    void phoneNumber;
    void message;
    throw new Error("Must be mocked in tests");
  }
}

module.exports = { NotificationService };
