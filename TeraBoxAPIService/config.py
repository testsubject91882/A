
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os


class Settings(BaseSettings):
    BOT_TOKEN: str
    API_ID: int
    API_HASH: str
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "terabox_service"
    ADMIN_IDS: List[int] = []
    TERA_BASE_API: str = "https://teraapi.boogafantastic.workers.dev"

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: Union[str, int, List[int]]) -> List[int]:
        if isinstance(v, list):
            return v
        if isinstance(v, int):
            return [v]
        if isinstance(v, str):
            if not v.strip():
                return []
            # handle comma-separated string
            return [int(x.strip()) for x in v.split(",") if x.strip().isdigit()]
        return []


settings = Settings()
