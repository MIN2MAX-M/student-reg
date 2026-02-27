from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "student-reg"
    ENV: str = "dev"

    DATABASE_URL: str
    ADMIN_API_KEY: str = "change-me"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ✅ Ignore env vars that aren't defined in this Settings model
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
