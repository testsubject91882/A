"""Small helper to create a trial key for a user and optionally call the local API.

Usage:
    python tools/create_trial_and_test.py <telegram_user_id>

This script requires the environment variables (see .env.example) and installed dependencies.
It connects to MongoDB, creates a trial key for the given user id, and prints a curl command
you can use to call the `/run` endpoint locally.
"""
import asyncio
import os
import sys
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "terabox_service")
LOCAL_API = os.getenv("LOCAL_API", "http://127.0.0.1:8000/run")


async def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/create_trial_and_test.py <telegram_user_id>")
        return
    user_id = int(sys.argv[1])
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]

    # generate a simple key (not cryptographically strong here; in production use keygen)
    import secrets, string
    alphabet = string.ascii_letters + string.digits
    key_value = ''.join(secrets.choice(alphabet) for _ in range(36))
    expiry = datetime.utcnow()
    # default 7 days
    from datetime import timedelta
    expiry = expiry + timedelta(days=7)

    key_doc = {
        "key": key_value,
        "owner_id": user_id,
        "status": "active",
        "plan": "trial",
        "expiry": expiry,
        "usage_count": 0,
        "max_usage": 50,
        "created_at": datetime.utcnow(),
    }

    await db.keys.insert_one(key_doc)
    await db.users.update_one({"user_id": user_id}, {"$set": {"api_key": key_value, "plan": "trial", "expiry": expiry, "max_usage": 50}}, upsert=True)

    print("Created trial key:")
    print(key_value)
    print("")
    print("Call the local API with:")
    print(f"curl '{LOCAL_API}?key={key_value}&url=https://www.terabox.com/example' -s")


if __name__ == "__main__":
    asyncio.run(main())
