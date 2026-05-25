"""Data access layer (storage)."""

from app.database.memory_store import task_store

__all__ = ["task_store"]
