from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_uri = config["MONGO_DB_URI"]
        self.__database_name = config["DB_NAME"]
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        self.__client = MongoClient(self.__connection_uri)
        self.__db_connection = self.__client[self.__database_name]

    def get_db_connection(self):
        return self.__db_connection

    def get_db_client(self):
        return self.__client
