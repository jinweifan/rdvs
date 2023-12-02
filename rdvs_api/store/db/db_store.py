"""
Name:    mongodb
Author:  ReddyFan
Date:    2023/2/10 20:35
Desc:  
"""
from typing import List, Dict

import redis
from pymongo import MongoClient

HOST = "1.116.250.241"

MONGO_USERNAME = "admin"
MONGO_PASSWORD = "melon2021"
MONGO_AUTH_DB = "admin"

REDIS_RDVS_DB = 5
REDIS_PORT = 6379
REDIS_PASSWORD = "hiker2023"


def get_redis():
    """ 获取redis代理池连接 """
    pool = redis.ConnectionPool(
        host=HOST, port=REDIS_PORT, max_connections=10, db=REDIS_RDVS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True
    )

    return redis.Redis(connection_pool=pool,
                       host=HOST, port=REDIS_PORT, max_connections=10, db=REDIS_RDVS_DB,
                       password=REDIS_PASSWORD,
                       )


class Mongo:
    """ Pymongo的封装"""

    def __init__(self):
        self.client = MongoClient(
            f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{HOST}/?authSource={MONGO_AUTH_DB}&authMechanism=SCRAM-SHA-1"
        )
        self.db = self.client['rdvs']

    def change_db(self, db_name: str):
        """
        更改指定数据库
        :param db_name: 数据库名
        :return:
        """
        self.db = self.client[db_name]

    def __del__(self):
        self.client.close()

    def insert_many(self, table_name: str, data: List[Dict]):
        """
        插入多条数据
        :param table_name: 表名
        :param data: 数据列表
        :return:
        """
        return self.db[table_name].insert_many(data)

    def distinct(self, table_name):
        return self.db[table_name].distinct()

    def insert_one(self, table_name: str, data: Dict):
        """
        插入一条数据
        :param table_name: 表名
        :param data: 数据字典
        :return:
        """
        return self.db[table_name].insert_one(data)

    def drop(self, table_name: str):
        """
        删除表
        :param table_name: 表名
        :return:
        """
        self.db[table_name].drop()

    def delete_one(self, table_name: str, conditions: Dict = {}) -> int:
        """
        删除一条数据，未给条件删除第一条数据
        :param table_name: 表名
        :param conditions: 删除条件 删除条件 {"字段"："匹配值"} or  （正则匹配：）{"字段": {"$regex": "题$"}}
        :return: 删除条数
        """
        deleted = self.db[table_name].delete_one(conditions)
        return deleted.deleted_count

    def delete_many(self, table_name: str, conditions: Dict = {}) -> int:
        """
        删除多条数据，未给条件删除所有数据
        :param table_name: 表名
        :param conditions: 删除条件 {"字段"："匹配值"} or  （正则匹配：）{"字段": {"$regex": "题$"}}
        :return: 删除条数
        """
        deleted = self.db[table_name].delete_many(conditions)
        return deleted.deleted_count

    def update_one(self, table_name: str, query_conditions: Dict = {}, new_replace_old: Dict = {}) -> int:
        """
        更新一条数据
        :param table_name: 表名
        :param query_conditions: 更新条件 {"字段"："匹配值"} or  正则匹配：{"字段": {"$regex": "题$"}}
        :param new_replace_old: 替换值  {"替换字段"："新值"}
        :return:
        """
        updated = self.db[table_name].update_one(query_conditions, {"$set": new_replace_old})
        return updated.modified_count

    def update_many(self, table_name: str, query_conditions: Dict = {}, new_replace_old: Dict = {}) -> int:
        """
        更新多条数据
        :param table_name:  表命
        :param query_conditions: 更新条件： {"字段"："匹配值"} or  （正则匹配）{"字段": {"$regex": "题$"}}
        :param new_replace_old: 替换值 {"替换字段"："新值"}
        :return:
        """
        updated = self.db[table_name].update_many(query_conditions, {"$set": new_replace_old})
        return updated.modified_count

    def find(self, table_name: str, query_conditions: dict = {}, columns_conditions: dict = {"_id": 0}, skip: int = 0,
             limit: int = 0) -> list:
        """
        查询多条数据

        :param table_name: 表名
        :param query_conditions: 查询条件
        :param columns_conditions: 过滤字段
        :param skip: 起始位置，默认起始0
        :param limit: 查询数据条数，默认为0（表示没有限制）
        :return:
        """
        return list(self.db[table_name].find(query_conditions, columns_conditions)
                    .limit(limit).skip(skip))

    def find_one(self, table_name: str, query_conditions: dict = None, columns_conditions: dict = {"_id": 0}) -> dict:
        """
        查询一条数据
        :param table_name: 表名
        :param query_conditions: 查询条件
        :param columns_conditions: 过滤字段
        :return:
        """
        return self.db[table_name].find_one(query_conditions, columns_conditions)

    def count(self, table_name: str, query_conditions: dict = None) -> int:
        """
        返回数据表总记录数
        :param query_conditions:
        :param table_name: 表明
        :return: 总记录数
        """
        if query_conditions is None:
            query_conditions = {}
        # count_documents() pymongo3.7版本以上支持
        return self.db[table_name].count_documents(query_conditions)

    def collection_names(self) -> List[str]:
        """
        列出指定默认数据库的表名
        :return:
        """
        return self.db.collection_names()


if __name__ == '__main__':
    # r = get_redis()
    # r.set("username", "reddy", ex=50)

    # r.lpush("list", *['http://114.99.9.205:4278', 'http://113.120.24.95:4256', 'http://180.120.174.41:4231',
    #                   'http://111.76.66.228:4215', 'http://1.49.231.38:4213', 'http://125.87.95.48:4256',
    #                   'http://60.185.42.104:4226', 'http://114.99.11.16:4225', 'http://122.194.122.250:4213',
    #                   'http://117.95.171.158:4264'])
    # r.expire("list", 20)

    # lrange = r.lrange("list", 0, -1)
    # print('lr', lrange)

    # get = r.get("username")
    # print(get)
    # print(r.keys())
    # print( f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{HOST}/?authSource={MONGO_AUTH_DB}&authMechanism=SCRAM-SHA-1")
    pass