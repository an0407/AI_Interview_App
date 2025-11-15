from pydantic import BaseModel

class LLMResponse(BaseModel):
    questions: list
    metadata: dict