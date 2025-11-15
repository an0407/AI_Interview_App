from fastapi import APIRouter, Depends, Query, Path
from typing import Optional

from app.database import get_db
from app.services.qs_generator_service import QuestionService
from app.schemas.pydantic.question_schemas import (
    # Request schemas
    CreateManualQuestionRequest,
    GenerateAIQuestionsRequest,
    # Response schemas
    QuestionResponse,
    QuestionListResponse,
    CreateQuestionResponse,
    BulkCreateQuestionsResponse,
    DeleteQuestionResponse,
    BulkDeleteResponse,
)


question_generator_router = APIRouter(prefix="/questions", tags=["Questions Generator"])


def get_question_service(db=Depends(get_db)) -> QuestionService:
    """Dependency to get QuestionService instance"""
    return QuestionService(db)


@question_generator_router.post(
    "/manual",
    response_model=CreateQuestionResponse,
    status_code=201,
    summary="Create Manual Question",
    description="Create a single manual interview question"
)
async def create_manual_question(
    request: CreateManualQuestionRequest,
    service: QuestionService = Depends(get_question_service)
):
    """
    Create a manual question with the following fields:
    - interview_id: ID of the interview
    - question: The question text
    - category: Question category
    - expected_answer: Expected answer
    - difficulty: Optional difficulty level
    - Additional metadata fields
    """
    return await service.create_manual_question(request)


@question_generator_router.post(
    "/ai/generate",
    response_model=BulkCreateQuestionsResponse,
    status_code=201,
    summary="Generate AI Questions",
    description="Generate multiple questions using AI/LLM"
)
async def generate_ai_questions(
    request: GenerateAIQuestionsRequest,
    service: QuestionService = Depends(get_question_service)
):
    """
    Generate AI questions with parameters:
    - interview_id: ID of the interview
    - title: Interview title/role
    - difficulty_level: easy, moderate, or hard
    - count: Number of questions (1-50)
    - specific_skill_focus: Optional skill focus
    - technology_stack: List of technologies
    """
    return await service.generate_ai_questions(request)



@question_generator_router.get(
    "/",
    response_model=QuestionListResponse,
    summary="Get All Questions",
    description="Get all questions with optional filters and pagination"
)
async def get_all_questions(
    interview_id: Optional[str] = Query(None, description="Filter by interview ID"),
    type: Optional[str] = Query(None, description="Filter by type (ai or manual)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    service: QuestionService = Depends(get_question_service)
):
    """
    Get all questions with optional filtering and pagination.

    Query Parameters:
    - interview_id: Filter by interview
    - type: Filter by question type (ai/manual)
    - category: Filter by category
    - difficulty: Filter by difficulty level
    - is_active: Filter active/inactive questions
    - skip: Pagination offset
    - limit: Maximum results to return
    """
    from app.schemas.pydantic.question_schemas import QuestionFilters

    filters = QuestionFilters(
        interview_id=interview_id,
        type=type,
        category=category,
        difficulty=difficulty,
        is_active=is_active,
        skip=skip,
        limit=limit,
    )

    return await service.get_all_questions(filters)


@question_generator_router.get(
    "/interview/{interview_id}",
    response_model=QuestionListResponse,
    summary="Get Questions by Interview ID",
    description="Get all questions for a specific interview"
)
async def get_questions_by_interview(
    interview_id: str = Path(..., description="Interview ID"),
    type: Optional[str] = Query(None, description="Filter by type (ai or manual)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    service: QuestionService = Depends(get_question_service)
):
    """
    Get all questions associated with a specific interview.
    Optionally filter by question type (ai or manual).
    """
    return await service.get_questions_by_interview_id(
        interview_id=interview_id,
        question_type=type,
        skip=skip,
        limit=limit,
    )


@question_generator_router.get(
    "/{question_id}",
    response_model=QuestionResponse,
    summary="Get Question by ID",
    description="Retrieve a single question by its unique ID"
)
async def get_question_by_id(
    question_id: str = Path(..., description="Unique question ID"),
    service: QuestionService = Depends(get_question_service)
):
    """
    Get a specific question by its question_id.
    Returns 404 if question not found.
    """
    return await service.get_question_by_id(question_id)




@question_generator_router.delete(
    "/interview/{interview_id}",
    response_model=BulkDeleteResponse,
    summary="Delete All Questions for Interview",
    description="Delete all questions associated with an interview"
)
async def delete_questions_by_interview(
    interview_id: str = Path(..., description="Interview ID"),
    service: QuestionService = Depends(get_question_service)
):
    """
    Permanently delete all questions for a specific interview.

    Warning: This action cannot be undone.
    """
    return await service.delete_questions_by_interview_id(interview_id)


@question_generator_router.delete(
    "/{question_id}",
    response_model=DeleteQuestionResponse,
    summary="Delete Question",
    description="Permanently delete a question by ID"
)
async def delete_question(
    question_id: str = Path(..., description="Unique question ID"),
    service: QuestionService = Depends(get_question_service)
):
    """
    Permanently delete a question from the database.
    Returns 404 if question not found.

    Warning: This action cannot be undone. Consider using deactivate instead.
    """
    return await service.delete_question(question_id)