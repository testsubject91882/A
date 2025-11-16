# TeraBox API-Key Service

This project provides a modular Telegram bot and API server that issues and validates API keys for parsing TeraBox links using an external parsing API.

Features
- MongoDB (motor) for `users` and `keys` collections
- Pyrogram bot for issuing and managing keys
- FastAPI server exposing `/run?key=...&url=...`
- Async HTTP client (`httpx`) to call the base parsing API

Quick start
1. Copy `.env.example` to `.env` and fill values for `BOT_TOKEN`, `API_ID`, `API_HASH`, `MONGO_URI` and `ADMIN_IDS`.
2. Install dependencies:
```bash
python -m pip install -r TeraBoxAPIService/requirements.txt
```
3. Run API server:
```bash
uvicorn TeraBoxAPIService.api.server:app --host 0.0.0.0 --port 8000
```
4. Run bot (in separate process):
```bash
python -m TeraBoxAPIService.bot.main
```

Files
- `bot/` - Pyrogram bot and handlers
- `api/` - FastAPI server and routes
- `config.py` - configuration from environment
- `requirements.txt` - Python dependencies
