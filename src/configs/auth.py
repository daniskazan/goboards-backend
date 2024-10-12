import os


class AuthConfig:
    # 30 min in secs
    ACCESS_TOKEN_TTL: int = os.environ.get("ACCESS_TOKEN_TTL", 60 * 30)
    # 30 days in secs
    REFRESH_TOKEN_TTL: int = os.environ.get("REFRESH_TOKEN_TTL", 60 * 60 * 24 * 30)


auth = AuthConfig()
