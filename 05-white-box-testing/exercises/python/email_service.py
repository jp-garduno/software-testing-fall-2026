"""External email service abstraction."""


class EmailService:
    """Simulates an external email service API."""

    def __init__(self, api_key):
        """Initialize the service with its API key."""
        self.api_key = api_key
        self.sent_emails = []

    def send_email(self, to_address, subject, body):
        """Send an email and return whether delivery was accepted."""
        if not self._is_valid_email(to_address):
            raise ValueError(f"Invalid email address: {to_address}")

        self.sent_emails.append(
            {"to": to_address, "subject": subject, "body": body}
        )
        return True

    def _is_valid_email(self, email):
        """Validate the minimal email format required by this exercise."""
        return "@" in email and "." in email
