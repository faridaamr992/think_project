from fastapi import FastAPI,Depends
from app.api.search_api import router as search_router
from app.api.files_api import router as file_router
from app.api.auth_api import router as auth_router
from app.api.answer_api import router as answer_router
from app.utils.auth_dependcies import get_current_user


#Init the app
app = FastAPI(title="AnswerRAG")

# Include file processing route
app.include_router(file_router, prefix="/file", tags=["files_processing"],dependencies=[Depends(get_current_user)])

# Include search route 
app.include_router(search_router, prefix="/hybrid", tags=["Search"],dependencies=[Depends(get_current_user)])

# Include answer route
app.include_router(answer_router, prefix="/rag", tags=["Answer"], dependencies=[Depends(get_current_user)])

# Include Authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])


