# """
# Name:    crawl_recruitment_data
# Author:  ReddyFan
# Date:    2023/2/11 16:31
# Desc:
# """
# import time
# from datetime import datetime
# from multiprocessing import RLock
#
# import selenium
# import ujson
# from selenium import webdriver
# from selenium.common import TimeoutException as TimeoutException_1
# from selenium.common.exceptions import NoSuchElementException, WebDriverException
# from selenium.webdriver import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
#
# from spider.utils.cum_exception import CUMException
# from store.db.db_store import Mongo, get_redis
# from utils.ip_proxiy import choice_proxy
#
# # from threading import RLock
#
# INDEX_URL = "https://www.zhipin.com/"
#
# rlock = RLock()
#
#
# def spend_time(begin, fnd):
#     tt = fnd - begin
#     h = int(tt / 60 / 60)
#     m = int(tt / 60 % 60)
#     s = int(tt % 60)
#     # return f"运行时间: {int(tt / 60 / 60)}小时{int(tt / 60 % 60)}分{int(tt % 60)}秒"
#     return h, m, s
#
#
# def output_running_time():
#     pass
#
#
# def get_options():
#     """ 设置代理 """
#     options = Options()
#     proxy = choice_proxy()
#     options.add_argument(
#         "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
#     options.add_argument(f"--proxy-server={proxy}")
#     # options.add_experimental_option("detach", True)
#     options.add_argument(f"--headless")
#
#     return options
#
#
# def find_element_xpath_text(obj, expression):
#     try:
#         return obj.find_element(By.XPATH, expression).text
#     except selenium.common.exceptions.NoSuchElementException:
#         return None
#
#
# class AutoCrawlBoss:
#
#     def __init__(self, no):
#         self.iis = 'iis'
#         self.page_timeout_count = 1
#         self.no = no
#         self.mongo = Mongo()
#         self.redis = get_redis()
#         self.lock = RLock()
#
#         self.lock.acquire()
#         industry = self.redis.lpop(self.iis)
#         industry_dict: dict = ujson.loads(industry) if industry else None
#         print(f"获取行业信息：{industry_dict}")
#         self.lock.release()
#
#         self.current_url = industry_dict.get('url', None)  # 当前url
#         self.industry = industry_dict.get('industry', None)
#         self.page = industry_dict.get('page', 1)  # 当前页码
#         # 页面详情爬取索引
#         self.detail_page_index = industry_dict.get('index', 0)
#         self.stop = False  # 是否中止程序
#         self.is_boot = True
#         self.driver = None
#         # 显示等待
#         self.display_wait = None
#
#         # 数据表
#         self.table_job = 't_job'
#         self.table_company = 't_company'
#         self.table_enterprise = 't_enterprise'
#         self.table_succeed = 't_succeed'
#         self.table_failed = 't_failed'
#
#         # 数据统计
#         self.crawled_recruitment_count = 0  # 爬取的招聘信息条数
#         self.crawled_company_count = 0  # 当前公司条数
#         self.crawled_enterprise_count = 0  # 当前企业条数
#
#         self.start_time = time.time()
#         self.last_time = time.time()
#         self.run()
#
#     def run(self):
#         if not self.current_url:
#             return
#         print(f'self.current_url: {self.current_url}')
#         print("+" * 50, f'NO:{self.no}，正在爬取---{self.industry}---行业', "+" * 50)
#         while self.current_url and not self.stop:
#             try:
#                 if self.is_boot:
#                     self.boot()
#                     self.is_boot = False
#                 self.get_recruitment_page()
#                 self.click_next_page()
#             except(selenium.common.exceptions.TimeoutException, NoSuchElementException, WebDriverException):
#                 if self.page_timeout_count >= 20:
#                     print(f"{self.industry}超时，第{self.page_timeout_count}次爬取结束！")
#                     self.failed_store()
#                     self.stop = True
#                 self.page_timeout_count += 1
#                 # 未找到元素
#                 self.is_boot = True
#             except CUMException:
#                 print(f"NO: {self.no},{self.industry}未获取到代理")
#                 self.is_boot = True
#             except KeyboardInterrupt:
#                 print(f'{self.industry}数据回写')
#                 self.failed_store()
#                 break
#         self.driver.quit()
#         hms = spend_time(self.start_time, time.time())
#         print(f'{self.industry}行业,第{self.page}页--爬取花费：{hms[0]}时{hms[1]}分{hms[2]}秒')
#
#     def failed_store(self):
#         failed_data = {
#             "industry": self.industry,
#             "crawled_recruitment_count": self.crawled_recruitment_count,
#             "crawled_enterprise_count": self.crawled_enterprise_count,
#             "crawled_company_count": self.crawled_company_count,
#             "failed_url": self.current_url,
#             "detail_page_index": self.detail_page_index,
#             "page": self.page,
#             "failed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
#         r_data = {
#             'industry': self.industry,
#             'url': self.current_url,
#             'page': self.page,
#             'index': self.detail_page_index
#         }
#         print("===失败存储===")
#         print(f'r_data: {r_data}')
#         self.redis.lpush(self.iis, ujson.dumps(r_data))
#         self.mongo.insert_one(self.table_failed, failed_data)
#
#     def get_recruitment_page(self):
#         """
#
#         :return:
#         """
#         self.driver.implicitly_wait(10)
#         key = self.wait_key("pl", By.XPATH,
#                             '//ul/li[1]/div[1]/a/div[1]/span[@class="job-name"]')
#         li_list = self.driver.find_elements(By.XPATH, '//ul[@class="job-list-box"]/li')
#         print(f'NO:{self.no},{self.industry}正在爬取：第{self.page}页,当前页数目：{len(li_list)}')
#         recruitment_source = self.driver.page_source
#         source_list = []
#         while self.detail_page_index < len(li_list):
#             print(f'NO:{self.no},{self.industry}正在爬取：第{self.page}页,第{self.detail_page_index + 1}条信息')
#             href = li_list[self.detail_page_index].find_element(By.XPATH, 'div[1]/a').get_attribute('href')
#             # company_id, details, pub_time =\
#             detail_sources = self.get_detail_page(href)
#             # print(f'li{self.detail_page_index + 1}')
#             source_list.append(detail_sources)
#             print(f'NO:{self.no},{self.industry},第{self.page}页,第{self.detail_page_index + 1}条信息,爬取成功！')
#             self.detail_page_index += 1
#
#         # self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#         return recruitment_source, source_list
#
#     def get_detail_page(self, href):
#         """
#         跳转详情页
#         :return:
#         """
#         self.driver.execute_script(f'window.open("{href}", "_blank");')
#         # 切换到新的标签页
#         self.driver.switch_to.window(self.driver.window_handles[-1])
#
#         company_href = self.wait_key(0, By.XPATH,
#                                      '//a[@ka="job-cominfo"]').get_attribute(
#             'href')
#         company_source = self.driver.page_source
#         # 跳转到企业页面
#         enterprise_source = self.get_enterprise_page(company_href)
#
#         self.driver.close()
#         self.driver.switch_to.window(self.driver.window_handles[0])
#
#         # return company_id, details, update_time
#         return company_source, enterprise_source
#
#     def get_enterprise_page(self, company_href):
#         """
#         跳转到企业信息页面
#         :return:
#         """
#
#         self.driver.execute_script(f'window.open("{company_href}", "_blank");')
#         # 切换到新的标签页
#         self.driver.switch_to.window(self.driver.window_handles[-1])
#
#         expand_button = self.wait_key(1, By.XPATH, '//label[@ka="company_full_info"]/span')
#         self.driver.execute_script("arguments[0].click()", expand_button)
#         enterprise_source = self.driver.page_source
#         # 爬取企业信息并返回企业唯一标识
#         # enterprise_id = self.extraction_enterprise_data()
#         self.driver.close()
#         self.driver.switch_to.window(self.driver.window_handles[-1])
#         # return enterprise_id
#         return enterprise_source
#
#     def click_next_page(self):
#         self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#         next_page_button = self.driver.find_element(
#             By.XPATH,
#             '//div[@class="options-pages"]/a[last()]'
#         )
#
#         if next_page_button and self.driver.find_element(
#                 By.XPATH,
#                 '//div[@class="options-pages"]/a[last()]'
#         ).get_attribute("class"):
#             print("-" * 5, f"NO:{self.no}，{self.industry}行业数据爬取完毕，总计爬取{self.crawled_recruitment_count}条数据！", "-" * 5)
#             self.mongo.insert_one(self.table_succeed, {
#                 "industry": self.industry,
#                 "crawled_recruitment_count": self.crawled_recruitment_count,
#                 "crawled_company_count": self.crawled_company_count,
#                 "crawled_enterprise_count": self.crawled_enterprise_count,
#                 "succeed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             })
#             self.stop = True
#             return
#         self.driver.find_element(
#             By.XPATH,
#             '//div[@class="options-pages"]/a[last()]'
#         ).send_keys(Keys.ENTER)
#         hms = spend_time(self.last_time, time.time())
#         print(f'{self.industry}行业,第{self.page}页爬取花费：{hms[0]}时{hms[1]}分{hms[2]}秒')
#         self.last_time = time.time()
#         self.page_timeout_count = 1
#         self.detail_page_index = 0
#         self.page += 1
#         time.sleep(1)
#         self.current_url = self.driver.current_url if 'https://www.zhipin.com/web/geek/job' in self.driver.current_url else self.current_url
#
#
#     def wait_key(self, action, by: By, locator: str):
#         """
#         延迟WebElement对象
#         :param action: 具体行为
#         :param by: 选择器类型
#         :param locator: 选择器字符串
#         :return:
#         """
#         # try:
#         if action == 'pl' or action == 0:
#             return self.display_wait.until(EC.presence_of_element_located((by, locator)))
#         elif action == 'ec' or action == 1:
#             return self.display_wait.until(EC.element_to_be_clickable((by, locator)))
#         # except Exception:
#         #     print("=" * 10, f"NO:{self.no} {self.industry} wait_key 访问频繁！", "=" * 10)
#         #     return None
#
#     def boot(self):
#         print(
#             f"No:{self.no},{self.industry}行业，第{self.page}页，第{self.detail_page_index + 1}条数据，第{self.page_timeout_count}次启动浏览器！")
#         rlock.acquire()
#         self.driver = webdriver.Chrome(options=get_options())
#         rlock.release()
#         # 显示等待
#         self.display_wait = WebDriverWait(driver=self.driver, timeout=25)
#         self.driver.get(self.current_url)
#         self.driver.maximize_window()
#
#
# if __name__ == '__main__':
#     try:
#         start = time.time()
#
#         AutoCrawlBoss(1)
#
#         end = time.time()
#         rt = end - start
#         print(f"运行时间:{rt} {int(rt / 60 / 60)}小时{int(rt / 60 % 60)}分{int(rt % 60)}秒")
#     except KeyboardInterrupt:
#         print("程序退出")
