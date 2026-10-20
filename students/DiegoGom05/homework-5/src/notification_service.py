class NotificationService:
    """Servicio externo de notificaciones. En los tests siempre se mockea."""

    def send_email(self, recipient, subject, body):
        raise NotImplementedError("Must be mocked in tests")

    def send_sms(self, phone_number, message):
        raise NotImplementedError("Must be mocked in tests")
