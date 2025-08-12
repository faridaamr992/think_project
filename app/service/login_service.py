from fastapi import HTTPException, status
from app.repository.auth_repository import AuthRepository
from app.utils.jwt_handler import verify_password, create_access_token

class LoginService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def login_user(self, username: str, password: str):
        user = await self.auth_repo.get_user_by_username(username)
        if not user or not verify_password(password, user.get("hashed_password", "")):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
