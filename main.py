from fastapi import FastAPI
from app.container import (
    mongo_client,
    qdrant_client,
    cohere_client,
)
from app.api.upload_api import init_upload_routes
from app.api.search_api import init_search_routes
from app.repository.mongo_repository import MongoRepository
from app.repository.qdrant_repository import QdrantRepository
from app.service.upload_service import UploadService
from app.service.search_service import SearchService
from app.constant_manager import MongoConstants
from app import container
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="Hybrid Search API")

@app.on_event("startup")
async def startup_event():
    await mongo_client.connect()
    await qdrant_client.connect()
    

    container.mongo_repo = MongoRepository(
        mongo_client.get_db(MongoConstants.DB_NAME.value)
    )
    await container.mongo_repo.create_text_index()

    qdrant_repo = QdrantRepository(qdrant_client)
    container.qdrant_repo = qdrant_repo  # THIS IS THE MISSING LINE

    container.upload_service = UploadService(
        container.mongo_repo,
        container.qdrant_repo,  # now it's not None
        cohere_client
    )

    container.search_service = SearchService(
        container.mongo_repo,
        container.qdrant_repo,
        cohere_client
    )

    app.include_router(init_upload_routes(container.upload_service))
    app.include_router(init_search_routes(container.search_service))

@app.on_event("shutdown")
async def shutdown_event():
    await mongo_client.disconnect()
    await qdrant_client.disconnect()
