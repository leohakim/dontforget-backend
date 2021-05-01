from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    is_active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "is_active": True,
            }
        }
