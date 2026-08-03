from bson import ObjectId
from app.models.task_model import task_collection
from app.schemas.task_schema import TaskCreate
from app.ai.gemini_service import analyze_task


async def create_task(task: TaskCreate,current_user):
    # Convert Pydantic model to dictionary
    task_dict = task.model_dump()

    # Analyze task using Gemini
    ai_result = await analyze_task(task)

    # Merge AI analysis into task
    task_dict["ai_priority"] = ai_result.get("priority_score")
    task_dict["urgency"] = ai_result.get("urgency")
    task_dict["complexity"] = ai_result.get("difficulty")
    task_dict["completion_probability"] = ai_result.get("completion_probability")
    task_dict["recommended_start"] = ai_result.get("recommended_start")
    task_dict["risk"] = ai_result.get("risk")
    task_dict["reason"] = ai_result.get("reason")

    # Store in MongoDB
    task_dict["user_id"] = str(current_user["_id"])

    result = await task_collection.insert_one(task_dict)

    task_dict["_id"] = str(result.inserted_id)
    return task_dict


async def get_all_tasks(current_user):
    """
    Fetch all tasks from MongoDB.
    """
    tasks = []

    async for task in task_collection.find( {
        "user_id": str(current_user["_id"])
    }):
        task["_id"] = str(task["_id"])
        tasks.append(task)

    return await tasks


async def get_task(task_id: str,current_user):
    """
    Fetch a single task by ID.
    """
    task = await task_collection.find_one(
    {
        "user_id": str(current_user["_id"])
    ,

        "_id": ObjectId(task_id)}
    )

    if task:
        task["_id"] = str(task["_id"])

    return await task


async def update_task(task_id: str, task: TaskCreate,current_user):
    """
    Update an existing task.
    """
    await task_collection.update_one(
        {"_id": ObjectId(task_id),
         "user_id": str(current_user["_id"])},
        {"$set": task.model_dump()}
    )

    updated_task = await task_collection.find_one(
        {   
            "_id": ObjectId(task_id),
            "user_id": str(current_user["_id"])
        }
    )

    if updated_task:
        updated_task["_id"] = str(updated_task.pop("_id"))

    return await updated_task


async def delete_task(task_id: str,current_user):
    """
    Delete a task.
    """
    result = await task_collection.delete_one(
        {
                "user_id": str(current_user["_id"]),
                "_id": ObjectId(task_id)}
    )

    return await result.deleted_count