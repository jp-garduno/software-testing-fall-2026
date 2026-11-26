"""External-notification boundary for TaskFlow."""


class NotificationService:
    """Interface for external email and SMS providers."""

    def send_email(self, recipient, subject, body):
        """Send an email notification."""
        raise NotImplementedError("Must be implemented by a notification adapter")

    def send_sms(self, phone_number, message):
        """Send an SMS notification."""
        raise NotImplementedError("Must be implemented by a notification adapter")
