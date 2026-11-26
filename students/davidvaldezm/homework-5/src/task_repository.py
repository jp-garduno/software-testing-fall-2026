"""Repository boundary used by TaskService.

Real persistence is intentionally outside this exercise.  Tests use a mock at
this boundary so no database or filesystem is required.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .task import Task


class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:  # pragma: no cover - interface contract
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, task_id: int) -> Task | None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def find_by_title(self, title: str) -> Task | None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[Task]:  # pragma: no cover
        raise NotImplementedError
