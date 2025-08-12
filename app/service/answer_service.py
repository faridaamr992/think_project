from app.service.search_service import SearchService
from app.clients.cohere_llm_client import CohereLLMClient
from app.utils.prompt_builder import build_rag_prompt
from app.schemas.answer_schemas import AnswerRequest, AnswerResponse, RetrievedDocument
from app.constant_manager import CohereConstants
from app.schemas.search_schemas import SearchRequest
from app.schemas.get_user_schemas import UserSchema
from app.domain.factories.llm_factory import LLMFactory

class AnswerService:
    def __init__(self, search_service: SearchService, llm_client):
        self.search_service = search_service
        self.llm_client = llm_client

    async def get_answer(self, request: AnswerRequest, current_user: UserSchema) -> AnswerResponse:

        if request.provider: 
            self.llm_client = LLMFactory.create(request.provider)

        # Step 1: Build a SearchRequest object from AnswerRequest
        search_request = SearchRequest(
            query=request.query,
            search_type=request.search_type,
            top_k=request.top_k,
            file_id=request.file_id, user_id=current_user.id
        )

        # Step 2: Retrieve documents using SearchService
        docs = await self.search_service.search(search_request, user_id=current_user.id)
        
        if not docs:
            return {
                "answer": "I don't know",
                "context": []
            }

        # Step 3: Convert results into RetrievedDocument models
        retrieved_docs = [
            RetrievedDocument(
                id=str(doc.id),
                content=doc.content,
                score=doc.metadata.get("score", 0)
            )
            for doc in docs
        ]

        # Step 4: Build RAG prompt from retrieved documents
        prompt = build_rag_prompt(request.query, retrieved_docs)

        # Step 5: Get LLM answer
        answer = await self.llm_client.generate_answer(
            prompt
        )

        return AnswerResponse(answer=answer, context=retrieved_docs)

