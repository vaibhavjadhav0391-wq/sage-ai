from fastapi import FastAPI

from app.api.routes.students import router as students_router


app = FastAPI(
    title="SAGE AI Teacher",
    description="Adaptive AI Teacher API",
    version="1.0.0"
)


app.include_router(students_router)


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