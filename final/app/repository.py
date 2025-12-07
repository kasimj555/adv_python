from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Student

class StudentRepository:
    """Репозиторий для студентов"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, score: float, group: Optional[str] = None) -> Student:
        s = Student(name=name, score=score, group=group)
        self.session.add(s)
        self.session.commit()
        self.session.refresh(s)
        return s

    def get(self, student_id: int) -> Optional[Student]:
        return self.session.query(Student).filter(Student.id == student_id).first()

    def list(self) -> List[Student]:
        return self.session.query(Student).all()

    def update_score(self, student_id: int, new_score: float) -> Optional[Student]:
        s = self.get(student_id)
        if not s:
            return None
        s.score = new_score
        self.session.commit()
        self.session.refresh(s)
        return s

    def delete(self, student_id: int) -> bool:
        s = self.get(student_id)
        if not s:
            return False
        self.session.delete(s)
        self.session.commit()
        return True