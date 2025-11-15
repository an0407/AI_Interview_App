from typing import Optional, List, Dict, Any
from datetime import datetime


class QuestionModel:
    """
    MongoDB model for storing interview questions.
    Supports both AI-generated and manually created questions.
    """

    @staticmethod
    def create_document(
        question_id: str,
        question: str,
        category: str,
        expected_answer: str,
        interview_id: str,
        question_type: str,  # 'ai' or 'manual'
        difficulty: Optional[str] = None,
        title: Optional[str] = None,
        skill_focus: Optional[List[str]] = None,
        tech_stack: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        order: Optional[int] = None,
        is_active: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a standardized question document for MongoDB
        """
        return {
            "question_id": question_id,
            "interview_id": interview_id,
            "type": question_type,
            "question": question,
            "category": category,
            "difficulty": difficulty,
            "expected_answer": expected_answer,
            "title": title,
            "skill_focus": skill_focus or [],
            "tech_stack": tech_stack or [],
            "metadata": metadata or {},
            "order": order,
            "is_active": is_active,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

    @staticmethod
    def update_document(update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare update document with updated_at timestamp
        """
        update_data["updated_at"] = datetime.utcnow()
        return update_data


class SelectedQuestionsModel:
    """
    MongoDB model for storing selected questions for an interview
    """

    @staticmethod
    def create_document(
        interview_id: str,
        selected_questions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a document for storing selected questions
        """
        return {
            "interview_id": interview_id,
            "selected_questions": selected_questions,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
