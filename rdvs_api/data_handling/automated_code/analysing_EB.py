"""
Name:    analysing_EB
Author:  ReddyFan
Date:    2023/4/2 23:17
Desc:   学历
"""
import ujson

from spider.utils.cum_exception import CUMException
from store.db.db_store import get_redis, Mongo

dt = {
    "skip": 0,
    "data": {
        '在校生': 0,
        '应届生': 0,
        '经验不限': 0,
        '1年以内': 0,
        '3-5年': 0,
        '1-3年': 0,
        '5-10年': 0,
        '10年以上': 0,
    }
}

redis = get_redis()
mongo = Mongo()


def statistics_EB(limit: int = 500):
    """ 统计经验占比 """
    dataEB = redis.get('dataEB')
    dataEB = ujson.loads(dataEB) if dataEB else dt
    print('dataEB', dataEB)
    try:
        data = mongo.find('t2_job', skip=dataEB.get('skip', 1) - 1, limit=limit)
        if not data:
            raise CUMException('表中数据统计完毕或该表为空！')
        for d in data:
            experience = d.get('job_experience', None)
            if experience in dataEB.get('data', {}).keys():
                dataEB['data'][experience] = dataEB['data'].get(experience, 0) + 1
        dataEB['skip'] = dataEB.get('skip', 0) + limit
    except KeyboardInterrupt:
        print('键中断')
    finally:
        redis.set('dataEB', ujson.dumps(dataEB))

i8

if __name__ == '__main__':









    
    while True:
        statistics_EB()

    # print('在校生' in dt['data'].keys())
