from fastapi import HTTPException, status
from app.repository.auth_repository import AuthRepository
from app.utils.jwt_handler import hash_password

class RegisterService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def register_user(self, username: str, email: str, password: str):
        # Check if username exists
        if await self.auth_repo.get_user_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already exists"
            )

        # Check if email exists
        if await self.auth_repo.get_user_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already exists"
            )

        # Hash password and store user
        hashed_pwd = hash_password(password)
        user_data = {
            "username": username,
            "email": email,
            "hashed_password": hashed_pwd
        }
        await self.auth_repo.create_user(user_data)
        
        return {"msg": "User registered successfully"}

