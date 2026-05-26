import os
import time
import logging
from dotenv import load_dotenv

from services.groq_provider import call_groq
from services.openrouter_provider import call_openrouter
from services.openai_provider import call_openai
from services.gemini_provider import call_gemini

load_dotenv()
logger = logging.getLogger(__name__)

PROVIDER_ORDER = ["groq", "openrouter", "gemini", "openai"]

PROVIDER_FUNCTIONS = {
    "groq": call_groq,
    "openrouter": call_openrouter,
    "openai": call_openai,
    "gemini": call_gemini,
}

PROVIDER_KEY_ENV = {
    "groq": "GROQ_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
}


def is_provider_configured(provider: str) -> bool:
    env_var = PROVIDER_KEY_ENV.get(provider, "")
    return bool(os.getenv(env_var, ""))


def get_available_providers() -> list:
    return [p for p in PROVIDER_ORDER if is_provider_configured(p)]


def call_llm(system_prompt: str, user_content: str, preferred_provider: str = "auto") -> str:
    if preferred_provider != "auto" and preferred_provider in PROVIDER_FUNCTIONS:
        providers = [preferred_provider] + [p for p in PROVIDER_ORDER if p != preferred_provider]
    else:
        providers = PROVIDER_ORDER

    last_error = None
    for provider in providers:
        if not is_provider_configured(provider):
            continue

        for attempt in range(2):
            try:
                logger.info(f"Calling LLM provider: {provider} (attempt {attempt + 1})")
                result = PROVIDER_FUNCTIONS[provider](system_prompt, user_content)
                return result
            except Exception as e:
                last_error = e
                error_str = str(e)
                logger.warning(f"Provider {provider} failed (attempt {attempt + 1}): {error_str}")
                if "429" in error_str and attempt == 0:
                    time.sleep(2)
                    continue
                break

    raise Exception(f"All LLM providers failed. Last error: {last_error}")


def test_provider(provider: str) -> dict:
    if provider not in PROVIDER_FUNCTIONS:
        return {"success": False, "message": f"Unknown provider: {provider}"}
    if not is_provider_configured(provider):
        return {"success": False, "message": f"{provider} API key not configured"}
    try:
        result = PROVIDER_FUNCTIONS[provider](
            "You are a test assistant.",
            "Respond with exactly: 'Connection successful'"
        )
        return {"success": True, "message": result}
    except Exception as e:
        return {"success": False, "message": str(e)}
