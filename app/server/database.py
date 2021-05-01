""" Persistence Classes and methods """
from app.config import settings
import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
database = client.dontforget
task_collection = database.get_collection('dontforget')


# helpers

def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "name": task["name"],
        "timestamp": task["timestamp"],
        "completed": task["completed"],
    }


###  CRUD

# Retrieve all tasks present in the database
# TODO: Filter by user (Token JWT)
async def retrieve_tasks():
    tasks = []
    async for task in task_collection.find({"is_active": True}):
        tasks.append(task_helper(task))
    return tasks


# Add a new task into to the database
async def add_task(task_data: dict) -> dict:
    task = await task_collection.insert_one(task_data)
    new_task = await task_collection.find_one({"_id": task.inserted_id})
    return task_helper(new_task)


# Retrieve a task with a matching ID
async def retrieve_task(id: str) -> dict:
    task = await task_collection.find_one({"_id": ObjectId(id), "is_active": True})
    if task:
        return task_helper(task)


# Update a task with a matching ID
async def update_task(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    task = await task_collection.find_one({"_id": ObjectId(id), "is_active": True})
    if task:
        updated_task = await task_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_task:
            return True
    return False


# Delete a task from the database
async def delete_task(id: str):
    task = await task_collection.find_one({"_id": ObjectId(id)})

    if task:
        task['is_active'] = False
        updated_task = await task_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": task}
        )
        if updated_task:
            return True
        return False


# Mark a task as completed in the database
async def complete_task(id: str):
    task = await task_collection.find_one({"_id": ObjectId(id)})

    if not task['completed']:
        task['completed'] = True
        task['completed_at'] = datetime.now()
        updated_task = await task_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": task}
        )
        if updated_task:
            return True
    return False


# Mark a task as uncompleted in the database
async def uncomplete_task(id: str):
    task = await task_collection.find_one({"_id": ObjectId(id)})

    if task['completed']:
        task['completed'] = False
        task['completed_at'] = None
        updated_task = await task_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": task}
        )
        if updated_task:
            return True
    return False
