from fastapi import APIRouter, HTTPException

from app.schemas.task_schema import TaskCreate
from app.services.task_service import (
    create_task,
    get_all_tasks,
    get_task,
    update_task,
    delete_task
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/")
async def add_task(task: TaskCreate):
    return await create_task(task)


@router.get("/")
async def fetch_tasks():
    return await get_all_tasks()


@router.get("/{task_id}")
async def fetch_task(task_id: str):
    task = await get_task(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}")
async def edit_task(task_id: str, task: TaskCreate):
    updated_task = await update_task(task_id, task)

    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task


@router.delete("/{task_id}")
async def remove_task(task_id: str):
    deleted = await delete_task(task_id)

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }