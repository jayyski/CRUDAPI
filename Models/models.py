from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=16)