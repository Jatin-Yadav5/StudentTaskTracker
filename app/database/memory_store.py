"""
In-memory task storage.

This layer only reads and writes data. It does not know about HTTP or business rules.
"""

from app.models.task import Task


class MemoryTaskStore:
    """Simple list-based store for tasks (data is lost when the server stops)."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def list_all(self) -> list[Task]:
        """Return a copy of all tasks."""
        return list(self._tasks)

    def allocate_id(self) -> int:
        """Return the next task id and increment the counter."""
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def add(self, task: Task) -> Task:
        """Save a new task and return it."""
        self._tasks.append(task)
        return task

    def find_index(self, task_id: int) -> int | None:
        """Return list index for a task id, or None if not found."""
        for index, task in enumerate(self._tasks):
            if task.id == task_id:
                return index
        return None

    def delete_at(self, index: int) -> None:
        """Remove the task at the given index."""
        self._tasks.pop(index)

    def replace_at(self, index: int, task: Task) -> None:
        """Replace the task at the given index."""
        self._tasks[index] = task


# Single shared store for the whole app (prototype style).
task_store = MemoryTaskStore()
