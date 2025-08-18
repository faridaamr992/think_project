from app.clients.mongo_client import MongoClient

class AuthRepository:
    def __init__(self, client: MongoClient):
        self._db = client.get_client()  
        self.collection = self._db.get_collection("users")

    async def get_user_by_username(self, username: str):
        return await self.collection.find_one({"username": username})

    async def create_user(self, user_data: dict):
        await self.collection.insert_one(user_data)

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})