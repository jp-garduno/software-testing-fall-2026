"""Notification gateway client for TaskFlow: email and SMS through an external HTTP API."""

import re

SMS_MAX_LENGTH = 160
_EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
_PHONE_PATTERN = re.compile(r"\+\d{8,15}")


class NotificationError(Exception):
    """Raised when the gateway could not deliver a notification."""


class NotificationService:
    """Sends notifications through an injected HTTP client (anything with a requests-style post)."""

    def __init__(self, http_client, base_url="https://api.notify.example.com", timeout=5):
        self.http_client = http_client
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def send_email(self, recipient, subject, body):
        """Send an email and return the gateway's message id."""
        if not isinstance(recipient, str) or not _EMAIL_PATTERN.fullmatch(recipient):
            raise ValueError(f"Invalid email address: {recipient!r}")
        return self._post("/email", {"to": recipient, "subject": subject, "body": body})

    def send_sms(self, phone_number, message):
        """Send an SMS, shortening messages over 160 characters, and return the message id."""
        if not isinstance(phone_number, str) or not _PHONE_PATTERN.fullmatch(phone_number):
            raise ValueError(f"Invalid phone number: {phone_number!r}")
        if len(message) > SMS_MAX_LENGTH:
            message = message[: SMS_MAX_LENGTH - 3] + "..."
        return self._post("/sms", {"to": phone_number, "message": message})

    def _post(self, path, payload):
        try:
            response = self.http_client.post(f"{self.base_url}{path}", json=payload, timeout=self.timeout)
        except OSError as error:
            # ConnectionError, TimeoutError and requests' exceptions are all OSError subclasses.
            raise NotificationError(f"Notification gateway unreachable: {error}") from error
        if response.status_code >= 400:
            raise NotificationError(f"Notification gateway answered HTTP {response.status_code}")
        return response.json().get("id")
