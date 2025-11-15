from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid

from app.repositories.question_repository import QuestionRepository
from app.schemas.model.question_model import QuestionModel
from app.schemas.pydantic.question_schemas import (
    CreateManualQuestionRequest,
    GenerateAIQuestionsRequest,
    UpdateQuestionRequest,
    QuestionFilters,
)
from app.services.llm_service import LLMService




def generate_question_id() -> str:
    """Generate unique question ID"""
    return f"QSTN-{uuid.uuid4()}"



class QuestionService:
    """
    Service layer for Question operations
    Handles business logic and uses repository for data access
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.repository = QuestionRepository(db)
        self.llm_service = LLMService()


    async def create_manual_question(
        self,
        request: CreateManualQuestionRequest
    ) -> Dict[str, Any]:
        """
        Create a single manual question
        """
        question_doc = QuestionModel.create_document(
            question_id=generate_question_id(),
            question=request.question,
            category=request.category,
            expected_answer=request.expected_answer,
            interview_id=request.interview_id,
            question_type="manual",
            difficulty=request.difficulty,
            title=request.title,
            skill_focus=request.skill_focus,
            tech_stack=request.tech_stack,
            metadata=request.metadata,
        )

        # Save to database using repository
        saved_question = await self.repository.create(question_doc)

        return {
            "message": "Manual question created successfully",
            "question": saved_question,
        }

    async def generate_ai_questions(
        self,
        request: GenerateAIQuestionsRequest
    ) -> Dict[str, Any]:
        """
        Generate AI questions using LLM service
        """
        try:
            llm_result = await self.llm_service.generate_questions(
                role=request.title,
                difficulty=request.difficulty_level,
                count=request.count,
                skill_focus=request.specific_skill_focus or "",
                tech_stack=request.technology_stack or [],
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

        # Create question documents
        question_docs = []
        for q in llm_result.get("questions", []):
            question_doc = QuestionModel.create_document(
                question_id=generate_question_id(),
                question=q.get("question"),
                category=q.get("category"),
                expected_answer=q.get("expected_answer"),
                interview_id=request.interview_id,
                question_type="ai",
                difficulty=q.get("difficulty"),
                title=request.title,
                skill_focus=[request.specific_skill_focus] if request.specific_skill_focus else [],
                tech_stack=request.technology_stack,
                metadata=llm_result.get("metadata", {}),
            )
            question_docs.append(question_doc)

        # Bulk insert into database
        saved_questions = await self.repository.bulk_create(question_docs)

        return {
            "message": "AI questions generated successfully",
            "count": len(saved_questions),
            "questions": saved_questions,
        }

    # ==================== READ Operations ====================

    async def get_question_by_id(self, question_id: str) -> Dict[str, Any]:
        """
        Get a single question by ID
        """
        question = await self.repository.find_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found")
        return question

    async def get_all_questions(
        self,
        filters: Optional[QuestionFilters] = None,
    ) -> Dict[str, Any]:
        """
        Get all questions with optional filters and pagination
        """
        if filters:
            # Build query filters
            query = {}
            if filters.interview_id:
                query["interview_id"] = filters.interview_id
            if filters.type:
                query["type"] = filters.type
            if filters.category:
                query["category"] = filters.category
            if filters.difficulty:
                query["difficulty"] = filters.difficulty
            if filters.is_active is not None:
                query["is_active"] = filters.is_active

            questions = await self.repository.find_all(
                filters=query,
                skip=filters.skip,
                limit=filters.limit,
            )
            total_count = await self.repository.count(query)
        else:
            questions = await self.repository.find_all()
            total_count = await self.repository.count()

        return {
            "count": total_count,
            "questions": questions,
            "skip": filters.skip if filters else 0,
            "limit": filters.limit if filters else 100,
        }

    async def get_questions_by_interview_id(
        self,
        interview_id: str,
        question_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Get all questions for a specific interview
        """
        questions = await self.repository.find_by_interview_id(
            interview_id=interview_id,
            question_type=question_type,
            skip=skip,
            limit=limit,
        )

        query = {"interview_id": interview_id}
        if question_type:
            query["type"] = question_type
        total_count = await self.repository.count(query)

        return {
            "count": total_count,
            "questions": questions,
            "skip": skip,
            "limit": limit,
        }

    # ==================== UPDATE Operations ====================

    async def update_question(
        self,
        question_id: str,
        update_data: UpdateQuestionRequest,
    ) -> Dict[str, Any]:
        """
        Update a question by ID
        """
        # Check if question exists
        existing_question = await self.repository.find_by_id(question_id)
        if not existing_question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found")

        # Prepare update data (exclude None values)
        update_dict = update_data.model_dump(exclude_none=True)
        if not update_dict:
            raise HTTPException(status_code=400, detail="No update data provided")

        # Use model to prepare update
        update_dict = QuestionModel.update_document(update_dict)

        # Update in database
        updated_question = await self.repository.update(question_id, update_dict)

        return {
            "message": "Question updated successfully",
            "question": updated_question,
        }

    # ==================== DELETE Operations ====================

    async def delete_question(self, question_id: str) -> Dict[str, Any]:
        """
        Delete a single question by ID
        """
        # Check if question exists
        existing_question = await self.repository.find_by_id(question_id)
        if not existing_question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found")

        # Delete from database
        success = await self.repository.delete(question_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete question")

        return {
            "message": "Question deleted successfully",
            "question_id": question_id,
        }

    async def delete_questions_by_interview_id(self, interview_id: str) -> Dict[str, Any]:
        """
        Delete all questions for a specific interview
        """
        deleted_count = await self.repository.delete_many({"interview_id": interview_id})

        return {
            "message": f"Deleted {deleted_count} questions for interview {interview_id}",
            "deleted_count": deleted_count,
        }




