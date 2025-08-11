from pydantic import BaseModel
from typing import List, Optional
from app.models.search_schemas import SearchType

class AnswerRequest(BaseModel):
    query: str
    search_type: SearchType
    top_k: Optional[int] = 5

class RetrievedDocument(BaseModel):
    id: str
    content: str
    score: float

class AnswerResponse(BaseModel):
    answer: str
    context: List[RetrievedDocument]
