"""External notification service interface (intended to be mocked in tests)."""


class NotificationService:
    """External notification service for alerting users about task events."""

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send email notification to recipient."""
        raise NotImplementedError("Must be mocked in tests")

    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send SMS notification to recipient phone number."""
        raise NotImplementedError("Must be mocked in tests")
