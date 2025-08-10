from fastapi import FastAPI,Depends
from app.api.search_api import router as search_router
from app.api.upload_api import router as upload_router
from app.api.login_api import router as login_router
from app.api.register_api import router as register_router
from app.utils.auth_dependcies import get_current_user


#Init the app
app = FastAPI(title="Hybrid Search API")

# Include upload route
app.include_router(upload_router, prefix="/upload", tags=["Upload"],dependencies=[Depends(get_current_user)])


# Include search route 
app.include_router(search_router, prefix="/search", tags=["Search"],dependencies=[Depends(get_current_user)])

app.include_router(register_router, prefix="/auth", tags=["register"])
app.include_router(login_router, prefix="/auth", tags=["login"])

