"""Routes for HTML pages (home)."""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.routes import html_pages

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home():
    """Landing page."""
    return html_pages.render_home()
