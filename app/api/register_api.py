from fastapi import APIRouter, Depends
from app.schemas.register_schemas import UserRegister
from app.container import container

router = APIRouter()

@router.post("/register")
async def register(user: UserRegister):
    return await container.register_service.register_user(user.username, user.email, user.password)
