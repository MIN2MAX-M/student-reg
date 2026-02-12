# app/services/student_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


def create_student(db: Session, payload: StudentCreate) -> Student:
    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_student(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def get_student_by_email(db: Session, email: str) -> Student | None:
    stmt = select(Student).where(Student.email == email)
    return db.execute(stmt).scalars().first()


def list_students(db: Session, limit: int = 50, offset: int = 0) -> list[Student]:
    stmt = select(Student).order_by(Student.id.desc()).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())


def search_students(db: Session, q: str, limit: int = 50, offset: int = 0) -> list[Student]:
    like = f"%{q.strip()}%"
    stmt = (
        select(Student)
        .where(
            or_(
                Student.first_name.ilike(like),
                Student.last_name.ilike(like),
                Student.email.ilike(like),
                Student.phone.ilike(like),
                Student.address.ilike(like),
            )
        )
        .order_by(Student.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.execute(stmt).scalars().all())


def update_student(db: Session, student: Student, payload: StudentUpdate) -> Student:
    data = payload.model_dump(exclude_unset=True)

    # If payload had only unknown fields or empty JSON, nothing to do
    if not data:
        return student

    # Explicitly set allowed fields
    for field in ("first_name", "last_name", "email", "phone", "age", "address"):
        if field in data:
            setattr(student, field, data[field])

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Student) -> None:
    db.delete(student)
    db.commit()
