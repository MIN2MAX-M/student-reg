from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.student import StudentCreate, StudentOut
from app.services import student_service

router = APIRouter(prefix="/public", tags=["public"])


@router.post(
    "/register", response_model=StudentOut, status_code=status.HTTP_201_CREATED
)
def register_student(payload: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, payload)
