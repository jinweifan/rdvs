"""
Name:    common
Author:  ReddyFan
Date:    2023/4/20 17:41
Desc:  
"""
import re
from typing import Union, Dict

import ujson

from store.db.db_store import Mongo, get_redis

mongo = Mongo()
redis = get_redis()


def query_city() -> Union[Dict, None]:
    city = ujson.loads(redis.get('city'))
    return city


def query_relation_content(searchString: str):
    return  mongo.find(
        't2_company',
        {'company_name': re.compile(f'{searchString}')},
        {'company_name': 1, '_id': 0},
        limit=10
    )


if __name__ == '__main__':
    print(query_relation_content('阿里'))
