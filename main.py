from fastapi import FastAPI
from app.api.search_api import router as search_router
from app.api.upload_api import router as upload_router


#Init the app
app = FastAPI(title="Hybrid Search API")

# Include upload route
app.include_router(upload_router, prefix="/upload", tags=["Upload"])


# Include search route 
app.include_router(search_router, prefix="/search", tags=["Search"])
