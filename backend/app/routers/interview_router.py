from fastapi import APIRouter, HTTPException
from app.schemas.pydantic.interview_schema import InterviewCreate, InterviewUpdate
from app.services.interview_service import (
    create_interview,
    get_all_interviews,
    get_interview_by_id,
    update_interview,
    delete_interview,
    get_interviews_by_created_by
)


router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.post("/", summary="Create a new interview")
async def create(data: InterviewCreate):
    return await create_interview(data)

@router.get("/", summary="Get all interviews")
async def get_all():
    return await get_all_interviews()

@router.get("/{interview_id}", summary="Get interview by ID")
async def get_one(interview_id: str):
    interview = await get_interview_by_id(interview_id)
    if not interview:
        raise HTTPException(404, "Interview not found")
    return interview

@router.put("/{interview_id}", summary="Update interview")
async def update(interview_id: str, data: InterviewUpdate):
    updated = await update_interview(interview_id, data)
    if not updated:
        raise HTTPException(404, "Interview not found or no changes made")
    return updated

@router.delete("/{interview_id}", summary="Delete interview")
async def delete(interview_id: str):
    success = await delete_interview(interview_id)
    if not success:
        raise HTTPException(404, "Interview not found")
    return {"message": "Interview deleted successfully"}

@router.get("/created-by/{email}", summary="Get interviews created by a specific admin")
async def get_interviews_created_by_admin(email: str):
    return await get_interviews_by_created_by(email)
