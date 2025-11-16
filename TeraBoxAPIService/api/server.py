from fastapi import FastAPI
from .routes import router
from TeraBoxAPIService.config import settings
from TeraBoxAPIService.bot.utils.database import Database

app = FastAPI(title="TeraBox API-Key Service")


@app.on_event("startup")
async def startup_event():
    # ensure indexes
    db = Database()
    db.connect()
    await db.ensure_indexes()


@app.on_event("shutdown")
async def shutdown_event():
    db = Database()
    db.connect()
    db.close()


app.include_router(router)
