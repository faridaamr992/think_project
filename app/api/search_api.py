from fastapi import APIRouter, HTTPException
from typing import List
from app.models.search_schemas import SearchRequest
from app.models.upload_schemas import DocumentRead
from app.container import container  # import prebuilt container

router = APIRouter()

@router.post("/search", response_model=List[DocumentRead])
async def search_documents(request: SearchRequest):
    """
    Search documents using either full-text or semantic search.
    """
    try:
        results = await container.search_service.search(request)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
