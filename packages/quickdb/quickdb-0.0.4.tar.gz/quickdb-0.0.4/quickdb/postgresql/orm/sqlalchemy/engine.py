"""
    pg 连接类

    engine = PostgreSQLAlchemyEngine(host='localhost', port=5432, user='postgres', pwd='1234', db='postgres')
    method = MysqlSQLAlchemyMethods(engine=engine)
"""
from quickdb.orm.sqlalchemy.engine import SQLAlchemyEngineBase


class PostgreSQLAlchemyEngine(SQLAlchemyEngineBase):
    def __init__(self, host: str, port: int, user: str, pwd: str, db: str, **kwargs):
        """

        :param host: ip
        :param port: port
        :param user: 账号
        :param pwd: 密码
        :param db: 对应的数据库
        :param kwargs: 其余 SQLAlchemy 参数
        """
        super().__init__('postgresql+psycopg2', host, port, user, pwd, db, **kwargs)
