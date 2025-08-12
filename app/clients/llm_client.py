import cohere
from app.config import settings

class LLMClient:
    def __init__(self, api_key):
        self.client = cohere.Client(api_key=api_key)

    async def generate_answer(self, prompt: str, model):
        response = self.client.chat(
            model=model,
            message=prompt,
            max_tokens=500,
            temperature=0.3
        )
        return response.text.strip()
