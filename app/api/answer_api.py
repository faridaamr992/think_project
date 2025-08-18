from fastapi import APIRouter, HTTPException, Depends
from app.schemas.answer_schemas import AnswerRequest, AnswerResponse
from app.utils.auth_dependcies import get_current_user
from app.container import container
import uuid

router = APIRouter()

@router.post("/answer", response_model=AnswerResponse)
async def generate_answer(
    request: AnswerRequest,
    current_user = Depends(get_current_user)
):
    """
    Generate Answer with LLM
    """
    try:
        # If client provided session_id, use it
        if request.session_id:
            session_id = request.session_id
        else:
            # Otherwise create/get one automatically
            
            session_id = await container.chat_history_service.get_or_create_session(current_user.id)


        # Pass session_id explicitly
        return await container.answer_service.get_answer(request, current_user, session_id=session_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
