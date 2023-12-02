"""
Name:    login12306
Author:  ReddyFan
Date:    2023/2/2 09:02
Desc:  
"""
import time

import numpy as np
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def ease_out_quart(x):
    return 1 - pow(1 - x, 4)


def get_tracks(distance, seconds=3):
    """
    :param distance: offset
    :param seconds: 拉动时间
    :return:
    """
    tracks = [0]
    offsets = [0]
    # print("np_value:", np.arange(0.0, seconds, 0.1))
    for t in np.arange(0.0, seconds, 0.1):
        offset = round(ease_out_quart(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return offsets, tracks


class Login12306:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.get("https://kyfw.12306.cn/otn/resources/login.html")
        # self.driver.implicitly_wait(2)
        self.display_wait = WebDriverWait(driver=self.driver, timeout=10)
        self.username = self.display_wait.until(EC.presence_of_element_located((By.ID, 'J-userName')))
        self.username.send_keys("18783935413")
        self.password = self.driver.find_element(By.ID, 'J-password')
        self.password.send_keys("melon2021")
        self.login_button = self.driver.find_element(By.ID, 'J-login')
        time.sleep(0.5)
        self.login_button.click()


        self.actions = ActionChains(self.driver)
        self.box = self.display_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal"]/div[2]')))
        print("box: ", self.box.text)
        # time.sleep(8)
        # self.sliding_block = self.driver.find_element(By.ID, 'nc_3_n1z')
        # self.driver.switch_to.active_element()
        self.sliding_block = self.display_wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="J-slide-passcode"]/div/div[1]/span')))
        self.follow_block = self.display_wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="J-slide-passcode"]/div/div[1]/div[1]')))
        self.actions.click_and_hold(self.sliding_block).perform()
        time.sleep(0.2)
        # for x in range(1, 301):
        offsets, tracks = get_tracks(301, 1.1234)
        # self.actions.move_by_offset(300, 0).perform()
        for x in tracks:
            # self.follow_block
            self.actions.move_by_offset(x, 0).perform()

        # self.actions.pause(0.5).release(self.sliding_block).perform()
        print("登录成功")
        # self.driver..pause(0.5)
        time.sleep(10)


if __name__ == '__main__':
    Login12306()
    # offsets, tracks = get_tracks(300, 5)
    # print("offsets:", offsets)
    # print("offsets:", tracks)
