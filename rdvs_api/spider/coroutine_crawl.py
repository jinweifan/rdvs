"""
Name:    coroutine_crawl
Author:  ReddyFan
Date:    2023/2/15 15:36
Desc:  
"""
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from spider.crawl_recruitment_data import AutoCrawlBoss
from store.db.db_store import get_redis

RECRUITMENT_URL = 'https://www.zhipin.com/web/geek/job'


def construct_recruitment_url(prefix_url: str, position: str = '', city: str = 100010000, query: str = ''):
    """

    :param prefix_url:
    :param position:
    :param city: 100010000 全国
    :param query:
    :return:
    """
    return f'{prefix_url}?query={query}&city={city}&position={position}'


def update_url():
    pass


class MultipleProcessCrawl:
    """ 多进程爬取BOSS职聘 """

    def __init__(self, process_num=5, crawl_num=-1):
        start = time.time()
        self.redis = get_redis()
        self.process_num = process_num
        self.crawl_num = crawl_num
        self.pool = ProcessPoolExecutor(self.process_num)
        no = 1
        task_list = list()
        while no <= self.crawl_num or self.crawl_num == -1:
            task = self.pool.submit(
                AutoCrawlBoss,
                no
            )
            task_list.append(task)
            no += 1

        self.pool.shutdown(wait=True)

        end = time.time()
        rt = end - start
        print(f"运行时间: {int(rt / 60 / 60)}小时{int(rt / 60 % 60)}分{int(rt % 60)}秒")


class MultipleThreadCrawl:
    """ 多线程爬取BOSS职聘 """

    def __init__(self, process_num=5, crawl_num=-1):
        start = time.time()
        self.process_num = process_num
        self.crawl_num = crawl_num
        self.pool = ThreadPoolExecutor(self.process_num)

        no = 1
        task_list = list()
        while no <= self.crawl_num or self.crawl_num == -1:
            task = self.pool.submit(AutoCrawlBoss, no)
            task_list.append(task)
            no += 1
        self.pool.shutdown()

        end = time.time()
        rt = end - start
        print(f"运行时间: {int(rt / 60 / 60)}小时{int(rt / 60 % 60)}分{int(rt % 60)}秒")

        amount = 0
        for task in task_list:
            count = task.result().crawled_recruitment_count
            amount += count
            print(f'NO:{task.result().no},{task.result().industry},当前爬取{count}')
        print(f"此次爬取了总计爬取了{amount}条数据")


class MultipleTaskCoroutineCrawl:

    def __init__(self):
        pass


def yey():
    print("me")


if __name__ == '__main__':
    try:
        MultipleProcessCrawl(4, 4)
        # MultipleThreadCrawl(5, 5)
    except KeyboardInterrupt:
        print("键盘中断，)程序退出！")