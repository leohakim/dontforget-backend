from pydantic import BaseSettings

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


class CommonSettings(BaseSettings):
    PROJECT_NAME: str = "Don't Forget!"
    APP_NAME: str = "Dontforget Backend"
    DEBUG_MODE: bool = config("DEBUG_MODE", cast=bool)
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = config("SECRET_KEY", cast=Secret, default="CHANGEME")
    TIMEZONE: str = config("TIMEZONE", default="CET")


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    MONGODB_URL: str = config("MONGODB_URL", cast=str)
    MONGODB_NAME: str = config("MONGODB_NAME", cast=str)


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
