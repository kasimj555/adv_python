from sqlalchemy import Column, Integer, String, Float
from .db import Base

class Student(Base):
    """Простая модель студента"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    group = Column(String, nullable=True)
    score = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Student id={self.id} name={self.name!r} score={self.score}>"