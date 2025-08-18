import uuid
from datetime import datetime, timedelta
from app.repository.chat_repository import ChatRepository

class ChatHistoryService:
    def __init__(self, chat_repo: ChatRepository, expiry_minutes: int = 30):
        self.chat_repo = chat_repo
        self.expiry_minutes = expiry_minutes

    async def get_or_create_session(self, user_id: str) -> str:
       

        # Step 1: create new session
        new_session_id = str(uuid.uuid4())
        await self.chat_repo.create_session(user_id, new_session_id)
        return new_session_id
