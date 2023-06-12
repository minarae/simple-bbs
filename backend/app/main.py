from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database.connection import get_db
from .database import models
from .database.connection import engine
from .routers import members

app = FastAPI(title="account-book-api")

app.include_router(members.router)

@app.on_event("startup")
async def startup():
    async with engine.connect() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()

@app.get("/")
async def main():
    return {"message": "Hello World"}
