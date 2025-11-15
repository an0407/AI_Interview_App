from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import connect_to_mongo, close_mongo_connection
from app.routers.question_router import question_router
from app.routers.qs_generator_router import question_generator_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    connect_to_mongo()
    yield
    # Shutdown
    close_mongo_connection()


app = FastAPI(
    title="AI Interview App API",
    lifespan=lifespan
)


app.include_router(question_router)

app.include_router(question_generator_router)
