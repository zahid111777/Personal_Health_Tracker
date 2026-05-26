from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.llm import LLMProviderStatus, LLMProviderUpdate, LLMTestRequest, LLMTestResponse
from services.auth_service import get_current_user
from services.llm_service import is_provider_configured, test_provider, get_available_providers
from services.encryption_service import encrypt_value

router = APIRouter(prefix="/settings", tags=["Settings"])

PROVIDERS = ["groq", "openrouter", "openai", "gemini"]


@router.get("/providers", response_model=list[LLMProviderStatus])
def get_provider_status(current_user: User = Depends(get_current_user)):
    statuses = []
    for p in PROVIDERS:
        statuses.append(LLMProviderStatus(
            provider=p,
            is_configured=is_provider_configured(p),
            is_available=is_provider_configured(p),
        ))
    return statuses


@router.put("/providers")
def update_provider_keys(
    data: LLMProviderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.groq_api_key is not None:
        current_user.encrypted_groq_key = encrypt_value(data.groq_api_key)
    if data.openrouter_api_key is not None:
        current_user.encrypted_openrouter_key = encrypt_value(data.openrouter_api_key)
    if data.openai_api_key is not None:
        current_user.encrypted_openai_key = encrypt_value(data.openai_api_key)
    if data.gemini_api_key is not None:
        current_user.encrypted_gemini_key = encrypt_value(data.gemini_api_key)
    if data.preferred_provider is not None:
        current_user.preferred_provider = data.preferred_provider
    db.commit()
    return {"message": "Provider settings updated"}


@router.post("/providers/test", response_model=LLMTestResponse)
def test_provider_endpoint(data: LLMTestRequest, current_user: User = Depends(get_current_user)):
    result = test_provider(data.provider)
    return LLMTestResponse(
        provider=data.provider,
        success=result["success"],
        message=result["message"],
    )
