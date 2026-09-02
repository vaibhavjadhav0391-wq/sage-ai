from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.student import Student
from app.models.concept import Concept
from app.models.student_concept import StudentConcept


router = APIRouter(
    prefix="/api/students",
    tags=["Student Concepts"]
)


@router.post("/{student_id}/concepts/{concept_id}")
def connect_student_concept(
    student_id: int,
    concept_id: int,
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

    concept = (
        db.query(Concept)
        .filter(Concept.id == concept_id)
        .first()
    )

    if concept is None:
        raise HTTPException(
            status_code=404,
            detail="Concept not found"
        )

    existing = (
        db.query(StudentConcept)
        .filter(
            StudentConcept.student_id == student_id,
            StudentConcept.concept_id == concept_id
        )
        .first()
    )

    if existing:
        return {
            "message": "Student is already connected to this concept",
            "student_id": student_id,
            "concept_id": concept_id
        }

    student_concept = StudentConcept(
        student_id=student_id,
        concept_id=concept_id,
        mastery_score=0.0,
        attempts=0,
        correct_attempts=0
    )

    db.add(student_concept)
    db.commit()
    db.refresh(student_concept)

    return {
        "message": "Student connected to concept successfully",
        "student_id": student_id,
        "concept_id": concept_id,
        "mastery_score": student_concept.mastery_score,
        "attempts": student_concept.attempts,
        "correct_attempts": student_concept.correct_attempts
    }