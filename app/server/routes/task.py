from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_task,
    delete_task,
    retrieve_task,
    retrieve_tasks,
    update_task,
    complete_task,
    uncomplete_task,
)
from app.server.models.task import TaskModel, UpdateTaskModel
from app.server.models.response import ResponseModel
from app.server.models.errorresponse import ErrorResponseModel

router = APIRouter()


@router.post("/", response_description="Task added into the database")
async def add_task_(task: TaskModel = Body(...)):
    task = jsonable_encoder(task)
    new_task = await add_task(task)
    return ResponseModel(new_task, "Task added successfully.")


@router.get("/", response_description="Tasks retrieved")
async def retrieve_tasks_():
    tasks = await retrieve_tasks()
    if tasks:
        return ResponseModel(tasks, "Tasks retrieved successfully")
    return ResponseModel(tasks, "Empty list returned")


@router.get("/{id}", response_description="Get a single task")
async def retrieve_task_(id: str):
    task = await retrieve_task(id)
    if task:
        return ResponseModel(task, "Task retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Task doesn't exist.")


@router.delete("/{id}", response_description="Task deleted")
async def delete_task_(id: str):
    deleted_task = await delete_task(id)
    if deleted_task:
        return ResponseModel(
            "Task with ID: {} removed".format(id), "Task deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Task with id {0} doesn't exist".format(id)
    )


@router.patch("/{id}/complete", response_description="Task completed")
async def complete_task_(id: str):
    completed_task = await complete_task(id)
    if completed_task:
        task = await retrieve_task(id)
        return ResponseModel(
            task,
            "Task completed successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 400, "Task with id {0} is completed or doesn't exist".format(id)
    )


@router.patch("/{id}/uncomplete", response_description="Task uncompleted")
async def uncomplete_task_(id: str):
    completed_task = await uncomplete_task(id)
    if completed_task:
        task = await retrieve_task(id)
        return ResponseModel(
            task,
            "Task uncompleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 400, "Task with id {0} is uncompleted or doesn't exist".format(id)
    )


@router.put("/{id}")
async def update_task_(id: str, req: UpdateTaskModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_task = await update_task(id, req)
    if updated_task:
        task = await retrieve_task(id)
        return ResponseModel(task,
                             "Task with ID: {} update is successful".format(id))

    return ErrorResponseModel("An error occurred", 404, "There was an error updating the task.")
