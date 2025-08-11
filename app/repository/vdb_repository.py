from typing import List,Dict
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter
from app.clients.qdrant_client import QdrantClient
from qdrant_client import AsyncQdrantClient
from app.models.upload_schemas import UploadSchema
from app.constant_manager import QdrantConstants
from app.utils.chunking import simple_chunk_text
from qdrant_client.models import ScoredPoint

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
        self.qdrant_client = qdrant_client
        

    async def count(self) -> int:
            """
            Returns the total number of vectors stored in the collection.
            Compatible with older Qdrant client versions.
            """
            try:
                result = await self.qdrant_client.count(
                    collection_name=QdrantConstants.COLLECTION_NAME.value,
                    exact=True
                )
                return result.count
            except Exception as e:
                print(f"[ERROR] Failed to count vectors: {e}")
                return -1



    async def create_collection(self):
        """
        Creates or recreates the Qdrant collection with the specified parameters.
        """
        collections = await self.qdrant_client.get_collections()
        existing = QdrantConstants.COLLECTION_NAME.value in [c.name for c in collections.collections]

        if existing:
            await self.qdrant_client.delete_collection(QdrantConstants.COLLECTION_NAME.value)

        await self.qdrant_client.recreate_collection(
            collection_name=QdrantConstants.COLLECTION_NAME.value,
            vectors_config=VectorParams(
                size=QdrantConstants.VECTOR_DIM.value,
                distance=Distance.COSINE,
            )
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
        await self.qdrant_client.upsert(
            collection_name=QdrantConstants.COLLECTION_NAME.value,
            points=points
        )

    

    async def search(self, query_vector: List[float], limit: int = 5, file_filter: dict = None) -> List[ScoredPoint]:
        """
        Performs a semantic search in the Qdrant collection using the query vector,
        optionally filtering by file_id.
        """
        try:
            query_filter = None
            if file_filter:
                query_filter = {
                    "must": [
                        {"key": "metadata.file_id", "match": {"value": str(file_filter["file_id"])}}
                    ]
                }

            results = await self.qdrant_client.search(
                collection_name=QdrantConstants.COLLECTION_NAME.value,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
                query_filter=query_filter
            )
            return results

        except Exception as e:
            raise Exception(f"Qdrant search failed: {str(e)}")



    async def insert_many(self, vectors: List[Dict]):
        """
        Insert multiple vectors into Qdrant.
        
        Args:
            vectors (List[Dict]): List of vectors with id, vector, and payload
        """
        try:
            collection_name = QdrantConstants.COLLECTION_NAME.value

            # Check if collection exists
            exists = await self.qdrant_client.collection_exists(collection_name)
            if not exists:
                print(f"[INFO] Collection '{collection_name}' not found. Creating it...")

                # Determine vector size from first item
                vector_size = len(vectors[0]["vector"])
                await self.qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                )
                print(f"[INFO] Collection '{collection_name}' created.")

            # Prepare points
            points = [
                PointStruct(
                    id=item["id"],
                    vector=item["vector"],
                    payload=item["payload"]
                )
                for item in vectors
            ]

            # Upsert points
            await self.qdrant_client.upsert(
                collection_name=collection_name,
                points=points
            )

        except Exception as e:
            print(f"[ERROR] Qdrant insert_many failed: {e}")
            raise Exception(f"Qdrant insert_many failed: {e}")
