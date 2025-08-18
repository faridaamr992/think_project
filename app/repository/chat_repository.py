from app.clients.mongo_client import MongoClient
from app.schemas.chat_schemas import ChatMessage
from datetime import datetime
from typing import Optional
from datetime import datetime, timedelta


class ChatRepository:
    def __init__(self, mongo_client: MongoClient):
        db = mongo_client.get_client()  
        self.collection = db["chat_history"]

    async def get_active_session(self, user_id: str, expiry_minutes: int = 30) -> Optional[dict]:
        """Find the most recent active chat session for the user that is not expired."""
        expiry_threshold = datetime.utcnow() - timedelta(minutes=expiry_minutes)

        session = await self.collection.find_one(
            {
                "user_id": user_id,
                "status": "active",
                "last_activity": {"$gte": expiry_threshold}
            },
            sort=[("last_activity", -1)]  # 👈 pick the latest
        )
        return session
    
    async def create_session(self, user_id: str, session_id: str):
        """Create a new chat session."""
        now = datetime.utcnow()
        await self.collection.insert_one({
            "user_id": user_id,
            "session_id": session_id,
            "messages": [],
            "status": "active",          
            "created_at": now,
            "last_activity": now
        })


    async def save_message(self, session_id: str, role: str, content: str):
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.utcnow()
        ).dict()

        await self.collection.update_one(
            {"session_id": session_id},
            {
                "$push": {"messages": message},
                "$set": {"last_activity": datetime.utcnow()}  # 👈 refresh
            },
            upsert=True
        )


    async def get_history(self, session_id: str, limit: int = 5):
        doc = await self.collection.find_one({"session_id": session_id})
        if not doc:
            return []
        messages = doc.get("messages", [])
        return messages[-limit:] if limit > 0 else messages
