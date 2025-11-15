from fastapi import APIRouter, Depends, Query, Path

from app.database import get_db
from app.services.question_service import SelectedQuestionsService
from app.services.qs_generator_service import QuestionService
from app.schemas.pydantic.question_schemas import (
    # Request schemas
    UpdateQuestionRequest,
    SaveSelectedQuestionsRequest,
    # Response schemas
    UpdateQuestionResponse,
    DeleteQuestionResponse,
    SelectedQuestionsResponse,
    SaveSelectedQuestionsResponse,
)



question_router = APIRouter(prefix="/questions", tags=["Questions"])



def get_question_service(db=Depends(get_db)) -> QuestionService:
    """Dependency to get QuestionService instance"""
    return QuestionService(db)


def get_selected_service(db=Depends(get_db)) -> SelectedQuestionsService:
    """Dependency to get SelectedQuestionsService instance"""
    return SelectedQuestionsService(db)


# ==================== CREATE Endpoints ====================

@question_router.post(
    "/selected",
    response_model=SaveSelectedQuestionsResponse,
    status_code=201,
    summary="Save Selected Questions",
    description="Save/update the selected questions for an interview"
)
async def save_selected_questions(
    request: SaveSelectedQuestionsRequest,
    service: SelectedQuestionsService = Depends(get_selected_service)
):
    """
    Save or update the selected questions for an interview.
    Questions will be ordered according to the provided list.

    Request body:
    - interview_id: Interview ID
    - selected_question_ids: Ordered list of question IDs
    """
    return await service.save_selected_questions(
        interview_id=request.interview_id,
        selected_ids=request.selected_question_ids,
    )

# ==================== READ Endpoints ====================

@question_router.get(
    "/selected/{interview_id}",
    response_model=SelectedQuestionsResponse,
    summary="Get Selected Questions",
    description="Get the selected questions for an interview"
)
async def get_selected_questions(
    interview_id: str = Path(..., description="Interview ID"),
    service: SelectedQuestionsService = Depends(get_selected_service)
):
    """
    Retrieve the selected questions for a specific interview.
    Returns empty list if no questions have been selected.
    """
    return await service.get_selected_questions(interview_id)



# ==================== UPDATE Endpoints ====================


@question_router.put(
    "/{question_id}",
    response_model=UpdateQuestionResponse,
    summary="Update Question",
    description="Update an existing question by ID"
)
async def update_question(
    question_id: str = Path(..., description="Unique question ID"),
    update_data: UpdateQuestionRequest = ...,
    service: QuestionService = Depends(get_question_service)
):
    """
    Update a question's fields. Only provided fields will be updated.
    Returns 404 if question not found.

    Updatable fields:
    - question: Question text
    - category: Category
    - expected_answer: Expected answer
    - difficulty: Difficulty level
    - title: Title
    - skill_focus: Skills list
    - tech_stack: Technologies list
    - metadata: Additional data
    - is_active: Active status
    """
    return await service.update_question(question_id, update_data)


# ==================== DELETE Endpoints ====================


@question_router.delete(
    "/selected/{interview_id}",
    response_model=DeleteQuestionResponse,
    summary="Delete Selected Questions",
    description="Remove the selected questions for an interview"
)
async def delete_selected_questions(
    interview_id: str = Path(..., description="Interview ID"),
    service: SelectedQuestionsService = Depends(get_selected_service)
):
    """
    Delete the selected questions for a specific interview.
    This does not delete the actual questions, only the selection.
    """
    result = await service.delete_selected_questions(interview_id)
    return result



