"""
Task business logic.

Routes call these functions. This layer uses the database store and returns API schemas.
"""

from fastapi import HTTPException

from app.database.memory_store import task_store
from app.models.task import Task as TaskEntity
from app.schemas.task import Task, TaskCreate


def _to_schema(task: TaskEntity) -> Task:
    """Convert a domain task to an API response schema."""
    return Task(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
    )


def _require_index(task_id: int) -> int:
    """Find task index or raise 404 (business rule)."""
    index = task_store.find_index(task_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return index


def get_all_tasks() -> list[Task]:
    """Return every task as API schemas."""
    return [_to_schema(task) for task in task_store.list_all()]


def add_task(payload: TaskCreate) -> Task:
    """Create a new task from API input."""
    entity = TaskEntity(
        id=task_store.allocate_id(),
        title=payload.title,
        description=payload.description,
    )
    task_store.add(entity)
    return _to_schema(entity)


def delete_task(task_id: int) -> None:
    """Delete a task by id."""
    index = _require_index(task_id)
    task_store.delete_at(index)


def mark_task_completed(task_id: int) -> Task:
    """Mark a task as completed."""
    index = _require_index(task_id)
    current = task_store.list_all()[index]
    updated = TaskEntity(
        id=current.id,
        title=current.title,
        description=current.description,
        completed=True,
    )
    task_store.replace_at(index, updated)
    return _to_schema(updated)
