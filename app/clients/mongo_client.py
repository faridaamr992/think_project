from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


class MongoClient(settings):
    """
    Handles connection to MongoDB and returns database client.
    """

    def __init__(self):
        self._client = None

    async def connect(self):
        """
        Connects to the MongoDB database.
        """
        self._client = AsyncIOMotorClient(settings.MONGO_URI)

    async def disconnect(self):
        """
        Closes the MongoDB connection.
        """
        self._client.close()

    def get_database(self, db_name: str):
        """
        Returns a MongoDB database instance.

        Args:
            db_name (str): Name of the database to retrieve.

        Returns:
            AsyncIOMotorDatabase: MongoDB database object.
        """
        return self._client[db_name]
