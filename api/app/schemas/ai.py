from pydantic import BaseModel
from typing import Any, Optional


class AIGenerateRequest(BaseModel):
    prompt: str
    request_type: str  # "generate_risks", "generate_tasks", "generate_content"
    context: Optional[dict] = None


class AIGenerateResponse(BaseModel):
    success: bool
    data: list[dict[str, Any]]
    tokens_used: int
    request_type: str
