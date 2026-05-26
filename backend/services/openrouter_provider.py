import os
import requests
from dotenv import load_dotenv

load_dotenv()


def call_openrouter(system_prompt: str, user_content: str, api_key: str = None) -> str:
    key = api_key or os.getenv("OPENROUTER_API_KEY", "")
    if not key:
        raise ValueError("OpenRouter API key not configured")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/llama-3-70b-instruct:free",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "temperature": 0.7,
            "max_tokens": 1024,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
