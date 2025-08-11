from typing import List, Dict
from app.models.search_schemas import SearchRequest, SearchType
from app.models.upload_schemas import DocumentRead
from app.repository.db_repository import MongoRepository
from app.repository.vdb_repository import QdrantRepository
from app.clients.embedding_client import EmbeddingClient
from app.constant_manager import CohereConstants
import logging

logger = logging.getLogger(__name__)

class SearchService:
    """
    Service for handling both full-text and semantic search queries.
    """

    def __init__(
        self,
        mongo_repo: MongoRepository,
        qdrant_repo: QdrantRepository,
        embedding_client: EmbeddingClient
    ):
        self.mongo_repo = mongo_repo
        self.qdrant_repo = qdrant_repo
        self.embedding_client = embedding_client

    def chunk_document(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split document into overlapping chunks."""
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            
            if end < text_length:
                # Find the last period or newline in the chunk
                last_period = text[start:end].rfind('.')
                last_newline = text[start:end].rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point != -1:
                    end = start + break_point + 1
            else:
                end = text_length

            chunks.append(text[start:end].strip())
            start = end - overlap

        return chunks

    def reconstruct_document(self, chunks: List[Dict]) -> DocumentRead:
        """Reconstruct a full document from its chunks."""
        sorted_chunks = sorted(chunks, key=lambda x: x.metadata.get("chunk_idx", 0))
        full_content = " ".join(chunk.content for chunk in sorted_chunks)
        original_metadata = sorted_chunks[0].metadata.get("original_metadata", {})
        
        return DocumentRead(
            _id=sorted_chunks[0].metadata.get("doc_id"),
            content=full_content,
            metadata=original_metadata
        )

   

    async def search(self, request: SearchRequest) -> List[DocumentRead]:
        """
        Perform semantic or full-text search based on the request type.
        """
        if request.search_type == SearchType.FULL_TEXT:
            logger.debug(f"[SEARCH] Performing full-text search for: {request.query}")
            return await self.mongo_repo.full_text_search(request.query, request.top_k)

        elif request.search_type == SearchType.SEMANTIC:
            try:
                logger.debug(f"[SEARCH] Performing semantic search for: {request.query}")
                
                # Generate query embedding
                embeddings = await self.embedding_client.embed_texts([request.query],
                                                                     model_name= CohereConstants.MODEL_NAME.value, input_type= CohereConstants.INPUT_TYPE.value)
                if not embeddings or not embeddings[0]:
                    raise ValueError("Failed to generate embeddings for query.")
                
                embedding = embeddings[0]
                logger.debug(f"[SEARCH] Generated embedding length: {len(embedding)}")
                
                # Perform vector search
                results = await self.qdrant_repo.search(
                    query_vector=embedding,
                    limit=request.top_k
                )
                logger.debug(f"[SEARCH] Found {len(results)} results")

                # Process results
                documents = []
                for idx, result in enumerate(results):
                    try:
                        # Extract payload
                        payload = result.payload or {}
                        logger.debug(f"[SEARCH] Processing result {idx + 1} payload: {payload}")
                        
                        # Extract content and metadata
                        content = payload.get("content")
                        metadata = payload.get("metadata", {})
                        
                        if not content:
                            logger.warning(f"[SEARCH] No content found in result {idx + 1}")
                            continue
                        
                        # Create document
                        doc = DocumentRead(
                            _id=str(result.id),
                            content=content.strip(),
                            metadata={
                                **metadata,
                                "score": result.score
                            }
                        )
                        documents.append(doc)
                        logger.debug(f"[SEARCH] Successfully processed result {idx + 1}")

                    except Exception as e:
                        logger.error(f"[SEARCH] Error processing result {idx + 1}: {str(e)}")
                        logger.error(f"[SEARCH] Problematic payload: {result.payload}")
                        continue

                logger.debug(f"[SEARCH] Returning {len(documents)} documents")
                return documents

            except Exception as e:
                logger.error(f"[SEARCH] Semantic search failed: {str(e)}")
                raise RuntimeError(f"Semantic search failed: {e}")

        else:
            raise ValueError(f"Unsupported search type: {request.search_type}")