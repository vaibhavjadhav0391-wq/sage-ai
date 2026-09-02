from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class StudentConcept(Base):
    __tablename__ = "student_concepts"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False
    )

    concept_id = Column(
        Integer,
        ForeignKey("concepts.id", ondelete="CASCADE"),
        nullable=False
    )

    mastery_score = Column(Float, default=0.0)
    attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)

    student = relationship("Student")
    concept = relationship("Concept")