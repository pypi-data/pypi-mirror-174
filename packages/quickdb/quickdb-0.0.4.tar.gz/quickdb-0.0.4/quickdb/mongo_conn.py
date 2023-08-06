"""
    MongoConn：一个实例一个连接
"""
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoConn:
    def __init__(self, host: str, port: int):
        """

        :param host: ip
        :param port: 端口
        """
        self.host = host
        self.port = port

        self.conn = MongoClient(self.host, self.port)
        self.conn_map = {}

    def get_collection(self, db: str, col: str) -> Collection:
        """
        获取集合连接

        :param db: 库名
        :param col: 集合名
        :return:
        """
        if db not in self.conn_map:
            self.conn_map[db] = {}

        if col not in self.conn_map[db]:
            self.conn_map[db][col] = self.conn[db][col]

        return self.conn_map[db][col]

    def close(self):
        """
        关闭连接

        :return:
        """
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()