"""
Name:    crawl_recruitment_data
Author:  ReddyFan
Date:    2023/2/11 16:31
Desc:  
"""
import time
from datetime import datetime
from multiprocessing import RLock, Semaphore

import selenium
import ujson
from selenium import webdriver
from selenium.common import TimeoutException as TimeoutException_1
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from spider.utils.cum_exception import CUMException
from store.db.db_store import Mongo, get_redis
from utils.ip_proxiy import choice_proxy

# from threading import RLock

INDEX_URL = "https://www.zhipin.com/"

rlock = RLock()  # 进程锁
semaphore = Semaphore(1)  # 进程型号量


def spend_time(begin, fnd):
    """
    计算运行花费的时间
    :param begin: 起始时间
    :param fnd:  结束时间
    :return: 返回时、分、秒
    """
    tt = fnd - begin
    h = int(tt / 60 / 60)
    m = int(tt / 60 % 60)
    s = int(tt % 60)
    # return f"运行时间: {int(tt / 60 / 60)}小时{int(tt / 60 % 60)}分{int(tt % 60)}秒"
    return h, m, s


def get_options():
    """ 获取代理 """
    options = Options()
    semaphore.acquire()
    proxy = choice_proxy()
    semaphore.release()
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
    options.add_argument(f"--proxy-server={proxy}")  # 设置代理
    # options.add_experimental_option("detach", True) # 程序结束，不关闭浏览器
    options.add_argument(f"--headless")  # 无头浏览器

    return options


def find_element_xpath_text(obj, expression):
    """ 针对于selenium find_element方法未找到元素返回None """
    try:
        return obj.find_element(By.XPATH, expression).text
    except selenium.common.exceptions.NoSuchElementException:
        return None


