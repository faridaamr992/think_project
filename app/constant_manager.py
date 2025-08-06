from enum import Enum


class MongoConstants(str, Enum):
    DB_NAME = "my_database"
    COLLECTION_NAME = "documents"

class QdrantConstants(str, Enum):
    COLLECTION_NAME = "documents"
    VECTOR_DIM = 384
    DISTANCE_COS = "Cosine"
    DISTANCE_DOT = "Dot"

class CohereConstants(str,Enum):
    MODEL_NAME="embed-english-v3.0"
    INPUT_TYPE= "search_document"
    VECTOR_SIZE = 384
