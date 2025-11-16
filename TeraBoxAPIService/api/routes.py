from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from TeraBoxAPIService.config import settings
from TeraBoxAPIService.bot.utils.database import Database
import httpx
from datetime import datetime

router = APIRouter()


@router.get("/run")
async def run_endpoint(key: str, url: str):
    db = Database()
    db.connect()
    key_doc = await db.get_key(key)
    if not key_doc:
        return JSONResponse(status_code=401, content={"status": "error", "message": "Invalid API key"})

    # check status
    if key_doc.get("status") != "active":
        return JSONResponse(status_code=403, content={"status": "error", "message": "Key is not active"})

    # check expiry
    expiry = key_doc.get("expiry")
    if expiry and isinstance(expiry, datetime) and expiry < datetime.utcnow():
        await db.update_key(key, {"status": "expired"})
        return JSONResponse(status_code=403, content={"status": "error", "message": "API key expired"})

    # usage limits
    max_usage = key_doc.get("max_usage")
    usage = key_doc.get("usage_count", 0)
    if max_usage is not None and usage >= max_usage and key_doc.get("plan") != "premium":
        return JSONResponse(status_code=429, content={"status": "error", "message": "Usage limit reached"})

    # forward request to base API
    base = settings.TERA_BASE_API.rstrip("/") + "/api"
    params = {"url": url}
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.get(base, params=params)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting base API: {str(e)}")

    # Map fields (expecting particular structure from base API)
    mapped = {
        "status": "success",
        "file_name": data.get("file_name") or data.get("name") or None,
        "size_bytes": data.get("size_bytes") or data.get("size") or None,
        "fast_download_url": data.get("fast_download_url") or data.get("download_url") or data.get("url"),
        "stream_url": data.get("stream_url"),
        "thumbnail": None,
    }
    # attempt to extract thumbnails
    thumbs = data.get("thumbnails") or data.get("thumbnail") or data.get("images")
    if isinstance(thumbs, list) and thumbs:
        mapped["thumbnail"] = thumbs[0]
    elif isinstance(thumbs, str):
        mapped["thumbnail"] = thumbs

    # increment usage
    await db.increment_usage(key)
    # fetch updated usage to compute usage_left
    key_after = await db.get_key(key)
    if key_after:
        mapped["usage_left"] = None
        if key_after.get("max_usage") is not None:
            mapped["usage_left"] = max(0, key_after.get("max_usage") - key_after.get("usage_count", 0))

    return JSONResponse(content=mapped)
