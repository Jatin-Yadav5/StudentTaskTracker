"""
Application entry point.

Creates the FastAPI app and registers route modules.
Run from the project root (see README).
"""

import sys
from pathlib import Path

# Put project root on sys.path so `app` is this package, not another app.py on the machine.
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from fastapi import FastAPI

from app.routes import docs, pages, tasks

app = FastAPI(
    title="Student Task Tracker",
    description=(
        "**App pages:** [Home](/) · [My Tasks](/tasks) · "
        "[API Docs](/docs) · [ReDoc](/redoc)"
    ),
    docs_url=None,
    redoc_url=None,
)

app.include_router(pages.router)
app.include_router(tasks.router)
app.include_router(docs.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
