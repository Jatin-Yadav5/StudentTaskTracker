"""Task domain model used inside the application (not sent directly over HTTP)."""

from dataclasses import dataclass


@dataclass
class Task:
    """A student task stored in the application."""

    id: int
    title: str
    description: str | None = None
    completed: bool = False
