"""Notification contract for external email and SMS adapters."""

from typing import Protocol


class NotificationError(RuntimeError):
    """An adapter could not deliver a notification."""


class NotificationService(Protocol):
    """Adapters translate delivery failures into NotificationError."""

    def send_email(self, recipient: str, subject: str, body: str) -> None:
        """Deliver an email or raise NotificationError."""
        ...

    def send_sms(self, phone_number: str, message: str) -> None:
        """Deliver a text message or raise NotificationError."""
        ...
