from bson import ObjectId
from app.database import get_db
from app.schemas.pydantic.interview_schema import InterviewCreate, InterviewUpdate
from app.schemas.model.interview_model import interview_model
from datetime import datetime
from uuid import uuid4


def generate_interview_id():
    return f"INTV-{uuid4()}"


async def create_interview(data: InterviewCreate):
    db = await get_db()  # ✅ fetch DB at runtime
    collection = db["interviews"]

    interview_dict = data.dict()
    interview_dict["created_at"] = datetime.utcnow()
    interview_dict["interview_id"] = generate_interview_id()

    result = await collection.insert_one(interview_dict)
    new_doc = await collection.find_one({"_id": result.inserted_id})
    return interview_model(new_doc)


async def get_all_interviews():
    db = await get_db()
    collection = db["interviews"]

    docs = []
    async for doc in collection.find():
        docs.append(interview_model(doc))
    return docs


async def get_interview_by_id(interview_id: str):
    db = await get_db()
    collection = db["interviews"]

    if not ObjectId.is_valid(interview_id):
        return None

    doc = await collection.find_one({"_id": ObjectId(interview_id)})
    return interview_model(doc) if doc else None


async def update_interview(interview_id: str, data: InterviewUpdate):
    db = await get_db()
    collection = db["interviews"]

    if not ObjectId.is_valid(interview_id):
        return None

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    await collection.update_one(
        {"_id": ObjectId(interview_id)},
        {"$set": update_data}
    )

    updated_doc = await collection.find_one({"_id": ObjectId(interview_id)})
    return interview_model(updated_doc) if updated_doc else None


async def delete_interview(interview_id: str):
    db = await get_db()
    collection = db["interviews"]

    if not ObjectId.is_valid(interview_id):
        return False

    result = await collection.delete_one({"_id": ObjectId(interview_id)})
    return result.deleted_count == 1


async def get_interviews_by_created_by(email: str):
    db = await get_db()
    collection = db["interviews"]

    docs = []
    async for doc in collection.find({"created_by": email}):
        docs.append(interview_model(doc))
    return docs
