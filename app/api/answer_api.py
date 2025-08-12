from fastapi import APIRouter, HTTPException
from app.models.answer_schemas import AnswerRequest, AnswerResponse
from app.container import container

router = APIRouter()

@router.post("/answer", response_model=AnswerResponse)
async def generate_answer(request: AnswerRequest):
    """
    Generate an AI answer based on indexed documents (RAG).
    """
    try:
        return await container.answer_service.get_answer(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
