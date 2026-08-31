from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    level: str | None = None
    preferred_language: str | None = None
    learning_goal: str | None = None


class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True