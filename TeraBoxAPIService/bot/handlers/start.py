from pyrogram import filters
from pyrogram.types import Message
from TeraBoxAPIService.bot.utils.database import Database
from TeraBoxAPIService.config import settings


async def handle_start(client, message: Message):
    db = Database()
    db.connect()
    user_id = message.from_user.id
    # create user if missing and issue trial if no key
    user = await db.get_user(user_id)
    if not user or not user.get("api_key"):
        trial = await db.create_trial_key(user_id)
        text = (
            f"🎉 Your trial API key: `{trial['key']}`\n"
            f"Expiry: {trial['expiry'].isoformat()}\n"
            f"Usage limit: {trial['max_usage']}\n"
            "Use it with: `https://myapi.com/run?key=YOUR_KEY&url=TERABOX_LINK`"
        )
        await message.reply_text(text)
        return

    # show existing key
    text = (
        f"Your API key: `{user['api_key']}`\n"
        f"Plan: {user.get('plan')}\n"
        f"Expiry: {user.get('expiry')}\n"
        f"Usage: {user.get('usage_count',0)}/{user.get('max_usage',0)}"
    )
    await message.reply_text(text)
