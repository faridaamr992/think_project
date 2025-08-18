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
    MODEL_NAME="embed-multilingual-v3.0"
    MODEL_LLM_NAME = "command-r"
    INPUT_TYPE= "search_document"
    VECTOR_SIZE = 1024

class MistralConstants(str,Enum):
    MODEL_LLM_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
    INPUT_TYPE= "search_document"
    