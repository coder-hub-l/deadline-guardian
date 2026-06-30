from datetime import datetime
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str
    deadline: datetime
    estimated_hours: float = Field(..., gt=0)
    priority: int = Field(..., ge=1, le=5)


class TaskResponse(TaskCreate):
    id: str