class EmailService:  # pylint: disable=too-few-public-methods
    """Simulates an external email service API."""

    def __init__(self, api_key):
        """Initialize the email service with an API key."""
        self.api_key = api_key
        self.sent_emails = []

    def send_email(self, to_address, subject, body):
        """Send an email, raising ValueError for an invalid address."""
        if not self._is_valid_email(to_address):
            raise ValueError(f"Invalid email address: {to_address}")

        self.sent_emails.append({"to": to_address, "subject": subject, "body": body})
        return True

    def _is_valid_email(self, email):
        """Validate email format."""
        return "@" in email and "." in email
