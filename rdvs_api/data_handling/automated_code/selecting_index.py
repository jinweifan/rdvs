"""
Name:    selecting_index
Author:  ReddyFan
Date:    2023/4/3 10:36
Desc:  
"""
import pandas as pd
import ujson

from spider.utils.cum_exception import CUMException
from store.db.db_store import get_redis, Mongo

redis = get_redis()
mongo = Mongo()


def statistics_hot_city(limit: int = 1000):

    hotCityAll = redis.get('hotCityAll2')
    hotCityAll = ujson.loads(hotCityAll) if hotCityAll and ujson.loads(hotCityAll) else {'skip': 0, 'data': {}}
    print('hotCityAll:', hotCityAll)
    try:
        skip = hotCityAll.get('skip', 0)
        skip = skip - 1 if skip else 0
        raw_data = mongo.find('job_nationwide', columns_conditions={'job_area': 1, '_id': 0},
                              skip=skip, limit=limit)
        if not raw_data:
            raise CUMException('正在数据的数据为空数据为空！')
        df = pd.DataFrame(raw_data)
        city_dt = df.job_area.map(lambda x: x.split('·')[0]).value_counts().to_dict()

        for k in city_dt:
            hotCityAll['data'][k] = hotCityAll['data'].get(k, 0) + city_dt.get(k, 0)
        hotCityAll['skip'] = hotCityAll.get('skip', 0) + limit
    except KeyboardInterrupt:
        print('键中断')
    finally:
        redis.set('hotCityAll2', ujson.dumps(hotCityAll))




if __name__ == '__main__':
    while True:
        statistics_hot_city(10000)
