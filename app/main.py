from fastapi import FastAPI
import uvicorn

from app.core.config import settings
from app.api.routes_students import router as students_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    app.include_router(students_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
