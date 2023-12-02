"""
Name:    charts
Author:  ReddyFan
Date:    2023/4/3 18:18
Desc:  
"""
import re
import time

import ujson
from bson import SON, ObjectId

from store.db.db_store import Mongo, get_redis

mongo = Mongo()
redis = get_redis()


def query_salary_range(
        industryQuery: str = r'[\s\S]*',
        cityQuery: str = r'[\s\S]*',
):
    """ 查询薪资范围 """
    level = 0 if industryQuery == r'[\s\S]*' else len(industryQuery.split('&'))
    print(industryQuery, cityQuery)
    data = tuple(mongo.db['t2_job'].aggregate([
        {'$match': {'third_industry': re.compile(f'^{industryQuery}'), 'city': re.compile(fr'^{cityQuery}')}},
        {'$group': {
            '_id': '$' + ['first_industry', 'second_industry', 'industry', 'industry'][level],
            'mean': {'$avg': '$salary_low'},
            'max': {'$max': '$salary_low'},
            'min': {'$min': '$salary_low'},
        }
        },
        {
            '$project': {
                '_id': 0,
                'industry': '$_id',
                'mean': {'$floor': "$mean"},
                'max': {'$floor': "$max"},
                'min': {'$floor': "$min"},
            }
        },
        {'$sort': SON({'mean': -1})},
        {'$limit': 8}
    ]))
    dt = {}
    for i in data:
        dt['columns'] = dt.get('columns', []) + [i.get('industry')]
        dt['max'] = dt.get('max', []) + [int(i.get('max')) if i.get('max') else 0]
        dt['min'] = dt.get('min', []) + [int(i.get('min')) if i.get('min') else 0]
        dt['mean'] = dt.get('mean', []) + [int(i.get('mean')) if i.get('mean') else 0]
    print(dt)
    return dt


def query_company_salary_range(company_id: str):
    """ 查询薪资范围 """
    data = tuple(mongo.db['t2_job'].aggregate([
        {'$match': {
            'company_id': ObjectId(company_id),
            'industry': {"$exists": True}
        }
        },
        {'$group': {
            '_id': '$industry',
            'mean': {'$avg': '$salary_low'},
            'max': {'$max': '$salary_low'},
            'min': {'$min': '$salary_low'},
        }
        },
        {
            '$project': {
                '_id': 0,
                'industry': '$_id',
                'mean': {'$floor': "$mean"},
                'max': {'$floor': "$max"},
                'min': {'$floor': "$min"},
            }
        },
        {'$sort': SON({'mean': -1})},
        {'$limit': 8}
    ]))
    dt = {}
    for i in data:
        dt['columns'] = dt.get('columns', []) + [i.get('industry')]
        dt['max'] = dt.get('max', []) + [int(i.get('max')) if i.get('max') else 0]
        dt['min'] = dt.get('min', []) + [int(i.get('min')) if i.get('min') else 0]
        dt['mean'] = dt.get('mean', []) + [int(i.get('mean')) if i.get('mean') else 0]
    print(dt)
    return dt


def query_account_size() -> int:
    """ 获取系统数据量 """
    return mongo.count('t2_job')


def query_data_added_day() -> int:
    """ 获取系统每日新增数据量 """
    currentDate = time.strftime("%Y-%m-%d", time.localtime())
    print(currentDate)
    return mongo.count('t2_job', {'crawled_time': {'$regex': f'^{currentDate}'}})


def query_experience_data(industryQuery: str = r'[\s\S]*', cityQuery: str = r'[\s\S]*'):
    """ 工作经验占比 """
    query = industryQuery.replace('+', '\+')
    return tuple(mongo.db['t2_job'].aggregate([
        {'$match': {'third_industry': re.compile(fr'^{query}'), 'city': re.compile(fr'^{cityQuery}')}},
        {'$group': {'_id': '$job_experience', 'value': {'$sum': 1}}},
        {'$project': {'_id': 0, 'name': '$_id', 'value': 1}},
        {'$sort': SON({'value': -1})},
        {'$limit': 8}
    ]))


def query_company_experience_data(company_id: str):
    """ 企业工作经验占比 """
    return tuple(mongo.db['t2_job'].aggregate([
        {'$match': {'company_id': ObjectId(company_id)}},
        {'$group': {'_id': '$job_experience', 'value': {'$sum': 1}}},
        {'$project': {'_id': 0, 'name': '$_id', 'value': 1}},
        {'$sort': SON({'value': -1})},
        {'$limit': 8}
    ]))


def query_company_vocation_data(company_id: str):
    """ 企业职位占比 """
    return tuple(mongo.db['t2_job'].aggregate([
        {'$match': {'company_id': ObjectId(company_id),
                    'industry': {"$exists": True}}},
        {'$group': {'_id': '$industry', 'value': {'$sum': 1}}},
        {'$project': {'_id': 0, 'name': '$_id', 'value': 1}},
        {'$sort': SON({'value': -1})},
        {'$limit': 8}
    ]))


def query_hot_city():
    """ 查询热门城市TOP """
    return sorted([{"name": i[0], "value": i[1]} for i in ujson.loads(redis.get('hotCity:all')).get('data', {}).items()
                   if i[1]], key=lambda x: x['value'])
    # return tuple(mongo.db['t2_job'].aggregate([
    #     {'$group': {'_id': '$city', 'value': {'$sum': 1}}},
    #     {'$project': {'_id': 0, 'name': '$_id', 'value': 1}},
    #     {'$sort': SON({'value': -1})},
    #     {'$limit': 8}
    # ]))


def query_hot_industry(industryQuery: str = r'[\s\S]*', cityQuery: str = r'[\s\S]*'):
    """ 查询热门行业 """
    return tuple(mongo.db['t2_job'].aggregate([
        {'$match': {'third_industry': re.compile(fr'^{industryQuery}'), 'city': re.compile(fr'^{cityQuery}')}},
        {'$group': {'_id': '$brand_industry', 'value': {'$sum': 1}}},
        {'$project': {'_id': 0, 'name': '$_id', 'value': 1}},
        {'$sort': SON({'value': -1})},
        {'$limit': 100}
    ]))


def query_skills(query: str = None):
    """ 查询技能 """
    if query:
        return list(mongo.db['t2_job'].find({'third_industry': re.compile(fr'^{query}')}, {'_id': 0, 'skills': 1}))
    else:
        return ujson.loads(redis.get('skills'))


if __name__ == '__main__':
    # print(mongo.find('t2_job', columns_conditions={'third_industry': 1, '_id': 0}))
    # 人事/财务/行政&人力资源&HRBP
    # data = query_hot_industry('人事/财务/')
    # print(len(data), data)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(list(query_skills('运营')))
    print(len('运营'.split('&')))
    print(len('运营&'.split('&')))
    print(query_salary_range('运营'))
    print(query_salary_range('运营&'))
    # print(re.fullmatch(re.compile(r'[\s\S]*'), '132'))
    # ls = list(mongo.db['t2_job'].find({}, {'_id': 0, 'skills': 1}))
    # print(ls)
    # redis.set('skills', ujson.dumps(ls))
