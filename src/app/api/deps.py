from fastapi import Header, HTTPException

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.config import settings


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin(x_api_key: str | None = Header(default=None)):
    if x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized (admin)")
    return True
