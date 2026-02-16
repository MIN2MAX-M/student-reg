# app/api/routes_students.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.schemas.student import StudentCreate, StudentOut, StudentUpdate
from app.services import student_service

router = APIRouter(prefix="/students", tags=["students"])


def _norm_email(email: str) -> str:
    return email.strip().lower()


@router.post("", response_model=StudentOut, dependencies=[Depends(require_admin)])
def create(payload: StudentCreate, db: Session = Depends(get_db)):
    payload.email = _norm_email(payload.email)

    # Friendly pre-check (DB constraint is still source of truth)
    existing = student_service.get_student_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    try:
        return student_service.create_student(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")


@router.get("", response_model=list[StudentOut])
def list_(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    q: str | None = Query(
        default=None, description="Search query (name/email/phone/address)"
    ),
):
    if q:
        return student_service.search_students(db, q=q, limit=limit, offset=offset)
    return student_service.list_students(db, limit=limit, offset=offset)


@router.get("/{student_id}", response_model=StudentOut)
def get_one(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.patch(
    "/{student_id}", response_model=StudentOut, dependencies=[Depends(require_admin)]
)
def update(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = student_service.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # If email provided, normalize + check uniqueness up-front
    if payload.email is not None:
        payload.email = _norm_email(payload.email)

        # If same as current, no-op is fine (return current resource)
        if payload.email == student.email:
            return student

        other = student_service.get_student_by_email(db, payload.email)
        if other and other.id != student.id:
            raise HTTPException(status_code=409, detail="Email already exists")

    try:
        return student_service.update_student(db, student, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")


@router.delete("/{student_id}", dependencies=[Depends(require_admin)])
def delete(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_service.delete_student(db, student)
    return {"status": "deleted"}
