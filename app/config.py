from pydantic import BaseSettings


class Settings(BaseSettings):

    MONGO_URI: str

    QDRANT_HOST: str
    QDRANT_PORT: int

    COHERE_API_KEY: str


    class Config:
        env_file = ".env"


settings = Settings()
