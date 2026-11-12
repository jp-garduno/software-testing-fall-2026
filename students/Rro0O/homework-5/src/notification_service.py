"""External notification gateway (an interface, mocked in tests)."""


class NotificationService:
    """Email and SMS delivery through external APIs."""

    def send_email(self, recipient, subject, body):
        """Send an email notification."""
        raise NotImplementedError("Must be mocked in tests")

    def send_sms(self, phone_number, message):
        """Send an SMS notification."""
        raise NotImplementedError("Must be mocked in tests")
