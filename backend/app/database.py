from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

client: AsyncIOMotorClient = None
db = None


def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    print("Connected to MongoDB")


def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


# Dependency injection for FastAPI
async def get_db():
    return db
