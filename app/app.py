from fastapi import FastAPI
from app.server.routes.task import router as TaskRouter

app = FastAPI()

app.include_router(TaskRouter, tags=["Tasks"], prefix="/task")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Async To-Do List"}
