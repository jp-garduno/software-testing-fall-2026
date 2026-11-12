"""External notification service (to be mocked in tests)."""


class NotificationService:
    """External notification service for sending email and SMS alerts."""

    def send_email(self, recipient, subject, body):
        """Send email notification."""
        raise NotImplementedError("Must be mocked in tests")

    def send_sms(self, phone_number, message):
        """Send SMS notification."""
        raise NotImplementedError("Must be mocked in tests")
