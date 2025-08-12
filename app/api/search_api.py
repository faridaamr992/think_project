from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.search_schemas import SearchRequest
from app.schemas.upload_schemas import DocumentRead
from app.container import container
from app.utils.auth_dependcies import get_current_user  # adjust import path

router = APIRouter()

@router.post("/search", response_model=List[DocumentRead])
async def search_documents(
    request: SearchRequest,
    current_user = Depends(get_current_user)
):
    """
    Search documents using either full-text or semantic search.
    The user_id filter is added internally.
    """
    try:
        results = await container.search_service.search(request, current_user)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
