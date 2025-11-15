from typing import Dict, Any, List
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.question_repository import QuestionRepository, SelectedQuestionsRepository
from app.schemas.model.question_model import SelectedQuestionsModel




class SelectedQuestionsService:
    """
    Service layer for Selected Questions operations
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.question_repo = QuestionRepository(db)
        self.selected_repo = SelectedQuestionsRepository(db)


    #=================== CREATE Operations ====================
    
    async def save_selected_questions(
        self,
        interview_id: str,
        selected_ids: List[str],
    ) -> Dict[str, Any]:
        """
        Save selected questions for an interview
        """
        if not selected_ids:
            raise HTTPException(status_code=400, detail="No question IDs provided")

        # Fetch all questions with matching question_id
        questions = await self.question_repo.find_by_ids(selected_ids)

        if not questions:
            raise HTTPException(status_code=404, detail="No matching questions found")

        # Sort in the order user selected
        ordered_questions = []
        for index, qid in enumerate(selected_ids):
            match = next((q for q in questions if q["question_id"] == qid), None)
            if match:
                ordered_questions.append({
                    "question_id": match["question_id"],
                    "question": match["question"],
                    "difficulty": match.get("difficulty"),
                    "category": match.get("category"),
                    "expected_answer": match.get("expected_answer"),
                    "type": match.get("type"),
                    "order": index + 1,
                    "skill_focus": match.get("skill_focus", []),
                    "tech_stack": match.get("tech_stack", []),
                })

        # Create document
        doc = SelectedQuestionsModel.create_document(
            interview_id=interview_id,
            selected_questions=ordered_questions,
        )

        # Update or create
        await self.selected_repo.update(interview_id, doc)

        return {
            "message": "Selected questions saved successfully",
            "interview_id": interview_id,
            "count": len(ordered_questions),
            "selected_questions": ordered_questions,
        }

    #=================== READ Operations ====================

    async def get_selected_questions(self, interview_id: str) -> Dict[str, Any]:
        """
        Get selected questions for an interview
        """
        result = await self.selected_repo.find_by_interview_id(interview_id)

        if not result:
            return {
                "interview_id": interview_id,
                "selected_questions": [],
            }

        return result
    

 #=================== DELETE Operations ====================

    async def delete_selected_questions(self, interview_id: str) -> Dict[str, Any]:
        """
        Delete selected questions for an interview
        """
        success = await self.selected_repo.delete(interview_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"No selected questions found for interview {interview_id}"
            )

        return {
            "message": "Selected questions deleted successfully",
            "interview_id": interview_id,
        }
