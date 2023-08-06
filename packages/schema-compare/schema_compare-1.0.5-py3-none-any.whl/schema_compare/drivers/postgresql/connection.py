import urllib.parse
import pandas as pds
from sqlalchemy import create_engine
from sqlalchemy import text

class Connection:
    def __init__(self, username:str, password:str, hostname:str, database:str):
        self.__hostname__ = hostname
        password= urllib.parse.quote_plus(password)
        self.__uri__ = f'postgresql+psycopg2://{username}:{password}@{hostname}/{database}'
        self.__alchemyEngine__ = create_engine(self.__uri__, pool_recycle=3600)

    def __connect__(self):
        try:
            return self.__alchemyEngine__.connect()
        except Exception:
            raise Exception(f"Could not connect to database. Is {self.__hostname__} running and accepting connections?")

    def get_schema(self):
        print(f"Trying to connect to {self.__hostname__}")
        connection = self.__connect__()
        print(f"Connected to {self.__hostname__}")
        query ="select table_name, column_name from information_schema.columns c where c.table_schema = 'app' order by table_name"
        schema = pds.read_sql(text(query),connection);
        connection.close()

        return schema