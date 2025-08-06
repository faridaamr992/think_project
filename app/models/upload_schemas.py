from pydantic import BaseModel, Field
from typing import Optional, Dict,List
from datetime import datetime


class DocumentCreate(BaseModel):
    content: str
    metadata: Optional[Dict] = Field(default_factory=dict)


class DocumentRead(DocumentCreate):
    id: str = Field(..., alias="_id")
    created_at: Optional[datetime] = None


class DocumentUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[Dict] = None

class UploadSchema(BaseModel):
    id: str
    content: str
    metadata: dict
    embedding: List[float]