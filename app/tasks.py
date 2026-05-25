from fastapi import HTTPException

from app import data
from app.models import Task, TaskCreate


def get_all_tasks() -> list[Task]:
    return list(data.tasks)


def add_task(payload: TaskCreate) -> Task:
    task = Task(
        id=data.next_id,
        title=payload.title,
        description=payload.description,
    )
    data.tasks.append(task)
    data.next_id += 1
    return task


def delete_task(task_id: int) -> None:
    for index, task in enumerate(data.tasks):
        if task.id == task_id:
            data.tasks.pop(index)
            return
    raise HTTPException(status_code=404, detail="Task not found")


def mark_task_completed(task_id: int) -> Task:
    for index, task in enumerate(data.tasks):
        if task.id == task_id:
            updated = task.model_copy(update={"completed": True})
            data.tasks[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Task not found")
