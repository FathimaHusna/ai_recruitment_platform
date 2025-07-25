# api_client.py
import openai
import time
from typing import Optional

class OpenAIClient:
    """Client for interacting with the OpenAI API."""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"

    def generate_text(self, prompt: str, context: str = "You are an expert HR professional.") -> Optional[str]:
        """Generate text using the OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except openai.RateLimitError:
            print("Rate limit exceeded. Retrying after 10 seconds...")
            time.sleep(10)
            return self.generate_text(prompt, context)
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return None