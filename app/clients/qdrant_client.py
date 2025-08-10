from qdrant_client import AsyncQdrantClient

class QdrantClient:
    """
    Lazy async client for Qdrant vector database.
    """

    def __init__(self, host: str, port: int):
        self._client: AsyncQdrantClient | None = None
        self._host = host
        self._port = port

    def _init_client(self):
        """Initialize Qdrant client if not already done."""
        if self._client is None:
            self._client = AsyncQdrantClient(
                host=self._host,
                port=self._port,
            )

    def get_client(self) :
        """
        Returns the internal Qdrant client instance, lazily initializing it.
        """
        self._init_client()
        return self._client

    async def disconnect(self):
        """Gracefully closes the connection."""
        if self._client:
            await self._client.close()
            self._client = None
