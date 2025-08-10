from typing import Optional
from app.models.upload_schemas import DocumentCreate, UploadSchema
from app.repository.db_repository import MongoRepository
from app.repository.vdb_repository import QdrantRepository
from app.clients.cohere_client import CohereClient
from app.utils.chunking import simple_chunk_text
from uuid import uuid4


class UploadService:
    def __init__(
        self,
        mongo_repo: MongoRepository,
        qdrant_repo: QdrantRepository,
        cohere_client: CohereClient
    ):
        self.mongo_repo = mongo_repo
        self.qdrant_repo = qdrant_repo
        self.cohere_client = cohere_client

    async def upload_document(self, doc: DocumentCreate):
        try:
            #create index
            await self.mongo_repo.create_text_index()
            # Step 1: Generate document ID and get metadata
            document_id = str(uuid4())
            title = doc.metadata.get("title", "Untitled")
            print("*****************************step1")

            # Step 2: Chunk text
            chunks = simple_chunk_text(doc.content)
            print("*****************************step2")
            print(f"[DEBUG] Created {len(chunks)} chunks from document")

            # Step 3: Generate embeddings for all chunks
            vectors = await self.cohere_client.embed_texts(chunks)
            print("*****************************step3")
            print(f"[DEBUG] Generated {len(vectors)} embeddings")

            # Step 4: Prepare documents for MongoDB and Qdrant
            documents_to_insert = []
            embeddings_to_insert = []

            for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
                chunk_id = str(uuid4())

                # MongoDB document
                documents_to_insert.append({
                    "content": chunk,
                    "metadata": {
                        "title": title,
                        "chunk_index": i,
                        "document_id": document_id
                    }
                })

                # Qdrant point - THIS IS THE KEY CHANGE
                embeddings_to_insert.append({
                    "id": chunk_id,
                    "vector": vector,
                    "payload": {
                        "content": chunk,  # Store the actual content!
                        "metadata": {
                            "title": title,
                            "chunk_index": i,
                            "document_id": document_id
                        }
                    }
                })

            # Insert into MongoDB
            await self.mongo_repo.insert_many(documents_to_insert)
            
            # Insert into Qdrant
            await self.qdrant_repo.insert_many(embeddings_to_insert)

            return {
                "message": f"Successfully uploaded {len(chunks)} chunks",
                "document_id": document_id
            }

        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")