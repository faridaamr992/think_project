from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.utils.jwt_handler import verify_token
from app.container import container

security = HTTPBearer()

async def get_current_user(credentials=Depends(security)):
    token = credentials.credentials  # Extract token string
    payload = verify_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    user = await container.auth_repo.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
