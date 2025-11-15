from pydantic import BaseModel, Field
from typing import List, Optional
from app.utils.objectid import PyObjectId

class EvaluationCriteria(BaseModel):
    technical_knowledge: int
    problem_solving: int
    communication_skills: int
    code_quality: int
    creativity_innovation: int

class InterviewCreate(BaseModel):
    interview_id: Optional[str] = None
    title: str
    interview_date: str
    due_date: Optional[str]
    start_time: str
    duration: int
    difficulty_level: str

    evaluation_criteria: EvaluationCriteria
    domain_category: str
    specific_skill_focus: Optional[str]
    technology_stack: List[str]
    assigned_candidates: List[str]

    created_by: str

class InterviewUpdate(BaseModel):
    title: Optional[str]
    interview_date: Optional[str]
    due_date: Optional[str]
    start_time: Optional[str]
    duration: Optional[int]
    difficulty_level: Optional[str]

    evaluation_criteria: Optional[EvaluationCriteria]
    domain_category: Optional[str]
    specific_skill_focus: Optional[str]
    technology_stack: Optional[List[str]]
    assigned_candidates: Optional[List[str]]

class InterviewResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    interview_id: str
    title: str
    interview_date: str
    due_date: Optional[str]
    start_time: str
    duration: int
    difficulty_level: str

    evaluation_criteria: EvaluationCriteria
    domain_category: str
    specific_skill_focus: Optional[str]
    technology_stack: List[str]
    assigned_candidates: List[str]

    created_by: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        populate_by_name = True
