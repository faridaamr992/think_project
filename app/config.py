from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MONGO_URI: str

    QDRANT_HOST: str
    QDRANT_PORT: int

    COHERE_API_KEY: str

    SECRET_KEY : str  
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int 


    class Config:
        env_file = ".env" 


settings = Settings()
