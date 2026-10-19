class NotificationService:
    def send_email(self, recipient, subject, body): raise NotImplementedError()
    def send_sms(self, phone_number, message): raise NotImplementedError()