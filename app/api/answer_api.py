from fastapi import APIRouter, HTTPException, Depends
from app.models.answer_schemas import AnswerRequest, AnswerResponse
from app.utils.auth_dependcies import get_current_user  # adjust import path as needed
from app.container import container

router = APIRouter()

@router.post("/answer", response_model=AnswerResponse)
async def generate_answer(
    request: AnswerRequest,
    current_user = Depends(get_current_user)
):
    """
    Generate an AI answer based on indexed documents (RAG).
    """
    try:
        return await container.answer_service.get_answer(request, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
