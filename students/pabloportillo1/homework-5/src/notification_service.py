import logging
import re
from typing import Protocol

logger = logging.getLogger(__name__)

EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
PHONE_PATTERN = re.compile(r"\+[1-9]\d{7,14}")
SMS_MAX_LENGTH = 160
SMS_ELLIPSIS = "..."
DEFAULT_MAX_ATTEMPTS = 3


class GatewayError(Exception):
    """Raised by an email or SMS provider client when a delivery request fails."""


class NotificationError(RuntimeError):
    """Raised when a notification could not be delivered after every attempt."""


class EmailGateway(Protocol):
    """Client of the external email provider."""

    def send(self, recipient: str, subject: str, body: str) -> None:
        """Hand one email to the provider."""


class SmsGateway(Protocol):
    """Client of the external SMS provider."""

    def send(self, phone_number: str, message: str) -> None:
        """Hand one text message to the provider."""


def validate_email_address(address):
    """Return the address, or raise ValueError if it is not shaped like name@domain.tld."""
    if not EMAIL_PATTERN.fullmatch(address or ""):
        raise ValueError(f"Invalid email address: {address!r}")
    return address


def validate_phone_number(phone_number):
    """Return the number, or raise ValueError if it is not in E.164 format (+ and 8-15 digits)."""
    if not PHONE_PATTERN.fullmatch(phone_number or ""):
        raise ValueError(f"Invalid phone number: {phone_number!r}")
    return phone_number


class NotificationService:
    """Sends email and SMS notifications, retrying failed provider calls up to max_attempts times."""

    def __init__(self, email_gateway: EmailGateway, sms_gateway: SmsGateway, max_attempts=DEFAULT_MAX_ATTEMPTS):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self._email_gateway = email_gateway
        self._sms_gateway = sms_gateway
        self._max_attempts = max_attempts

    def send_email(self, recipient, subject, body):
        """Deliver an email, or raise NotificationError once every attempt has failed."""
        validate_email_address(recipient)
        self._deliver("Email", self._email_gateway.send, recipient, subject, body)

    def send_sms(self, phone_number, message):
        """Deliver an SMS, cut to 160 characters, or raise NotificationError once every attempt has failed."""
        validate_phone_number(phone_number)
        if len(message) > SMS_MAX_LENGTH:
            message = message[: SMS_MAX_LENGTH - len(SMS_ELLIPSIS)] + SMS_ELLIPSIS
        self._deliver("SMS", self._sms_gateway.send, phone_number, message)

    def _deliver(self, channel, send, *args):
        last_error = None
        for attempt in range(1, self._max_attempts + 1):
            try:
                send(*args)
                return
            except GatewayError as error:
                last_error = error
                logger.warning("%s attempt %d of %d failed: %s", channel, attempt, self._max_attempts, error)
        raise NotificationError(f"{channel} delivery failed after {self._max_attempts} attempts") from last_error
