import pymongo
from magic_config import Config


class MongoClient:
    """
    Singleton instance of storage for accessed to MongoDB
    """
    __instance: "MongoClient" = None
    __client: pymongo = None
    __db: str = None

    def __new__(cls, *args, **kwargs):
        """
        Create singleton instance of MongoClient
        @param args:
        @param kwargs:
        """
        if not cls.__instance:
            cls.__instance = super(MongoClient, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        """
        Constructor
        """
        self.__client = pymongo.MongoClient(Config.mongo_url)
        self.__db = self.__client[Config.MongoStorage.db_name]

    def __call__(self, collection):
        """
        Call mongo client as function constructor like
        @param collection:
        @return:
        """
        return self.__db[collection]

    @property
    def db(self):
        """
        Get database
        @return:
        """
        return self.__db


# Initiate storage instance singleton
Storage = MongoClient()
