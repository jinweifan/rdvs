"""
Name:    handling_column
Author:  ReddyFan
Date:    2023/4/9 16:12
Desc:  
"""
from bson import ObjectId

from store.db.db_store import get_redis, Mongo

redis = get_redis()
mongo = Mongo()


def add_column_welfare():
    """ 统计公司福利 """
    skip = redis.get('skip:welfare')
    skip = int(skip if skip else 0)
    while True:
        job = mongo.db['t2_job'].find(None, {'_id': 0, 'company_id': 1, 'welfare_list': 1}).limit(1).skip(skip)[0]
        if not job:
            print('数据不存在 或 skill字段已更新完毕！')
            break
        job_welfare = job.get('welfare_list', [])[0].split('，')
        job_welfare = job_welfare if job_welfare else []
        company_id = job.get('company_id')
        company_welfare = mongo.db['t2_company'].find_one({'_id': company_id}, {'welfare': 1}).get('welfare_list',
                                                                                                   [])
        welfare_list = list(set(job_welfare + company_welfare))
        mongo.db['t2_company'].update_one({'_id': company_id}, {'$set': {'welfare': welfare_list}})
        skip += 1
        print(f'更新到第{skip}条数据')
        redis.set('skip:welfare', skip)


def add_column_skills():
    """ 统计公司技能 """
    skip = redis.get('skip:skills')
    skip = int(skip if skip else 0)
    while True:
        job = mongo.db['t2_job'].find(None, {'_id': 0, 'company_id': 1, 'skill_list': 1}).limit(1).skip(skip)[0]
        if not job:
            print('数据不存在 或 skill字段已更新完毕！')
            break
        job_skills = job.get('skill_list', [])
        company_id = job.get('company_id')
        company_skills = mongo.db['t2_company'].find_one({'_id': company_id}, {'skill_list': 1}).get('skill_list',
                                                                                                     [])
        skill_list = list(set(job_skills + company_skills))
        mongo.db['t2_company'].update_one({'_id': company_id}, {'$set': {'skill_list': skill_list}})
        skip += 1
        print(f'更新到第{skip}条数据')
        redis.set('skip:skills', skip)


def simple_salary_transform(salary: str):
    """ 简单薪资区间转换 如： 12-17K  """
    low, raw_high = salary.split('-')
    high = raw_high[:-1]
    return int(low), int(high)


def salary_range_handle(salary: str):
    """" 薪资转换函数 """
    if '薪' in salary:
        s1, r_xin = salary.split('·')
        xin = int(r_xin[:-1])
        r_low, r_high = simple_salary_transform(s1)
        low, high = round(r_low * xin / 12, 2), round(r_high * xin / 12, 2)
    elif '元' in salary:
        s1 = salary.split('/')[0]
        r_low, r_high = simple_salary_transform(s1)
        low, high = round(r_low * 20 / 1000, 2), round(r_high * 20 // 1000, 2)
    else:
        low, high = simple_salary_transform(salary)
    return round(low * 1000), round(high * 1000)


def add_column_row_high_salary():
    """ 量化字段 """
    skip = redis.get('skip:salary')
    skip = int(skip if skip else 0)
    while True:
        job = mongo.db['t2_job'].find(None, {'_id': 1, 'salary': 1 }).limit(1).skip(skip)[0]
        if not job:
            print('数据不存在 或 skill字段已更新完毕！')
            break
        job_id = job.get('_id')
        salary = job.get('salary')
        salary_low, salary_high = salary_range_handle(salary)
        mongo.db['t2_job'].update_one({'_id':ObjectId(job_id)},{'$set': {'salary_low': salary_low,'salary_high': salary_high}})
        skip += 1
        print(f'更新到第{skip}条数据')
        redis.set('skip:salary', skip)

if __name__ == '__main__':
    add_column_row_high_salary()
