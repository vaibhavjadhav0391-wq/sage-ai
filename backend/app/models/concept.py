from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)
    description = Column(Text)
    difficulty = Column(String(50))