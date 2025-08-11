import cohere
from app.config import settings
from app.constant_manager import CohereConstants


class EmbeddingClient():
    """
    Wrapper for the Embedding client to generate text embeddings.
    """

    def __init__(self,api_key):
        """
        Initializes the Embedding client using the API key from environment settings.
        """
        self.api_key=api_key
        self._client = cohere.Client(api_key=self.api_key)

    async def embed_texts(self, texts: list[str],model_name,input_type) -> list[list[float]]:
        """
        Generates embeddings for a list of input texts.

        Args:
            texts (list[str]): A list of strings to embed.

        Returns:
            list[list[float]]: A list of embeddings corresponding to the input texts.
        """
        response = self._client.embed(
            texts=texts,
            model=model_name,
            input_type=input_type,
        )
        return response.embeddings
