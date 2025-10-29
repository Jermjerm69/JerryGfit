from pydantic import BaseModel
from typing import Any, Optional


class AIGenerateRequest(BaseModel):
    prompt: str
    request_type: str  # "caption", "hashtag", "workout_plan", "generate_risks", "generate_tasks", "content"
    model: Optional[str] = "gpt-4"  # OpenAI model to use
    context: Optional[dict] = None


class AIGenerateResponse(BaseModel):
    success: bool
    data: list[dict[str, Any]]
    tokens_used: int
    request_type: str
