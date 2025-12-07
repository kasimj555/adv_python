from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import csv
from io import StringIO
import logging

from .db import Base, engine, get_session
from .models import Student
from .repository import StudentRepository
from .processors import AverageScoreProcessor, GroupFilterProcessor, apply_processor, AutoRegisterMeta
from .analytics import time_compare, student_generator, profile_function
from .utils import setup_logging, timing

Base.metadata.create_all(bind=engine)

setup_logging()
logger = logging.getLogger("smart-data-analyzer")

app = FastAPI(title="Smart Data Analyzer")

class StudentIn(BaseModel):
    name: str
    score: float
    group: str = None


class StatsOut(BaseModel):
    average_score: float


def get_repo():
    with get_session() as session:
        yield StudentRepository(session)


@app.post("/students/", response_model=dict)
def create_student(s: StudentIn, repo: StudentRepository = Depends(get_repo)):
    created = repo.create(name=s.name, score=s.score, group=s.group)
    return {"id": created.id, "name": created.name}


@app.get("/students/", response_model=List[dict])
def list_students(repo: StudentRepository = Depends(get_repo)):
    res = repo.list()
    return [{"id": r.id, "name": r.name, "score": r.score, "group": r.group} for r in res]


@app.get("/students/{student_id}")
def get_student(student_id: int, repo: StudentRepository = Depends(get_repo)):
    s = repo.get(student_id)
    if not s:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": s.id, "name": s.name, "score": s.score}


@app.delete("/students/{student_id}")
def delete_student(student_id: int, repo: StudentRepository = Depends(get_repo)):
    ok = repo.delete(student_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return JSONResponse({"status": "deleted"})


@app.post("/upload_csv/")
def upload_csv(content: str, repo: StudentRepository = Depends(get_repo)):
    """Ожидает CSV в виде строки"""
    f = StringIO(content)
    reader = csv.DictReader(f, fieldnames=["name", "score", "group"])
    created = []
    # Не хочет читать несколько строк (исправить)
    for row in reader:
        try:
            created.append(repo.create(name=row["name"], score=float(row["score"]), group=row.get("group")))
        except Exception as e:
            logger.exception("Error creating student: %s", e)
    return {"created": len(created)}


@app.get("/stats/average", response_model=StatsOut)
def average_score(repo: StudentRepository = Depends(get_repo)):
    rows = repo.list()
    avg = AverageScoreProcessor().process([{"score": r.score} for r in rows])
    return {"average_score": avg}


@app.get("/processors/registry")
def processors_registry():
    """Возвращает автоматически зарегистрированные процессоры"""
    return {k: v.__name__ for k, v in AutoRegisterMeta.registry.items()}


@app.get("/benchmark")
def benchmark(repo: StudentRepository = Depends(get_repo)):
    rows = repo.list()

    def use_list():
        return [r.score for r in rows]

    def use_generator():
        return [r for r in (x for x in (s.score for s in rows))]

    results = time_compare({"list": use_list, "generator": use_generator}, number=1000)
    return results


if __name__ == "__main__":
    print("Run uvicorn - app.main:app --reload")