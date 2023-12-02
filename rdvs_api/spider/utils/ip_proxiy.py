"""
Name:    ip_proxiy
Author:  ReddyFan
Date:    2023/2/13 14:20
Desc:  
"""
import time
from math import ceil
from multiprocessing import Semaphore, RLock

import requests
from requests import JSONDecodeError

from spider.utils.cum_exception import NoProxyException, CUMException
from store.db.db_store import get_redis

semaphore = Semaphore(4)
r_lock = RLock()


def mogu_proxies_pool(url, count=5):
    """
    获取蘑菇代理
    :param count: 获取的条数
    :param url: 蘑菇代理url
    :return: 代理池
    """
    url = url + f'&count={count}'
    semaphore.acquire()
    resp = requests.get(url)
    time.sleep(0.25)
    semaphore.release()
    proxies_pool = []
    if resp.status_code == 200:
        json = resp.json()
        if json['code'] == '0':
            for item in json['msg']:
                proxies_pool.append(f"http://{item['ip']}:{item['port']}")
            print('已获取代理池')
        elif json['code'] == '3001':
            print('appkey提取频繁，请按照所购买订单规定的频率进行合理提取。如仍未解决，建议检查相关后台进程！')
        elif json['code'] == '3002' or json['code'] == '3005':
            print('请检查订单的有效时间！')
        elif json['code'] == '3006':
            print('请检查订单的剩余数量！')
        elif json['code'] == '3004':
            print('appkey有误！')
        else:
            print('代理有误！')

    else:
        print('代理有误！')

    return proxies_pool


def zm_proxies_pool(num=1, time_len=1):
    """
    :param num: 请求条数
    :param time_len: int	按次提取必填	稳定时长 1:5-25min 2:25min-3h 3:3-6h
    :return:
    """
    r_lock.acquire()
    zm_url = f"http://http.tiqu.letecs.com/getip3?num={num}&type=2&pro=510000&city=510100&yys=0&port=1&time={time_len}&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=&gm=4"
    resp = requests.get(zm_url)
    time.sleep(2)
    r_lock.release()
    proxies_pool = []
    if resp.status_code == 200:
        json = resp.json()
        print(f"json:{json}")
        code = json.get('code', [])
        if code != 0:
            print(f"code:{code},获取失败代理失败！")
            return
        ip_list = json.get("data", [])
        if ip_list:
            for item in ip_list:
                proxies_pool.append(f"http://{item['ip']}:{item['port']}")
    return proxies_pool


# lg_proxy
def choice_proxy(num: int = 2):
    """
    流冠代理获取
    :param num:
    :return:
    """
    with get_redis() as redis:
        ip = redis.lpop('ips')
        if ip:
            return ip
        url = f'''https://api.hailiangip.com:8522/api/getIp?type=1&num={num}&pid=18&unbindTime=180&cid=188&orderId=O23021617133636094987&time=1678066129&sign=27acd50ebee7eb3ed35398a5d1a343e2&noDuplicate=1&dataType=0&lineSeparator=0'''
        try:
            resp = requests.get(url)
            json = resp.json()
            print(f"json:{json}")
            code = json.get('code', [])
            ip_list = json.get("data", [])
            if code == 0 and ip_list:
                proxies_pool = [f"http://{item['ip']}:{item['port']}" for item in ip_list]
                redis.rpush('ips', *proxies_pool)
                redis.expire('ips', 60 * 5)
                ip = redis.lpop('ips')
                if ip:
                    return ip
        except JSONDecodeError:
            time.sleep(10)
            raise CUMException("未获取到代理")
        time.sleep(10)
        raise CUMException("未获取到代理")


def choice_proxy1(proxy_num: int = 10, expire: int = 60 * 20):
    """
    随机获取一条代理
    :return:
    """

    redis = get_redis()

    pool = redis.lrange("proxy_pool", 0, -1)
    if not pool:
        proxy_pool = zm_proxies_pool(proxy_num)
        if not proxy_pool:
            raise NoProxyException(message="未获取到代理！")
        print("proxy_pool: ", proxy_pool)
        redis.lpush("proxy_pool", *proxy_pool)
        redis.expire("proxy_pool", expire)
        # pool = redis.lrange("proxy_pool", 0, -1)

    return redis.lpop("proxy_pool")


if __name__ == '__main__':
    # print(ip_proxy.pool)
    # print(choice_proxy2())
    # print(choice_proxy())
    # print(zm_proxies_pool())
    print(ceil(5 / 2) * 3)
