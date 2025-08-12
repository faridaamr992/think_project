from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.utils.jwt_handler import verify_token
from app.container import container
from app.models.get_user_schemas import UserSchema

security = HTTPBearer()

async def get_current_user(credentials=Depends(security)) -> UserSchema:
    token = credentials.credentials
    payload = verify_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user_data = await container.auth_repo.get_user_by_username(username)
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    user_data["_id"] = str(user_data["_id"])
    return UserSchema(**user_data)

