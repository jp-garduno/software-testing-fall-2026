"""Notification service for TaskFlow.

NotificationService formats the messages and talks to two external gateways: an
``email_client`` (``send(recipient, subject, body)``) and an ``sms_client``
(``send(phone_number, message)``). Both gateways are real network calls in
production, so the tests replace them with mocks.
"""

from __future__ import annotations

import re

from task import Task, TaskStatus

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\+?\d{10,15}$")
SMS_MAX_LENGTH = 160
DEFAULT_MAX_RETRIES = 2


class NotificationError(Exception):
    """Raised when a notification could not be delivered."""


class NotificationService:
    """Sends email and SMS notifications through external gateways, with retries."""

    def __init__(self, email_client, sms_client, max_retries: int = DEFAULT_MAX_RETRIES) -> None:
        if max_retries < 0:
            raise ValueError("max_retries must be zero or greater")
        self.email_client = email_client
        self.sms_client = sms_client
        self.max_retries = max_retries

    # ------------------------------------------------------------------ #
    # Channels
    # ------------------------------------------------------------------ #
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send an email. Retries transient failures; raises NotificationError at the end."""
        if not EMAIL_PATTERN.match(recipient or ""):
            raise NotificationError(f"Invalid email address: {recipient!r}")
        if not subject:
            raise NotificationError("Email subject is required")
        return self._deliver(lambda: self.email_client.send(recipient, subject, body), "email")

    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send an SMS (truncated to 160 characters)."""
        if not PHONE_PATTERN.match(phone_number or ""):
            raise NotificationError(f"Invalid phone number: {phone_number!r}")
        text = message if len(message) <= SMS_MAX_LENGTH else message[: SMS_MAX_LENGTH - 3] + "..."
        return self._deliver(lambda: self.sms_client.send(phone_number, text), "SMS")

    def _deliver(self, send, channel: str) -> bool:
        """Call ``send`` up to 1 + max_retries times."""
        last_error: Exception | None = None
        for _attempt in range(self.max_retries + 1):
            try:
                send()
                return True
            except Exception as exc:  # pylint: disable=broad-exception-caught
                last_error = exc
        raise NotificationError(
            f"{channel} delivery failed after {self.max_retries + 1} attempt(s): {last_error}"
        ) from last_error

    # ------------------------------------------------------------------ #
    # Task events
    # ------------------------------------------------------------------ #
    def notify_task_created(self, recipient: str, task: Task) -> bool:
        return self.send_email(recipient, "New Task Created", f"Task '{task.title}' has been created")

    def notify_status_change(self, recipient: str, task: Task, old_status: TaskStatus) -> bool:
        return self.send_email(
            recipient,
            "Task Status Updated",
            f"Task '{task.title}' changed from {old_status.value} to {task.status.value}",
        )

    def notify_overdue(self, recipient: str, task: Task) -> bool:
        return self.send_email(recipient, "Task Overdue", f"Task '{task.title}' is overdue!")

    def notify_urgent_sms(self, phone_number: str, task: Task) -> bool:
        return self.send_sms(phone_number, f"URGENT task: {task.title}")
