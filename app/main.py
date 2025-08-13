from fastapi import FastAPI,Depends
from app.api.search_api import router as search_router
from app.api.upload_api import router as upload_router
from app.api.login_api import router as login_router
from app.api.register_api import router as register_router
from app.api.answer_api import router as answer_router
from app.api.get_files_api import router as get_files_router
from app.utils.auth_dependcies import get_current_user


#Init the app
app = FastAPI(title="Hybrid Search API")
print("CICD DONE!!")
# Include upload route
app.include_router(upload_router, prefix="/upload", tags=["Upload"],dependencies=[Depends(get_current_user)])


# Include search route 
app.include_router(search_router, prefix="/search", tags=["Search"],dependencies=[Depends(get_current_user)])

# Include answer route
app.include_router(answer_router, prefix="/answer", tags=["Answer"], dependencies=[Depends(get_current_user)])

# Include get files route 
app.include_router(get_files_router, prefix="/get_files", tags=["Get Files"], dependencies=[Depends(get_current_user)])


# Include Authentication routes
app.include_router(register_router, prefix="/auth", tags=["register"])
app.include_router(login_router, prefix="/auth", tags=["login"])

