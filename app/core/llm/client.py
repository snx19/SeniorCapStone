"""LLM client using Together.ai for JSON-based prompts."""
import json
import asyncio
from together import Together
from app.settings import get_settings

class LLMClient:
    """Client to interact with an LLM via Together.ai."""

    def __init__(self):
        settings = get_settings()
        self.model = settings.llm_model
        self.api_key = settings.together_api_key
        self.client = Together(api_key=self.api_key)

    async def generate_json(self, prompt: str, system_prompt: str = None) -> dict:
        """
        Generate a JSON response from the LLM.

        Args:
            prompt (str): The user prompt.
            system_prompt (str, optional): System-level instructions.

        Returns:
            dict: Parsed JSON response from the LLM.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Together SDK is synchronous, wrap in async
        loop = asyncio.get_event_loop()

        def call_llm_with_retry():
            # Simple retry for temporary server issues (503)
            for _ in range(3):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    print("LLM call failed, retrying:", e)
            # If all retries fail
            raise RuntimeError("LLM request failed after 3 attempts")

        result_text = await loop.run_in_executor(None, call_llm_with_retry)

        # Attempt to parse JSON
        try:
            return json.loads(result_text)
        except json.JSONDecodeError as e:
            # Provide debugging info if JSON is invalid
            print("Failed to parse LLM response as JSON:", result_text)
            raise e