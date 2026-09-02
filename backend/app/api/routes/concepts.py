from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.concept import Concept
from app.schemas.concept import ConceptCreate, ConceptResponse


router = APIRouter(
    prefix="/api/concepts",
    tags=["Concepts"]
)


@router.post("", response_model=ConceptResponse)
def create_concept(
    concept: ConceptCreate,
    db: Session = Depends(get_db)
):
    new_concept = Concept(
        name=concept.name,
        subject=concept.subject,
        description=concept.description,
        difficulty=concept.difficulty
    )

    db.add(new_concept)
    db.commit()
    db.refresh(new_concept)

    return new_concept