"""Notification service wrapping the external email and SMS providers.

The provider clients (``email_client.send`` and ``sms_client.send``) are
external API calls and are replaced by mocks in tests.
"""

import re

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_PATTERN = re.compile(r"^\+?\d{10,15}$")
SMS_MAX_LENGTH = 160


class NotificationError(Exception):
    """Raised when a notification cannot be delivered."""


class NotificationService:

    def __init__(self, email_client, sms_client):
        self.email_client = email_client
        self.sms_client = sms_client

    def send_email(self, recipient, subject, body):
        if not recipient or not _EMAIL_PATTERN.match(recipient):
            raise NotificationError(f"Invalid email recipient: {recipient!r}")
        if not subject:
            raise NotificationError("Email subject is required")
        try:
            return self.email_client.send(to=recipient, subject=subject, body=body)
        except Exception as error:  # pylint: disable=broad-exception-caught
            raise NotificationError(f"Email delivery failed: {error}") from error

    def send_sms(self, phone_number, message):
        if not phone_number or not _PHONE_PATTERN.match(phone_number):
            raise NotificationError(f"Invalid phone number: {phone_number!r}")
        if len(message) > SMS_MAX_LENGTH:
            # Providers reject long messages; truncate rather than fail.
            message = message[: SMS_MAX_LENGTH - 3] + "..."
        try:
            return self.sms_client.send(to=phone_number, message=message)
        except Exception as error:  # pylint: disable=broad-exception-caught
            raise NotificationError(f"SMS delivery failed: {error}") from error
