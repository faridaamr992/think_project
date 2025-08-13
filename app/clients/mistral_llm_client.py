from openai import OpenAI
from app.domain.interfaces.llm_client_interface import ILLMClient

class MistralLLMClient(ILLMClient):
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url.rstrip("/")  
        )
        self.model = model

    async def generate_answer(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
