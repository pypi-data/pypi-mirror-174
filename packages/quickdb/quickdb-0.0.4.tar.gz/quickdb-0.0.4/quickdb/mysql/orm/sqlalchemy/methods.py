"""
    MYSQL 方法类

    示例：
        method = MysqlSQLAlchemyMethods(engine=MysqlSQLAlchemyEngine())

        method.reverse_table_model(path='./modules.py', tables=[])
        res = method.execute(sql='select * from user', fetchone=True, back_dict=True)
"""
from typing import List
from sqlalchemy.engine import Result
from sqlalchemy.dialects.mysql import insert
from quickdb.orm.sqlalchemy.engine import SQLAlchemyEngineBase
from quickdb.orm.sqlalchemy.methods import SQLAlchemyMethodsBase, BaseModel


class MysqlSQLAlchemyMethods(SQLAlchemyMethodsBase):
    def __init__(self, engine: SQLAlchemyEngineBase):
        super().__init__(engine)

    def upsert_one(
            self,
            instance: BaseModel,
            update_keys: List[str] = None,
            exclude_keys: List[str] = None
    ) -> Result:
        """
        做 更新或插入 操作
        详情见：https://docs.sqlalchemy.org/en/20/dialects/postgresql.html

        index_where=my_table.c.user_email.like('%@gmail.com')

        :param instance: 数据
        :param update_keys: 需要更新的字段（无则全更）
        :param exclude_keys: 需要排除的字段（无则全更）
        :return:
        """
        instance_dict = self._get_dict(instance)  # 获取实例的字典
        update_dict = self._get_update_data(instance_dict, update_keys, exclude_keys)  # 获取需要更新的字典

        # 构造 sql 语句
        upsert_sql = insert(instance.__table__).values(instance_dict).on_duplicate_key_update(update_dict)

        return self.execute(upsert_sql)

    def upsert_many(
            self,
            instance: List[BaseModel],
            update_keys: List[str] = None,
            exclude_keys: List[str] = None
    ) -> Result:
        """
        做 更新或插入 操作（这里使用原生 sql）

        :param instance: 数据
        :param update_keys: 需要更新的字段（无则全更）
        :param exclude_keys: 需要排除的字段（无则全更）
        :return:
        """
        instance_dict = self._get_dict(instance[0])  # 获取实例的字典
        update_dict = self._get_update_data(instance_dict, update_keys, exclude_keys)  # 获取需要更新的字典

        # 构造更新的字段
        if len(instance_dict) == 1:
            instance_tuple = f'({instance_dict[0]})'
        else:
            instance_tuple = str(tuple(instance_dict.keys())).replace("'", '')

        # 构造更新的数据
        if len(instance_dict.values()) == 1:
            update_values = ','.join([f'({list(self._get_dict(i).values())[0]})' for i in instance])
        else:
            update_values = ','.join([str(tuple(self._get_dict(i).values())) for i in instance])

        # 构造 sql 语句（只是利用其构造语句）
        sql = f'''
            INSERT INTO {instance[0].__table__.name} {instance_tuple}
            VALUES
                {update_values}
                ON DUPLICATE KEY UPDATE
                {', '.join([f"{i} = values({i})" for i in update_dict.keys()])}
        '''

        # 使用原生的连接执行，否则会无法执行
        with self.engine.connect() as conn, conn.begin():
            return conn.execute(sql, [self._get_dict(i) for i in instance])
