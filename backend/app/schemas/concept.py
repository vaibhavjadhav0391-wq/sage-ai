from pydantic import BaseModel


class ConceptCreate(BaseModel):
    name: str
    subject: str
    description: str | None = None
    difficulty: str | None = None


class ConceptResponse(BaseModel):
    id: int
    name: str
    subject: str
    description: str | None = None
    difficulty: str | None = None

    class Config:
        from_attributes = True