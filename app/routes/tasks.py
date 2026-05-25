"""Routes for task API and HTML forms."""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.routes import html_pages
from app.schemas.task import Task, TaskCreate
from app.services import task_service

router = APIRouter()


def _wants_html(request: Request) -> bool:
    """True when the client prefers an HTML page over JSON."""
    accept = request.headers.get("accept", "")
    return "text/html" in accept and "application/json" not in accept.split(",")[0].strip()


@router.get("/tasks")
def list_tasks(request: Request, msg: str | None = None):
    """List tasks as JSON (API) or HTML (browser)."""
    tasks = task_service.get_all_tasks()
    if _wants_html(request):
        return HTMLResponse(html_pages.render_tasks_page(tasks, message=msg))
    return tasks


@router.post("/tasks/create")
def create_task_form(
    title: str = Form(...),
    description: str | None = Form(None),
):
    """Add a task from the HTML form."""
    desc = description.strip() if description and description.strip() else None
    task_service.add_task(TaskCreate(title=title.strip(), description=desc))
    return RedirectResponse(url="/tasks?msg=Task+added", status_code=303)


@router.post("/tasks/{task_id}/complete")
def complete_task_form(task_id: int):
    """Mark complete from the HTML form."""
    task_service.mark_task_completed(task_id)
    return RedirectResponse(url="/tasks?msg=Task+marked+complete", status_code=303)


@router.post("/tasks/{task_id}/delete")
def delete_task_form(task_id: int):
    """Delete from the HTML form."""
    task_service.delete_task(task_id)
    return RedirectResponse(url="/tasks?msg=Task+deleted", status_code=303)


@router.post("/tasks", response_model=Task, status_code=201)
def create_task_api(payload: TaskCreate):
    """Create a task via JSON API."""
    return task_service.add_task(payload)


@router.delete("/tasks/{task_id}", status_code=204)
def remove_task_api(task_id: int):
    """Delete a task via JSON API."""
    task_service.delete_task(task_id)


@router.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task_api(task_id: int):
    """Mark a task complete via JSON API."""
    return task_service.mark_task_completed(task_id)
