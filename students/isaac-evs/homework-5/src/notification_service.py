"""Notification gateway. Real delivery goes through injected clients so tests can mock them."""


class NotificationError(Exception):
    """Raised when a notification cannot be delivered."""


class NotificationService:
    """Sends email and SMS notifications through pluggable transport clients."""

    def __init__(self, email_client=None, sms_client=None):
        self.email_client = email_client
        self.sms_client = sms_client

    def send_email(self, recipient, subject, body):
        """Send an email; raises NotificationError if it cannot be delivered."""
        if self.email_client is None:
            raise NotificationError("Email client is not configured")
        if not recipient:
            raise ValueError("Recipient is required")
        try:
            return self.email_client.send(recipient, subject, body)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise NotificationError(f"Email delivery failed: {exc}") from exc

    def send_sms(self, phone_number, message):
        """Send an SMS; raises NotificationError if it cannot be delivered."""
        if self.sms_client is None:
            raise NotificationError("SMS client is not configured")
        if not phone_number:
            raise ValueError("Phone number is required")
        try:
            return self.sms_client.send(phone_number, message)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise NotificationError(f"SMS delivery failed: {exc}") from exc
