from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from TeraBoxAPIService.config import settings


class Database:
    def __init__(self, uri: str = None, db_name: str = None):
        self._uri = uri or settings.MONGO_URI
        self._db_name = db_name or settings.MONGO_DB
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None

    def connect(self):
        self.client = AsyncIOMotorClient(self._uri)
        self.db = self.client[self._db_name]

    def close(self):
        if self.client:
            self.client.close()

    # Users collection helpers
    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        return await self.db.users.find_one({"user_id": user_id})

    async def create_user_if_missing(self, user_id: int) -> Dict[str, Any]:
        user = await self.get_user(user_id)
        if user:
            return user
        # create a placeholder user doc
        doc = {
            "user_id": user_id,
            "api_key": None,
            "plan": "none",
            "expiry": None,
            "usage_count": 0,
            "max_usage": 0,
            "banned": False,
        }
        await self.db.users.insert_one(doc)
        return doc

    # Keys collection helpers
    async def get_key(self, key: str) -> Optional[Dict[str, Any]]:
        return await self.db.keys.find_one({"key": key})

    async def insert_key(self, key_doc: Dict[str, Any]):
        key_doc.setdefault("created_at", datetime.utcnow())
        await self.db.keys.insert_one(key_doc)

    async def increment_usage(self, key: str) -> int:
        await self.db.keys.update_one({"key": key}, {"$inc": {"usage_count": 1}})
        res = await self.db.keys.find_one({"key": key})
        return res.get("usage_count", 0) if res else 0

    async def update_key(self, key: str, update: Dict[str, Any]):
        await self.db.keys.update_one({"key": key}, {"$set": update})

    async def list_active_keys(self):
        cursor = self.db.keys.find({"status": "active"})
        return [k async for k in cursor]

    async def delete_key(self, key: str):
        await self.db.keys.delete_one({"key": key})

    async def ensure_indexes(self):
        await self.db.keys.create_index("key", unique=True)
        await self.db.keys.create_index("owner_id")
        await self.db.users.create_index("user_id", unique=True)

    # convenience creation: create trial key for a user
    async def create_trial_key(self, user_id: int, days: int = 7, max_usage: int = 50) -> Dict[str, Any]:
        from .keygen import generate_key

        key_value = generate_key(36)
        expiry = datetime.utcnow() + timedelta(days=days)
        doc = {
            "key": key_value,
            "owner_id": user_id,
            "status": "active",
            "plan": "trial",
            "expiry": expiry,
            "usage_count": 0,
            "max_usage": max_usage,
            "created_at": datetime.utcnow(),
        }
        await self.insert_key(doc)
        # link to users collection
        await self.db.users.update_one({"user_id": user_id}, {"$set": {"api_key": key_value, "plan": "trial", "expiry": expiry, "max_usage": max_usage}}, upsert=True)
        return doc

    async def create_premium_key(self, user_id: int, days: int = 30, max_usage: int = 10**9) -> Dict[str, Any]:
        from .keygen import generate_key

        key_value = generate_key(48)
        expiry = datetime.utcnow() + timedelta(days=days)
        doc = {
            "key": key_value,
            "owner_id": user_id,
            "status": "active",
            "plan": "premium",
            "expiry": expiry,
            "usage_count": 0,
            "max_usage": max_usage,
            "created_at": datetime.utcnow(),
        }
        await self.insert_key(doc)
        await self.db.users.update_one({"user_id": user_id}, {"$set": {"api_key": key_value, "plan": "premium", "expiry": expiry, "max_usage": max_usage}}, upsert=True)
        return doc
