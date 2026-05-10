import pytest
import respx
from httpx import Response, TimeoutException
from app.services import openrouter_client 
from app.core import settings

pytestmark = pytest.mark.asyncio

class TestOpenRouterClient:
    async def test_success(self):
        expected_text = "Привет! Я LLM."
        mock_response = {
            "choices": [{"message": {"content": expected_text}}]
        }
        url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"

        async with respx.mock:
            respx.post(url).mock(return_value=Response(200, json=mock_response))

            client = openrouter_client
            answer = await client.chat_completion([{"role": "user", "content": "Привет"}])

        assert answer == expected_text

    async def test_http_error(self):
        url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"

        async with respx.mock:
            respx.post(url).mock(return_value=Response(401, json={"error": "Unauthorized"}))

            client = openrouter_client
            with pytest.raises(Exception, match="401"):
                await client.chat_completion([{"role": "user", "content": "test"}])

    async def test_network_timeout(self):
        url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"

        async with respx.mock:
            respx.post(url).mock(side_effect=TimeoutException("Connection timed out"))

            client = openrouter_client
            with pytest.raises(Exception, match="Connection timed out"):
                await client.chat_completion([{"role": "user", "content": "test"}])

    async def test_connection_error(self):
        url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"

        async with respx.mock:
            respx.post(url).mock(side_effect=Exception("Connection error"))

            client = openrouter_client
            with pytest.raises(Exception, match="Connection error"):
                await client.chat_completion([{"role": "user", "content": "test"}])
