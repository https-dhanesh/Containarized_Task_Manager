from pydantic import BaseModel

class TaskCreate(BaseModel):
    content: str

class Task(BaseModel):
    id: int
    content: str
    status: str

    class Config:
        from_attributes = True