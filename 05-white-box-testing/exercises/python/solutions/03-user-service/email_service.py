"""Reference solution for Exercise 3: User Service (Module 05 - White Box Testing) - external API layer."""


class EmailService:  # pylint: disable=too-few-public-methods
    """Simulates an external email service API."""

    def __init__(self, api_key):
        """
        Initialize email service with API key.

        Args:
            api_key: API authentication key
        """
        self.api_key = api_key
        self.sent_emails = []  # For testing purposes

    def send_email(self, to_address, subject, body):
        """
        Send an email via external API.

        Args:
            to_address: Recipient email address
            subject: Email subject
            body: Email body content

        Returns:
            True if email sent successfully

        Raises:
            ConnectionError: If API is unreachable
            ValueError: If email address is invalid
        """
        if not self._is_valid_email(to_address):
            raise ValueError(f"Invalid email address: {to_address}")

        # Simulate API call
        # In real implementation, this would make an HTTP request
        self.sent_emails.append({"to": to_address, "subject": subject, "body": body})
        return True

    def _is_valid_email(self, email):
        """Validate email format."""
        return "@" in email and "." in email
