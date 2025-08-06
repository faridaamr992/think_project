from qdrant_client import AsyncQdrantClient
from app.config import settings


class QdrantClient(settings):
    """
    Asynchronous client manager for connecting to the Qdrant vector database.
    """

    def __init__(self):
        self._client: AsyncQdrantClient | None = None

    async def connect(self):
        """
        Initializes and connects to the Qdrant database using the provided host and port.
        """
        self._client = AsyncQdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

    async def disconnect(self):
        """
        Gracefully closes the connection to the Qdrant database.
        """
        if self._client:
            await self._client.close()

    def get_client(self) -> AsyncQdrantClient:
        """
        Returns the internal Qdrant client instance.

        Raises:
            RuntimeError: If the client has not been initialized via `connect`.
        """
        if not self._client:
            raise RuntimeError("Qdrant client not connected.")
        return self._client
