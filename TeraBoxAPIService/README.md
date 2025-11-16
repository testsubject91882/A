# TeraBox API-Key Service

A complete Telegram bot + FastAPI server for issuing and validating API keys to parse TeraBox links.

## Features

- **MongoDB** (motor) for persistent `users` and `keys` collections
- **Pyrogram Telegram Bot** for issuing and managing API keys
- **FastAPI Server** exposing `/run?key=...&url=...` endpoint
- **Async HTTP client** (httpx) for calling the base parsing API
- **Admin commands** for managing premium keys, bans, and usage
- **Free trial system** with 7-day keys and usage limits
- **Docker & Docker Compose** for easy deployment



Quick start
1. Copy `.env.example` to `.env`:
   ```bash
   cp TeraBoxAPIService/.env.example TeraBoxAPIService/.env
   ```
   Edit `.env` and fill in your real secrets for `BOT_TOKEN`, `API_ID`, `API_HASH`, `MONGO_URI`, `ADMIN_IDS`, etc.
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

## API Endpoint

**Local Development:**
```
http://localhost:8000/run?key=YOUR_API_KEY&url=TERABOX_LINK
```

**Production Examples:**
- Railway: `https://terabox-api-production.up.railway.app/run?key=YOUR_API_KEY&url=TERABOX_LINK`
- Heroku: `https://terabox-api.herokuapp.com/run?key=YOUR_API_KEY&url=TERABOX_LINK`
- Self-hosted: `https://api.yourdomain.com/run?key=YOUR_API_KEY&url=TERABOX_LINK`

See [DEPLOYMENT.md](./DEPLOYMENT.md) for full hosting setup guides.

## Docker Deployment

Run everything with Docker Compose:
```bash
docker-compose up -d
```

This starts MongoDB, API server, and bot automatically.

## Bot Commands

- `/start` - Get a free trial API key (7 days, 50 requests)
- `/mykey` - Show your current key and usage
- `/help` - Usage instructions
- `/upgrade` - Show premium options

**Admin Commands** (for users in `ADMIN_IDS`):
- `/addpremium <user_id> <days>` - Grant premium access
- `/extend <user_id> <days>` - Extend key expiry
- `/remove <user_id>` - Delete user's key
- `/ban <user_id>` - Ban a user
- `/unban <user_id>` - Unban a user
- `/allkeys` - List all active keys
- `/userinfo <user_id>` - Show user details
Files
- `bot/` - Pyrogram bot and handlers
- `api/` - FastAPI server and routes
- `config.py` - Configuration from environment variables
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image for containerization
- `docker-compose.yml` - Local development with MongoDB
- `DEPLOYMENT.md` - Production deployment guides
