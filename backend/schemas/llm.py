from pydantic import BaseModel
from typing import Optional


class LLMProviderStatus(BaseModel):
    provider: str
    is_configured: bool
    is_available: bool
    model: Optional[str] = None


class LLMProviderUpdate(BaseModel):
    groq_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    preferred_provider: Optional[str] = None


class LLMTestRequest(BaseModel):
    provider: str


class LLMTestResponse(BaseModel):
    provider: str
    success: bool
    message: str
    model_used: Optional[str] = None
