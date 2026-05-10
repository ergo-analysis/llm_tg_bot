import httpx
from ..core import settings

class OpenRouterClient:
    """Клиент для работы с OpenRouter API"""
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.site_url = settings.OPENROUTER_SITE_URL
        self.app_name = settings.OPENROUTER_APP_NAME

    async def chat_completion(self, messages: list[dict], temperature: float = 0.7) -> str:
        """Отправка запроса к OpenRouter и получение текста ответа"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url
        if self.app_name:
            headers["X-Title"] = self.app_name

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                raise Exception(f"OpenRouter error: {e.response.status_code} - {e.response.text}")
            
            except Exception as e:
                raise Exception(
                    f"Ошибка при обращении к OpenRouter: {str(e)}")

openrouter_client = OpenRouterClient()
