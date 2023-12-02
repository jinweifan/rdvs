"""
Name:    company
Author:  ReddyFan
Date:    2023/4/2 09:52
Desc:  
"""
import re

from bson import ObjectId

from store.db.db_store import Mongo

mongo = Mongo()


def id_to_str(dt):
    dt['_id'] = str(dt.get('_id', None))
    return dt


def get_job_list(
        skip: int = 0,
        limit: int = 20,
        industryQuery: str = r'[\s\S]*',
        cityQuery: str = r'[\s\S]*',
):
    try:
        job_list = mongo.find(
            table_name='t2_job',
            query_conditions={
                'third_industry': re.compile(f'^{industryQuery}'), 'city': re.compile(fr'^{cityQuery}')
            },
            columns_conditions={
                '_id': 1,
                'job_name': 1,
                'job_experience': 1,
                'job_degree': 1,
                'boss_name': 1,
                'brand_name': 1,
                'salary': 1,
                'brand_industry': 1,
                'job_area': 1,
                'pub_time': 1,
            },
            skip=skip,
            limit=limit
        )

        total = mongo.count('t2_job')
        print('total', total)
        job_list = list(map(id_to_str, job_list))
    except AttributeError:
        return None

    return job_list, total


def get_job(_id: str):
    one = mongo.find_one('t2_job',
                         {'_id': ObjectId(_id)},
                         {
                             '_id': 0,
                             'job_name': 1,
                             'job_experience': 1,
                             'job_degree': 1,
                             'boss_name': 1,
                             'brand_name': 1,
                             'salary': 1,
                             'brand_industry': 1,
                             'job_area': 1,
                             'pub_time': 1,
                             'welfares': 1,
                             'skills': 1,
                             'details': 1})
    return one


if __name__ == '__main__':
    li = get_job_list()
    print(len(li))
    # print(str(ObjectId('64069c823b81c5145c4cdd87')))
    # print(mongo.find('t2_enterprise', limit=5))
    # print(reduce(lambda x, y: x * y, [1, 2, 3, 4]))
