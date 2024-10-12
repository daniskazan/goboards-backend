import os


class DBConfig:
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: int = os.environ.get("DB_PORT", "5432")
    DB_USER: str = os.environ.get("DB_USER", "goboards")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "goboards")
    DB_NAME: str = os.environ.get("DB_NAME", "goboards")
    DB_URL: str = os.environ.get(
        "DB_URL",
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )

    def __str__(self):
        return f"<{self.__class__.__name__}: URL - {self.DB_URL}>"
