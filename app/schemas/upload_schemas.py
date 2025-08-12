from pydantic import BaseModel, Field
from typing import Optional, Dict,List
from datetime import datetime

class DocumentCreate(BaseModel):
    content: str = Field(..., min_length=10, max_length=1_000_000)
    metadata: Dict = Field(default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "content": "Sample document content",
                "metadata": {
                    "title": "Sample Document",
                    "author": "John Doe"
                }
            }
        }


class DocumentRead(BaseModel):
    id: str = Field(alias='_id')  # This allows both 'id' and '_id'
    content: str
    metadata: Dict = {}
    created_at: Optional[str] = None

    class Config:
        allow_population_by_alias = True


class DocumentUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[Dict] = None

class UploadSchema(BaseModel):
    id: Optional[str]
    content: str
    metadata: dict
    embedding: List[float]