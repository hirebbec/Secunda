import functools
from datetime import timedelta, timezone
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    root_dir: Path = Path(__file__).resolve().parent.parent.parent
    src_dir: Path = root_dir.joinpath("src")
    env_file: Path = src_dir.joinpath(".env.local")

    PROJECT_NAME: str = "secunda"

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8888
    SERVER_WORKERS_COUNT: int = 1

    MAX_ACTIVITY_DEPTH: int = 3

    ENVIRONMENT: str = "local"
    TIME_ZONE: timezone = timezone(offset=timedelta(hours=+3))
    CORS_ALLOW_ORIGIN_LIST: str = "*"

    USE_CORS_MIDDLEWARE: bool = True
    USE_TIMER_MIDDLEWARE: bool = False

    POSTGRES_HOST: str = "secunda-db"
    POSTGRES_PORT: int = 5932
    POSTGRES_USER: str = "secunda-db"
    POSTGRES_PASSWORD: str = "secunda-db"
    POSTGRES_DB: str = "secunda-db"

    READONLY_USER: str = "readonly_user"
    READONLY_PASSWORD: str = "readonly_user"

    @functools.cached_property
    def cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGIN_LIST.split("&")

    @functools.cached_property
    def postgres_dsn(self) -> str:
        postgres_host = "localhost" if self.ENVIRONMENT == "local" else self.POSTGRES_HOST
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{postgres_host}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=env_file if env_file else None,
        env_file_encoding="utf-8",
        extra="allow",
    )


@functools.lru_cache()
def settings() -> Settings:
    return Settings()
