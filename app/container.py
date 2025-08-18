import asyncio
from app.clients.mongo_client import MongoClient
from app.clients.qdrant_client import QdrantClient
from app.clients.embedding_client import EmbeddingClient
from app.domain.factories.llm_factory import LLMFactory
from app.repository.db_repository import MongoRepository
from app.repository.vdb_repository import QdrantRepository
from app.constant_manager import MongoConstants
from app.service.upload_service import UploadService
from app.service.search_service import SearchService
from app.repository.auth_repository import AuthRepository
from app.repository.chat_repository import ChatRepository  
from app.repository.prompt_repository import PromptRepository
from app.service.register_service import RegisterService
from app.service.login_service import LoginService
from app.service.answer_service import AnswerService 
from app.service.chat_history_service import ChatHistoryService
from app.config import settings

class Container:
    def __init__(self):
        # Clients
        self.mongo_client = MongoClient(
            uri=settings.MONGO_URI,
            db_name=MongoConstants.DB_NAME.value
        )
        self.qdrant_client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.embedding_client = EmbeddingClient(api_key=settings.COHERE_API_KEY)
        self.llm_client = LLMFactory.create()

        # Repositories
        self.mongo_repo = MongoRepository(
            self.mongo_client,
            collection_name=MongoConstants.COLLECTION_NAME.value
        )
        self.qdrant_repo = QdrantRepository(
            self.qdrant_client.get_client()
        )
        self.auth_repo = AuthRepository(self.mongo_client)
        self.chat_repo = ChatRepository(self.mongo_client) 
        self.prompt_repo = PromptRepository(self.mongo_client) 

        # Services
        self.upload_service = UploadService(
            self.mongo_repo, self.qdrant_repo, self.embedding_client
        )
        self.search_service = SearchService(
            self.mongo_repo, self.qdrant_repo, self.embedding_client
        )
        self.answer_service = AnswerService(
            self.search_service, self.llm_client, self.chat_repo,self.prompt_repo 
        )
        self.chat_history_service = ChatHistoryService(self.chat_repo) 
        self.register_service = RegisterService(self.auth_repo)
        self.login_service = LoginService(self.auth_repo)


container = Container()
