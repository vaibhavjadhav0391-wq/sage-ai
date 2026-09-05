from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func

from app.core.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id"),
        nullable=False
    )

    concept = Column(String(255))

    question = Column(Text)

    student_answer = Column(Text)

    correct = Column(Boolean)

    misconception = Column(Text)

    teacher_action = Column(Text)

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )