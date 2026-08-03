from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.auth.dependencies import get_current_user

from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services.task_service import (
    create_task as create_task_service,
    get_all_tasks as get_all_tasks_service,
    get_task as get_task_service,
    update_task as update_task_service,
    delete_task as delete_task_service,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", status_code=201)
async def create_task(
    task: TaskCreate,
    current_user=Depends(get_current_user)
):
    return await create_task_service(task, current_user)


@router.get("/")
async def fetch_tasks(current_user=Depends(get_current_user)):
    return await get_all_tasks_service(current_user)


@router.get("/{task_id}")
async def fetch_task(task_id: str, current_user=Depends(get_current_user)):
    task = await get_task_service(task_id, current_user)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}")
async def edit_task(task_id: str, task: TaskUpdate, current_user=Depends(get_current_user)):
    updated_task = await update_task_service(task_id, task, current_user)

    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task


@router.delete("/{task_id}")
async def remove_task(task_id: str, current_user=Depends(get_current_user)):
    deleted = await delete_task_service(task_id, current_user)

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }