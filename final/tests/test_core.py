import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.models import Student
from app.repository import StudentRepository

TEST_DB = "sqlite:///:memory:"

@pytest.fixture()
def session():
    engine = create_engine(TEST_DB)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    s = SessionLocal()
    yield s
    s.close()

def test_crud(session):
    repo = StudentRepository(session)
    st = repo.create("Alice", 88.5, "A")
    assert st.id is not None
    assert repo.get(st.id).name == "Alice"
    assert repo.update_score(st.id, 90.0).score == 90.0
    assert repo.delete(st.id) is True

def test_processors():
    from app.processors import AverageScoreProcessor, GroupFilterProcessor

    data = [{"name": "A", "score": 10}, {"name": "B", "score": 20}, {"name": "C", "score": 30}]
    avg = AverageScoreProcessor().process(data)
    assert pytest.approx(avg) == 20.0
    gf = GroupFilterProcessor("G")
    assert gf.process([{"name": "X", "score": 1, "group": "G"}]) == ["X"]