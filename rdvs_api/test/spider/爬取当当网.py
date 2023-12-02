"""
Name:    爬取当当网
Author:  ReddyFan
Date:    2023/1/28 10:57
Desc:  
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


class BSDD:
    """ 爬取最近30天数据"""

    def __init__(self, url: str, headers: dict = None, params: dict = None):
        self.url = url
        self.headers = headers
        self.params = params
        self.resp = None
        self.soup: BeautifulSoup = None
        self.data: dict = {
            "图书排名": [],
            "图书名称": [],
            "图书作者": [],
            "图书出版时间": [],
            "图书出版社": [],
            "图书价格": [],
        }
        self.current_page = 1
        self.current_page_count = 1
        self.total_count = 0

    def parse_html(self):
        li_list = self.soup.select(".bang_list li")
        self.current_page_count = 1
        for li in li_list:
            print(f"正在解析第{self.current_page}页的第{self.current_page_count}条数据")
            self.data["图书排名"].append(li.select(".list_num")[0].text.replace(".", ""))
            self.data["图书名称"].append(li.select(".name a")[0].text)
            self.data["图书作者"].append(li.select(".publisher_info")[0].text)
            self.data["图书出版时间"].append(li.select(".publisher_info span")[0].text)
            self.data["图书出版社"].append(li.select(".publisher_info")[1].select("a")[0].text)
            self.data["图书价格"].append(li.select(".price .price_n")[0].text.replace("￥", ""))
            self.current_page_count += 1
            self.total_count += 1

    def crawler(self, star: int = 1, end: int = 5):
        self.current_page = star
        while self.current_page <= end:
            self.url = self.url.rsplit('-', maxsplit=1)[0] + "-" + str(self.current_page)
            self.resp = requests.get(url=self.url, headers=self.headers, params=self.params)
            print(f"=====正在爬取第{self.current_page}页数据,目前数据量为：{self.total_count}=====")
            self.soup = BeautifulSoup(self.resp.text, "lxml")
            self.parse_html()
            self.current_page += 1
        print("=" * 20, f"爬取数据量为：{self.total_count}", "=" * 20, )


if __name__ == '__main__':
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    # # url = "https://movie.douban.com/j/chart/top_list"
    # url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-2"
    # bsdd = BSDD(url, headers=headers)
    # bsdd.crawler(end=2)
    # print(bsdd.data)
    # # print(json.dumps(bsdd.data, indent=4, ensure_ascii=False, separators=(',', ':')))
    # ds = pd.DataFrame(bsdd.data)
    # pd.DataFrame(bsdd.data)
    print("¥49.00"[1:])
    # print(ds)
