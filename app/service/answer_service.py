from app.service.search_service import SearchService
from app.clients.cohere_llm_client import CohereLLMClient
from app.utils.prompt_builder import build_rag_prompt
from app.schemas.answer_schemas import AnswerRequest, AnswerResponse, RetrievedDocument
from app.constant_manager import CohereConstants
from app.schemas.search_schemas import SearchRequest
from app.schemas.get_user_schemas import UserSchema
from app.domain.factories.llm_factory import LLMFactory
from app.repository.chat_repository import ChatRepository
from app.repository.prompt_repository import PromptRepository
class AnswerService:
    def __init__(self, search_service: SearchService, llm_client, chat_repo: ChatRepository,prompt_repo: PromptRepository):
        self.search_service = search_service
        self.llm_client = llm_client
        self.chat_repo = chat_repo
        self.prompt_repo = prompt_repo

    async def get_answer(self, request: AnswerRequest, current_user: UserSchema, session_id: str) -> AnswerResponse:
        if request.provider:
            self.llm_client = LLMFactory.create(request.provider)

        # Step 1: Save the user message
        await self.chat_repo.save_message(session_id, "user", request.query)

        # Step 2: Get history
        history = await self.chat_repo.get_history(session_id)

        # 🔹 Step 2.1: Get the last user query from history (if exists)
        prev_query = None
        for msg in reversed(history):
            if msg["role"] == "user":
                prev_query = msg["content"]
                break

        # 🔹 Step 2.2: Build search query using both current + previous query
        if prev_query:
            search_query = f"{prev_query} {request.query}"
        else:
            search_query = request.query

        # Step 3: Search documents
        search_request = SearchRequest(
            query=search_query,   
            search_type=request.search_type,
            top_k=request.top_k,
            file_id=request.file_id,
            user_id=current_user.id
        )
        docs = await self.search_service.search(search_request, user_id=current_user.id)

        if not docs:
            answer_text = "I don't know"
            await self.chat_repo.save_message(session_id, "assistant", answer_text)
            return AnswerResponse(answer=answer_text, context=[], history=history, session_id=session_id)

        # Step 4: Convert results
        retrieved_docs = [
            RetrievedDocument(
                id=str(doc.id),
                content=doc.content,
                score=doc.metadata.get("score", 0)
            )
            for doc in docs
        ]

        # Step 5: Build prompt (still use only current query for answer)
        prompt = await build_rag_prompt(request.query, retrieved_docs, history=history,prompt_repo=self.prompt_repo)

        # Step 6: LLM answer
        answer_text = await self.llm_client.generate_answer(prompt)

        # Step 7: Save assistant response
        await self.chat_repo.save_message(session_id, "assistant", answer_text)

        return AnswerResponse(
            answer=answer_text,
            context=retrieved_docs,
            history=history,
            session_id=session_id  
        )
