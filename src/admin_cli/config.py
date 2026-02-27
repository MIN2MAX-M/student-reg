import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Always load .env from repo root (../.env from this file)
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")


@dataclass(frozen=True)
class Settings:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str = field(repr=False)  # <-- hides password in print/repr
    db_sslmode: str = "prefer"


def load_settings() -> Settings:
    return Settings(
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=int(os.getenv("DB_PORT", "5432")),
        db_name=os.getenv("DB_NAME", "appdb"),
        db_user=os.getenv("DB_USER", "app_user"),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_sslmode=os.getenv("DB_SSLMODE", "prefer"),
    )
