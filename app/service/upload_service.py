from typing import Optional
from app.models.upload_schemas import DocumentCreate, UploadSchema
from app.repository.db_repository import MongoRepository
from app.repository.vdb_repository import QdrantRepository
from app.clients.embedding_client import EmbeddingClient
from app.utils.chunking import simple_chunk_text
from uuid import uuid4
import json
from uuid import uuid4
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.models.upload_schemas import DocumentCreate
from app.utils.chunking import simple_chunk_text
from app.constant_manager import CohereConstants


class UploadService:
    def __init__(
        self,
        mongo_repo: MongoRepository,
        qdrant_repo: QdrantRepository,
        embedding_client: EmbeddingClient
    ):
        self.mongo_repo = mongo_repo
        self.qdrant_repo = qdrant_repo
        self.embedding_client = embedding_client

    async def prepare_document(self, file: UploadFile, metadata: Optional[str]) -> DocumentCreate:
        """Read file, validate, parse metadata, and return DocumentCreate."""
        
        # File size check
        if hasattr(file, "size") and file.size and file.size > 1_000_000:
            raise HTTPException(status_code=413, detail="File too large. Max 1MB.")

        # Read and decode
        content_bytes = b""
        chunk_size = 8192
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            content_bytes += chunk

        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text")
        finally:
            await file.close()

        # Validate content length
        if len(content_str) < 10:
            raise HTTPException(status_code=400, detail="File content too short")

        # Parse metadata
        metadata_dict = {}
        if metadata:
            try:
                metadata_dict = json.loads(metadata)
                if not isinstance(metadata_dict, dict):
                    raise ValueError()
            except (json.JSONDecodeError, ValueError):
                raise HTTPException(status_code=400, detail="Invalid metadata JSON")

        # Create and return DocumentCreate
        return DocumentCreate(
            content=content_str,
            metadata={
                **metadata_dict,
                "filename": file.filename,
                "content_type": file.content_type
            }
        )

    async def upload_document(self, doc: DocumentCreate, user_id: str):
        try:
            await self.mongo_repo.create_text_index()
            document_id = str(uuid4())
            title = doc.metadata.get("title") or doc.metadata.get("filename") or "Untitled"
            file_name = doc.metadata.get("filename") or "unknown_filename.ext"

            chunks = simple_chunk_text(doc.content)
            vectors = await self.embedding_client.embed_texts(
                chunks,
                model_name=CohereConstants.MODEL_NAME.value,
                input_type=CohereConstants.INPUT_TYPE.value
            )

            documents_to_insert = []
            embeddings_to_insert = []

            for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
                chunk_id = str(uuid4())

                documents_to_insert.append({
                    "content": chunk,
                    "metadata": {
                        "title": title,
                        "filename": file_name,
                        "chunk_index": i,
                        "document_id": document_id,
                        "file_id": document_id,
                        "user_id": user_id  # <-- Add user_id here
                    }
                })

                embeddings_to_insert.append({
                    "id": chunk_id,
                    "vector": vector,
                    "payload": {
                        "file_id": document_id,
                        "content": chunk,
                        "metadata": {
                            "title": title,
                            "filename": file_name,
                            "chunk_index": i,
                            "document_id": document_id,
                            "user_id": user_id  # <-- Add user_id here as well
                        }
                    }
                })

            await self.mongo_repo.insert_many(documents_to_insert)
            await self.qdrant_repo.insert_many(embeddings_to_insert)

            return {
                "message": f"Successfully uploaded {len(chunks)} chunks",
                "document_id": document_id
            }

        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")
