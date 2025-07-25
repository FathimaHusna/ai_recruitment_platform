import openai
import logging

logger = logging.getLogger(__name__)

class OpenAIClient:
    """Wrapper for OpenAI API client."""
    def __init__(self, api_key: str):
        """Initialize the OpenAI client with the provided API key."""
        self.client = openai.OpenAI(api_key=api_key)

    def generate_text(self, prompt: str, context: str = "", model: str = "gpt-3.5-turbo", max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using the OpenAI API."""
        try:
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating text with OpenAI API: {e}")
            raise