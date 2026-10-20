"""Notification gateway (email + SMS).

The real delivery happens in external clients (an SMTP client and an SMS
provider API) that are injected, so the tests mock them and never touch
the network.
"""

import re

from errors import NotificationError

SMS_MAX_LENGTH = 160
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_PATTERN = re.compile(r"^\+?\d{10,15}$")


class NotificationService:
    def __init__(self, email_client, sms_client):
        self.email_client = email_client
        self.sms_client = sms_client

    def send_email(self, recipient, subject, body):
        if not _EMAIL_PATTERN.match(recipient or ""):
            raise NotificationError(f"Invalid email recipient: {recipient!r}")
        if not subject:
            raise NotificationError("Email subject is required")
        try:
            self.email_client.send(to=recipient, subject=subject, body=body)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise NotificationError(f"Email delivery failed: {exc}") from exc
        return True

    def send_sms(self, phone_number, message):
        if not _PHONE_PATTERN.match(phone_number or ""):
            raise NotificationError(f"Invalid phone number: {phone_number!r}")
        if len(message) > SMS_MAX_LENGTH:
            message = message[: SMS_MAX_LENGTH - 3] + "..."
        try:
            self.sms_client.send(to=phone_number, message=message)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise NotificationError(f"SMS delivery failed: {exc}") from exc
        return True
