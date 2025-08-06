from enum import Enum


class MongoConstants(str, Enum):
    DB_NAME = "my_database"
    COLLECTION_NAME = "documents"
