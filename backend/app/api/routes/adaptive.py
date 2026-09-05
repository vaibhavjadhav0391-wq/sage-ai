from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.student_concept import StudentConcept
from app.models.concept import Concept


router = APIRouter(
    prefix="/api/adaptive",
    tags=["Adaptive Learning"]
)


@router.get("/students/{student_id}/concepts/{concept_id}/next-question")
def get_next_question(
    student_id: int,
    concept_id: int,
    db: Session = Depends(get_db)
):
    student_concept = (
        db.query(StudentConcept)
        .filter(
            StudentConcept.student_id == student_id,
            StudentConcept.concept_id == concept_id
        )
        .first()
    )

    if student_concept is None:
        raise HTTPException(
            status_code=404,
            detail="Student is not connected to this concept"
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

    mastery = student_concept.mastery_score
    attempts = student_concept.attempts

    # Determine difficulty from mastery
    if mastery <= 40:
        difficulty = "easy"

        questions = [
            "What is an array in Java?",
            "How do you declare an integer array in Java?",
            "How do you access an element of an array in Java?"
        ]

    elif mastery <= 70:
        difficulty = "medium"

        questions = [
            "How do you access the third element of an array in Java?",
            "What happens if you try to access an array index outside its valid range?",
            "How would you calculate the sum of all elements in an integer array?"
        ]

    else:
        difficulty = "hard"

        questions = [
            "How would you find the largest element in an integer array in Java?",
            "How would you find the second largest element in an integer array?",
            "How would you remove duplicate values from an integer array?"
        ]

    # Rotate through the questions
    question_index = attempts % len(questions)
    question = questions[question_index]

    return {
        "student_id": student_id,
        "concept_id": concept_id,
        "concept": concept.name,
        "mastery_score": round(mastery, 2),
        "next_difficulty": difficulty,
        "question": question
    }