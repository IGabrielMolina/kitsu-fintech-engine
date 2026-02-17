import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Kitsu Fintech Engine"
    API_V1_STR: str = "/api/v1"

    FINTECH_API_KEY: str = os.getenv("FINTECH_API_KEY", "your_default_secure_key")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://kitsu_brain:11434/api/generate")
    MODEL_NAME: str = "qwen2.5:14b"

    SYSTEM_PROMPT: str = """
    You are an expert accountant auditing corporate expenses.
    Your task is to extract structured information from the provided invoice or receipt text.

    STRICT Extraction Rules:
    1. vendor: Legal entity name (Inc, LLC, Ltd, etc).
    2. tax_id: The tax identification number. If not found or invalid, return null.
    3. total: The final amount to be paid as a number (use a dot for decimals).
    4. currency: 3-letter code (USD, ARS, EUR, etc).
    5. employee: Name of the person who made the purchase or the "Attention to" field.
    6. description: A very brief summary of what was purchased.

    Respond ONLY with a raw JSON object. Do not include markdown blocks or explanations.
    Format:
    {
        "vendor": "string",
        "tax_id": "string or null",
        "total": number,
        "currency": "string",
        "employee": "string",
        "description": "string"
    }
    """

settings = Settings()