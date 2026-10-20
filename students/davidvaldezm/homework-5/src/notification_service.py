"""External notification boundary used by TaskService."""

from __future__ import annotations

from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def send_email(
        self, recipient: str, subject: str, body: str
    ) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def send_sms(self, phone_number: str, message: str) -> None:  # pragma: no cover
        raise NotImplementedError
