from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase


class QuestionRepository:
    """
    Repository layer for handling all database operations for questions
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["questions"]

    async def create(self, question_doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new question document
        """
        result = await self.collection.insert_one(question_doc) 
        question_doc["_id"] = str(result.inserted_id)
        return question_doc

    async def find_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a question by question_id
        """
        question = await self.collection.find_one({"question_id": question_id})
        if question:
            question["_id"] = str(question["_id"])
        return question

    async def find_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> List[Dict[str, Any]]:
        """
        Find all questions with optional filters and pagination
        """
        query = filters or {}
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        questions = await cursor.to_list(length=limit)

        for question in questions:
            question["_id"] = str(question["_id"])

        return questions

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count questions matching filters
        """
        query = filters or {}
        return await self.collection.count_documents(query)

    async def find_by_interview_id(
        self,
        interview_id: str,
        question_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Find all questions for a specific interview
        """
        query = {"interview_id": interview_id}
        if question_type:
            query["type"] = question_type

        cursor = self.collection.find(query).skip(skip).limit(limit)
        questions = await cursor.to_list(length=limit)

        for question in questions:
            question["_id"] = str(question["_id"])

        return questions

    async def update(self, question_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a question by question_id
        """
        result = await self.collection.find_one_and_update(
            {"question_id": question_id},
            {"$set": update_data},
            return_document=True
        )

        if result:
            result["_id"] = str(result["_id"])

        return result

    async def delete(self, question_id: str) -> bool:
        """
        Delete a question by question_id
        """
        result = await self.collection.delete_one({"question_id": question_id})
        return result.deleted_count > 0

    async def delete_many(self, filters: Dict[str, Any]) -> int:
        """
        Delete multiple questions matching filters
        """
        result = await self.collection.delete_many(filters)
        return result.deleted_count

    async def bulk_create(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Insert multiple questions at once
        """
        if not questions:
            return []

        result = await self.collection.insert_many(questions)

        for idx, inserted_id in enumerate(result.inserted_ids):
            questions[idx]["_id"] = str(inserted_id)

        return questions

    async def find_by_ids(self, question_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Find multiple questions by their question_ids
        """
        cursor = self.collection.find({"question_id": {"$in": question_ids}})
        questions = await cursor.to_list(length=len(question_ids))

        for question in questions:
            question["_id"] = str(question["_id"])

        return questions


class SelectedQuestionsRepository:
    """
    Repository layer for handling selected questions for interviews
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["interview_selected_questions"]

    async def create(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new selected questions document
        """
        result = await self.collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        return document

    async def find_by_interview_id(self, interview_id: str) -> Optional[Dict[str, Any]]:
        """
        Find selected questions by interview_id
        """
        result = await self.collection.find_one({"interview_id": interview_id})
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def update(self, interview_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update or create selected questions for an interview
        """
        result = await self.collection.find_one_and_update(
            {"interview_id": interview_id},
            {"$set": document},
            upsert=True,
            return_document=True
        )

        if result:
            result["_id"] = str(result["_id"])

        return result

    async def delete(self, interview_id: str) -> bool:
        """
        Delete selected questions by interview_id
        """
        result = await self.collection.delete_one({"interview_id": interview_id})
        return result.deleted_count > 0
