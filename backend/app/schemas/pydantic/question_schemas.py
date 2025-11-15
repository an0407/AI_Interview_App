from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class QuestionType(str, Enum):
    """Question type enumeration"""
    AI = "ai"
    MANUAL = "manual"


class DifficultyLevel(str, Enum):
    """Difficulty level enumeration"""
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"



class CreateManualQuestionRequest(BaseModel):
    """Request schema for creating a manual question"""
    interview_id: str = Field(..., description="Interview ID")
    question: str = Field(..., description="The interview question")
    category: str = Field(..., description="Category of the question")
    expected_answer: str = Field(..., description="The expected answer for the question")
    difficulty: Optional[DifficultyLevel] = Field(None, description="Difficulty level")
    title: Optional[str] = Field(None, description="Question title or role")
    skill_focus: Optional[List[str]] = Field(default_factory=list, description="Specific skills")
    tech_stack: Optional[List[str]] = Field(default_factory=list, description="Technologies")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class GenerateAIQuestionsRequest(BaseModel):
    """Request schema for generating AI questions"""
    interview_id: str = Field(..., description="Interview ID")
    title: str = Field(..., description="Interview title/role")
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.MODERATE, description="Difficulty level")
    count: int = Field(default=10, ge=1, le=50, description="Number of questions to generate")
    specific_skill_focus: Optional[str] = Field(None, description="Specific skill focus")
    technology_stack: Optional[List[str]] = Field(default_factory=list, description="Technology stack")
    domain_category: Optional[str] = Field(None, description="Domain category")


class UpdateQuestionRequest(BaseModel):
    """Request schema for updating a question"""
    question: Optional[str] = Field(None, description="The interview question")
    category: Optional[str] = Field(None, description="Category of the question")
    expected_answer: Optional[str] = Field(None, description="The expected answer")
    difficulty: Optional[DifficultyLevel] = Field(None, description="Difficulty level")
    title: Optional[str] = Field(None, description="Question title")
    skill_focus: Optional[List[str]] = Field(None, description="Specific skills")
    tech_stack: Optional[List[str]] = Field(None, description="Technologies")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    is_active: Optional[bool] = Field(None, description="Whether question is active")


class QuestionFilters(BaseModel):
    """Request schema for filtering questions"""
    interview_id: Optional[str] = Field(None, description="Filter by interview ID")
    type: Optional[QuestionType] = Field(None, description="Filter by question type")
    category: Optional[str] = Field(None, description="Filter by category")
    difficulty: Optional[DifficultyLevel] = Field(None, description="Filter by difficulty")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=500, description="Maximum number of records")



class QuestionResponse(BaseModel):
    """Response schema for a single question"""
    question_id: str = Field(..., description="Unique question ID")
    interview_id: Optional[str] = Field(None, description="Interview ID")
    type: QuestionType = Field(..., description="Question type (ai or manual)")
    question: str = Field(..., description="The interview question")
    category: str = Field(..., description="Question category")
    difficulty: Optional[str] = Field(None, description="Difficulty level")
    expected_answer: str = Field(..., description="Expected answer")
    title: Optional[str] = Field(None, description="Question title")
    skill_focus: List[str] = Field(default_factory=list, description="Skills tested")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional data")
    order: Optional[int] = Field(None, description="Question order")
    is_active: bool = Field(default=True, description="Active status")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    id: Optional[str] = Field(None, alias="_id", description="MongoDB document ID")

    class Config:
        from_attributes = True
        populate_by_name = True


class QuestionListResponse(BaseModel):
    """Response schema for list of questions"""
    count: int = Field(..., description="Total number of questions")
    questions: List[QuestionResponse] = Field(..., description="List of questions")
    skip: int = Field(default=0, description="Number of records skipped")
    limit: int = Field(default=100, description="Maximum records returned")


class CreateQuestionResponse(BaseModel):
    """Response schema for creating a question"""
    message: str = Field(..., description="Success message")
    question: QuestionResponse = Field(..., description="Created question")


class BulkCreateQuestionsResponse(BaseModel):
    """Response schema for bulk creating questions"""
    message: str = Field(..., description="Success message")
    count: int = Field(..., description="Number of questions created")
    questions: List[QuestionResponse] = Field(..., description="Created questions")


class UpdateQuestionResponse(BaseModel):
    """Response schema for updating a question"""
    message: str = Field(..., description="Success message")
    question: QuestionResponse = Field(..., description="Updated question")


class DeleteQuestionResponse(BaseModel):
    """Response schema for deleting a question"""
    message: str = Field(..., description="Success message")
    question_id: str = Field(..., description="Deleted question ID")


class BulkDeleteResponse(BaseModel):
    """Response schema for bulk deleting questions"""
    message: str = Field(..., description="Success message")
    deleted_count: int = Field(..., description="Number of questions deleted")


# ==================== Selected Questions Schemas ====================

class SelectedQuestionItem(BaseModel):
    """Schema for a selected question item"""
    question_id: str = Field(..., description="Question ID")
    question: str = Field(..., description="The question text")
    difficulty: Optional[str] = Field(None, description="Difficulty level")
    category: str = Field(..., description="Question category")
    expected_answer: str = Field(..., description="Expected answer")
    type: QuestionType = Field(..., description="Question type")
    order: int = Field(..., description="Display order")
    skill_focus: List[str] = Field(default_factory=list, description="Skills")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies")


class SaveSelectedQuestionsRequest(BaseModel):
    """Request schema for saving selected questions"""
    interview_id: str = Field(..., description="Interview ID")
    selected_question_ids: List[str] = Field(..., description="List of selected question IDs")


class SelectedQuestionsResponse(BaseModel):
    """Response schema for selected questions"""
    interview_id: str = Field(..., description="Interview ID")
    selected_questions: List[SelectedQuestionItem] = Field(..., description="Selected questions")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class SaveSelectedQuestionsResponse(BaseModel):
    """Response schema for saving selected questions"""
    message: str = Field(..., description="Success message")
    interview_id: str = Field(..., description="Interview ID")
    count: int = Field(..., description="Number of selected questions")
    selected_questions: List[SelectedQuestionItem] = Field(..., description="Selected questions")
