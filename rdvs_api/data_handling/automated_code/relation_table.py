"""
Name:    relation_table
Author:  ReddyFan
Date:    2023/4/10 16:53
Desc:   建立行业-企业关系表
"""
from bson import ObjectId
from pymongo import ReturnDocument

from store.db.db_store import Mongo, get_redis

mongo = Mongo()
redis = get_redis()


def create_industry_company_relation():
    skip = redis.get('skip:relation_ic')
    skip = int(skip if skip else 0)
    while True:
        job = mongo.db['t2_job'].find(None, {'_id': 0, 'company_id': 1, 'third_industry': 1}).limit(1).skip(skip)[0]

        if not job:
            print('数据不存在 或 skill字段已更新完毕！')
            break

        first, second, third = job.get('third_industry').split('&')
        industry_id = mongo.db['industry_info'].find_one({'first_industry': first,
                                                          'second_industry': second,
                                                          'third_industry': third, }, {'_id': 1}).get('_id')
        company_id = job.get('company_id')
        mongo.db['relation_industry_company'].update_one(
            {'industry_id': industry_id, 'company_id': company_id},
            {'$set': {'industry_id': industry_id, 'company_id': company_id}},
            upsert=True
        )
        skip += 1
        print(f'更新到第{skip}条数据')
        redis.set('skip:relation_ic', skip)


if __name__ == '__main__':
    create_industry_company_relation()
    # ReturnDocument.BEFORE
    # ObjectId
