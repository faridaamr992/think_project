from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.container import container
from app.models.auth_schemas import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await container.login_service.login_user(form_data.username, form_data.password)
