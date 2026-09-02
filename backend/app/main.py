from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.student import Student
from app.models.concept import Concept
from app.api.routes.concepts import router as concepts_router
from app.api.routes.students import router as students_router
from app.api.routes.student_concepts import router as student_concepts_router
from app.models.interaction import Interaction
from app.api.routes.interactions import router as interactions_router
from app.models.lesson import Lesson

app = FastAPI(
    title="SAGE AI Teacher",
    description="Adaptive AI Teacher API",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

app.include_router(students_router)
app.include_router(concepts_router)
app.include_router(student_concepts_router)
app.include_router(interactions_router)

@app.get("/")
def root():
    return {
        "message": "SAGE AI Teacher API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }