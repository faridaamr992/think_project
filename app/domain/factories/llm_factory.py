import os
from typing import Optional
from app.domain.interfaces.llm_client_interface import ILLMClient
from app.clients.cohere_llm_client import CohereLLMClient
from app.clients.mistral_llm_client import MistralLLMClient
from app.config import settings
from app.constant_manager import CohereConstants,MistralConstants
class LLMFactory:
    @staticmethod
    def create(provider: Optional[str] = None) -> ILLMClient:
        if not provider:
            provider = settings.LLM_PROVIDER

        provider = provider.lower()

        if provider == "cohere":
            
            return CohereLLMClient(api_key=settings.COHERE_API_KEY,model=CohereConstants.MODEL_LLM_NAME)
        
        elif provider == "mistral":


            return MistralLLMClient(
                api_key=settings.MISTRAL_API_KEY,
                base_url=settings.MISTRAL_BASE_URL,
                model=MistralConstants.MODEL_LLM_NAME.value
            )

      

        raise ValueError(f"Unknown LLM provider: {provider}")
