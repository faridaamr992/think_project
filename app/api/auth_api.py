from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.container import container
from app.schemas.auth_schemas import Token
from app.schemas.register_schemas import UserRegister

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await container.login_service.login_user(form_data.username, form_data.password)


@router.post("/register")
async def register(user: UserRegister):
    return await container.register_service.register_user(user.username, user.email, user.password)
