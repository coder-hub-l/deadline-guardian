from fastapi import APIRouter

from app.ai.gemini_service import analyze_task
from app.schemas.task_schema import TaskCreate

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/test")
async def test_ai(task: TaskCreate):
    return await analyze_task(task)