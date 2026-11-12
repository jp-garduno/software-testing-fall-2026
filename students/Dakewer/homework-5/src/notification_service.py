"""Notification service: the external dependency (email / SMS provider).

All network traffic goes through an injected ``transport`` callable so the
class itself can be exercised without any real API. In the test suite the whole
service is replaced by a mock.
"""

import logging

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


class NotificationError(Exception):
    """Raised when a notification cannot be delivered."""


class NotificationService:
    """Sends email and SMS notifications through an external provider."""

    def __init__(self, transport=None, max_retries=MAX_RETRIES):
        self.transport = transport
        self.max_retries = max_retries

    def send_email(self, recipient, subject, body):
        """Send an email notification."""
        if not recipient or "@" not in recipient:
            raise NotificationError(f"Invalid email address: {recipient!r}")
        return self._deliver("email", recipient, {"subject": subject, "body": body})

    def send_sms(self, phone_number, message):
        """Send an SMS notification."""
        digits = (phone_number or "").lstrip("+")
        if not digits.isdigit():
            raise NotificationError(f"Invalid phone number: {phone_number!r}")
        return self._deliver("sms", phone_number, {"message": message})

    def _deliver(self, channel, recipient, payload):
        if self.transport is None:
            raise NotificationError("No transport configured")

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.transport(channel, recipient, payload)
            except Exception as exc:  # provider errors are opaque
                last_error = exc
                logger.warning("Attempt %s/%s failed: %s", attempt, self.max_retries, exc)

        raise NotificationError(f"Delivery failed after {self.max_retries} attempts") from last_error
