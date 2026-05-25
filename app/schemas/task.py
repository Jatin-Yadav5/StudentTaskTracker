"""API schemas for task endpoints (JSON request/response bodies)."""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Data required to create a new task via the API."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None


class Task(BaseModel):
    """Task returned by the API."""

    id: int
    title: str
    description: str | None = None
    completed: bool = False
