from typing import List
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter
from app.clients.qdrant_client import QdrantClient
from app.models.upload_schemas import UploadSchema
from app.constant_manager import QdrantConstants


class QdrantRepository:
    """
    Repository layer responsible for all vector-based operations
    on the Qdrant collection, including creating the collection,
    inserting points, and performing similarity search.
    """

    def __init__(self, qdrant_client: QdrantClient):
        """
        Initializes the repository with a connected Qdrant client.

        Args:
            qdrant_client (QdrantClient): The initialized Qdrant client wrapper.
        """
        self.qdrant = qdrant_client.get_client()

    async def create_collection(self):
        """
        Creates a Qdrant collection if it doesn't already exist.
        Uses cosine distance with a vector size of 384 (Cohere default).
        """
        if not await self.qdrant.collection_exists(QdrantConstants.COLLECTION_NAME.value):
            await self.qdrant.create_collection(
                collection_name=QdrantConstants.COLLECTION_NAME.value,
                vectors_config=VectorParams(size=QdrantConstants.VECTOR_DIM.value, distance=QdrantConstants.DISTANCE_COS.value),
            )

    async def insert_documents(self, docs: List[UploadSchema]):
        """
        Inserts a list of documents (as Qdrant points) into the vector database.

        Args:
            docs (List[UploadSchema]): List of documents containing embeddings and metadata.
        """
        points = [
            PointStruct(
                id=idx,
                vector=doc.embedding,
                payload=doc.dict(exclude={"embedding"})
            )
            for idx, doc in enumerate(docs)
        ]
        await self.qdrant.upsert(
            collection_name=QdrantConstants.COLLECTION_NAME.value,
            points=points
        )

    async def search(self, query_vector: List[float], limit: int = 5):
        """
        Performs a semantic search in the Qdrant collection using the query vector.

        Args:
            query_vector (List[float]): The embedding vector to search against.
            limit (int, optional): The maximum number of results to return. Defaults to 5.

        Returns:
            List[ScoredPoint]: A list of the closest matching documents.
        """
        return await self.qdrant.search(
            collection_name=QdrantConstants.COLLECTION_NAME.value,
            query_vector=query_vector,
            limit=limit,
        )
