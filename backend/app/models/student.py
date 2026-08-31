from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    level = Column(String(50))
    preferred_language = Column(String(50))
    learning_goal = Column(String(100))
    created_at = Column(
        DateTime,
        server_default=func.now()
    )