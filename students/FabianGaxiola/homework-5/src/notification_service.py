"""Notification boundary; concrete delivery is intentionally external."""


class NotificationError(Exception):
    """Raised when a notification cannot be delivered."""


class NotificationService:
    """External notification interface to be replaced with a real provider."""

    def send_email(self, recipient: str, subject: str, body: str) -> None:
        raise NotificationError("Email delivery is not configured")

    def send_sms(self, phone_number: str, message: str) -> None:
        raise NotificationError("SMS delivery is not configured")
