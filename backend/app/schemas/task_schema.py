from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class TaskStatus(str, Enum):
    pending =  "pending"
    in_progress = "in_progress"
    completed = "completed"



class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str
    deadline: datetime
    estimated_hours: float = Field(..., gt=0)
    priority: int = Field(..., ge=1, le=5)


class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str
    deadline: datetime
    estimated_hours: float = Field(..., gt=0)
    priority: int = Field(..., ge=1, le=5)
    status: str = "pending"

class TaskResponse(TaskCreate):
    id: str
    title: str = Field(..., min_length=3, max_length=100)
    description: str
    deadline: datetime
    estimated_hours: float = Field(..., gt=0)
    priority: int = Field(..., ge=1, le=5)
    status : TaskStatus
    user_id : str
    created_at : datetime
    completes_at : datetime| None=None

    ai_priority : int | None=None
    urgency : str | None=None
    complexity : str | None=None
    completion_probability : int | None=None
    recomended_start : str | None=None
    risk : str | None=None
    reason : str | None=None
