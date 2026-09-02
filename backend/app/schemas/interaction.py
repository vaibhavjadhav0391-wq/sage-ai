from pydantic import BaseModel


class InteractionCreate(BaseModel):
    lesson_id: int
    concept: str
    question: str
    student_answer: str
    correct: bool
    misconception: str | None = None
    teacher_action: str | None = None


class InteractionResponse(BaseModel):
    id: int
    lesson_id: int
    concept: str
    question: str
    student_answer: str
    correct: bool
    misconception: str | None = None
    teacher_action: str | None = None

    class Config:
        from_attributes = True