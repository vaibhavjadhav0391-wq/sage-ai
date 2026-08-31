from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse


router = APIRouter(
    prefix="/api/students",
    tags=["Students"]
)


@router.post(
    "",
    response_model=StudentResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = Student(
        name=student.name,
        level=student.level,
        preferred_language=student.preferred_language,
        learning_goal=student.learning_goal
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student