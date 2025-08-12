from enum import Enum


class MongoConstants(str, Enum):
    DB_NAME = "my_database"
    COLLECTION_NAME = "documents_2"

class QdrantConstants(str, Enum):
    COLLECTION_NAME = "documents_2"
    VECTOR_DIM = 1024
    DISTANCE_COS = "Cosine"
    DISTANCE_DOT = "Dot"

class CohereConstants(str,Enum):
    MODEL_NAME="embed-english-v3.0"
    MODEL_LLM_NAME = "command-r"
    INPUT_TYPE= "search_document"
    VECTOR_SIZE = 1024
