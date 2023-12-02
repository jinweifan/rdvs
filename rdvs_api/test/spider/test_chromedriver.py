import time

from selenium import webdriver

driver = webdriver.Chrome()
print("=" * 100)
driver.get("https://www.zhipin.com/web/geek/job?query=&city=101270100&position=100101")
# driver.implicitly_wait(10)

