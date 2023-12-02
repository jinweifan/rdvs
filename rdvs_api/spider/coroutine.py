"""
Name:    coroutine
Author:  ReddyFan
Date:    2023/2/17 08:33
Desc:  
"""
import asyncio
import time

from spider.crawl_recruitment_data import CrawlRecruitmentInfo
from store.db.db_store import Mongo


class MultipleTaskCoroutineCrawl:

    def __init__(self, process_num=2, crawl_num=20):
        start = time.time()
        self.process_num = process_num
        self.crawl_num = crawl_num
        self.top = 0

        mongo = Mongo()
        data = mongo.find('industry_info', columns_conditions={"_id": 0, "third_industry": 1, "third_industry_url": 1},
                          skip=231, limit=6)
        print(len(data), data)
        task_list = []
        index = 1
        for item in data:
            task = CrawlRecruitmentInfo(1, item["third_industry_url"], item["third_industry"])
            # asyncio.ensure_future(CrawlRecruitmentInfo,)
            task_list.append(task)
            index += 1
        loop = asyncio.get_event_loop()
        end = time.time()
        loop.run_until_complete(task_list)
        rt = end - start
        print(f"运行时间: {int(rt / 60 / 60)}小时{int(rt / 60)}分{int(rt % 60)}秒")

        sum = 0
        for i in task_list:
            print(type(i), i)
        print(f"此次爬取了总计爬取了{sum}条数据")
