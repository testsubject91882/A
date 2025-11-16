# Host Bot on GitHub

There are several ways to host the bot on GitHub. Choose the best option for your needs.

## Option 1: GitHub Codespaces (Recommended - Free & Always On)

GitHub Codespaces provides a full development environment that stays running continuously.

### Setup Steps:

1. **Enable Codespaces** in your repo:
   - Go to Settings → Codespaces
   - Click "Create codespace on main"

2. **Open the Codespace terminal** and run:
   ```bash
   source /workspaces/A/.venv/bin/activate
   python -m TeraBoxAPIService.bot.main
   ```

3. **Keep it running:**
   - The bot will run as long as the Codespace is open
   - You can minimize the browser - it continues running
   - Set auto-shutdown to never (Settings → Codespaces)

**Pros:**
- ✅ Completely free (GitHub-provided)
- ✅ Always on (no time limits)
- ✅ Full access to code and debugging
- ✅ Can update code live

**Cons:**
- Requires GitHub account with Codespaces enabled
- Browser tab must stay open (or use keep-alive extension)

---

## Option 2: GitHub Actions (Limited - 6-Hour Runs)

GitHub Actions can run the bot, but has limitations:

### Setup:

1. **Add Secrets** to your repo:
   - Go to Settings → Secrets and variables → Actions
   - Add these secrets:
     - `BOT_TOKEN`
     - `API_ID`
     - `API_HASH`
     - `MONGO_URI`
     - `MONGO_DB`
     - `ADMIN_IDS`
     - `API_URL`

2. **Workflow runs automatically:**
   - Every 6 hours (scheduled)
   - On every push to main
   - Manual trigger via "Run workflow"

3. **View logs:**
   - Go to Actions tab
   - Click "Keep Bot Alive" workflow
   - Check latest run logs

**Pros:**
- ✅ Fully automated
- ✅ No manual intervention needed
- ✅ Restarts automatically

**Cons:**
- ⚠️ Max 6-hour continuous run (resets)
- ⚠️ Limited monthly hours (2000 free)
- ⚠️ Some overlap possible during restarts

**File:** `.github/workflows/deploy-bot.yml`

---

## Option 3: Render Background Worker (Recommended for Production)

Already deployed! Your bot is running on Render as a background worker.

**URL:** Check your Render dashboard for status

**Pros:**
- ✅ Completely reliable
- ✅ 24/7 always on
- ✅ Auto-restarts on failure
- ✅ No time limits

---

## Option 4: Combine GitHub Actions + Keep-Alive Service

Use GitHub Actions with an external keep-alive service to extend uptime:

```bash
# In GitHub Actions, call a keep-alive API every 5 minutes
curl https://your-monitoring-service.com/ping
```

---

## Recommended Setup

**For Maximum Uptime, use Render + GitHub Actions:**

1. **Primary:** Render background worker (always running)
2. **Backup:** GitHub Actions (keeps running if Render fails)

This gives you:
- 24/7 coverage on Render
- Automatic failover with GitHub Actions
- Zero downtime deployments

---

## Setup GitHub Codespaces (Best for Development/Testing)

### Step-by-step:

1. **Create a Codespace:**
   ```
   Click "Code" → "Codespaces" → "Create codespace on main"
   ```

2. **In the terminal:**
   ```bash
   # Activate venv
   source .venv/bin/activate
   
   # Run bot
   python -m TeraBoxAPIService.bot.main
   ```

3. **Keep it running:**
   - Don't close the terminal
   - Minimize browser (continues running)
   - Set timeout to max (Settings → Codespaces)

4. **Access code live:**
   - Edit files in VS Code editor
   - Bot will use latest code
   - Restart to apply changes

---

## GitHub Actions Secrets Configuration

Add these in: **Settings → Secrets and variables → Actions**

```
BOT_TOKEN = your_bot_token_here
API_ID = 123456
API_HASH = your_hash_here
MONGO_URI = mongodb+srv://user:pass@cluster.mongodb.net/terabox_service
MONGO_DB = terabox_service
ADMIN_IDS = 123456789,987654321
API_URL = https://inert-tera-api.onrender.com
```

---

## Monitoring Bot Status

### On GitHub Actions:
1. Go to **Actions** tab
2. Click **"Keep Bot Alive"** workflow
3. See run history and logs

### On Render:
1. Go to Render Dashboard
2. Select **terabox-bot** service
3. View logs in real-time

---

## Troubleshooting

**Bot not responding:**
1. Check GitHub Actions logs (if using Actions)
2. Check Render logs (if using Render)
3. Verify environment variables are set
4. Ensure MongoDB connection is working

**Secrets not working:**
- Make sure they're in Settings → Secrets
- Not in `.env.example`
- Restart the workflow after adding secrets

**Bot keeps stopping:**
- Check logs for error messages
- Verify `MONGO_URI` is correct
- Ensure `BOT_TOKEN` is valid

---

## Summary

| Method | Uptime | Setup | Cost |
|--------|--------|-------|------|
| **Render** | 24/7 | Easy | Free |
| **GitHub Codespaces** | While open | Very easy | Free |
| **GitHub Actions** | 6h/run | Easy | Free |
| **Combination** | 24/7+ | Medium | Free |

**Recommended:** Use Render as primary + GitHub Actions as backup for 99.9% uptime.
