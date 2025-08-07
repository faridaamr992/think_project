from fastapi import APIRouter, HTTPException
from app.models.search_schemas import SearchRequest
from app.models.upload_schemas import DocumentRead
from app.service.search_service import SearchService
from typing import List

router = APIRouter(prefix="/search", tags=["Search"])


def init_search_routes(search_service: SearchService):
    @router.post("/search", response_model=List[DocumentRead])
    async def search_documents(request: SearchRequest):
        """
        Search documents using either full-text or semantic search.
        """
        try:
            results = await search_service.search(request)
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
