import asyncio
from pyrogram import Client, filters
from .handlers import start as start_h
from .handlers import keys as keys_h
from .handlers import admin as admin_h
from TeraBoxAPIService.config import settings


def run_bot():
    app = Client("terabox_bot", bot_token=settings.BOT_TOKEN, api_id=settings.API_ID, api_hash=settings.API_HASH)

    @app.on_message(filters.command("start"))
    async def _start(client, message):
        await start_h.handle_start(client, message)

    @app.on_message(filters.command("mykey"))
    async def _mykey(client, message):
        await keys_h.handle_mykey(client, message)

    @app.on_message(filters.command("help"))
    async def _help(client, message):
        await keys_h.handle_help(client, message)

    @app.on_message(filters.command("addpremium"))
    async def _addpremium(client, message):
        await admin_h.cmd_addpremium(client, message)

    @app.on_message(filters.command("extend"))
    async def _extend(client, message):
        await admin_h.cmd_extend(client, message)

    @app.on_message(filters.command("remove"))
    async def _remove(client, message):
        await admin_h.cmd_remove(client, message)

    @app.on_message(filters.command("ban"))
    async def _ban(client, message):
        await admin_h.cmd_ban(client, message)

    @app.on_message(filters.command("unban"))
    async def _unban(client, message):
        await admin_h.cmd_unban(client, message)

    @app.on_message(filters.command("allkeys"))
    async def _allkeys(client, message):
        await admin_h.cmd_allkeys(client, message)

    @app.on_message(filters.command("userinfo"))
    async def _userinfo(client, message):
        await admin_h.cmd_userinfo(client, message)

    print("Starting bot...")
    app.run()


if __name__ == "__main__":
    run_bot()
