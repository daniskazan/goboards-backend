import os
from typing import Final

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    VK_CLIENT_ID: int = os.environ.get("VK_CLIENT_ID", 7879893)
    VK_SECRET_KEY: str = os.environ.get("VK_SECRET_KEY", "KqosMtfIWJMsgAN8SNVd")
    VK_SERVICE_KEY: str = os.environ.get(
        "VK_SERVICE_KEY",
        "94668a1094668a1094668a10d8941eb6c59946694668a10f1772df7f16585e30db1fd58",
    )

    VK_AUTHORIZE_URL: str = os.environ.get("VK_AUTHORIZE_URL", "https://oauth.vk.com/authorize/?")
    VK_ACCESS_TOKEN_URL: str = os.environ.get("VK_ACCESS_TOKEN_URL", "https://oauth.vk.com/access_token/")
    VK_REDIRECT_URI: str = os.environ.get("VK_REDIRECT_URI", "http://127.0.0.1:8000/api/v1/oauth/vk/callback")
    VK_RESPONSE_TYPE: Final = os.environ.get("VK_RESPONSE_TYPE", "code")
    VK_API_VERSION: str = os.environ.get("VK_API_VERSION", "5.199")
    VK_PROFILE_URL: str = os.environ.get("VK_PROFILE_URL", "https://api.vk.com/method/users.get")


oauth = Settings()
