from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/health.db"
    secret_key: str
    access_token_expire_minutes: int = 60
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    @property
    def resolved_database_url(self) -> str:
        if self.database_url.startswith("sqlite:///./"):
            return "sqlite:///" + str(BASE_DIR / self.database_url.removeprefix("sqlite:///./"))
        return self.database_url

settings = Settings()
