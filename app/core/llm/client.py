"""LLM client for Together.ai API."""
import httpx
import json
import logging
from typing import Optional
from app.settings import get_settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with Together.ai API."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.together_api_key or ""
        self.model = self.settings.llm_model
        self.base_url = "https://api.together.xyz/v1"
        self.has_api_key = bool(self.api_key and self.api_key.strip())
        # Only include Authorization header if we have a key
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.has_api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, response_format: Optional[dict] = None) -> str:
        """Generate a response from the LLM."""
        if not self.has_api_key:
            raise ValueError("API key not configured. Cannot make LLM requests.")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.settings.llm_temperature,
            "max_tokens": self.settings.llm_max_tokens,
        }
        
        if response_format:
            payload["response_format"] = response_format
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            # Log the actual error response from the API
            error_detail = "No error details"
            try:
                error_detail = e.response.json()
            except:
                error_detail = e.response.text
            logger.error(f"LLM API error: {e}")
            logger.error(f"API Error Details: {error_detail}")
            logger.error(f"Request payload: {payload}")
            raise
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            raise
    
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        """Generate a JSON response from the LLM."""
        response_format = {"type": "json_object"}
        response = await self.generate(prompt, system_prompt, response_format)
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response was: {response}")
            raise

