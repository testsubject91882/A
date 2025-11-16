from pyrogram.types import Message
from TeraBoxAPIService.bot.utils.database import Database
from TeraBoxAPIService.bot.utils.validators import is_valid_url, looks_like_terabox


async def handle_mykey(client, message: Message):
    db = Database()
    db.connect()
    user = await db.get_user(message.from_user.id)
    if not user or not user.get("api_key"):
        await message.reply_text("You don't have a key yet. Send /start to get a trial key.")
        return
    text = (
        f"API Key: `{user['api_key']}`\n"
        f"Plan: {user.get('plan')}\n"
        f"Expiry: {user.get('expiry')}\n"
        f"Usage: {user.get('usage_count',0)}/{user.get('max_usage',0)}"
    )
    await message.reply_text(text)


async def handle_help(client, message: Message):
    text = (
        "Usage:\n"
        "1. Get your API key with /start\n"
        "2. Call the API: `https://myapi.com/run?key=YOUR_KEY&url=TERABOX_LINK`\n"
        "3. If you need premium, contact an admin or use /upgrade\n"
    )
    await message.reply_text(text)
