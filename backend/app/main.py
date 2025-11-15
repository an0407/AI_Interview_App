from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routers.interview_router import router as interview_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Interview Scheduler Backend Running"}

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(interview_router)
