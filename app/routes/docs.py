"""Routes for custom API documentation pages."""

from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.routes import html_pages

router = APIRouter(include_in_schema=False)


@router.get("/docs")
def swagger_docs(request: Request):
    """Swagger UI with app navigation."""
    response = get_swagger_ui_html(
        openapi_url=request.app.openapi_url,
        title=f"{request.app.title} — API Docs",
    )
    body = html_pages.inject_docs_nav(response.body.decode(), active="docs")
    return HTMLResponse(content=body)


@router.get("/redoc")
def redoc_docs(request: Request):
    """ReDoc with app navigation."""
    response = get_redoc_html(
        openapi_url=request.app.openapi_url,
        title=f"{request.app.title} — ReDoc",
    )
    body = html_pages.inject_docs_nav(response.body.decode(), active="redoc")
    return HTMLResponse(content=body)
