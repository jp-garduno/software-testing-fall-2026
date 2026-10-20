"""Notification API boundary with an injected email/SMS transport."""


class NotificationService:
    def __init__(self, transport):
        self.transport = transport

    def send_email(self, recipient, subject, body):
        return self.transport.send_email(recipient, subject, body)

    def send_sms(self, phone_number, message):
        return self.transport.send_sms(phone_number, message)
