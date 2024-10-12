import os

from configs.database import DBConfig
from configs.jwt import JWTConfig


class ServerConfig(
    DBConfig,
    JWTConfig,
):
    APP_HOST: str = os.environ.get("APP_HOST", "127.0.0.1")
    APP_PORT: int = os.environ.get("APP_PORT", 8000)
    APP_WORKERS_COUNT: int = os.environ.get("WORKERS", 1)
    DEBUG: bool = os.environ.get("DEBUG", True)
