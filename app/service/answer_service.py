from app.service.search_service import SearchService
from app.clients.llm_client import LLMClient
from app.utils.prompt_builder import build_rag_prompt
from app.models.answer_schemas import AnswerRequest, AnswerResponse, RetrievedDocument
from app.constant_manager import CohereConstants
from app.models.search_schemas import SearchRequest
class AnswerService:
    def __init__(self, search_service: SearchService, llm_client: LLMClient):
        self.search_service = search_service
        self.llm_client = llm_client

    async def get_answer(self, request: AnswerRequest) -> AnswerResponse:
        # Step 1: Build a SearchRequest object from AnswerRequest
        search_request = SearchRequest(
            query=request.query,
            search_type=request.search_type,
            top_k=request.top_k
        )

        # Step 2: Retrieve documents using SearchService
        docs = await self.search_service.search(search_request)

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
            prompt,
            model=CohereConstants.MODEL_LLM_NAME.value
        )

        return AnswerResponse(answer=answer, context=retrieved_docs)

