import csv
import os
import re
import json
import time
import datetime
import pandas as pd
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions
from lxml import etree


def last_comment_date(html):
    root = etree.HTML(html)
    # root = etree.HTML(chrome.page_source)
    comment_list = root.xpath('//*[@id="list"]')
    for comment_l in comment_list:
        comment_date = comment_l.xpath(
            '//*[@id="list"]//*[@class=" "]//*[@class="basic_info"]/text()'
        )
        temp = comment_date[len(comment_date) - 1]
        temp = temp.replace("更新于 ", "")
        today = time.strftime("%m-%d", time.localtime())
        if "今天" in temp:
            temp = temp.replace("今天", f"{today}")
        last = temp[0:-6]
        print(last)
        return last


def open_main(url, day):
    # global last_day_, day_
    chrome.get(url)
    time.sleep(2)
    # list_0 = chrome.find_element(By.XPATH, '//*[@id="mainlist"]/div/div[1]/div/ul/li[2]')
    list_1 = chrome.find_element(
        By.XPATH, '//*[@id="mainlist"]/div/div[1]/div/ul/li[3]'
    )
    # list_0.click()
    list_1.click()  # 点击摘要
    time.sleep(2)
    day_ = datetime.datetime.strptime(day, "%m-%d")

    last_day = last_comment_date(chrome.page_source)
    # print(last_day)

    last_day_ = datetime.datetime.strptime(last_day, "%m-%d")

    n = 1  # 初试页面 页号1
    while last_day_ >= day_:
        next_page()
        parse(chrome.page_source)
        last_day = last_comment_date(chrome.page_source)
        last_day_ = datetime.datetime.strptime(last_day, "%m-%d")


def next_page():
    next_button = chrome.find_element(By.CLASS_NAME, "nextp")
    next_page_link = next_button.get_attribute("href")
    chrome.get(next_page_link)


# def last_comment_date():
#     comment_date_ = chrome.find_element(By.XPATH, '//*[@id="list"]//*[@class=" "]//*[@class="basic_info"]')
#     comment_date = comment_date_.get_attribute('text')
#     temp = comment_date[len(comment_date) - 1]
#     temp = temp.replace('更新于 ', '')
#     today = time.strftime('%m-%d', time.localtime())
#     if '今天' in temp:
#         temp = temp.replace('今天', f'{today}')
#     last = temp[0:-6]
#     return last


def parse(html):
    global data
    root = etree.HTML(html)
    # root = etree.HTML(chrome.page_source)
    comment_list = root.xpath('//*[@id="list"]')  # element对象
    items = {}
    for comment_l in comment_list:
        comment_text = comment_l.xpath(
            '//*[@id="list"]//*[@class=" "]//*[@class="content"]/a/span/text()[1]'
        )
        comment_date = comment_l.xpath(
            '//*[@id="list"]//*[@class=" "]//*[@class="basic_info"]/text()'
        )
        for comment_text_, comment_date_ in zip(comment_text, comment_date):
            # print(comment_text_, comment_date_)

            items["comment_text"] = comment_text_
            temp = comment_date_
            temp = temp.replace("更新于 ", "")
            today = time.strftime("%m-%d", time.localtime())
            if "今天" in comment_date_:
                temp = temp.replace("今天", f"{today}")
            items["comment_date"] = temp
            tt = pd.DataFrame(data=[comment_text_, temp, temp[0:-6]]).T
            tt.columns = ["comment_text", "comment_date", "comment_time"]
            data = pd.concat((tt, data))


data = pd.DataFrame(columns=["comment_text", "comment_date", "comment_time"])
# day = "08-01"
# code = 300059
chrome = Chrome()
print("Chrome初始化成功")

data = data.sort_values(by=["comment_date"])


def grab_data(code=300059, day="08-01"):
    open_main(f"http://guba.eastmoney.com/list,{code}.html?from=BaiduAladdin", day)
    data.to_csv(f"./output/data_{code}.csv", encoding="gbk", index_label=None)
