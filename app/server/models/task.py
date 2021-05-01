""" Task Pydantic Model """
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class TaskModel(BaseModel):
    name: str = Field(...)
    timestamp: datetime = Field(default=datetime.now())
    completed: bool = False
    completed_at: datetime = Field(default=None)
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "My important task",
                "datetime": "2021-04-03T11:21:29:64129",
                "completed": False,
            }
        }

class UpdateTaskModel(BaseModel):
    name: Optional[str]
    completed: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "My important task",
                "datetime": "2021-04-03T11:21:29:64129",
                "completed": False,
            }
        }