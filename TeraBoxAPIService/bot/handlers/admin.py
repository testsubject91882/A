from pyrogram.types import Message
from TeraBoxAPIService.bot.utils.database import Database
from TeraBoxAPIService.config import settings
from datetime import timedelta, datetime


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


async def cmd_addpremium(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("You're not an admin.")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.reply_text("Usage: /addpremium <user_id> <days>")
        return
    try:
        uid = int(parts[1])
        days = int(parts[2])
    except ValueError:
        await message.reply_text("user_id and days must be integers")
        return
    db = Database()
    db.connect()
    await db.create_premium_key(uid, days)
    await message.reply_text(f"Premium granted to {uid} for {days} days")


async def cmd_extend(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("You're not an admin.")
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.reply_text("Usage: /extend <user_id> <days>")
        return
    try:
        uid = int(parts[1])
        days = int(parts[2])
    except ValueError:
        await message.reply_text("user_id and days must be integers")
        return
    db = Database()
    db.connect()
    user = await db.get_user(uid)
    if not user or not user.get("api_key"):
        await message.reply_text("User has no key")
        return
    key = user["api_key"]
    current_expiry = user.get("expiry") or datetime.utcnow()
    new_expiry = (current_expiry if current_expiry > datetime.utcnow() else datetime.utcnow()) + timedelta(days=days)
    await db.update_key(key, {"expiry": new_expiry})
    await db.db.users.update_one({"user_id": uid}, {"$set": {"expiry": new_expiry}})
    await message.reply_text(f"Extended {uid} by {days} days")


async def cmd_remove(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("You're not an admin.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply_text("Usage: /remove <user_id>")
        return
    try:
        uid = int(parts[1])
    except ValueError:
        await message.reply_text("user_id must be integer")
        return
    db = Database()
    db.connect()
    user = await db.get_user(uid)
    if user and user.get("api_key"):
        await db.delete_key(user["api_key"])
        await db.db.users.update_one({"user_id": uid}, {"$set": {"api_key": None, "plan": "none"}})
        await message.reply_text(f"Removed key for {uid}")
    else:
        await message.reply_text("User has no key")


async def cmd_ban(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("You're not an admin.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply_text("Usage: /ban <user_id>")
        return
    try:
        uid = int(parts[1])
    except ValueError:
        await message.reply_text("user_id must be integer")
        return
    db = Database()
    db.connect()
    user = await db.get_user(uid)
    if user and user.get("api_key"):
        await db.update_key(user["api_key"], {"status": "banned"})
        await db.db.users.update_one({"user_id": uid}, {"$set": {"banned": True}})
        await message.reply_text(f"Banned {uid}")
    else:
        await message.reply_text("User has no key")


async def cmd_unban(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("You're not an admin.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply_text("Usage: /unban <user_id>")
        return
    try:
        uid = int(parts[1])
    except ValueError:
        await message.reply_text("user_id must be integer")
        return
    db = Database()
    db.connect()
    user = await db.get_user(uid)
    if user and user.get("api_key"):
        await db.update_key(user["api_key"], {"status": "active"})
        await db.db.users.update_one({"user_id": uid}, {"$set": {"banned": False}})
        await message.reply_text(f"Unbanned {uid}")
    else:
        await message.reply_text("User has no key")


async def cmd_allkeys(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("You're not an admin.")
        return
    db = Database()
    db.connect()
    keys = await db.list_active_keys()
    text = "Active keys:\n"
    for k in keys[:50]:
        text += f"{k['key']} - owner: {k.get('owner_id')} plan: {k.get('plan')} expiry: {k.get('expiry')}\n"
    await message.reply_text(text)


async def cmd_userinfo(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("You're not an admin.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply_text("Usage: /userinfo <user_id>")
        return
    try:
        uid = int(parts[1])
    except ValueError:
        await message.reply_text("user_id must be integer")
        return
    db = Database()
    db.connect()
    user = await db.get_user(uid)
    if not user:
        await message.reply_text("No user found")
        return
    await message.reply_text(str(user))
