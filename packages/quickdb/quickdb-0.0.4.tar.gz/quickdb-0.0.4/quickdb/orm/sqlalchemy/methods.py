"""
    SQL 方法类

    示例：
        engine = MysqlSQLAlchemyEngine(host='localhost', port=3306, user='root', pwd='1234', db='test')

        method = MysqlSQLAlchemyMethods(engine=engine)

        # 案例 1
        method = MysqlSQLAlchemyMethods(engine=engine)
        with method.engine.session as session, session.begin():
            session.xxxx    # session 操作
            method.xxxx     # method 操作

        # 案例 2
        method.reverse_table_model(path='./modules.py', tables=[])
        res = method.execute(sql='select * from table', fetchone=True, back_dict=True)

    注意：
        with self.engine.session() as session：(自动关闭 session)
            with session.begin():   (自动提交回滚捕获错误)

        同时使用：
            with self.engine.session() as session, session.begin():
                session 会自动关闭
                session.begin 可以自动捕获错误，自动回滚，自动提交

        如果是 Table 类，那可能不起作用
"""
import os
from pathlib import Path
from copy import deepcopy
from typing import List, Union
from sqlalchemy.engine import Result, Row
from sqlalchemy.orm import declarative_base
from quickdb.orm.sqlalchemy.exception import SuffixError
from quickdb.orm.sqlalchemy.engine import SQLAlchemyEngineBase

BaseModel = declarative_base()


# 方法执行类
class SQLAlchemyMethodsBase:
    def __init__(self, engine: SQLAlchemyEngineBase):
        self.engine = engine

    def reverse_table_model(self, path: str, tables: List[str] = None, commands: str = None):
        """
        逆向表模型

        注意：pip install sqlacodegen

        注意，若生成的是 Table 而不是 class 类，有以下 3 种情况
            1、表无主键
            2、表是其他表之间的关联表
            3、使用了 -noclasses 参数

        :param path: 最终生成的 models.py 文件路径
        :param tables: 需要逆向的表，默认是所有表
        :param commands: 其他命令
        :return:
        """
        if Path(path).suffix != '.py':
            raise SuffixError(f'请输入文件路径，而非文件夹路径，输入：{path}')

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        conn_url = self.engine.conn_url.render_as_string(hide_password=False)  # 将 url 类转换为 url 字符串

        command = f"sqlacodegen {conn_url} > {path}"

        if tables:
            command += f" --tables {','.join(tables)}"

        if commands:
            command += f" {commands}"

        os.system(command)

    def insert_one(self, instance: BaseModel):
        """
        插入一条信息

        :param instance: 模型类
        :return:
        """
        with self.engine.session() as session, session.begin():
            session.add(instance)

    def insert_many(self, instance_list: List[BaseModel]):
        """
        插入多条

        :param instance_list: 模型类列表
        :return:
        """
        with self.engine.session() as session, session.begin():
            session.add_all(instance_list)

    def merge(self, instance, load: bool = True, options=None):
        """
        根据主键 upsert

        :param instance: 模型类
        :param load:
        :param options:
        :return:
        """
        with self.engine.session() as session, session.begin():
            session.merge(instance, load, options)

    def execute(self, sql: str, fetchone: bool = False, fetchmany: int = None, fetchall: bool = False,
                back_dict: bool = False, **kwargs) -> Union[Result, Row, dict, List[dict], None]:
        """

        :param sql: sql
        :param fetchone: 返回一条
        :param fetchmany: 返回指定数量
        :param fetchall: 返回多条
        :param back_dict: 以字典形式返回
        :return:
        """
        with self.engine.session() as session, session.begin():
            result = session.execute(sql, **kwargs)

        if fetchone:
            back = result.fetchone()
        elif fetchmany:
            back = result.fetchmany(size=fetchmany)
        elif fetchall:
            back = result.fetchall()
        else:
            return result

        # 判断是否需要生成字典
        if back_dict and back:
            if isinstance(back, list):
                back = [dict(zip(result.keys(), i)) for i in back]
            else:
                back = dict(zip(result.keys(), back))

        return back

    def delete(self, instance: BaseModel):
        """
        删除数据

        :param instance:
        :return:
        """
        with self.engine.session() as session, session.begin():
            session.delete(instance)

    @staticmethod
    def _get_dict(instance: BaseModel) -> dict:
        """
        将类实例转化为字典

        :param instance:
        :return:
        """
        instance_dict = {}
        for key, value in instance.__dict__.items():
            if not key.startswith('_'):
                instance_dict[key] = value

        return instance_dict

    @staticmethod
    def _get_update_data(instance_dict: dict, update_keys: List[str], exclude_keys: List[str]) -> dict:
        """
        获取更新的数据

        :param instance_dict: 数据字典
        :param update_keys: 需要更新的字段
        :param exclude_keys: 需要排除的字段
        :return:
        """
        update_dict = {}

        if not update_keys:
            update_dict = deepcopy(instance_dict)
        else:
            for key, value in instance_dict.items():
                if key in update_keys:
                    update_dict[key] = value

        if exclude_keys:
            for key in exclude_keys:
                if key in update_dict:
                    del update_dict[key]

        return update_dict
