from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes_public import router as public_router

from app.api.routes_students import router as students_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # API routes
    app.include_router(students_router)
    app.include_router(public_router)

    # Static GUI (end-user registration page)
    base_dir = Path(__file__).resolve().parent
    static_dir = base_dir / "static"
    static_dir.mkdir(parents=True, exist_ok=True)  # ensures folder exists

    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/", include_in_schema=False)
    def home():
        return FileResponse(str(static_dir / "index.html"))

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
