"""
Name:    company
Author:  ReddyFan
Date:    2023/4/2 09:52
Desc:  
"""
import re

import bson
from bson import ObjectId

from store.db.db_store import Mongo

mongo = Mongo()


def id_to_str(dt):
    dt['_id'] = str(dt.get('_id', None))
    return dt


def query_company_info_list(
        skip: int = 0,
        limit: int = 20,
        searchInput: str = r'[\s\S]*',
):
    try:
        company_list = mongo.find(
            table_name='t2_company',
            query_conditions={
                'company_name': re.compile(f'{searchInput}'),
            },
            columns_conditions={
                '_id': 1,
                'company_name': 1,
                # 'legal_person': 1,
                # 'registered_capital': 1,
                'welfare': 1
            },
            skip=skip,
            limit=limit
        )
        total = mongo.db['t2_company'].find({'company_name': re.compile(f'{searchInput}'),
                                             }).count()
        company_list = list(map(id_to_str, company_list))
    except AttributeError:
        return None

    return company_list, total


def query_company_info(company_id: str):
    try:
        company = mongo.find_one('t2_company', {'_id': ObjectId(company_id)}, {'enterprise_id': 0, 'crawled_time': 0})
    except bson.errors.InvalidId:
        return {}
    if not company:
        return {}

    company['_id'] = str(company.get('_id'))
    return company


def query_total_demand(company_id: str):
    try:
        return mongo.count('t2_job', {'company_id': ObjectId(company_id)})
    except bson.errors.InvalidId:
        return {}


if __name__ == '__main__':
    # li = get_company_info_list()
    # print(len(li))
    # print(str(ObjectId('64069c823b81c5145c4cdd87')))
    # print(mongo.find('t2_enterprise', limit=5))
    # print(reduce(lambda x, y: x * y, [1, 2, 3, 4]))
    # print(get_company_info('6406b35a3b81c5145c4cdf20'))
    pass
