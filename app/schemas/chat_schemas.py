from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime

class ChatHistory(BaseModel):
    session_id: str
    messages: List[ChatMessage]
