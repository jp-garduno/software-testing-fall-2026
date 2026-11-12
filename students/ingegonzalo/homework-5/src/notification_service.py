class NotificationService:
    """External notification service (to be mocked in tests)."""

    def send_email(self, recipient, subject, body):
        raise NotImplementedError("Must be mocked in tests")

    def send_sms(self, phone_number, message):
        raise NotImplementedError("Must be mocked in tests")