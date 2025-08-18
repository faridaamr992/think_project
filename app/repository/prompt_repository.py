# app/repository/prompt_repository.py
from app.repository.db_repository import MongoRepository

class PromptRepository:
    def __init__(self, mongo_client, collection_name: str = "prompts"):
        # Reuse your MongoRepository
        self.repo = MongoRepository(mongo_client, collection_name)

    async def get_prompt_template(self, template_id: str = "rag_prompt_v1") -> str:
        doc = await self.repo._collection.find_one({"_id": template_id})
        if not doc:
            raise ValueError(f"Prompt template {template_id} not found in MongoDB")
        return doc["template"]

    async def save_generated_prompt(self, query: str, prompt: str):
        await self.repo._collection.insert_one({
            "query": query,
            "prompt": prompt
        })
