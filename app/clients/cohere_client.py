import cohere
from app.config import settings
from app.constant_manager import CohereConstants


class CohereClient(settings):
    """
    Wrapper for the Cohere client to generate text embeddings.
    """

    def __init__(self):
        """
        Initializes the Cohere client using the API key from environment settings.
        """
        self._client = cohere.Client(api_key=settings.COHERE_API_KEY)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embeddings for a list of input texts.

        Args:
            texts (list[str]): A list of strings to embed.

        Returns:
            list[list[float]]: A list of embeddings corresponding to the input texts.
        """
        response = self._client.embed(
            texts=texts,
            model=CohereConstants.MODEL_NAME.value,
            input_type=CohereConstants.INPUT_TYPE.value,
        )
        return response.embeddings
