import httpx
from ..core.config import settings

class OllamaClient:
    def __init__(self):
        self.url = settings.OLLAMA_URL
        self.model = settings.MODEL_NAME
        self.system_prompt = settings.SYSTEM_PROMPT

    async def extract_invoice_data(self, content: str) -> str:
        payload = {
            "model": self.model,
            "system": self.system_prompt,
            "prompt": content,
            "stream": False,
            "format": "json"
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(self.url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Ollama Error: {e.response.status_code}")
            except httpx.RequestError as e:
                raise Exception(f"Connection Error with Ollama: {str(e)}")