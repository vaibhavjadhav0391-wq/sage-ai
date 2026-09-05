from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import json

from app.core.database import get_db
from app.models.interaction import Interaction
from app.models.student_concept import StudentConcept
from app.models.lesson import Lesson
from app.models.concept import Concept
from app.schemas.interaction import InteractionCreate, InteractionResponse
from app.services.gemini_service import analyze_answer


router = APIRouter(
    prefix="/api/interactions",
    tags=["Interactions"]
)


@router.post(
    "",
    response_model=InteractionResponse
)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):

    # 1. Find the lesson
    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == interaction.lesson_id)
        .first()
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    # 2. Find the concept
    concept = (
        db.query(Concept)
        .filter(Concept.name == interaction.concept)
        .first()
    )

    if concept is None:
        raise HTTPException(
            status_code=404,
            detail="Concept not found"
        )

    # 3. Find student's mastery record
    student_concept = (
        db.query(StudentConcept)
        .filter(
            StudentConcept.student_id == lesson.student_id,
            StudentConcept.concept_id == concept.id
        )
        .first()
    )

    if student_concept is None:
        raise HTTPException(
            status_code=404,
            detail="Student is not connected to this concept"
        )

    # 4. Ask AI to analyze the answer
    try:
        ai_result = analyze_answer(
            concept=interaction.concept,
            question=interaction.question,
            student_answer=interaction.student_answer
        )
        ai_data = json.loads(ai_result)
    except Exception as e:
        print(f"[INTERACTION ERROR] AI analysis failed: {e}", flush=True)
        # Fallback if AI fails — don't crash the endpoint
        ai_data = {
            "correct": False,
            "misconception": None,
            "explanation": "SAGE could not analyze your answer right now. Please try again.",
            "teacher_action": "Try answering the question again."
        }

    # 5. Get AI analysis
    correct = ai_data.get(
        "correct",
        interaction.correct
    )

    misconception = ai_data.get(
        "misconception"
    )

    explanation = ai_data.get(
        "explanation"
    )

    teacher_action = ai_data.get(
        "teacher_action"
    )

    # 6. Save interaction
    new_interaction = Interaction(
        lesson_id=interaction.lesson_id,
        concept=interaction.concept,
        question=interaction.question,
        student_answer=interaction.student_answer,
        correct=correct,
        misconception=misconception,
        teacher_action=teacher_action
    )

    db.add(new_interaction)

    # 7. Update attempts
    student_concept.attempts += 1

    # 8. Update correct attempts
    if correct:
        student_concept.correct_attempts += 1

    # 9. Calculate mastery
    student_concept.mastery_score = (
        student_concept.correct_attempts
        / student_concept.attempts
    ) * 100

    # 10. Save changes
    db.commit()
    db.refresh(new_interaction)

# 11. Return AI feedback to frontend
    return {
    "id": new_interaction.id,
    "lesson_id": new_interaction.lesson_id,
    "concept": new_interaction.concept,
    "question": new_interaction.question,
    "student_answer": new_interaction.student_answer,
    "correct": new_interaction.correct,
    "misconception": new_interaction.misconception,
    "explanation": explanation,
    "teacher_action": new_interaction.teacher_action
}