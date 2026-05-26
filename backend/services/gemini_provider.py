import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def call_gemini(system_prompt: str, user_content: str, api_key: str = None) -> str:
    key = api_key or os.getenv("GEMINI_API_KEY", "")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    if not key:
        raise ValueError("Gemini API key not configured")

    client = genai.Client(api_key=key)
    combined_prompt = f"{system_prompt}\n\n{user_content}"
    response = client.models.generate_content(
        model=model_name,
        contents=combined_prompt,
    )
    return response.text
