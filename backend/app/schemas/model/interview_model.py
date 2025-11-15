from typing import List, Optional, Dict, Any

def interview_model(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB doc to JSON serializable output"""
    return {
        "id": str(data["_id"]),
        "interview_id": data.get("interview_id"),
        "title": data["title"],
        "interview_date": data["interview_date"],
        "due_date": data.get("due_date"),
        "start_time": data["start_time"],
        "duration": data["duration"],
        "difficulty_level": data["difficulty_level"],
        "evaluation_criteria": data["evaluation_criteria"],
        "domain_category": data["domain_category"],
        "specific_skill_focus": data.get("specific_skill_focus"),
        "technology_stack": data["technology_stack"],
        "assigned_candidates": data["assigned_candidates"],
        "created_by": data.get("created_by"),
        "created_at": data.get("created_at"),
    }
