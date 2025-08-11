from motor.motor_asyncio import AsyncIOMotorClient

class MongoClient:
    """
    Handles lazy connection to MongoDB and returns database client.
    """

    def __init__(self, uri: str, db_name: str):
        self._client: AsyncIOMotorClient | None = None
        self._uri = uri
        self._db_name = db_name

    def _init_client(self):
        """Initialize the Mongo client if not already done."""
        if self._client is None:
            self._client = AsyncIOMotorClient(self._uri)

    def get_client(self):
        """
        Returns a MongoDB database instance.
        Lazily initializes the client if not connected yet.
        """
        self._init_client()
        return self._client[self._db_name]

    def disconnect(self):
        """Closes the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
