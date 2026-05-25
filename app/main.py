import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from fastapi import FastAPI, Form, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse, RedirectResponse

from app.models import Task, TaskCreate
from app import tasks as task_service
from app import pages

app = FastAPI(
    title="Student Task Tracker",
    description=(
        "**App pages:** [Home](/) · [My Tasks](/tasks) · "
        "[API Docs](/docs) · [ReDoc](/redoc)"
    ),
    docs_url=None,
    redoc_url=None,
)


@app.get("/docs", include_in_schema=False)
def swagger_docs():
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} — API Docs",
    )
    body = pages.inject_docs_nav(response.body.decode(), active="docs")
    return HTMLResponse(content=body)


@app.get("/redoc", include_in_schema=False)
def redoc_docs():
    response = get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} — ReDoc",
    )
    body = pages.inject_docs_nav(response.body.decode(), active="redoc")
    return HTMLResponse(content=body)


def _wants_html(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "text/html" in accept and "application/json" not in accept.split(",")[0].strip()


@app.get("/", response_class=HTMLResponse)
def home():
    return pages.render_home()


@app.get("/tasks")
def list_tasks(request: Request, msg: str | None = None):
    tasks = task_service.get_all_tasks()
    if _wants_html(request):
        return HTMLResponse(pages.render_tasks_page(tasks, message=msg))
    return tasks


@app.post("/tasks/create")
def create_task_form(
    title: str = Form(...),
    description: str | None = Form(None),
):
    desc = description.strip() if description and description.strip() else None
    task_service.add_task(TaskCreate(title=title.strip(), description=desc))
    return RedirectResponse(url="/tasks?msg=Task+added", status_code=303)


@app.post("/tasks/{task_id}/complete")
def complete_task_form(task_id: int):
    task_service.mark_task_completed(task_id)
    return RedirectResponse(url="/tasks?msg=Task+marked+complete", status_code=303)


@app.post("/tasks/{task_id}/delete")
def delete_task_form(task_id: int):
    task_service.delete_task(task_id)
    return RedirectResponse(url="/tasks?msg=Task+deleted", status_code=303)


@app.post("/tasks", response_model=Task, status_code=201)
def create_task_api(payload: TaskCreate):
    return task_service.add_task(payload)


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task_api(task_id: int):
    task_service.delete_task(task_id)


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task_api(task_id: int):
    return task_service.mark_task_completed(task_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
