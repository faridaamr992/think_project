import cohere
from app.domain.interfaces.llm_client_interface import ILLMClient
from app.config import settings

class CohereLLMClient(ILLMClient):
    def __init__(self, api_key, model: str):
        self.client = cohere.Client(api_key=api_key)
        self.model = model
    async def generate_answer(self, prompt: str):
        response = self.client.chat(
            model=self.model,
            message=prompt,
            max_tokens=500,
            temperature=0.1
        )
        return response.text.strip()
