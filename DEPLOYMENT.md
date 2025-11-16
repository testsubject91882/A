# Deployment Guide for TeraBoxAPIService

This guide covers deploying the TeraBox API-Key Service to production using Docker and popular hosting platforms.

## Quick Start (Local Docker)

### Prerequisites
- Docker and Docker Compose installed
- `.env` file configured with your credentials

### Run Locally with Docker

```bash
docker-compose up -d
```

This starts:
- **MongoDB** on `mongodb://localhost:27017`
- **API Server** on `http://localhost:8000`
- **Telegram Bot** (background service)

API Endpoint:
```
http://localhost:8000/run?key=YOUR_API_KEY&url=TERABOX_LINK
```

---

## Hosting Options & Full URLs

### Option 1: Railway.app (Recommended - Simple)

1. **Create account** at [railway.app](https://railway.app)
2. **Connect GitHub repository**
3. **Add MongoDB plugin** (Railway provides free tier)
4. **Deploy with docker-compose.yml**
5. **Get public URL** (e.g., `https://terabox-api-production.up.railway.app`)

**Full API Endpoint:**
```
https://terabox-api-production.up.railway.app/run?key=YOUR_API_KEY&url=TERABOX_LINK
```

### Option 2: Heroku (with Docker)

1. **Install Heroku CLI**
2. **Login:** `heroku login`
3. **Create app:** `heroku create terabox-api`
4. **Add MongoDB Atlas** (free tier available at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas))
5. **Set env vars:**
```bash
heroku config:set BOT_TOKEN="..." API_ID="..." API_HASH="..." MONGO_URI="..." ADMIN_IDS="..."
```
6. **Deploy:**
```bash
git push heroku main
```

**Full API Endpoint:**
```
https://terabox-api.herokuapp.com/run?key=YOUR_API_KEY&url=TERABOX_LINK
```

### Option 3: AWS (EC2 + RDS)

1. **Launch EC2 instance** (Ubuntu 22.04, t3.micro free tier)
2. **SSH into instance:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```
3. **Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
```
4. **Clone repo, setup `.env`, run:**
```bash
docker-compose up -d
```
5. **Configure security groups** to allow port 8000
6. **Point domain** (e.g., `api.yourdomain.com`) to instance IP

**Full API Endpoint:**
```
https://api.yourdomain.com/run?key=YOUR_API_KEY&url=TERABOX_LINK
```

### Option 4: DigitalOcean App Platform

1. **Create account** at [digitalocean.com](https://www.digitalocean.com)
2. **Connect GitHub repo**
3. **Create app from docker-compose.yml**
4. **Add MongoDB (DigitalOcean Managed Database)**
5. **Deploy** - DigitalOcean generates a URL automatically

**Full API Endpoint:**
```
https://terabox-api-xxxxx.ondigitalocean.app/run?key=YOUR_API_KEY&url=TERABOX_LINK
```

### Option 5: Self-Hosted (VPS + Cloudflare)

1. **Get a VPS** (Linode, Vultr, DigitalOcean Droplet)
2. **Setup domain** with Cloudflare (free SSL)
3. **Install Docker & Docker Compose**
4. **Clone repo and configure `.env`**
5. **Run:**
```bash
docker-compose up -d
```
6. **Setup nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
7. **Enable HTTPS with Let's Encrypt** (certbot)

**Full API Endpoint:**
```
https://api.yourdomain.com/run?key=YOUR_API_KEY&url=TERABOX_LINK
```

---

## Environment Variables for Deployment

Create a `.env` file in the repo root:

```env
BOT_TOKEN=your_telegram_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/terabox_service
MONGO_DB=terabox_service
ADMIN_IDS=123456789,987654321
TERA_BASE_API=https://teraapi.boogafantastic.workers.dev
```

---

## Production Checklist

- [ ] Use MongoDB Atlas (not local MongoDB) for production
- [ ] Enable database backups
- [ ] Configure bot webhook (optional, for better performance)
- [ ] Set up monitoring (Sentry for error tracking)
- [ ] Enable HTTPS/SSL (automatic on Railway, Heroku, DigitalOcean)
- [ ] Configure rate limiting in FastAPI
- [ ] Set up logging and log aggregation
- [ ] Test `/run` endpoint thoroughly
- [ ] Monitor API usage and set quotas

---

## Testing the Deployment

Once deployed, test with:

```bash
# Get a test key from the Telegram bot (/start)
# Then call:
curl "https://YOUR_DEPLOYED_URL/run?key=YOUR_API_KEY&url=https://www.terabox.com/example"
```

---

## Troubleshooting

**API not responding:**
- Check if containers are running: `docker-compose ps`
- Check logs: `docker-compose logs api`

**MongoDB connection errors:**
- Verify `MONGO_URI` in `.env`
- Ensure MongoDB is running and accessible

**Bot not responding:**
- Verify `BOT_TOKEN`, `API_ID`, `API_HASH`
- Check bot logs: `docker-compose logs bot`

---

## Support

For issues, refer to:
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Pyrogram Docs](https://docs.pyrogram.org/)
- [Docker Docs](https://docs.docker.com/)
