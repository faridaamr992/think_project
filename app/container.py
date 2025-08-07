from app.clients.mongo_client import MongoClient
from app.clients.qdrant_client import QdrantClient
from app.clients.cohere_client import CohereClient
from app.repository.mongo_repository import MongoRepository
from app.repository.qdrant_repository import QdrantRepository

# Initialize clients only
mongo_client = MongoClient()
qdrant_client = QdrantClient()
cohere_client = CohereClient()

# Repos and services will be initialized in startup
mongo_repo = None
qdrant_repo = None
upload_service = None
search_service = None

mongo_repo = None
qdrant_repo = None


