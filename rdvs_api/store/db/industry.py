"""
Name:    industry
Author:  ReddyFan
Date:    2023/4/4 16:29
Desc:  
"""
from typing import Union, Dict, List

import ujson

from store.db.db_store import Mongo, get_redis

mongo = Mongo()
redis = get_redis()


def query_industry_data() -> Union[List, None]:
    return ujson.loads(redis.get('fontEnd:industry_data'))
