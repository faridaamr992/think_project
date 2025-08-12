from pydantic import BaseModel, Field  
from typing import Optional
from enum import Enum


class SearchType(str, Enum):
    FULL_TEXT = "full_text"
    SEMANTIC = "semantic"


class SearchRequest(BaseModel):
    """
    Request schema for searching documents.

    Attributes:
        query (str): The search query text.
        search_type (SearchType): Type of search to perform.
        top_k (int): Number of results to return (default 5).
    """
    query: str = Field(..., example="machine learning in healthcare")
    search_type: SearchType = Field(..., example="semantic")
    top_k: Optional[int] = Field(default=5, example=5)
    return_full_documents: bool = False
    file_id: Optional[str] = None
