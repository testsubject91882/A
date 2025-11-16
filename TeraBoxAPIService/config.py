from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Telegram bot credentials
    BOT_TOKEN: str
    API_ID: int
    API_HASH: str

    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "terabox_service"

    # Admins (comma separated ids)
    ADMIN_IDS: List[int] = []

    # Base parsing API
    TERA_BASE_API: str = "https://teraapi.boogafantastic.workers.dev"

    class Config:
        env_file = ".env"


settings = Settings()
