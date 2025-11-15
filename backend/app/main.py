from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import health, auth_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()
app.include_router(health.router)
app.include_router(auth_router.router)