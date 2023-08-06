from motor.motor_asyncio import AsyncIOMotorClient
from magic_config import Config


class MongoClient:
    """
    Asinchronous implementation of MongoClient
    Singleton instance of storage for accessed to MongoDB
    """
    __instance: "MongoClient" = None
    __client: AsyncIOMotorClient = None
    __db: str = None

    def __new__(cls, *args, **kwargs) -> "MongoClient":
        """
        Create singleton instance of MongoClient
        """
        if not cls.__instance:
            cls.__instance = super(MongoClient, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        """
        Constructor
        """
        self.__client = AsyncIOMotorClient(Config.mongo_url, serverSelectionTimeoutMS=5000)
        self.__db = self.__client[Config.mongo_db]

    def __call__(self, collection):
        """
        Call MongoClient as function constructor like
        """
        return self.__db[collection]

    @property
    def db(self):
        """
        Get access to private property
        """
        return self.__db


# Initiate storage instance singleton
Storage = MongoClient()
