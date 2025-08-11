from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson.objectid import ObjectId
from typing import Optional, List, Dict, Any
from app.clients.mongo_client import MongoClient
from app.constant_manager import MongoConstants
from app.models.upload_schemas import DocumentCreate, DocumentRead, DocumentUpdate


class MongoRepository:
    """
    Repository class for interacting with MongoDB collections and documents.

    This class provides methods to perform CRUD operations on documents,
    execute full-text search, and manage collections such as listing and dropping.
    """

    def __init__(self, client: MongoClient, collection_name):
        """
        Initialize the repository with a MongoDB database instance.

        Args:
            client(MongoClient): Costum Wrapper.
        """
        self._db = client.get_client()  
        self._collection = self._db[collection_name]
        #self._files_collection = self._db["files"]

        
    # ----------------------------
    # Document-level operations
    # ----------------------------

    async def insert_document(self, document: DocumentCreate) -> str:
        """
        Insert a document into the collection.

        Args:
            document (DocumentCreate): The document data to insert.

        Returns:
            str: The ID of the inserted document.
        """
        doc_dict = document.dict()
        result = await self._collection.insert_one(doc_dict)
        return str(result.inserted_id)

    async def get_document(self, doc_id: str) -> Optional[DocumentRead]:
        """
        Retrieve a document by its ID.

        Args:
            doc_id (str): The document's ObjectId as a string.

        Returns:
            Optional[DocumentRead]: The document if found, else None.
        """
        doc = await self._collection.find_one({"_id": ObjectId(doc_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return DocumentRead(**doc)
        return None

    async def update_document(self, doc_id: str, updates: DocumentUpdate) -> bool:
        """
        Update fields in an existing document.

        Args:
            doc_id (str): The ID of the document to update.
            updates (DocumentUpdate): The fields to update.

        Returns:
            bool: True if the document was modified, False otherwise.
        """
        update_dict = {k: v for k, v in updates.dict().items() if v is not None}
        result = await self._collection.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": update_dict}
        )
        return result.modified_count > 0

    async def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document by its ID.

        Args:
            doc_id (str): The ID of the document to delete.

        Returns:
            bool: True if the document was deleted, False otherwise.
        """
        result = await self._collection.delete_one({"_id": ObjectId(doc_id)})
        return result.deleted_count > 0

    async def full_text_search(self, query: str, top_k: int = 5, file_filter: dict = None) -> List[DocumentRead]:
        """
        Perform a full-text search on the 'content' field, optionally filtering by file_id.
        """
        filter_query = {"$text": {"$search": query}}
        if file_filter:
            filter_query.update(file_filter)

        cursor = self._collection.find(
            filter_query,
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(top_k)

        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(DocumentRead(**doc))
        return results


    async def create_text_index(self, field: str = "content") -> None:
        """
        Create a text index on the specified field.

        Args:
            field (str): The field to index (default is "content").
        """
        await self._collection.create_index([(field, "text")])

    async def insert_many(self, docs: List[Dict]):
        try:
            await self._collection.insert_many(docs)
        except Exception as e:
            raise Exception(f"Mongo insert_many failed: {e}")
        
    async def list_documents(self):
        pipeline = [
            {
                "$group": {
                    "_id": "$metadata.document_id",
                    "filename": {"$first": "$metadata.filename"},
                    "chunks": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "id": "$_id",
                    "name": "$filename",
                    "chunks": 1,
                    "_id": 0
                }
            }
        ]
        cursor = self._collection.aggregate(pipeline)
        results = []
        async for doc in cursor:
            results.append(doc)
        return results




    # -----------------------------------------
    # Collection-level operations
    # -----------------------------------------

    async def list_collections(self) -> List[str]:
        """
        List all collection names in the database.

        Returns:
            List[str]: A list of collection names.
        """
        return await self._db.list_collection_names()

    async def drop_collection(self, collection_name: str) -> None:
        """
        Drop a collection by name.

        Args:
            collection_name (str): The name of the collection to drop.
        """
        await self._db.drop_collection(collection_name)

    async def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """
        Retrieve statistics and metadata about a collection.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            Dict[str, Any]: Stats such as document count, size, etc.
        """
        return await self._db.command("collstats", collection_name)
