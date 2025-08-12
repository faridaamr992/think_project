from typing import Protocol

class ILLMClient(Protocol):

    async def generate_answer(self, prompt: str) -> str:
        ...
