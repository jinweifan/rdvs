"""
Name:    crawl_home_page
Author:  ReddyFan
Date:    2023/2/10 15:35
Desc:  
"""
import requests
from lxml import etree

from store.db.db_store import Mongo


def parse_infos(func):
    def inner(html: str):
        dl_list = html.xpath('//*[@id="main"]/div/div[1]/div/div[1]/dl')
        for dl in dl_list:
            first_industry = dl.xpath('dd/b//text()')[0]
            li_list = dl.xpath('div/ul/li')
            for li in li_list:
                second_industry = li.xpath('h4//text()')[0]
                a_list = li.xpath('div/a')
                for a in a_list:
                    third_industry = a.xpath('text()')[0]
                    third_industry_url = "https://www.zhipin.com/" + str(a.xpath('@href')[0])
                return first_industry, second_industry, third_industry, third_industry_url

    return inner


class IndustryInfo:
    """
    行业数据爬取
    todo: 用装饰器降低耦合
    """

    def __init__(self):

        resp = requests.get("https://www.zhipin.com/", headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", }, )

        text = resp.text
        self.html = etree.HTML(text)

    def parse_to_dict(self):
        infos = {
            "first_industry": [],
            "second_industry": [],
            "third_industry": [],
            "third_industry_url": [],
        }
        dl_list = self.html.xpath('//*[@id="main"]/div/div[1]/div/div[1]/dl')
        for dl in dl_list:
            first_industry = dl.xpath('dd/b//text()')[0]
            li_list = dl.xpath('div/ul/li')
            for li in li_list:
                second_industry = li.xpath('h4//text()')[0]
                a_list = li.xpath('div/a')
                for a in a_list:
                    third_industry = a.xpath('text()')[0]
                    third_industry_url = "https://www.zhipin.com/" + str(a.xpath('@href')[0])
                    print(third_industry_url)
                    # print(first_industry, second_industry, third_industry, third_industry_url)
                    infos["first_industry"].append(first_industry)
                    infos["second_industry"].append(second_industry)
                    infos["third_industry"].append(third_industry)
                    infos["third_industry_url"].append(third_industry_url)
        return infos

    def parse_to_list(self):
        infos = []
        dl_list = self.html.xpath('//*[@id="main"]/div/div[1]/div/div[1]/dl')
        for dl in dl_list:
            first_industry = dl.xpath('dd/b//text()')[0]
            li_list = dl.xpath('div/ul/li')
            for li in li_list:
                second_industry = li.xpath('h4//text()')[0]
                a_list = li.xpath('div/a')
                for a in a_list:
                    third_industry = a.xpath('text()')[0]
                    third_industry_url = "https://www.zhipin.com" + a.xpath('@href')[0]
                    infos_model = {
                        "first_industry": first_industry,
                        "second_industry": second_industry,
                        "third_industry": third_industry,
                        "third_industry_url": third_industry_url,
                    }
                    infos.append(infos_model)
                    print(infos_model)

        return infos


if __name__ == '__main__':
    # print(get_industry_infos_to_dict())
    info = IndustryInfo()
    # IndustryInfo.p
    info_list = info.parse_to_list()
    # print(info_list)
    print(type(info_list))
    mongo = Mongo()
    print(mongo.db.industry_info.insert_many(info_list))
