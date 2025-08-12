from pydantic import BaseModel
from typing import List, Optional
from app.schemas.search_schemas import SearchType

class AnswerRequest(BaseModel):
    query: str
    search_type: SearchType
    top_k: Optional[int] = 5
    file_id: Optional[str] = None

class RetrievedDocument(BaseModel):
    id: str
    content: str
    score: float

class AnswerResponse(BaseModel):
    answer: str
    context: List[RetrievedDocument]