class AutoCrawlBoss:
    """ 自动爬取Boss """

    def __init__(self, no):
        self.iis = 'iis'
        self.page_timeout_count = 1
        self.no = no
        self.mongo = Mongo()
        self.redis = get_redis()
        self.lock = RLock()
        industry = None
        try:
            # self.lock.acquire()
            industry = self.redis.lpop(self.iis)
            industry_dict: dict = ujson.loads(industry) if industry else None
            print(f"获取行业信息：{industry_dict}")
            # self.lock.release()

            self.current_url = industry_dict.get('url', None)  # 当前url
            self.industry = industry_dict.get('industry', None)
            self.page = industry_dict.get('page', 1)  # 当前页码
            # 页面详情爬取索引
            self.detail_page_index = industry_dict.get('index', 0)

            self.stop = False  # 是否中止程序

            self.is_boot = True

            self.driver = None
            # 显示等待
            self.display_wait = None

            # 数据表
            self.table_job = 't2_job'
            self.table_company = 't2_company'
            self.table_enterprise = 't2_enterprise'
            self.table_succeed = 't2_succeed'
            self.table_failed = 't2_failed'

            # 数据统计
            self.crawled_recruitment_count = 0  # 爬取的招聘信息条数
            self.crawled_company_count = 0  # 当前公司条数
            self.crawled_enterprise_count = 0  # 当前企业条数

            self.start_time = time.time()
            self.last_time = time.time()
            self.run()
        except KeyboardInterrupt:
            print('其他异常')
            if industry:
                print(f"数据回写：{industry}")
                self.redis.lpush(self.iis, industry)

    def run(self):
        if not self.current_url:
            return
        print("+" * 50, f'NO:{self.no}，正在爬取---{self.industry}---行业', "+" * 50)
        while self.current_url and not self.stop:
            try:
                if self.is_boot:
                    self.boot()
                    self.is_boot = False
                self.get_recruitment_page()
                self.click_next_page()
            except(
                    selenium.common.exceptions.TimeoutException,
                    NoSuchElementException,
                    WebDriverException
            ):

                if self.page_timeout_count >= 20:
                    print(
                        f"No:{self.no},{self.industry},"
                        f"第{self.page}页,"
                        f"第{self.detail_page_index + 1}条数据超过最大爬取次数"
                        f"，第{self.page_timeout_count}次爬取结束！")
                    self.failed_store()
                    break
                print(
                    f"No:{self.no},{self.industry},第{self.page}页,"
                    f"第{self.detail_page_index + 1}条数据异常！"
                )
                self.page_timeout_count += 1
                # 未找到元素
                self.is_boot = True
            except CUMException:
                print(f"NO: {self.no},{self.industry}未获取到代理")
                self.is_boot = True
            except KeyboardInterrupt:
                print(f'{self.industry}数据回写')
                self.failed_store()
                break
        self.driver.quit()
        hms = spend_time(self.start_time, time.time())
        print(f'{self.industry}行业,第{self.page}页--爬取花费：{hms[0]}时{hms[1]}分{hms[2]}秒')

    def failed_store(self):
        """ 程序中断、爬取失败时存储当前爬取状态 """
        failed_data = {
            "industry": self.industry,
            "crawled_recruitment_count": self.crawled_recruitment_count,
            "crawled_enterprise_count": self.crawled_enterprise_count,
            "crawled_company_count": self.crawled_company_count,
            "failed_url": self.current_url,
            "detail_page_index": self.detail_page_index,
            "page": self.page,
            "failed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        r_data = {
            'industry': self.industry,
            'url': self.current_url,
            'page': self.page,
            'index': self.detail_page_index
        }
        print("===失败存储===")
        print(f'r_data: {r_data}')
        self.redis.lpush(self.iis, ujson.dumps(r_data))
        self.mongo.insert_one(self.table_failed, failed_data)

    def get_recruitment_page(self):
        """
        爬取招聘信息的页面
        """
        self.driver.implicitly_wait(10)
        key = self.wait_key("pl", By.XPATH,
                            '//ul/li[1]/div[1]/a/div[1]/span[@class="job-name"]')
        if not key:
            return
        li_list = self.driver.find_elements(By.XPATH, '//ul[@class="job-list-box"]/li')
        print(f'NO:{self.no},{self.industry}正在爬取：第{self.page}页,当前页数目：{len(li_list)}')

        while self.detail_page_index < len(li_list):
            print(f'NO:{self.no},{self.industry}正在爬取：第{self.page}页,第{self.detail_page_index + 1}条信息')
            href = li_list[self.detail_page_index].find_element(By.XPATH, 'div[1]/a').get_attribute('href')
            company_id, details, pub_time = self.get_detail_page(href)
            self.extraction_recruitment_data(li_list[self.detail_page_index], company_id, details, pub_time)
            print(f'NO:{self.no},{self.industry},第{self.page}页,第{self.detail_page_index + 1}条信息,爬取成功！')
            self.detail_page_index += 1

        return self.driver.page_source

    def get_detail_page(self, href):
        """
        跳转详情页
        :return:
        """
        self.driver.execute_script(f'window.open("{href}", "_blank");')
        # 切换到新的标签页
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # 跳转到企业页面
        enterprise_id = self.get_enterprise_page()

        # 获取详情信息
        company_id, details, update_time = self.extraction_detail_data(enterprise_id)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        return company_id, details, update_time

    def get_enterprise_page(self):
        """
        跳转到企业信息页面
        :return:
        """
        company_href = self.wait_key(0, By.XPATH,
                                     '//a[@ka="job-cominfo"]').get_attribute(
            'href')
        self.driver.execute_script(f'window.open("{company_href}", "_blank");')
        # 切换到新的标签页
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # 爬取企业信息并返回企业唯一标识
        enterprise_id = self.extraction_enterprise_data()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return enterprise_id

    def extraction_enterprise_data(self):
        """
        爬取企业数据
        :return:
        """
        # 等待页面元素加载

        enterprise_intro = find_element_xpath_text(
            self.driver,
            '//div[@class="job-sec"]/div[contains(@class,"text")]')
        expand_button = self.wait_key(1, By.XPATH, '//label[@ka="company_full_info"]/span')
        # expand_button.click()
        self.driver.execute_script("arguments[0].click()", expand_button)
        # expand_button.
        columns = [
            'enterprise_name', 'legal_person', 'register_date',
            'business_type', 'management_form', 'registered_capital',
            'registered_address', 'USI_code', 'business_scope',

        ]
        enterprise_info = dict()
        no = 1
        for i in columns:
            element = self.driver.find_element(
                By.XPATH,
                f'//div[@class="business-detail show-business-all"]/ul/li[{no}]'
            ).text

            enterprise_info[i] = element.split('\n')[1] if element and '\n' in element else None
            no += 1
        enterprise_info['enterprise_intro'] = enterprise_intro
        address_list_obj = self.driver.find_elements(By.XPATH, '//div/div[contains(@class,"location-item")]')
        enterprise_info['address_list'] = [i.find_element(By.XPATH, 'div[1]').text for i in address_list_obj]
        enterprise_info['crawled_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # print(f'企业信息：{enterprise_info}')

        # 数据库操作
        find = self.mongo.find_one(self.table_enterprise, {'USI_code': enterprise_info.get('USI_code')}, {'_id': 1})
        if find:
            return find.get('_id')
        one = self.mongo.insert_one(self.table_enterprise, enterprise_info)
        self.crawled_enterprise_count += 1
        return one.inserted_id

    def extraction_detail_data(self, enterprise_id):
        """
        抽取招聘信息详情和公司信息
        :return:
        """
        # 等待页面元素加载
        details = self.wait_key(1, By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[1]/div[2]').text

        company_intro = find_element_xpath_text(self.driver, '//*[@class="job-sec-text fold-text"]')
        columns = [
            'company_name', 'legal_person', 'register_date',
            'business_type', 'management_form', 'registered_capital']
        company_info = dict()
        no = 1
        for i in columns:
            element = self.driver.find_element(
                By.XPATH,
                f'//ul[@class="level-list"]/li[{no}]'
            ).text
            company_info[i] = element.split('\n')[1] if element and '\n' in element else None
            no += 1

        address = self.driver.find_element(By.XPATH, '//div[@class="location-address"]').text
        company_info['company_intro'] = company_intro
        company_info['address'] = address
        company_info['enterprise_id'] = enterprise_id
        company_info['crawled_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pub_time = self.driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/p').text.split("：")[1]

        # 数据库操作
        find = self.mongo.find_one(self.table_company,
                                   query_conditions={
                                       'register_date': company_info.get('register_date'),
                                       'company_name': company_info.get('company_name'),
                                       'legal_person': company_info.get('legal_person'),
                                   },
                                   columns_conditions={'_id': 1}
                                   )
        if find:
            return find.get('_id'), details, pub_time
        company = self.mongo.insert_one(self.table_company, company_info)
        self.crawled_company_count += 1
        return company.inserted_id, details, pub_time

    def extraction_recruitment_data(self, li, company_id, details, pub_time):
        job_name = li.find_element(By.XPATH, 'div[1]/a/div[1]/span[1]').text
        job_area = li.find_element(By.XPATH, 'div[1]/a/div[1]/span[2]/span').text
        salary = li.find_element(By.XPATH, 'div[1]/a/div[2]/span').text
        job_experience = li.find_element(By.XPATH, 'div[1]/a/div[2]/ul/li').text
        job_degree = li.find_element(By.XPATH, 'div[1]/a/div[2]/ul/li[2]').text
        skill_list = [i.text for i in li.find_elements(By.XPATH, 'div[2]/ul/li')]
        welfare_list = [i.text for i in li.find_elements(By.XPATH, 'div[2]/div')]

        # HR职位
        boss_title = li.find_element(By.XPATH, 'div[1]/a/div[2]/div/em').text
        # HR称呼
        boss_name = li.find_element(By.XPATH, 'div[1]/a/div[2]/div').text
        # 切片
        boss_name = boss_name[:-len(boss_title)]

        brand_logo = li.find_element(By.XPATH, 'div[1]/div/div[1]/a/img').get_attribute('src')
        brand_name = li.find_element(By.XPATH, 'div[1]/div/div[2]/h3/a').text
        brand_industry = li.find_element(By.XPATH, 'div[1]/div/div[2]/ul/li[1]').text
        brand_scale_name = li.find_element(By.XPATH, 'div[1]/div/div[2]/ul/li[2]').text
        brand_stage_name = find_element_xpath_text(li, 'div[1]/div/div[2]/ul/li[3]')

        job = {
            "third_industry": self.industry,
            "job_name": job_name,
            "job_area": job_area,
            "salary": salary,
            "job_experience": job_experience,
            "job_degree": job_degree,
            "skill_list": skill_list,
            "welfare_list": welfare_list,
            "boss_name": boss_name,
            "boss_title": boss_title,
            "brand_logo": brand_logo,
            "brand_name": brand_name,
            "brand_industry": brand_industry,
            "brand_scale_name": brand_scale_name,
            "brand_stage_name": brand_stage_name,
            "company_id": company_id,
            "details": details,
            "pub_time": pub_time,
            "crawled_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # print(f"job:{job}")
        # 数据库操作
        # find = self.mongo.find_one(self.table_job, {'job_name': job.get('job_name'),
        #                                             'brand_name': job.get('brand_name'),
        #                                             'job_area': job.get('job_area'), })
        # if find:
        #     return find.get('_id')
        info = self.mongo.insert_one(self.table_job, job)
        print(f'新增成功！info:{info}')
        self.crawled_recruitment_count += 1
        return info.inserted_id

    def click_next_page(self):
        """ 点击下一页操作 """
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        next_page_button = self.driver.find_element(
            By.XPATH,
            '//div[@class="options-pages"]/a[last()]'
        )

        if next_page_button and self.driver.find_element(
                By.XPATH,
                '//div[@class="options-pages"]/a[last()]'
        ).get_attribute("class"):
            print("-" * 5, f"NO:{self.no}，{self.industry}行业数据爬取完毕，总计爬取{self.crawled_recruitment_count}条数据！", "-" * 5)
            self.mongo.insert_one(self.table_succeed, {
                "industry": self.industry,
                "crawled_recruitment_count": self.crawled_recruitment_count,
                "crawled_company_count": self.crawled_company_count,
                "crawled_enterprise_count": self.crawled_enterprise_count,
                "succeed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.stop = True
            return
        self.driver.find_element(
            By.XPATH,
            '//div[@class="options-pages"]/a[last()]'
        ).send_keys(Keys.ENTER)
        hms = spend_time(self.last_time, time.time())
        print(f'{self.industry}行业,第{self.page}页爬取花费：{hms[0]}时{hms[1]}分{hms[2]}秒')
        self.last_time = time.time()
        self.page_timeout_count = 1
        self.detail_page_index = 0
        self.page += 1
        time.sleep(1)
        self.current_url = self.driver.current_url if 'https://www.zhipin.com/web/geek/job' in self.driver.current_url else self.current_url

    def wait_key(self, action, by: By, locator: str):
        """
        延迟WebElement对象
        :param action: 具体行为
        :param by: 选择器类型
        :param locator: 选择器字符串
        :return:
        """
        # try:
        if action == 'pl' or action == 0:
            return self.display_wait.until(EC.presence_of_element_located((by, locator)))
        elif action == 'ec' or action == 1:
            return self.display_wait.until(EC.element_to_be_clickable((by, locator)))
        # except Exception:
        #     print("=" * 10, f"NO:{self.no} {self.industry} wait_key 访问频繁！", "=" * 10)
        #     return None

    def boot(self):
        """ 启动浏览器 """
        print(
            f"No:{self.no},{self.industry}行业，第{self.page}页，第{self.detail_page_index + 1}条数据，第{self.page_timeout_count}次启动浏览器！")
        self.driver = webdriver.Chrome(options=get_options())
        # 显示等待
        self.display_wait = WebDriverWait(driver=self.driver, timeout=25)
        self.driver.get(self.current_url)
        self.driver.maximize_window()


if __name__ == '__main__':
    try:
        start = time.time()
        AutoCrawlBoss(1)
        end = time.time()
        rt = end - start
        print(f"运行时间:{int(rt / 60 / 60)}小时{int(rt / 60 % 60)}分{int(rt % 60)}秒")
    except KeyboardInterrupt:
        print("程序退出")
