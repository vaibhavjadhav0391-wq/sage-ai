from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func

from app.core.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    topic = Column(String(255), nullable=False)

    level = Column(String(50))

    language = Column(String(50))

    duration_minutes = Column(Integer)

    learning_goal = Column(String(255))

    status = Column(String(50))

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )